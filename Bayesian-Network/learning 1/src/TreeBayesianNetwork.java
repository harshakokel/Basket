import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

import org.jgrapht.DirectedGraph;
import org.jgrapht.alg.interfaces.SpanningTreeAlgorithm.SpanningTree;
import org.jgrapht.alg.spanning.KruskalMinimumSpanningTree;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.WeightedPseudograph;
import org.jgrapht.traverse.DepthFirstIterator;
import org.jgrapht.traverse.GraphIterator;


public class TreeBayesianNetwork extends ParameterLearningBN{
	
	List<int[]> trainingData;
	List<Double> dataWeights;
	Boolean firstSampleFlag = true;
	int numberOfTrainingSamples = 0;
	int[] count = new int[1];
	final int[][] values = {{0,0},{0,1},{1,1},{1,0}};
	public DirectedGraph<Integer, DefaultEdge> network ;
	public List<Object> networkParameters ;
	double testLogLikelihood = 0.0;
	int numberOfTestSamples = 0;
	
	public TreeBayesianNetwork() {
		// TODO Auto-generated constructor stub
		super();
	}
	
	
	@Override
	public String toString() {
		return "TreeBayesianNetwork [network=" + network.toString() + "]";
	}


	public TreeBayesianNetwork(List<int[]> trainingData,List<Double> dataWeights,int[] count, int numberOfTrainingSamples) {
		// TODO Auto-generated constructor stub
		super();
		this.trainingData = trainingData;
		this.count = count;
		this.dataWeights = dataWeights;
		this.numberOfTrainingSamples = numberOfTrainingSamples;
	}

	public void run(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Tree Bayesian Network");
		trainingData = null;
		this.firstSampleFlag = true;
		this.numberOfTrainingSamples = 0;
		this.count = new int[1];
		this.testLogLikelihood = 0.0;
		this.networkParameters = null;
		this.network = null;
		this.numberOfTestSamples = 0;
		String trainingFile = args[0];
		processData(trainingFile, true);
		learnBN();
		String testFile = args[1];
		processData(testFile, false);
		System.out.println("loglikelihood of "+ testFile+" is "+(this.testLogLikelihood/this.numberOfTestSamples));
	}

	public void learnBN() {
		this.network = learnBNStructure();
		this.networkParameters = learnBNParameters();
	}

	private  List<Object> learnBNParameters() {
		Integer s, v =0;
		Set<DefaultEdge> edges;
		List<Object> parameters = new ArrayList<>();
		for(v = 0; v < this.count.length; v++) {
			// Any variable will have exactly one parent or zero
			edges = this.network.incomingEdgesOf(v);
			if(!edges.isEmpty()) {
				s = this.network.getEdgeSource(edges.iterator().next());
				parameters.add(learnCPT(s,v));
			}
			else
				parameters.add(learnCPT(v));
		}
		return parameters;
	}

	private  Double learnCPT(Integer v) {
		return (double) (this.count[v]+2)/(this.numberOfTrainingSamples+4);
	}

	private  Double[] learnCPT(Integer s, Integer v) {
		// TODO Auto-generated method stub
		double[] jointcount = getCounts(s,v);
		Double[] prob = new Double[2];
		prob[0] = jointcount[1]/(jointcount[1]+ jointcount[0]);
		prob[1] = jointcount[2]/(jointcount[2]+ jointcount[3]);
		if(prob[0] < 0.0 || prob[1] <0.0) {
			System.out.println("Error prob is negative");
			System.exit(0);
		}

		return prob;
	}

