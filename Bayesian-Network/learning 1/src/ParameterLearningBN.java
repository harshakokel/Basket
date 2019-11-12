import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public abstract class ParameterLearningBN {


	public void processData(String filename, boolean trainingFlag) {
		// TODO Auto-generated method stub
		BufferedReader br = null;
		try {
			String cvsSplitBy = ",";
			
			br = new BufferedReader(new FileReader(filename));
			String line = br.readLine();
			String[] sample = line.split(",");
			// all samples should be of same length
			while (line != null) {
				sample = line.split(cvsSplitBy);
				// Length of all samples should always be equal to number of Variables
				if(trainingFlag)
					train(sample);
				else
					test(sample);
				line = br.readLine();
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

	public abstract void test(String[] sample);

	public abstract void train(String[] sample) ;
}
