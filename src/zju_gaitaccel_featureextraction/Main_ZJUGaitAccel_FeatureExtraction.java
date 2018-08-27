package zju_gaitaccel_featureextraction;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringTokenizer;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author manyi
 */
public class Main_ZJUGaitAccel_FeatureExtraction {
    //base folder for the dataset
    private static String BASE_FOLDER = "c:\\_DATA\\_DIPLOMADOLGOZATOK\\2018\\_ACCENTURE_STUDENT_RESEARCH\\GaitBiometrics\\_DATA\\zju-gaitacc\\";
    // folder names in the dataset
    private static final String SESSIONS[] = {"session_0", "session_1", "session_2"};
    // number of users per sessions
    private static final int NUMUSERS_PER_SESSION[] = {22, 153, 153};
    // Number of bins for histogram type features
    public static final int NUMBINS = 10;
    // number of samples for fixed size segments
    private static int WINSIZE = 128;
   

    // ************************************************************
    // processing cycleas instead of fixed length (WINSIZE) windows
    // CHANGE this to false in order to get features extracted from fixed length segments
    private static boolean CYCLE = false;

    public static void main(String[] args) {
        System.out.print("SEGMENTATION: ");
        if( CYCLE ){
            System.out.println( "step cycles using manual annotations");
        } else{
            System.out.println( WINSIZE + " samples length segments");
        }
        for (int sessionid = 0; sessionid < SESSIONS.length; ++sessionid) {
            String session = SESSIONS[sessionid];
            int numUsers = NUMUSERS_PER_SESSION[sessionid];
            System.out.println("Processing session "+session+" having "+numUsers+" users");

            // Create feature files
            String FOLDER = BASE_FOLDER +session + "\\";
            String outfilename = null, csvfilename = null;
            if (CYCLE) {
                outfilename = "zju_gaitaccel_" + session + "_CYCLE.arff";
                csvfilename = "zju_gaitaccel_" + session + "_CYCLE.csv";
            } else {
                outfilename = "zju_gaitaccel_" + session + "_" + WINSIZE + ".arff";
                csvfilename = "zju_gaitaccel_" + session + "_" + WINSIZE + ".csv";
            }
            PrintStream ps = null;
            PrintStream pscsv = null;
            try {
                ps = new PrintStream(outfilename);
                pscsv = new PrintStream(csvfilename);
            } catch (FileNotFoundException ex) {
                Logger.getLogger(Main_ZJUGaitAccel_FeatureExtraction.class.getName()).log(Level.SEVERE, null, ex);
            }
            Utils.printHeader(ps);

            // Extract features
            for (int i = 1; i <= numUsers; ++i) {
                String username = Utils.userName(i);
                String userFolder = "subj_" + username;
                int numUserFrames = 0;
                // number of recordings: 6
                for (int j = 1; j <= 6; ++j) {
                    String recordingFolder = userFolder + "\\" + "rec_" + j + "\\";
                    // 3.txt contains data from the accelerometer fixed on the right side of the pelvis
                    Signal signal = new Signal(FOLDER + recordingFolder + "3.txt");

                    if (CYCLE) {
                        // cycles.txt contains the manually annotated endpoints of the step cycles
                        ArrayList<Integer> endpoints = Utils.readEndpoints(FOLDER + recordingFolder + "cycles.txt");
                        int n = endpoints.size();
                        for (int k = 0; k < n - 2; ++k) {
                            FeatureVector fv = signal.computeFeatures(endpoints.get(k), endpoints.get(k + 1));
                            ps.println(fv + "u" + username);
                            pscsv.println(fv + "u" + username);
                        }    
                    } else {
                        int numFrames = signal.getNumSamples() / WINSIZE;
                        numUserFrames += numFrames;
                        //the first and the last segments are ignored
                        for (int k = 1; k < numFrames - 1; ++k) {
                            FeatureVector fv = signal.computeFeatures(k * WINSIZE, (k + 1) * WINSIZE);
                            ps.println(fv + "u" + username);
                            pscsv.println(fv + "u" + username);
                        }
                    }
                }
//                if (!CYCLE) {
//                    System.out.println(username + ", " + numUserFrames);
//                }
            }
            // Close feature files
            ps.close();
            pscsv.close();
        }
    }

}
