import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.jgrapht.DirectedGraph;
import org.jgrapht.graph.DefaultEdge;

public class MixtureTreeBayesianNetwork extends ParameterLearningBN {

	private static final double epsilon = 0.001;
	int sizeOfLatentVariable;
	double[] latentParameters;
	int maxIterations;
	List<int[]> trainingData;
	Boolean firstSampleFlag = true;
	int numberOfTrainingSamples = 0;
	int[] count = new int[1];
	final int[][] values = {{0,0},{0,1},{1,1},{1,0}};
	public DirectedGraph<Integer, DefaultEdge> network ;
	public List<Object> networkParameters ;
	double testLogLikelihood = 0.0;
	int numberOfTestSamples = 0;
	List<Double>[] dataWeights;
	Random rand;
	TreeBayesianNetwork[] treeBN;
	
	public MixtureTreeBayesianNetwork(int k, int l) {
		// TODO Auto-generated constructor stub
		super();
		this.sizeOfLatentVariable = k;
		this.maxIterations = l;
		this.latentParameters = new double[k];
	}

	public void run(String[] args) {
		System.out.println(this.sizeOfLatentVariable +" Mixture Tree Bayesian Network");
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
		runEM();
		String testFile = args[1];
		processData(testFile, false);
		System.out.println("K value: "+ this.sizeOfLatentVariable +" | loglikelihood of "+testFile+" is "+(this.testLogLikelihood/this.numberOfTestSamples));
	}

	private void runEM() {
		boolean converged = false;
		double[] randomWeights = new double[this.sizeOfLatentVariable];
		double sum = 0.0;
		for( int i = 0; i < this.sizeOfLatentVariable; i++) {
			randomWeights[i] = rand.nextDouble();
			sum += randomWeights[i];
		}
		for( int i = 0; i < this.sizeOfLatentVariable; i++) {
			this.latentParameters[i] = randomWeights[i]/sum;
		}
		treeBN = new TreeBayesianNetwork[this.sizeOfLatentVariable];				
		int l = 0; 
		while( !converged && l < this.maxIterations){
			converged = true; l++;
//			System.out.println(" Starting iteration: "+ l);
			double[][] tempDataWeights = new double[this.sizeOfLatentVariable][this.trainingData.size()];
			double[] tempLatentParameters = new double[this.sizeOfLatentVariable];
			for(int k = 0; k < this.sizeOfLatentVariable; k++) {
				treeBN[k] = new TreeBayesianNetwork(this.trainingData, this.dataWeights[k], this.count, this.numberOfTrainingSamples);
				treeBN[k].learnBN();
				for(int i = 0; i< this.trainingData.size(); i++) {
					int[] sample = this.trainingData.get(i);
					double prob = this.latentParameters[k];
					for(int j = 0; j < sample.length; j++) {
						double posProb = treeBN[k].getPositiveProbOfVariable(sample, j);
						if(sample[j]==1)
							prob *= posProb;
						else
							prob *= (1-posProb);
					}
					tempDataWeights[k][i] = prob;
				}
			}
			// Normalizing the weights and updating latent paramters
//			this.latentParameters = new double[this.sizeOfLatentVariable];
			for(int i = 0; i < this.trainingData.size(); i++) {
				sum = 0.0;
				for(int k = 0; k < this.sizeOfLatentVariable; k++) {
					sum += tempDataWeights[k][i];
				}
				for(int k = 0; k < this.sizeOfLatentVariable; k++) {
					double temp = (tempDataWeights[k][i]/sum);
					this.dataWeights[k].set(i, temp);
					tempLatentParameters[k] += temp;
				}
			}
			sum = 0.0;
			for(int k = 0; k < this.sizeOfLatentVariable; k++) {
				sum += tempLatentParameters[k] ;
			}
			for(int k = 0; k < this.sizeOfLatentVariable; k++) {
				double temp = tempLatentParameters[k]/sum;
				if(converged && Math.abs(this.latentParameters[k] - temp) > epsilon) {
					converged = false;
				}
				this.latentParameters[k] = temp ;
			}
		}
		System.out.println("converged after "+l+" iterations");
	}

	@Override
	public void test(String[] sample) {
		// TODO Auto-generated method stub
		int[] data = new int[sample.length];
		for(int i = 0; i < sample.length; i++) { 
			data[i] = Integer.parseInt(sample[i]);
		}
		double prob = 0;
		for(int k = 0; k< this.sizeOfLatentVariable; k++) {
			double kprob = 1, posProb;
			for(int i = 0; i < sample.length; i++) {
				posProb = this.treeBN[k].getPositiveProbOfVariable(data, i);
				if(data[i]==1)
					kprob *= posProb;
				else
					kprob *= 1-posProb;
			}
			prob += (kprob*this.latentParameters[k]);
		}
		this.testLogLikelihood += (Math.log(prob)/Math.log(2));
//		System.out.println("Test "+ this.numberOfTestSamples +" : prob "+ prob +" loglikelihood : "+ this.testLogLikelihood);
		this.numberOfTestSamples++;
	}

	@Override
	public void train(String[] sample) {
		if(this.firstSampleFlag) {
			trainingData = new ArrayList<int[]>();
			this.count = new int[sample.length];
			this.firstSampleFlag = false;
			dataWeights = new ArrayList[this.sizeOfLatentVariable];
			for( int i = 0; i < this.sizeOfLatentVariable; i++) {
				dataWeights[i] = new ArrayList<Double>();
			}
			rand = new Random();
		}
		int[] s = new int[sample.length];
		for(int i = 0; i < sample.length; i++) {
			s[i] = Integer.parseInt(sample[i]);
			this.count[i] += s[i];
		}
		trainingData.add(s);
		double[] randomWeights = new double[this.sizeOfLatentVariable];
		double sum = 0.0;
		for( int i = 0; i < this.sizeOfLatentVariable; i++) {
			randomWeights[i] = rand.nextDouble();
			sum += randomWeights[i];
		}
		for( int i = 0; i < this.sizeOfLatentVariable; i++) {
			dataWeights[i].add(randomWeights[i]/sum);
		}
		this.numberOfTrainingSamples++;	
	}
}
