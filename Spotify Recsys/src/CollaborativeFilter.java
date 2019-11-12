import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import java.util.TreeMap;

import org.apache.commons.lang.ArrayUtils;

/**
 * @author Harsha Kokel
 *
 */
public class CollaborativeFilter {
	private static final int ALBUM_INDEX = 1;
	private static final int ARTIST_INDEX = 0;
	private static final int MaximumK = 1001;
	private static final Random RANDOM = new Random();
	static HashMap<String, HashSet<String>> playlistTrackMap;
	static HashMap<String, String[]> trackArtistAlbumMap;
	static HashSet<String> trainTracks;
	static HashMap<String, HashSet<String>> testMap;
//	static HashMap<String, TreeMap<String, Double>> prediction;
	static HashMap<String, HashMap<String, Double>> playlistArtistMap;
	static HashMap<String, HashMap<String, Double>> playlistAlbumMap;
	static HashMap<String, Double> tracksCorrelation;
	static HashMap<String, Double> albumsCorrelation;
	static HashMap<String, Double> artistsCorrelation;
	static HashMap<String,Double> artistAverageValues;
	static HashMap<String,Double> albumAverageValues;
	static double precision_10,  precision_50, precision_100, precision_200, precision_500, precision_1000; 

	public static void main(String[] args) {
		// Getting training file names
		String trainingFilename = args[0];
		long startTime = System.currentTimeMillis();
		//Initializing all global the variables
		playlistTrackMap = new HashMap<String, HashSet<String>>();
		trainTracks = new HashSet<String>();
		testMap = new HashMap<String, HashSet<String>>();
		tracksCorrelation = new HashMap<String, Double>();
		albumsCorrelation = new HashMap<String, Double>();
		artistsCorrelation = new HashMap<String, Double>();
//		prediction = new HashMap<String, TreeMap<String, Double>>();
		playlistArtistMap = new HashMap<String, HashMap<String, Double>>();
		playlistAlbumMap = new HashMap<String, HashMap<String, Double>>();
		artistAverageValues= new HashMap<String, Double>();
		albumAverageValues=new HashMap<String, Double>();
		trackArtistAlbumMap = new HashMap<String, String[]>();
		//Reading all the training files into the hash maps
		hashPlaylists(trainingFilename);
		long endTime   = System.currentTimeMillis();
		System.out.println("Training completed in "+ (endTime - startTime)/1000+ " secs");
		//Testing the playlists		
		testPlaylists();
		startTime   = System.currentTimeMillis();
		System.out.println("Testing completed in "+ (startTime - endTime)/1000+ " secs");
	}

