
public class Test {

	private static final String pathPrefix = "datasets/";
	private static final int limitOfConvergence = 100;

	/*Test file, training file, validation file, K for mixture, K for Bagging*/
	static String[][] datasets = {
			// {"accidents.test.data","accidents.ts.data", "accidents.valid.data", "20", "10"},
			// {"baudio.test.data", "baudio.ts.data", "baudio.valid.data", "17", "15"},
			// {"bnetflix.test.data","bnetflix.ts.data","bnetflix.valid.data","25", "30"},
			// {"dna.test.data","dna.ts.data","dna.valid.data","5", "5"},
			// {"jester.test.data", "jester.ts.data","jester.valid.data","15", "25"},
			// {"kdd.test.data", "kdd.ts.data","kdd.valid.data","4", "15"},
			// {"msnbc.test.data", "msnbc.ts.data","msnbc.valid.data","4", "10"},
			// {"nltcs.test.data", "nltcs.ts.data", "nltcs.valid.data", "35", "10"},
			// {"plants.test.data", "plants.ts.data", "plants.valid.data","45", "20"},
	};

	public static void main(String[] args) {
		int[] kValues = {2,4,5,7,10,12,15,17,20,25,30,35};
		int numberOfIterations = 10;
// 		findKofMixtureBN(kValues,numberOfIterations, false);
//		findKofBaggingBN(kValues, numberOfIterations, false);
//		testIndependentBN();
//		testTreeBN();
//		testBaggingBN(numberOfIterations);
// 		testMixtureBN(numberOfIterations);
	}

