
/*** Author :Vibhav Gogate
The University of Texas at Dallas
 *****/

import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Random;
import java.util.stream.IntStream;

import javax.imageio.ImageIO;

public class KMeans {
	public static void main(String[] args) {
		if (args.length < 3) {
			System.out.println("Usage: Kmeans <input-image> <k> <output-image>");
			return;
		}
		try {
			BufferedImage originalImage = ImageIO.read(new File(args[0]));
			int k = Integer.parseInt(args[1]);
			BufferedImage kmeansJpg = kmeans_helper(originalImage, k);
			ImageIO.write(kmeansJpg, "jpg", new File(args[2]));

		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
	}

	private static BufferedImage kmeans_helper(BufferedImage originalImage, int k) {
		int w = originalImage.getWidth();
		int h = originalImage.getHeight();
		BufferedImage kmeansImage = new BufferedImage(w, h, originalImage.getType());
		Graphics2D g = kmeansImage.createGraphics();
		g.drawImage(originalImage, 0, 0, w, h, null);
		// Read rgb values from the image
		int[] rgb = new int[w * h];
		int count = 0;
		for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				rgb[count++] = kmeansImage.getRGB(i, j);
			}
		}
		// Call kmeans algorithm: update the rgb values
		rgb = kmeans(rgb, k);

		// Write the new rgb values to the image
		count = 0;
		for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				kmeansImage.setRGB(i, j, rgb[count++]);
			}
		}
		return kmeansImage;
	}

	// Your k-means code goes here
	// Update the array rgb by assigning each entry in the rgb array to its cluster
	// center
	private static int[] kmeans(int[] rgb, int k) {
		Random rand = new Random();
		int[] centers = new int[k];
		// Assign Random cluster centers
		for(int i=0; i<k; ) {
			int center = rgb[rand.nextInt(rgb.length)];
			boolean contains = IntStream.of(centers).anyMatch(x -> x == center);
			if(!contains) {
				centers[i] = center;
				i++;
			}
		}
		ArrayList<Color> rgbArray = new ArrayList<Color>();
		IntStream.of(rgb).forEach(x -> rgbArray.add(new Color(x)));
		ArrayList<Color> clusterCenters = new ArrayList<Color>();
		for(int c : centers) {
			clusterCenters.add(new Color(c));
		}
		int iteration = 0;
		int maxIterations = 1000;
		boolean converged = false;
		ArrayList<Color>[] clusterAssignments;
		while( (!converged) && iteration < maxIterations) {
			clusterAssignments = assignPixelsToCluster(rgbArray, clusterCenters);
			ArrayList<Color> clusterMeans = new ArrayList<Color>();
			for (int i = 0; i < clusterAssignments.length; i++) {
				clusterMeans.add(getMeans(clusterAssignments[i]));
			}
			if (clusterMeans.equals(clusterCenters)) {
				converged = true;
				System.out.println("Converged after iteration: "+ iteration);
			}
			clusterCenters = clusterMeans;
			iteration++;
		}

		// Update rgb based on cluster centers
		rgb = assignPixelsToCluster(rgb, clusterCenters);
		return rgb;

	}

	private static Color getMeans(ArrayList<Color> colors) {
		int redSum = 0, blueSum = 0, greenSum = 0, alphaSum = 0;
		for (Color rgb : colors) {
			redSum += rgb.getRed();
			blueSum += rgb.getBlue();
			greenSum += rgb.getGreen();
			alphaSum += rgb.getAlpha();
		}
		Color mean = new Color((int)redSum/colors.size(), (int) greenSum/colors.size(), (int) blueSum/colors.size(), (int) alphaSum/colors.size());
		return mean;
	}



	private static ArrayList<Color>[] assignPixelsToCluster(ArrayList<Color> rgbArray, ArrayList<Color> clusterCenters) {
		ArrayList<Color>[] clusterAssignment = new ArrayList[clusterCenters.size()];

		for (int r = 0; r < rgbArray.size(); r++) {
			Double minDistance = Double.MAX_VALUE;
			int cluster = 0;
			for (int i = 0; i < clusterCenters.size(); i++) {
				Double distance = distance(clusterCenters.get(i), rgbArray.get(r));
				if (minDistance > distance) {
					minDistance = distance;
					cluster = i;
				}
			}
			if (clusterAssignment[cluster] == null) {
				clusterAssignment[cluster] = new ArrayList<Color>();
			}
			clusterAssignment[cluster].add(rgbArray.get(r));
		}
		return clusterAssignment;
	}

	private static int[] assignPixelsToCluster(int[] rgb, ArrayList<Color> clusterCenters) {
		int[] clusterAssignment = new int[rgb.length];

		for (int r = 0; r < rgb.length; r++) {
			Double minDistance = Double.MAX_VALUE;
			int cluster = 0;
			Color color = new Color(rgb[r]);
			for (int i = 0; i < clusterCenters.size(); i++) {
				Double distance = distance(clusterCenters.get(i), color);
				if (minDistance > distance) {
					minDistance = distance;
					cluster = i;
				}
			}
			Color clusterColor = clusterCenters.get(cluster);
			clusterAssignment[r] = (((clusterColor.getRed() & 0x000000FF) << 16) | ((clusterColor.getGreen() & 0x000000FF) << 8) |((clusterColor.getBlue() & 0x000000FF) << 0));
		}
		return clusterAssignment;
	}


	private static Double distance(Color clusterCenter, Color rgb) {
		int redDist = rgb.getRed() - clusterCenter.getRed();
		int greenDist = rgb.getGreen() - clusterCenter.getGreen();
		int blueDist = rgb.getBlue() - clusterCenter.getBlue();
		int alphaDist = rgb.getAlpha() - clusterCenter.getAlpha();
		Double dist = Math.sqrt(redDist * redDist + greenDist * greenDist + blueDist * blueDist + alphaDist * alphaDist);
		return dist;
	}

}
