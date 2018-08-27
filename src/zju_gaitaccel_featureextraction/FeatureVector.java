/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package zju_gaitaccel_featureextraction;

import static zju_gaitaccel_featureextraction.Main_ZJUGaitAccel_FeatureExtraction.NUMBINS;

/**
 *
 * @author manyi
 */
public class FeatureVector {
    private double minimum_for_axis_X;
    private double minimum_for_axis_Y;
    private double minimum_for_axis_Z;
    private double minimum_for_magnitude;
    
    private double average_acceleration_for_axis_X;
    private double average_acceleration_for_axis_Y;
    private double average_acceleration_for_axis_Z;
    private double average_acceleration_for_magnitude;
    
    private double standard_deviation_for_axis_X;
    private double standard_deviation_for_axis_Y;
    private double standard_deviation_for_axis_Z;
    private double standard_deviation_for_magnitude;
    
    private double average_absolute_difference_for_axis_X;
    private double average_absolute_difference_for_axis_Y;
    private double average_absolute_difference_for_axis_Z;
    private double average_absolute_difference_for_magnitude;
    
    private double zero_crossing_rate_for_axis_X;
    private double zero_crossing_rate_for_axis_Y;
    private double zero_crossing_rate_for_axis_Z;
    
    private double binX[] = new double[ NUMBINS ];
    private double binY[] = new double[ NUMBINS ];
    private double binZ[] = new double[ NUMBINS ];
    private double binM[] = new double[ NUMBINS ];



    public double getMinimum_for_axis_X() {
        return minimum_for_axis_X;
    }

    public void setMinimum_for_axis_X(double minimum_for_axis_X) {
        this.minimum_for_axis_X = minimum_for_axis_X;
    }

    public double getMinimum_for_axis_Y() {
        return minimum_for_axis_Y;
    }

    public void setMinimum_for_axis_Y(double minimum_for_axis_Y) {
        this.minimum_for_axis_Y = minimum_for_axis_Y;
    }

    public double getMinimum_for_axis_Z() {
        return minimum_for_axis_Z;
    }

    public void setMinimum_for_axis_Z(double minimum_for_axis_Z) {
        this.minimum_for_axis_Z = minimum_for_axis_Z;
    }

    public double getMinimum_for_magnitude() {
        return minimum_for_magnitude;
    }

    public void setMinimum_for_magnitude(double minimum_for_magnitude) {
        this.minimum_for_magnitude = minimum_for_magnitude;
    }

    public double getAverage_acceleration_for_axis_X() {
        return average_acceleration_for_axis_X;
    }

    public void setAverage_acceleration_for_axis_X(double average_acceleration_for_axis_X) {
        this.average_acceleration_for_axis_X = average_acceleration_for_axis_X;
    }

    public double getAverage_acceleration_for_axis_Y() {
        return average_acceleration_for_axis_Y;
    }

    public void setAverage_acceleration_for_axis_Y(double average_acceleration_for_axis_Y) {
        this.average_acceleration_for_axis_Y = average_acceleration_for_axis_Y;
    }

    public double getAverage_acceleration_for_axis_Z() {
        return average_acceleration_for_axis_Z;
    }

    public void setAverage_acceleration_for_axis_Z(double average_acceleration_for_axis_Z) {
        this.average_acceleration_for_axis_Z = average_acceleration_for_axis_Z;
    }

    public double getAverage_acceleration_for_magnitude() {
        return average_acceleration_for_magnitude;
    }

    public void setAverage_acceleration_for_magnitude(double average_acceleration_for_magnitude) {
        this.average_acceleration_for_magnitude = average_acceleration_for_magnitude;
    }

    public double getStandard_deviation_for_axis_X() {
        return standard_deviation_for_axis_X;
    }

    public void setStandard_deviation_for_axis_X(double standard_deviation_for_axis_X) {
        this.standard_deviation_for_axis_X = standard_deviation_for_axis_X;
    }

    public double getStandard_deviation_for_axis_Y() {
        return standard_deviation_for_axis_Y;
    }

    public void setStandard_deviation_for_axis_Y(double standard_deviation_for_axis_Y) {
        this.standard_deviation_for_axis_Y = standard_deviation_for_axis_Y;
    }

    public double getStandard_deviation_for_axis_Z() {
        return standard_deviation_for_axis_Z;
    }

    public void setStandard_deviation_for_axis_Z(double standard_deviation_for_axis_Z) {
        this.standard_deviation_for_axis_Z = standard_deviation_for_axis_Z;
    }

    public double getStandard_deviation_for_magnitude() {
        return standard_deviation_for_magnitude;
    }

    public void setStandard_deviation_for_magnitude(double standard_deviation_for_magnitude) {
        this.standard_deviation_for_magnitude = standard_deviation_for_magnitude;
    }