	private static void testMixtureBN(int numberOfIterations) {
		String[] arguments;
		for(String[] dataset : datasets) {
			System.out.println("Running dataset "+ dataset[1]+ " ...");
			arguments = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[0]};
			testMixtureBN(Integer.parseInt(dataset[3]), numberOfIterations, arguments);
		}
	}

	private static void testBaggingBN(int numberOfIterations) {
		String[] arguments;
		for(String[] dataset : datasets) {
			System.out.println("Running dataset "+ dataset[1]+ " ...");
			arguments = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[0]};
			testBaggingBN(Integer.parseInt(dataset[4]), numberOfIterations, arguments);
		}
	}

	private static void testTreeBN() {
		   String[] arguments;
		   TreeBayesianNetwork bn;
		   for(String[] dataset : datasets) {
			   System.out.println("Running dataset "+ dataset[1]+ " ...");
			   long startTime = System.currentTimeMillis();
			   arguments = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[0]};
			   bn = new TreeBayesianNetwork();
			   bn.run(arguments);
			   long endTime   = System.currentTimeMillis();
			   System.out.println("time: "+ (endTime - startTime)/1000+ " secs");
		   }

	}

	private static void testIndependentBN() {
		   String[] arguments;
		   IndependentBayesianNetwork bn;
		   for(String[] dataset : datasets) {
			   System.out.println("Running dataset "+ dataset[1]+ " ...");
			   long startTime = System.currentTimeMillis();
			   arguments = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[0]};
			   bn = new IndependentBayesianNetwork();
			   bn.run(arguments);
			   long endTime   = System.currentTimeMillis();
			   System.out.println("time: "+ (endTime - startTime)/1000+ " secs");
		   }
	}

	/**
	 * Runs the Mixture Tree Bayesian Network
	 *
	 * @param kValues
	 * @param numberOfIterations
	 * @param test
	 */
	private static void findKofMixtureBN(int[] kValues, int numberOfIterations, boolean test) {
		String[] validationArgs;
//		double bestLogLikelihood = Double.NEGATIVE_INFINITY;
		for(String[] dataset : datasets) {
			MixtureTreeBayesianNetwork bn = null;
			double bestLogLikelihood = Double.NEGATIVE_INFINITY;
			int bestK = 0;
			validationArgs = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[2]};
			System.out.println("Running dataset "+ dataset[1]+ " ...");
			double prevLogLikelihood = Double.NEGATIVE_INFINITY;
			for(int k : kValues) {
				double avgLogLikelihood = 0.0;
				for(int j=0; j<numberOfIterations;j++) {
					long startTime = System.currentTimeMillis();
					bn = new MixtureTreeBayesianNetwork(k,limitOfConvergence);
					bn.run(validationArgs);
					avgLogLikelihood += (bn.testLogLikelihood/bn.numberOfTestSamples);
					long endTime = System.currentTimeMillis();
					System.out.println("time: "+ (endTime - startTime)/1000+ " secs");
				}
				avgLogLikelihood = avgLogLikelihood/numberOfIterations;
				System.out.println("Average logLikelihood for K="+ k+ " is "+ avgLogLikelihood);
				if(avgLogLikelihood > bestLogLikelihood) {
					bestLogLikelihood = avgLogLikelihood;
					bestK = k;
				}
				if(prevLogLikelihood > (avgLogLikelihood) ) {
					System.out.println("Threshold found at: "+ bestK+ ", breaking the loop");
					break;
				}
				prevLogLikelihood = avgLogLikelihood;
			}
			System.out.println("Best K Value is "+ bestK);
			if(test) {
				String[] testArgs = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[0]};
				testMixtureBN(bestK, 10, testArgs);
			}
		}
	}

	private static void testMixtureBN(int sizeOfLatentVariable, int numberOfIterations, String[] testArgs) {
		// TODO Auto-generated method stub
		MixtureTreeBayesianNetwork bn = null;
		double avgLogLikelihood = 0.0;
		for(int j=0; j<numberOfIterations;j++) {
			long startTime = System.currentTimeMillis();
			bn = new MixtureTreeBayesianNetwork(sizeOfLatentVariable,limitOfConvergence);
			bn.run(testArgs);
			avgLogLikelihood += (bn.testLogLikelihood/bn.numberOfTestSamples);
			long endTime = System.currentTimeMillis();
			System.out.println("time: "+ (endTime - startTime)/1000+ " secs");
		}
		avgLogLikelihood = avgLogLikelihood/numberOfIterations;
		System.out.println("Average logLikelihood for K="+ sizeOfLatentVariable+ " is "+ avgLogLikelihood);
	}

	private static void findKofBaggingBN(int[] kValues, int numberOfIterations, boolean test) {
		String[] validationArgs;
//		double bestLogLikelihood = Double.NEGATIVE_INFINITY;
		for(String[] dataset : datasets) {
			BaggingMixtureTreeBayesianNetwork bn = null;
                        double bestLogLikelihood = Double.NEGATIVE_INFINITY;
			int bestK = 0;
			validationArgs = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[2]};
			System.out.println("Running dataset "+ dataset[1]+ " ...");
			double prevLogLikelihood = Double.NEGATIVE_INFINITY;
			for(int k : kValues) {
				double avgLogLikelihood = 0.0;
				double baselineAvgLogLikelihood = 0.0;
				for(int j=0; j<numberOfIterations;j++) {
					long startTime = System.currentTimeMillis();
					bn = new BaggingMixtureTreeBayesianNetwork(k);
					bn.run(validationArgs);
					avgLogLikelihood += (bn.testLogLikelihood/bn.numberOfTestSamples);
					baselineAvgLogLikelihood += (bn.baselineTestLogLikelihood/bn.numberOfTestSamples);
					long endTime = System.currentTimeMillis();
					System.out.println("time: "+ (endTime - startTime)/1000+ " secs");
				}
				avgLogLikelihood = avgLogLikelihood/numberOfIterations;
				System.out.println("Average Baseline logLikelihood for K="+ k+ " is "+ baselineAvgLogLikelihood/numberOfIterations);
				System.out.println("Average logLikelihood for K="+ k+ " is "+ avgLogLikelihood);
				if(avgLogLikelihood < baselineAvgLogLikelihood/numberOfIterations) {
					System.out.println("========Baseline is better==========");
				}
				if(avgLogLikelihood > bestLogLikelihood) {
					bestLogLikelihood = avgLogLikelihood;
					bestK = k;
				}
				if(prevLogLikelihood > (avgLogLikelihood) ) {
					System.out.println("Threshold found at "+ bestK+ ", breaking the loop");
					break;
				}
				prevLogLikelihood = avgLogLikelihood;
			}
			System.out.println("Best K Value is "+ bestK);
			if(test) {
				String[] testArgs = new String[] {pathPrefix+dataset[1], pathPrefix+dataset[0]};
				testBaggingBN(bestK, 10, testArgs);
			}
		}
	}

	private static void testBaggingBN(int sizeOfLatentVariable, int numberOfIterations, String[] testArgs) {
		// TODO Auto-generated method stub
		BaggingMixtureTreeBayesianNetwork bn = null;
		double avgLogLikelihood = 0.0;
		double baselineAvgLogLikelihood = 0.0;
		for(int j=0; j<numberOfIterations;j++) {
			long startTime = System.currentTimeMillis();
			bn = new BaggingMixtureTreeBayesianNetwork(sizeOfLatentVariable);
			bn.run(testArgs);
			avgLogLikelihood += (bn.testLogLikelihood/bn.numberOfTestSamples);
			baselineAvgLogLikelihood += (bn.baselineTestLogLikelihood/bn.numberOfTestSamples);
			long endTime = System.currentTimeMillis();
			System.out.println("time: "+ (endTime - startTime)/1000+ " secs");
		}
		avgLogLikelihood = avgLogLikelihood/numberOfIterations;
		System.out.println("Average logLikelihood for K="+ sizeOfLatentVariable+ " is "+ avgLogLikelihood);
		System.out.println("Average Baseline logLikelihood for K="+ sizeOfLatentVariable+ " is "+ baselineAvgLogLikelihood/numberOfIterations);
	}

}
