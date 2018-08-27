/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package zju_gaitaccel_featureextraction;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

import static zju_gaitaccel_featureextraction.Main_ZJUGaitAccel_FeatureExtraction.NUMBINS;

/**
 *
 * @author manyi
 * Corresponds fro one file - one recording
 * a file contains three lines - each line corresponds to one directional acceleration: ax, ay, az
 */
public class Signal {
   private double ax[], ay[], az[], am[];
   private int numSamples;
    
    public Signal( String filename ){
        Scanner scanner = null;
        try {
            scanner = new Scanner( new File( filename ));
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Signal.class.getName()).log(Level.SEVERE, null, ex);
        }
        String axline = scanner.nextLine();
        String ayline = scanner.nextLine();
        String azline = scanner.nextLine();
        String axtokens[] = axline.split(",");
        String aytokens[] = ayline.split(",");
        String aztokens[] = azline.split(",");
        numSamples = axtokens.length; 
        ax = new double[ numSamples ];
        ay = new double[ numSamples ];
        az = new double[ numSamples ];
        am = new double[ numSamples ];
       
        for( int i=0; i<numSamples; ++i ){
            ax[ i ] = Double.parseDouble(axtokens[ i ]);
            ay[ i ] = Double.parseDouble(aytokens[ i ]);
            az[ i ] = Double.parseDouble(aztokens[ i ]);
            am[ i ] = Math.sqrt( ax[i] * ax[i]+ ay[i] * ay[ i ]+ az[i]*az[i]);
        }   
    }
    
    
    public int getNumSamples(){
        return numSamples;
    }
    
    
    /*
    * Computes features from the signal [startIndex, stopIndex)
    */
    public FeatureVector computeFeatures( int startIndex, int stopIndex ){
        // min & avg
        double minX = ax[ startIndex ], minY = ay[ startIndex ], minZ = az[ startIndex ], minM = am[ startIndex ];
        double avgX = 0, avgY= 0, avgZ = 0, avgM = 0;
        int len = stopIndex - startIndex;
        for( int i= startIndex; i<stopIndex; ++i){
            if( ax[ i ] < minX ){
                minX = ax[ i ];
            }
            if( ay[ i ] < minY ){
                minY = ay[ i ];
            }
            if( az[ i ] < minZ ){
                minZ = az[ i ];
            }
            if( am[ i ] < minM ){
                minM = am[ i ];
            }
            avgX += ax[ i ];
            avgY += ay[ i ];
            avgZ += az[ i ];
            avgM += am[ i ];
            
        }
        avgX /=len; avgY /= len; avgZ /= len; avgM /= len;
        // variance (standard deviation ^2)
        // average absolute difference
        double varx = 0, vary = 0, varz = 0, varm = 0;
        double absdifx = 0, absdify = 0, absdifz = 0, absdifm = 0;
       
        for( int i= startIndex; i<stopIndex; ++i){
            varx += (ax[ i ] - avgX) * (ax[ i ] - avgX);
            vary += (ay[ i ] - avgY) * (ay[ i ] - avgY);
            varz += (ay[ i ] - avgZ) * (az[ i ] - avgZ);
            varm += (am[ i ] - avgM) * (am[ i ] - avgM);
            
            absdifx += Math.abs(ax[ i ] -avgX);
            absdify += Math.abs(ay[ i ] -avgY);
            absdifz += Math.abs(az[ i ] -avgZ);
            absdifm += Math.abs(am[ i ] -avgM);
            
        }
        varx /= len; vary /= len; varz /= len; varm /= len;
        absdifx /= len; absdify /= len; absdifz /= len; absdifm /= len; 
        
        
        double zcrx = 0, zcry = 0, zcrz=0;
        for( int i= startIndex+1; i<stopIndex; ++i){
            if ( ( ax[ i ] <= 0 && ax[ i-1 ] > 0 ) || ( ax[ i ] >= 0 && ax[ i-1 ]< 0 )){
                ++zcrx;
            }
            if ( ( ay[ i ] <= 0 && ay[ i-1 ] > 0 ) || ( ay[ i ] >= 0 && ay[ i-1 ]< 0 )){
                ++zcry;
            }
            if ( ( az[ i ] <= 0 && az[ i-1 ] > 0 ) || ( az[ i ] >= 0 && az[ i-1 ]< 0 )){
                ++zcrz;
            }
        }
        zcrx /= len; zcry /= len; zcrz /= len;
        FeatureVector fv = new FeatureVector();
        fv.setMinimum_for_axis_X(minX); fv.setMinimum_for_axis_Y(minY); fv.setMinimum_for_axis_Z(minZ);fv.setMinimum_for_magnitude(minM);
        fv.setAverage_acceleration_for_axis_X(avgX);fv.setAverage_acceleration_for_axis_Y(avgY); fv.setAverage_acceleration_for_axis_Z(avgZ); fv.setAverage_acceleration_for_magnitude(avgM);
        fv.setStandard_deviation_for_axis_X(varx);  fv.setStandard_deviation_for_axis_Y(vary); fv.setStandard_deviation_for_axis_Z(varz); fv.setStandard_deviation_for_magnitude(varm);
        fv.setAverage_absolute_difference_for_axis_X(absdifx);fv.setAverage_absolute_difference_for_axis_Y(absdify); fv.setAverage_absolute_difference_for_axis_Z(absdifz); fv.setAverage_absolute_difference_for_magnitude(absdifm);
        fv.setZero_crossing_rate_for_axis_X(zcrx); fv.setZero_crossing_rate_for_axis_Y(zcry); fv.setZero_crossing_rate_for_axis_Z(zcrz);
        fv.setBinX( getHistogram(ax, startIndex, stopIndex, -1.5, 1.5, NUMBINS));
        fv.setBinY( getHistogram(ay, startIndex, stopIndex, -1.5, 1.5, NUMBINS));
        fv.setBinZ( getHistogram(az, startIndex, stopIndex, -1.5, 1.5, NUMBINS));
        fv.setBinM( getHistogram(am, startIndex, stopIndex, 0, 2, NUMBINS));
        return fv;
    }
    
  
    public static double[] getHistogram(double signal[], int startIndex, int stopIndex, double min, double max, int bins) {
        if( stopIndex <= startIndex ){
            throw new RuntimeException("Zero length signal:  stopIndex <= startIndex ");
        }
        double[] distribution = new double[bins];
        double step = (max - min) / bins;
        for (int i = startIndex; i < stopIndex; ++i) {
            if (signal[i] < min) {
                distribution[0]++;
            } else {
                if (signal[i] > max) {
                    distribution[bins - 1]++;
                } else {
                    for (int j = bins - 1; j >= 0; --j) {
                        if (signal[i] > min + j * step) {
                            distribution[j]++;
                            break;
                        }
                    }
                }
            }
        }
        for (int i = 0; i < distribution.length; ++i) {
            distribution[i] /= (stopIndex-startIndex);
        }
        return distribution;
    }

    

}