	/**
	 * Loop over training files and create a artist, album and track map
	 * 
	 * @param trainingTrackFilename
	 */
	private static void hashPlaylists(String trainingFilename) {
		BufferedReader br = null;
		String line = "",  cvsSplitBy = ",", playlistId, track, artist, album;
		int playlistLength;
		String[] row, artistAlbumArray ;
		List<Integer> testTrackIndexes;
		HashSet<String> testTracks, playlistTracks;
		HashMap<String, Double> playlistArtists, playlistAlbums;
		try {
			br = new BufferedReader(new FileReader(trainingFilename));
			int rand;
			// each line in csv is a playlist
			while ((line = br.readLine()) != null) {
				//Get new row of excel
				row = line.split(cvsSplitBy);
				
				//Get playlist ID from first column and remove it from row
				playlistId = row[0];
				row = (String[]) ArrayUtils.removeElement(row, playlistId);

				//Put aside 10% of tracks from playlist for testing 
				testTracks = new HashSet<String>();
				playlistLength = row.length/3;
				int noOfTestTracks =  (playlistLength > 10) ? (int) (playlistLength*0.1) : 1;
				for(int i =0; i< noOfTestTracks; i++ ) {
					int t = RANDOM.nextInt(playlistLength)*3;
					if(row[t].contains("album") || row[t].contains("artist")) {
						System.exit(0);
					}
					testTracks.add(row[t]);
					row = (String[]) ArrayUtils.remove(row, t); //Removing the track
					row = (String[]) ArrayUtils.remove(row, t); //Removing the artist
					row = (String[]) ArrayUtils.remove(row, t); //Removing the album
					playlistLength--;
				}
				
				//Hash training items
				playlistTracks = new HashSet<String>();
				playlistArtists = new HashMap<String, Double>();
				playlistAlbums = new HashMap<String, Double>();
				artistAlbumArray = new String[2];
				for(int i=0 ; i< row.length;) {
					track = row[i++];
					artist = row[i++];
					album = row[i++];
					playlistTracks.add(track);
					if (playlistArtists.containsKey(artist)) {
						playlistArtists.put(artist, playlistArtists.get(artist)+1);
					} else {
						playlistArtists.put(artist, 1.0);
					}
					if (playlistAlbums.containsKey(album)) {
						playlistAlbums.put(album, playlistAlbums.get(album)+1);
					} else {
						playlistAlbums.put(album, 1.0);
					}
					artistAlbumArray[ARTIST_INDEX] = artist;
					artistAlbumArray[ALBUM_INDEX] = album;
					if(!trackArtistAlbumMap.containsKey(track)) {
						trackArtistAlbumMap.put(track, artistAlbumArray);
					}
				}
				//Normalizing 
				for (String key : playlistArtists.keySet()) {
					playlistArtists.put(key, playlistArtists.get(key)/playlistTracks.size());
				}
				for (String key : playlistAlbums.keySet()) {
					playlistAlbums.put(key, playlistAlbums.get(key)/playlistTracks.size());
				}
				playlistArtistMap.put(playlistId, playlistArtists);
				playlistAlbumMap.put(playlistId, playlistAlbums);
				playlistTrackMap.put(playlistId, playlistTracks);
				trainTracks.addAll(playlistTracks);
				testMap.put(playlistId, testTracks);
				
				//Averaging
				
				double count = 0.0;
				for (String key : playlistArtists.keySet()) {
					count+=playlistArtists.get(key);
				}
				artistAverageValues.put(playlistId, count/playlistArtists.keySet().size());
				
				count = 0.0;
				for (String key : playlistAlbums.keySet()) {
					count+=playlistAlbums.get(key);
				}
				albumAverageValues.put(playlistId, count/playlistAlbums.keySet().size());
				
			}
			System.out.println("Number of Playlists: " + playlistTrackMap.size());
			System.out.println("Number of unique train tracks: " + trainTracks.size());
			
			// Drop Test Tracks which are not available in training tracks;
			for(String pid : testMap.keySet()) {
				testTracks = new HashSet<String>();
				for(String test : testMap.get(pid)) {
					if(!trainTracks.contains(test)) {
						testTracks.add(test);
					}
				}
//				System.out.println("Removing "+ testTracks.size() + " tracks out of "+ testMap.get(pid).size() +" from playlist "+ pid);
				testMap.get(pid).removeAll(testTracks);
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
	

	public static TreeMap<String, Double> sortMapByValue(TreeMap<String, Double> recommendations) {
		Comparator<String> comparator = new ValueComparator(recommendations);
		TreeMap<String, Double> result = new TreeMap<String, Double>(comparator);
		result.putAll(recommendations);
		return result;
	}

	private static void testPlaylists() {
		Iterator<String> it = testMap.keySet().iterator();
		String playlist1;
		Set<String> originalTracks;
		double k = 0.0, predictedValue;
		TreeMap<String, Double> recommendations;
		int count =0;
		// Iterating over all playlists in testMap 
		while (it.hasNext()) {
			playlist1 = it.next();
			System.out.println("Testing playlist "+ playlist1);
			originalTracks = testMap.get(playlist1);
			if(originalTracks.size()==0){
				continue;
			}
			count++;
			recommendations = new TreeMap<String, Double>();
			for (String track : trainTracks) {
				predictedValue = 0.0;
				for (String playlist2 : playlistTrackMap.keySet()) {
					predictedValue += correlation(playlist1, playlist2, track);
				}
				recommendations.put(track, predictedValue);
			}
			recommendations = sortMapByValue(recommendations);
			evaluate(originalTracks, recommendations);
		}
		System.out.println("Precision @ 10 "+ precision_10 +" - "+ (double) precision_10/count);
		System.out.println("Precision @ 50 "+ precision_50/count);
		System.out.println("Precision @ 100 "+ precision_100/count);
		System.out.println("Precision @ 200 "+ precision_200/count);
		System.out.println("Precision @ 500 "+ precision_500/count);
		System.out.println("Precision @ 1000 "+ precision_1000/count );
	}

	
	/**
	 * Computes the Precision values
	 * 
	 * @param originalTracks
	 * @param recommendations
	 */
	private static void evaluate(Set<String> originalTracks, TreeMap<String, Double> recommendations) {
		int p =0 ;
		for(int i=0; i < MaximumK; i++) {
			Entry<String, Double> recommendation = recommendations.pollFirstEntry();
			if(originalTracks.contains(recommendation.getKey())) {
				p++;
			}
				switch (i) {
				case 10:
					precision_10 += (double) p/originalTracks.size();
					break;
				case 50:
					precision_50 += (double) p/originalTracks.size();
					break;
				case 100:
					precision_100 += (double) p/originalTracks.size();
					break;
				case 200:
					precision_200 += (double) p/originalTracks.size();
					break;
				case 500:
					precision_500 += (double) p/originalTracks.size();
					break;
				case 1000:
					precision_1000 += (double) p/originalTracks.size();
					break;
				default:
					break;
				}
		    
		}
		System.out.println("Found "+ p +" tracks out of "+ originalTracks.size());
	}

	private static double correlation(String playlist1, String playlist2, String track ) {
		// TODO Weighted correlations
		double weightedCorrelation = 0;
		if(playlistTrackMap.get(playlist2).contains(track)) {
			weightedCorrelation += tracksCorrelation(playlist1, playlist2);
	//		weightedCorrelation += albumsCorrelation(playlist1, playlist2)/3;
	//		weightedCorrelation += artistsCorrelation(playlist1, playlist2)/3;
		} 
		return weightedCorrelation;
	}

	private static double tracksCorrelation(String playlist1, String playlist2) {
		String key = generateKey(playlist1, playlist2);
		//Return from memory if available
		if (!tracksCorrelation.containsKey(key)) {
			//Calculate track correlation
			HashSet<String> commonTracks = (HashSet<String>) playlistTrackMap.get(playlist1).clone();
			commonTracks.retainAll(playlistTrackMap.get(playlist2));
			//correlation = (|commontracks|)^2/ (|playlist1|*|playlist2|)
			double correlation = (double) (commonTracks.size()*commonTracks.size())/(playlistTrackMap.get(playlist1).size()*playlistTrackMap.get(playlist2).size());
			tracksCorrelation.put(key, correlation);
		}
		return tracksCorrelation.get(key);
	}

	private static String generateKey(String playlist1, String playlist2) {
		String key;
		if (playlist1.compareTo(playlist2) < 0) {
			key = playlist1 + "_" + playlist2;
		} else {
			key = playlist2 + "_" + playlist1;
		}
		return key;
	}	
		
	private static double albumsCorrelation(String playlist1, String playlist2) {
		String key = generateKey(playlist1, playlist2);
		//Return from memory if available
		if (!albumsCorrelation.containsKey(key)) {
			//Calculate Album Correlation
			double correlation = 0;
			Set<String> commonAlbums = new HashSet<String>(playlistAlbumMap.get(playlist1).keySet());
			commonAlbums.retainAll(playlistAlbumMap.get(playlist2).keySet());
			if(!commonAlbums.isEmpty()) {
				double numerator = 0;
				double denominatorTerm1 = 0;
				double denominatorTerm2 = 0;
				for (String album : commonAlbums) {
					numerator+=((playlistAlbumMap.get(playlist1).get(album) - albumAverageValues.get(playlist1))*(playlistAlbumMap.get(playlist2).get(album) - albumAverageValues.get(playlist2)));
					denominatorTerm1+=Math.pow((playlistAlbumMap.get(playlist1).get(album) - albumAverageValues.get(playlist1)), 2);
					denominatorTerm2+=Math.pow((playlistAlbumMap.get(playlist2).get(album) - albumAverageValues.get(playlist2)), 2);
				}
				correlation = numerator/Math.sqrt((denominatorTerm1*denominatorTerm2));
			}
			albumsCorrelation.put(key, correlation);
		}
		return albumsCorrelation.get(key);
	}
	

	private static double artistsCorrelation(String playlist1, String playlist2) {
		String key = generateKey(playlist1, playlist2);
		//Return from memory if available
		if (!artistsCorrelation.containsKey(key)) {
			//Calculate Artist Correlation
			double correlation = 0;
			//Cloning
			Set<String> commonArtists = new HashSet<String>(playlistArtistMap.get(playlist1).keySet());
			commonArtists.retainAll(playlistArtistMap.get(playlist2).keySet());
			if(!commonArtists.isEmpty()) {
				double numerator = 0;
				double denominatorTerm1 = 0;
				double denominatorTerm2 = 0;
				for (String artist : commonArtists) {
					numerator+=((playlistArtistMap.get(playlist1).get(artist) - artistAverageValues.get(playlist1))*(playlistArtistMap.get(playlist2).get(artist) - artistAverageValues.get(playlist2)));
					denominatorTerm1+=Math.pow((playlistArtistMap.get(playlist1).get(artist) - artistAverageValues.get(playlist1)), 2);
					denominatorTerm2+=Math.pow((playlistArtistMap.get(playlist2).get(artist) - artistAverageValues.get(playlist2)), 2);
				}
				correlation = numerator/Math.sqrt((denominatorTerm1*denominatorTerm2));
			}
			artistsCorrelation.put(key, correlation);
		}
		return artistsCorrelation.get(key);
	}

}

class ValueComparator implements Comparator {
	Map map;

	public ValueComparator(Map map) {
		this.map = map;
	}

	public int compare(Object keyA, Object keyB) {
		Comparable valueA = (Comparable) map.get(keyA);
		Comparable valueB = (Comparable) map.get(keyB);
		int x = valueB.compareTo(valueA);
		if(x == 0) {
			keyA = (String) keyA;
			keyB = (String) keyB;
			if(!keyA.equals(keyB)) {
				return 1;
			}
		}
		return x;
	}
}
