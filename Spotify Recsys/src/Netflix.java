import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Set;

public class Netflix {

	public static void main(String[] args) {


		File Trainingfile = new File(
				"C:\\Users\\Mythri Thippareddy\\Desktop\\Machine_Learning\\HW3\\netflix\\TrainingRatings.txt");
		File Testingfile = new File(
				"C:\\Users\\Mythri Thippareddy\\Desktop\\Machine_Learning\\HW3\\netflix\\TestingRatings.txt");
		
//		File Trainingfile = new File(args[0]);
//		File Testingfile = new File(args[1]);

		BufferedReader br1;
		BufferedReader br2;
		BufferedReader br3;
		try {
			br1 = new BufferedReader(new FileReader(Trainingfile));

			HashMap<Integer, HashMap<Integer, Double>> outerTrainingRatingsMap = new HashMap<Integer, HashMap<Integer, Double>>();
			outerTrainingRatingsMap = HashingRatings(br1, outerTrainingRatingsMap);

			br1 = new BufferedReader(new FileReader(Trainingfile));
			br3= new BufferedReader(new FileReader(Trainingfile));
			
			HashMap<Integer, Double> averageMap = new HashMap<Integer, Double>();
			
			double maxNumberOfUsers = CheckMaxUserID(br3);
			
			averageMap = calculateAverage(br1, averageMap, maxNumberOfUsers);
			br2 = new BufferedReader(new FileReader(Testingfile));
			System.out.println("");
			 testingRating(br2, averageMap, outerTrainingRatingsMap);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static double CheckMaxUserID(BufferedReader br1) {
		String st;
		double maxUSERID=0;
		try {
			while ((st = br1.readLine()) != null) {
				String[] str_array = st.split(",");
				double USERID = Double.parseDouble(str_array[1]);
				if(USERID>maxUSERID) {
					maxUSERID = USERID;
				}		
			}
			System.out.println("maxUSERID = "+maxUSERID);
			System.out.println("");
		} catch (IOException e) {
			e.printStackTrace();
		}		
		return maxUSERID;
	}

	private static void testingRating(BufferedReader br, HashMap<Integer, Double> averageMap,
			HashMap<Integer, HashMap<Integer, Double>> outerTrainingRatingsMap) {
		System.out.println("Starting predicting from test set");
		String st;
		double meanAbsoluteError = 0;
		double rootMeanSquareError = 0;
		double numberOfTestValues = 0;
		
		int USERID;
		int MOVIEID;
		double actualRATING;
		double predictedValue;
		double weight;
		double k;
		double endTime;
		double totalTime;
		double previoustime = 0;
		double taken;
		String[] str_array;
		double startTime = System.nanoTime();
		try {			
			while ((st = br.readLine()) != null) {
				numberOfTestValues++;
				str_array = st.split(",");
				USERID = Integer.parseInt(str_array[1]);
				MOVIEID = Integer.parseInt(str_array[0]);
				actualRATING = Double.parseDouble(str_array[2]);
				predictedValue=0;
				k = 0;
				for (Integer USERID2 : averageMap.keySet()) {
					weight = calculateweight(USERID, USERID2, averageMap,outerTrainingRatingsMap);
					if(Double.compare(weight,0)!=0){
						try {
							k = k +Math.abs(weight);
							predictedValue = predictedValue + weight*(outerTrainingRatingsMap.get(USERID2).get(MOVIEID) - averageMap.get(USERID2));
						}catch(NullPointerException e) {
						}
					}
				}
				if(k!=0) {
					predictedValue = predictedValue/k;
				}
				predictedValue = predictedValue + averageMap.get(USERID);

//				System.out.println("UserID:"+USERID+" MovieID:"+MOVIEID);
//				System.out.println("Predicted Rating:"+predictedValue);
//				System.out.println("Actual Rating:"+actualRATING);
//				System.out.println("Difference:"+Math.abs(actualRATING-predictedValue));
//				System.out.println("");

				meanAbsoluteError= meanAbsoluteError+Math.abs(actualRATING-predictedValue);
				rootMeanSquareError = rootMeanSquareError+ ((actualRATING-predictedValue)*(actualRATING-predictedValue));

				if((numberOfTestValues%1000)==0) {
					System.out.println("Number of Test Values Predicted:"+numberOfTestValues);
					System.out.println("Mean square Error Accumulated = "+meanAbsoluteError);
					System.out.println("rootMeanSquareError Accumulated = "+rootMeanSquareError);
					endTime   = System.nanoTime();
					totalTime = endTime - startTime;
					System.out.println("time in seconds: "+(totalTime/1000000000));
					taken = endTime - previoustime;
					System.out.println("time taken by this block "+taken/1000000000);
					previoustime = endTime;
					System.out.println("");
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		meanAbsoluteError = meanAbsoluteError/numberOfTestValues;
		rootMeanSquareError = Math.sqrt(rootMeanSquareError/numberOfTestValues);

		System.out.println("Total Number of Test Values:"+numberOfTestValues);
		System.out.println("Final MeanAbsoluteError = "+meanAbsoluteError);
		System.out.println("Final RootMeanSquareError = "+rootMeanSquareError);
		endTime   = System.nanoTime();
		totalTime = endTime - startTime;
		System.out.println("Total time in seconds: "+(totalTime/1000000000));
	}

	private static double calculateweight(int USERID1, Integer USERID2, HashMap<Integer, Double> averageMap,
			HashMap<Integer, HashMap<Integer, Double>> outerTrainingRatingsMap) {
		
		HashMap<Integer, Double> map1 = outerTrainingRatingsMap.get(USERID1);
		HashMap<Integer, Double> map2 = outerTrainingRatingsMap.get(USERID2);
		Set<Integer> intersectionSet = map1.keySet();
		Set<Integer> keyset2 = map2.keySet();
		intersectionSet.retainAll(keyset2);

		double numerator = 0;
		double denominator = 0;
		double denominator1 = 0;
		double denominator2 = 0;
		double weightValue =0;
		double a;
		double b;

		for (Integer key : intersectionSet) {
			a = outerTrainingRatingsMap.get(USERID1).get(key) - averageMap.get(USERID1);
			b = outerTrainingRatingsMap.get(USERID2).get(key) - averageMap.get(USERID2);
			numerator = numerator + (a * b);
			denominator1 = denominator1 + (a * a);
			denominator2 = denominator2 + (b * b);
		}
		denominator = denominator1 * denominator2;

		if(Double.compare(denominator, 0)!=0){
			weightValue = numerator / Math.sqrt(denominator);
		}
		return (weightValue);
	}

	private static HashMap<Integer, Double> calculateAverage(BufferedReader br, HashMap<Integer, Double> averageMap, double maxNumberOfUsers) {
		System.out.println("Initiaizing the Hash map for averages");
		double averageUserRating[][] = new double[(int) (maxNumberOfUsers+1)][2];
		try {
			String st;
			int USERID;
			double RATING;
			String[] str_array ;
			while ((st = br.readLine()) != null) {
				str_array = st.split(",");
				USERID = Integer.parseInt(str_array[1]);
				RATING = Double.parseDouble(str_array[2]);
				averageUserRating[USERID][0]++;
				averageUserRating[USERID][1] = averageUserRating[USERID][1] + RATING;
			}
			for (int i = 0; i <= maxNumberOfUsers; i++) {
				if (Double.compare(averageUserRating[i][0], 0) != 0) {
					averageMap.put(i, averageUserRating[i][1] / averageUserRating[i][0]);
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		System.out.println("Averages Hash Map initialized");
		System.out.println("");
		return averageMap;
	}

	private static HashMap<Integer, HashMap<Integer, Double>> HashingRatings(BufferedReader br,
			HashMap<Integer, HashMap<Integer, Double>> outerMap) {
		System.out.println("Initializing the Hash map with Users, movies and ratings");
		try {
			String st;
			int numberOfCollisions = 0;
			String[] str_array;
			int USERID;
			int MOVIEID;
			double RATING;
			Double value;
			while ((st = br.readLine()) != null) {
				str_array = st.split(",");
				USERID = Integer.parseInt(str_array[1]);
				MOVIEID = Integer.parseInt(str_array[0]);
				RATING = Double.parseDouble(str_array[2]);
				try {
					value = outerMap.get(USERID).get(MOVIEID);
					if (value == null) {
						HashMap<Integer, Double> innerMap;
						innerMap = outerMap.get(USERID);
						innerMap.put(MOVIEID, RATING);
					} else {
						System.out.println(
								"First function. Value already exist. Here this should not happen. Collision occurred");
						numberOfCollisions++;
					}
				} catch (NullPointerException e) {
					HashMap<Integer, Double> innerMap = new HashMap<Integer, Double>();
					outerMap.put(USERID, innerMap);
					innerMap.put(MOVIEID, RATING);
				}
			}
			System.out.println("numberOfCollisions = " + numberOfCollisions);
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Training set Rating Hash Map initialized");
		System.out.println("");
		return outerMap;
	}
}
