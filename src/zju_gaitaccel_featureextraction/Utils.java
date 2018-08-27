/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package zju_gaitaccel_featureextraction;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringTokenizer;
import java.util.logging.Level;
import java.util.logging.Logger;
import static zju_gaitaccel_featureextraction.Main_ZJUGaitAccel_FeatureExtraction.NUMBINS;

/**
 *
 * @author manyi
 */
public class Utils {
     public static String userName(int subjectid) {
        String username = "";
        if (subjectid < 10) {
            username = "00" + subjectid;
        } else {
            if (subjectid < 100) {
                username = "0" + subjectid;
            } else {
                username += subjectid;
            }
        }
        return username;
    }
    
    public static ArrayList<Integer> readEndpoints(String filename){
        ArrayList<Integer> endpoints = new ArrayList<>();
        Scanner scanner = null;
        try {
            scanner = new Scanner( new File(filename) );
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Main_ZJUGaitAccel_FeatureExtraction.class.getName()).log(Level.SEVERE, null, ex);
        }
        String line = scanner.nextLine();
        //System.out.println( line );
        StringTokenizer stk = new StringTokenizer( line, ",.");
        while( stk.hasMoreTokens()){
            endpoints.add( Integer.parseInt(stk.nextToken()));
        }
        return endpoints;
    }

    public static void printHeader(PrintStream ps) {
        ps.println("@relation accelerometer");
        ps.println("@attribute minimum_for_axis_X numeric");
        ps.println("@attribute minimum_for_axis_Y numeric");
        ps.println("@attribute minimum_for_axis_Z numeric");
        ps.println("@attribute minimum_for_magnitude numeric");
        ps.println("@attribute average_acceleration_for_axis_X numeric");
        ps.println("@attribute average_acceleration_for_axis_Y numeric");
        ps.println("@attribute average_acceleration_for_axis_Z numeric");
        ps.println("@attribute average_acceleration_for_magnitude numeric");
        ps.println("@attribute standard_deviation_for_axis_X numeric");
        ps.println("@attribute standard_deviation_for_axis_Y numeric");
        ps.println("@attribute standard_deviation_for_axis_Z numeric");
        ps.println("@attribute standard_deviation_for_magnitude numeric");
        ps.println("@attribute average_absolute_difference_for_axis_X numeric");
        ps.println("@attribute average_absolute_difference_for_axis_Y numeric");
        ps.println("@attribute average_absolute_difference_for_axis_Z numeric");
        ps.println("@attribute average_absolute_difference_for_magnitude numeric");
        ps.println("@attribute zero_crossing_rate_for_axis_X numeric");
        ps.println("@attribute zero_crossing_rate_for_axis_Y numeric");
        ps.println("@attribute zero_crossing_rate_for_axis_Z numeric");
        for( int i=0; i<NUMBINS; ++i ){
            ps.println("@attribute bin"+i+"_X numeric");
        }
        for( int i=0; i<NUMBINS; ++i ){
            ps.println("@attribute bin"+i+"_Y numeric");
        }
        for( int i=0; i<NUMBINS; ++i ){
            ps.println("@attribute bin"+i+"_Z numeric");
        }
        for( int i=0; i<NUMBINS; ++i ){
            ps.println("@attribute bin"+i+"_M numeric");
        }
        ps.println("@attribute userid {u001,u002,u003,u004,u005,u006,u007,u008,u009,u010,u011,u012,u013,u014,u015,u016,u017,u018,u019,u020,u021,u022,u023,u024,u025,u026,u027,u028,u029,u030,u031,u032,u033,u034,u035,u036,u037,u038,u039,u040,u041,u042,u043,u044,u045,u046,u047,u048,u049,u050,u051,u052,u053,u054,u055,u056,u057,u058,u059,u060,u061,u062,u063,u064,u065,u066,u067,u068,u069,u070,u071,u072,u073,u074,u075,u076,u077,u078,u079,u080,u081,u082,u083,u084,u085,u086,u087,u088,u089,u090,u091,u092,u093,u094,u095,u096,u097,u098,u099,u100,u101,u102,u103,u104,u105,u106,u107,u108,u109,u110,u111,u112,u113,u114,u115,u116,u117,u118,u119,u120,u121,u122,u123,u124,u125,u126,u127,u128,u129,u130,u131,u132,u133,u134,u135,u136,u137,u138,u139,u140,u141,u142,u143,u144,u145,u146,u147,u148,u149,u150,u151,u152,u153}");
        ps.println("@data");

    }
}
