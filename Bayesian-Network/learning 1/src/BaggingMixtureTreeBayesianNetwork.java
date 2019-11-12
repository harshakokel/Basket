import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

import org.jgrapht.DirectedGraph;
import org.jgrapht.graph.DefaultEdge;

public class BaggingMixtureTreeBayesianNetwork extends ParameterLearningBN {
	
	int sizeOfLatentVariable;
	double[] latentParameters;
	private static final double epsilon = 0.001;
	int maxIterations;;
	List<int[]> trainingData;
	Boolean firstSampleFlag = true;
	int numberOfTrainingSamples = 0;
	final int[][] values = {{0,0},{0,1},{1,1},{1,0}};
	double testLogLikelihood = 0.0;
	double baselineTestLogLikelihood = 0.0;
	int numberOfTestSamples = 0;
	Random rand;
	TreeBayesianNetwork treeBN[];
	
	public BaggingMixtureTreeBayesianNetwork(int k) {
		// TODO Auto-generated constructor stub
		super();
		this.sizeOfLatentVariable = k;
		this.latentParameters = new double[k];
		this.treeBN = new TreeBayesianNetwork[k];
	}
	
	public void run(String[] args) {
		System.out.println("Bagging "+ this.sizeOfLatentVariable +" Mixture Tree Bayesian Network");
		trainingData = null;
		this.firstSampleFlag = true;
		this.numberOfTrainingSamples = 0;
		this.testLogLikelihood = 0.0;
		this.baselineTestLogLikelihood = 0.0;
		this.numberOfTestSamples = 0;
		String trainingFile = args[0];
		processData(trainingFile, true);
		learnBaggingMixture();
		String testFile = args[1];
		processData(testFile, false);
		System.out.println("K value: "+ this.sizeOfLatentVariable +" | Baseline loglikelihood of "+testFile+" is "+(this.baselineTestLogLikelihood/this.numberOfTestSamples));
		System.out.println("K value: "+ this.sizeOfLatentVariable +" | loglikelihood of "+testFile+" is "+(this.testLogLikelihood/this.numberOfTestSamples));
	}

	private void learnBaggingMixture() {
		// TODO Auto-generated method stub
		List<int[]> bootstrapData;
		int[] count; 
		List<Double> dataWeights;
		for(int i = 0; i< this.sizeOfLatentVariable; i++) {
			// Generate Bootstrap Sample
			bootstrapData = new ArrayList<int[]>();
			count =  new int[trainingData.get(0).length];
			dataWeights = new ArrayList<Double>();
			for(int j =0 ; j < this.numberOfTrainingSamples; j++) {
				int randomNum = ThreadLocalRandom.current().nextInt(0, this.numberOfTrainingSamples );
				
				int[] bootstrapSample = trainingData.get(randomNum);
				for(int k =0; k< count.length; k++) {
					count[k] += bootstrapSample[k];
				}
				bootstrapData.add(bootstrapSample);
				dataWeights.add(1.0);
			}
			// Learn Tree Bayesian Network
			treeBN[i] = new TreeBayesianNetwork(bootstrapData, dataWeights , count, this.numberOfTrainingSamples);
			treeBN[i].learnBN();
//			System.out.println("Learnt tree "+ i +" : "+ treeBN[i].toString());
			for(int j =0 ; j < this.numberOfTrainingSamples; j++) {
				treeBN[i].test(this.trainingData.get(j));
			}
			this.latentParameters[i] = treeBN[i].testLogLikelihood/treeBN[i].numberOfTestSamples;
		}
		double sum = 0.0;
		for(int i = 0; i< this.sizeOfLatentVariable; i++) {
			sum += this.latentParameters[i];
		}
		for(int i = 0; i< this.sizeOfLatentVariable; i++) {
			this.latentParameters[i] = (sum-this.latentParameters[i]);
		}
		sum = 0.0;
		for(int i = 0; i< this.sizeOfLatentVariable; i++) {
			sum += this.latentParameters[i];
		}
		for(int i = 0; i< this.sizeOfLatentVariable; i++) {
			this.latentParameters[i] = this.latentParameters[i]/sum;
		}
	}

	@Override
	public void test(String[] sample) {
		int[] data = new int[sample.length];
		for(int i = 0; i < sample.length; i++) { 
			data[i] = Integer.parseInt(sample[i]);
		}
		double prob = 0, baseProb = 0.0;
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
			baseProb += (kprob/this.sizeOfLatentVariable);
		}
		this.testLogLikelihood += (Math.log(prob)/Math.log(2));
		this.baselineTestLogLikelihood += (Math.log(baseProb)/Math.log(2));
//		System.out.println("Test "+ this.numberOfTestSamples +" : prob "+ prob +" loglikelihood : "+ this.testLogLikelihood);
		this.numberOfTestSamples++;
	}

	@Override
	public void train(String[] sample) {
		if(this.firstSampleFlag) {
			trainingData = new ArrayList<int[]>();
			this.firstSampleFlag = false;	
			rand = new Random();
		}
		int[] s = new int[sample.length];
		for(int i = 0; i < sample.length; i++) {
			s[i] = Integer.parseInt(sample[i]);
		}
		trainingData.add(s);
		this.numberOfTrainingSamples++;
	}

}