	private  DirectedGraph<Integer, DefaultEdge> learnBNStructure() {
		WeightedPseudograph<Integer, DefaultWeightedEdge> weightedGraph = new WeightedPseudograph<>(DefaultWeightedEdge.class);
		DirectedGraph<Integer, DefaultEdge> directedGraph = new DefaultDirectedGraph<>(DefaultEdge.class);
		for(int i=0; i< this.count.length; i++) {
			weightedGraph.addVertex(i);
			directedGraph.addVertex(i);
		}
		for(int i=0; i< this.count.length; i++) {
			for(int j=i+1; j< this.count.length; j++) {

				DefaultWeightedEdge e = new DefaultWeightedEdge();
				weightedGraph.addEdge(i, j, e);
				double mi = -1 * calculateMutualIndependence(i, j);
				weightedGraph.setEdgeWeight(e, mi);				
			}
		}
		KruskalMinimumSpanningTree<Integer, DefaultWeightedEdge> mstAlgo = new KruskalMinimumSpanningTree<>(weightedGraph);
		SpanningTree<DefaultWeightedEdge> mst = mstAlgo.getSpanningTree();
		Set<DefaultWeightedEdge> edges = mst.getEdges();
		int[] edgeCount = new int[this.count.length];
		for(DefaultWeightedEdge edge: edges) {
			edgeCount[weightedGraph.getEdgeSource(edge)] ++;
			edgeCount[weightedGraph.getEdgeTarget(edge)] ++;
		}
		Set<DefaultWeightedEdge> removeEdges = new LinkedHashSet<DefaultWeightedEdge>(weightedGraph.edgeSet());
		removeEdges.removeAll(edges);
		weightedGraph.removeAllEdges(removeEdges);
		GraphIterator<Integer, DefaultWeightedEdge> iterator = 
				new DepthFirstIterator<Integer, DefaultWeightedEdge>(weightedGraph);		
		Integer v;
		Integer t;
		while (iterator.hasNext()) {
			v = iterator.next();
			edges = weightedGraph.edgesOf(v);
			for(DefaultWeightedEdge edge: edges) {
				t = weightedGraph.getEdgeSource(edge);
				if(t == v)
					t = weightedGraph.getEdgeTarget(edge);
				if(!directedGraph.containsEdge(t, v))
					directedGraph.addEdge(v,t);
			}
		}
		return directedGraph;
	}

	private  double calculateMutualIndependence(int X, int Y) {
		double mutualInfo = 0.0, c_X, c_Y, N, mi;
		double[] jointCount = getCounts(X, Y);
		for (int i = 0; i< values.length ; i++) {
			if(values[i][0]==1) // Add one in Mutual Info
				c_X = jointCount[2]+jointCount[3];
			else
				c_X = jointCount[0]+jointCount[1];
			if(values[i][1]==1)
				c_Y = jointCount[1]+jointCount[2];
			else
				c_Y = jointCount[0]+jointCount[3];;
			if (jointCount[i] ==0 )
				continue;
			N = (double) this.numberOfTrainingSamples +4;
			mi = jointCount[i]*Math.log((jointCount[i] * N)/(c_X*c_Y))/N;
			mutualInfo += mi ;
		}
		if(mutualInfo < 0 || Double.isNaN(mutualInfo)) {
			System.out.println(" Error Mutual info negative edge: or NaN"+ X +" - "+ Y);
			System.exit(0);
		}
		return mutualInfo;
	}



	private  double[] getCounts(int x, int y) {
		double[] jointCounts = new double[]{1.0,1.0,1.0,1.0};// Add One in counts
		for(int j= 0; j < trainingData.size(); j++ ) {
			int[] sample = trainingData.get(j); 
			for(int i = 0; i < values.length; i++) {
				if(sample[x]==values[i][0] && sample[y]==values[i][1])
					jointCounts[i]+= this.dataWeights.get(j);
			}
		}
		return jointCounts;
	}

	@Override
	public void test(String[] sample) {
		// TODO Auto-generated method stub
		int[] data = new int[sample.length];
		for(int i = 0; i < sample.length; i++) { 
			data[i] = Integer.parseInt(sample[i]);
		}
		test(data);
	}


	public void test(int[] data) {
		double posProb;
		Set<DefaultEdge> edges;
		int s;

		for(int i = 0; i < data.length; i++) {
			posProb = getPositiveProbOfVariable(data, i);
			if(data[i]==1)
				this.testLogLikelihood += (Math.log(posProb)/Math.log(2));
			else
				this.testLogLikelihood += (Math.log(1-posProb)/Math.log(2));
		}
		this.numberOfTestSamples++;
	}

	public double getPositiveProbOfVariable(int[] data, int variable) {
		double posProb;
		Set<DefaultEdge> edges;
		int s;
		edges = this.network.incomingEdgesOf(variable);
		if(!edges.isEmpty()) {
			s = this.network.getEdgeSource(edges.iterator().next());
			posProb = ((Double[]) this.networkParameters.get(variable))[data[s]];
		}
		else
			posProb = (Double) this.networkParameters.get(variable);
		return posProb;
	}

	@Override
	public void train(String[] sample) {
		if(this.firstSampleFlag) {
			trainingData = new ArrayList<int[]>();
			this.dataWeights = new ArrayList<Double>();
			this.count = new int[sample.length];
			this.firstSampleFlag = false;
		}
		int[] s = new int[sample.length];
		for(int i = 0; i < sample.length; i++) {
			s[i] = Integer.parseInt(sample[i]);
			this.count[i] += s[i];
		}
		trainingData.add(s);
		this.dataWeights.add(1.0);
		this.numberOfTrainingSamples++;
	}


}