    public double getAverage_absolute_difference_for_axis_X() {
        return average_absolute_difference_for_axis_X;
    }

    public void setAverage_absolute_difference_for_axis_X(double average_absolute_difference_for_axis_X) {
        this.average_absolute_difference_for_axis_X = average_absolute_difference_for_axis_X;
    }

    public double getAverage_absolute_difference_for_axis_Y() {
        return average_absolute_difference_for_axis_Y;
    }

    public void setAverage_absolute_difference_for_axis_Y(double average_absolute_difference_for_axis_Y) {
        this.average_absolute_difference_for_axis_Y = average_absolute_difference_for_axis_Y;
    }

    public double getAverage_absolute_difference_for_axis_Z() {
        return average_absolute_difference_for_axis_Z;
    }

    public void setAverage_absolute_difference_for_axis_Z(double average_absolute_difference_for_axis_Z) {
        this.average_absolute_difference_for_axis_Z = average_absolute_difference_for_axis_Z;
    }

    public double getAverage_absolute_difference_for_magnitude() {
        return average_absolute_difference_for_magnitude;
    }

    public void setAverage_absolute_difference_for_magnitude(double average_absolute_difference_for_magnitude) {
        this.average_absolute_difference_for_magnitude = average_absolute_difference_for_magnitude;
    }

    public double getZero_crossing_rate_for_axis_X() {
        return zero_crossing_rate_for_axis_X;
    }

    public void setZero_crossing_rate_for_axis_X(double zero_crossing_rate_for_axis_X) {
        this.zero_crossing_rate_for_axis_X = zero_crossing_rate_for_axis_X;
    }

    public double getZero_crossing_rate_for_axis_Y() {
        return zero_crossing_rate_for_axis_Y;
    }

    public void setZero_crossing_rate_for_axis_Y(double zero_crossing_rate_for_axis_Y) {
        this.zero_crossing_rate_for_axis_Y = zero_crossing_rate_for_axis_Y;
    }

    public double getZero_crossing_rate_for_axis_Z() {
        return zero_crossing_rate_for_axis_Z;
    }

    public void setZero_crossing_rate_for_axis_Z(double zero_crossing_rate_for_axis_Z) {
        this.zero_crossing_rate_for_axis_Z = zero_crossing_rate_for_axis_Z;
    }

    public double[] getBinX() {
        return binX;
    }

    public void setBinX(double[] binX) {
        this.binX = binX;
    }

    public double[] getBinY() {
        return binY;
    }

    public void setBinY(double[] binY) {
        this.binY = binY;
    }

    public double[] getBinZ() {
        return binZ;
    }

    public void setBinZ(double[] binZ) {
        this.binZ = binZ;
    }

    public double[] getBinM() {
        return binM;
    }

    public void setBinM(double[] binM) {
        this.binM = binM;
    }
    
    public String toString(){
        StringBuffer sb = new StringBuffer();
        sb.append(this.minimum_for_axis_X);sb.append(',');sb.append(this.minimum_for_axis_Y);sb.append(',');
        sb.append(this.minimum_for_axis_Z);sb.append(',');sb.append(this.minimum_for_magnitude);sb.append(',');
        sb.append(this.average_acceleration_for_axis_X); sb.append(','); sb.append(this.average_acceleration_for_axis_Y); sb.append(',');
        sb.append(this.average_acceleration_for_axis_Z); sb.append(','); sb.append(this.average_acceleration_for_magnitude); sb.append(',');
        sb.append(this.standard_deviation_for_axis_X); sb.append(',');sb.append(this.standard_deviation_for_axis_Y); sb.append(',');
        sb.append(this.standard_deviation_for_axis_Z); sb.append(',');sb.append(this.standard_deviation_for_magnitude); sb.append(',');
        sb.append(this.average_absolute_difference_for_axis_X);sb.append(','); sb.append(this.average_absolute_difference_for_axis_Y);sb.append(',');
        sb.append(this.average_absolute_difference_for_axis_Z);sb.append(','); sb.append(this.average_absolute_difference_for_magnitude);sb.append(',');
        sb.append(this.zero_crossing_rate_for_axis_X); sb.append(','); sb.append(this.zero_crossing_rate_for_axis_Y); sb.append(',');
        sb.append(this.zero_crossing_rate_for_axis_Z); sb.append(',');
        for( int i=0; i<binX.length; ++i){
            sb.append(binX[ i ]); sb.append(',');
        }
        for( int i=0; i<binY.length; ++i){
            sb.append(binY[ i ]); sb.append(',');
        }
        for( int i=0; i<binZ.length; ++i){
            sb.append(binZ[ i ]); sb.append(',');
        }
        for( int i=0; i<binM.length; ++i){
            sb.append(binM[ i ]); sb.append(',');
        }
        //sb.append(binM[ binM.length-1 ]);
        return sb.toString();
        
        
    }
    
    
    
}
