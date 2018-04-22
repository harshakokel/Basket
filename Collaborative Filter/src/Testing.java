import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Timestamp;
import java.util.Date;
import java.util.Hashtable;

public class Testing {

	public static Hashtable<Integer, Hashtable<Integer, Double>> userTable = new Hashtable<Integer, Hashtable<Integer,Double>>();

	@SuppressWarnings("resource")
	public static void main(String[] args) {
		String prediction = "../Run_1.out";
		String test = "../data/netflix/TestingRatings.txt";
		Date date = new Date();
        System.out.println(new Timestamp(date.getTime()));
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = " ";

		try {

            br = new BufferedReader(new FileReader(prediction));
            while ((line = br.readLine()) != null) {
//            		System.out.println(line);
                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                Integer movie = Integer.valueOf(data[1]);
                Integer user = Integer.valueOf(data[2]);
                Double rating = Double.valueOf(data[4]);
                if (!userTable.containsKey(user)) {
                		userTable.put(user, new Hashtable<Integer, Double>());
                	}
                userTable.get(user).put(movie, rating);
            }
            br = new BufferedReader(new FileReader(test));
            cvsSplitBy =",";
            Double absolute_error = 0.0;
            Double squared_error = 0.0;
            int count = 0;
            while ((line = br.readLine()) != null) {
            		String[] data = line.split(cvsSplitBy);
                Integer movie = Integer.valueOf(data[0]);
                Integer user = Integer.valueOf(data[1]);
                Double rating = Double.valueOf(data[2]);
                Double prediction1 = userTable.get(user).get(movie);
                System.out.println(movie+" "+user+" "+" "+rating+" "+prediction1);

	            absolute_error += Math.abs(prediction1 - rating);
	            squared_error += Math.pow((prediction1 - rating), 2);
	            count++;
            }
            System.out.println("Absolute  Error "+ absolute_error);
            System.out.println("Squared Error "+ squared_error);
            System.out.println("Absolute Mean Error"+ (absolute_error/count));
            System.out.println("Root Mean Squared Error"+ Math.sqrt(squared_error/count));
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
}
