public class IndependentBayesianNetwork extends ParameterLearningBN {

	double defaultPrior = 0.0;
	double[] posProb = new double[1];
	int numberOfTrainingSamples = 0;
	int[] count = new int[1];
	double testLogLikelihood = 0.0;
	int numberOfTestSamples = 0;
	boolean firstSampleFlag = true;

	public void run(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Independent Bayesian Network");
		defaultPrior = 0.0;
		posProb = new double[1];
		numberOfTrainingSamples = 0;
		count = new int[1];
		testLogLikelihood = 0.0;
		numberOfTestSamples = 0;
		firstSampleFlag = true;
		String trainingFile = args[0];
		processData(trainingFile, true);
		learnParameters();
		String testFile = args[1];
		processData(testFile, false);
		System.out.println("loglikelihood of "+testFile+" is "+(testLogLikelihood/numberOfTestSamples));
	}	

	public void test(String[] sample) {
		for(int i = 0; i < sample.length; i++) { 
			if(Integer.parseInt(sample[i]) == 1) {
				testLogLikelihood += (Math.log(posProb[i])/Math.log(2));
			} else {
				testLogLikelihood += (Math.log(1 - posProb[i])/Math.log(2));
			}
		}
		numberOfTestSamples++;
	}

	private void learnParameters() {
		// Add One Laplace smoothing. 
		defaultPrior = (double) 1/(numberOfTrainingSamples+2);
		posProb = new double[count.length];
		for(int i =0; i< count.length; i++) {
			if(count[i] != 0)
				posProb[i] = (double) (count[i] +1)/(numberOfTrainingSamples+2);
			else
				posProb[i] = defaultPrior;
		}
	}

	public void train(String[] sample) {
		if(firstSampleFlag) {
			count = new int[sample.length];
			firstSampleFlag = false;
		}
		for(int i = 0; i < sample.length; i++) { 
			count[i] += Integer.parseInt(sample[i]);
		}
		numberOfTrainingSamples++;
	}

}
