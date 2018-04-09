import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;
import java.util.ArrayList;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Set;

class Model{

	public Hashtable<Integer, Hashtable<Integer, Double>> userTable = new Hashtable<Integer, Hashtable<Integer,Double>>();
	public Hashtable<Integer, Double> meanRatings =  new Hashtable<Integer, Double>();
	public Hashtable<String, Double> userCorrelation = new Hashtable<String, Double>();

}

class Test extends Thread{

	Model m;
	ArrayList<String> lines;
	int i;

	public Test(int i, Model m, ArrayList<String> lines) {
		super();
		this.i = i;
		this.m = m;
		this.lines = lines;
	}

	private Double predict(Integer user, Integer movie) {
		// TODO Auto-generated method stub
		Double prediction = 0.0;
		Double weightSum = 0.0;
		Enumeration<Integer> userEnumeration = m.userTable.keys();
		while (userEnumeration.hasMoreElements()) {
			Integer u = userEnumeration.nextElement();
			Hashtable<Integer, Double> userRatings = m.userTable.get(u);
			if (!userRatings.containsKey(movie))
			continue;
			Double weight = getCorrelation(user, u);
			if (weight == 0.0)
			continue;
			prediction += weight*(userRatings.get(movie) - m.meanRatings.get(u));
			weightSum += Math.abs(weight);
		}
		if(prediction == 0.0)
		return prediction + m.meanRatings.get(user);
		prediction = prediction/weightSum;
		prediction += m.meanRatings.get(user);
		return prediction;
	}

	private Double getCorrelation(Integer user_a, Integer user_i) {
		if (user_a > user_i) {
			Integer temp = user_a;
			user_a = user_i;
			user_i = temp;
		}
		String key = user_a+"_"+user_i;
		if( m.userCorrelation.containsKey(key))
		return m.userCorrelation.get(key);
		Hashtable<Integer, Double> ratings_a = m.userTable.get(user_a);
		Hashtable<Integer, Double> ratings_i = m.userTable.get(user_i);
		Set<Integer> ratedMovies = new HashSet<Integer>(ratings_a.keySet());
		ratedMovies.retainAll(ratings_i.keySet());
		if (ratedMovies.isEmpty()) {
			m.userCorrelation.put(key, 0.0);
			return m.userCorrelation.get(key);
		}
		Double numerator = 0.0;
		Double denominator_a = 0.0;
		Double denominator_i = 0.0;
		Double mean_a = m.meanRatings.get(user_a);
		Double mean_i = m.meanRatings.get(user_i);
		for (Integer movie : ratedMovies) {
			numerator += (ratings_a.get(movie) - mean_a)*(ratings_i.get(movie) - mean_i);
			denominator_a += Math.pow((ratings_a.get(movie) - mean_a), 2);
			denominator_i += Math.pow((ratings_i.get(movie) - mean_i), 2);
		}
		if (numerator == 0.0)
		m.userCorrelation.put(key, 0.0);
		else
		m.userCorrelation.put(key, numerator/Math.sqrt(denominator_a*denominator_i));
		return m.userCorrelation.get(key);

	}

	public void run()
	{
		try
		{
			String cvsSplitBy = ",";
			Double absoluteError = 0.0;
			Double squaredError = 0.0;
			int count =0;
			System.out.println("Movie User Rating Prediction");
			for(String line : lines) {
				String[] data = line.split(cvsSplitBy);
				Integer movie = Integer.valueOf(data[0]);
				Integer user = Integer.valueOf(data[1]);
				Double rating = Double.valueOf(data[2]);
				Double prediction = predict(user, movie);
				System.out.println(movie+" "+user+" "+rating+" "+ prediction);
				absoluteError += Math.abs(prediction - rating);
				squaredError += Math.pow((prediction - rating), 2);
				count ++;
			}
			System.out.println(" Absolute Error: "+ absoluteError);
			System.out.println(" Squared Error: "+ squaredError);
	                System.out.println(" Mean Absolute Error: "+ (absoluteError/count));
	                System.out.println(" Root Mean Squared Error: "+ Math.sqrt(squaredError/count));
		}
		catch (Exception e)
		{
			// Throwing an exception
			System.out.println ("Exception is caught");
		}
	}
}

public class CollaborativeFilter{

	public static void main(String[] args) {
		if (args.length < 2) {
			System.out.println("Expects 2 arguments: java CollaborativeFilter <training file> <testing file>");
			return;
		}
		String train = args[0];
		String test = args[1];
		Model CF = new Model();
		processingNetflixFile(CF, train);
		System.out.println("Training file read");
		testData(CF, test);
	}

	private static void testData(Model m, String test) {
		// TODO Auto-generated method stub
		BufferedReader br = null;
		try {
			LineNumberReader lineNumberReader = new LineNumberReader(new FileReader(test));
			lineNumberReader.skip(Long.MAX_VALUE);
			int numberOfLines = lineNumberReader.getLineNumber();
			lineNumberReader.close();
			br = new BufferedReader(new FileReader(test));
			int numberOfThreads = 1;
			int max = numberOfLines/numberOfThreads;
			ArrayList<String>[] testLines = new ArrayList[numberOfThreads];
			String line = "";
			int count = 1;
			int thread = 0;
			int s = max;
			testLines[thread] = new ArrayList<String>();
			while ((line = br.readLine()) != null) {
				if(count > s) {
					thread ++;
					s = max*thread+1;
					if(thread <20) {
						testLines[thread] = new ArrayList<String>();
					} else {
						thread = 19;
					}
				}
				testLines[thread].add(line);
				count++;
			}
			for(int i =0; i< numberOfThreads;i++) {
				Test testThread = new Test(i, m, testLines[i]);
				testThread.start();
			}

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}





	private static void processingNetflixFile(Model CF, String train) {
		// TODO Auto-generated method stub
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";

		try {

			br = new BufferedReader(new FileReader(train));
			while ((line = br.readLine()) != null) {
				//            		System.out.println(line);
				// use comma as separator
				String[] data = line.split(cvsSplitBy);
				Integer movie = Integer.valueOf(data[0]);
				Integer user = Integer.valueOf(data[1]);
				Double rating = Double.valueOf(data[2]);
				if (!CF.userTable.containsKey(user)) {
					CF.userTable.put(user, new Hashtable<Integer, Double>());
					CF.meanRatings.put(user,0.0);
					//                		break;
				}
				CF.userTable.get(user).put(movie, rating);
				Double mean = CF.meanRatings.get(user);
				CF.meanRatings.put(user, (mean + rating));

			}
			setMeanRatings(CF);

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}

	private static void setMeanRatings(Model CF) {
		// TODO Auto-generated method stub
		Enumeration<Integer> userEnumeration = CF.userTable.keys();
		while (userEnumeration.hasMoreElements()) {
			Integer user = userEnumeration.nextElement();
			Double mean = CF.meanRatings.get(user)/CF.userTable.get(user).size();
			CF.meanRatings.put(user, mean);
		}
	}

}
