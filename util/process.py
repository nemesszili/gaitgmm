import pathlib
import numpy as np
import pandas as pd
import sys
from sklearn.mixture import GaussianMixture
from sklearn import metrics
from scipy.optimize import brentq
from scipy.interpolate import interp1d
import copy

from util.const import *
from util.settings import *
from util.gmm import create_ubm_gmm, gmm_map_mean_adaptation
from util.helper import *
from util.myplots import *

##
#  Extract and load features from the dataset.
#
#  @param[in] force_extract  Flag for re-extracting feature files
#  @param[in] cycle          Flag for using features from annotated cycles
#  @return    df0, df1, df2  One dataframe for each session
#

def extract_load_feat(force_extract, cycle):
    # Create directory for feature CSVs
    pathlib.Path(FEAT_DIR).mkdir(exist_ok=True)

    num_csv = len(list(pathlib.Path(FEAT_DIR).glob('*.csv')))
    force_extract |= (num_csv < 6)

    # Extract features
    if force_extract:
        extract()
    
    # Load features
    return load(cycle)

##
#  Load features from the appropriate CSV files for all sessions
#
def load(cycle):
    if cycle == True:
        filename_session0 = FEAT_DIR + "/zju_gaitaccel_session_0_CYCLE.csv"
        filename_session1 = FEAT_DIR + "/zju_gaitaccel_session_1_CYCLE.csv"
        filename_session2 = FEAT_DIR + "/zju_gaitaccel_session_2_CYCLE.csv"
    else:
        filename_session0 = FEAT_DIR + "/zju_gaitaccel_session_0_128.csv"
        filename_session1 = FEAT_DIR + "/zju_gaitaccel_session_1_128.csv"
        filename_session2 = FEAT_DIR + "/zju_gaitaccel_session_2_128.csv"

    # session0 is used for UBM training (u1..u11) and
    # and negative samples (u12..u22)
    data0 = pd.read_csv(filename_session0, header=None)
    df0 = pd.DataFrame(data0)

    # session1 is used for training user-specific GMM models
    # and providing positive samples for same-day testing
    data1 = pd.read_csv(filename_session1, header=None)
    df1 = pd.DataFrame(data1)

    # session2 is used for providing positive samples for 
    # cross-day testing
    data2 = pd.read_csv(filename_session2, header=None)
    df2 = pd.DataFrame(data2)

    return df0, df1, df2

##
#  Extract features from the dataset
#
def extract():
    pass

##
#  Train and evaluate the model.
#
def train_evaluate(df0, df1, df2):
    # Setup
    numFeatures = df0.shape[1]
    userids  = ['u%03d' % i for i in range(1, NUM_USERS + 1)]
    auc_list = []
    eer_list = []
    system_positive_scores = []
    system_negative_scores = []

    # Global system score file
    scorefile = open("scores.csv", "w")

    # Train the UBM
    gmm_ubm = create_ubm_gmm(df0)

    # Train user-specific GMMs and evaluate them
    for i in range(0, NUM_USERS):
        # Select all samples belonging to current user
        user_train_data = df1.loc[df1.iloc[:, -1].isin([userids[i]])]
        numSamples = user_train_data.shape[0]

        # Select data for training
        user_train_data = user_train_data.drop(
            user_train_data.columns[-1], axis=1)
        array = user_train_data.values
        half = (int)(numSamples / 2)
        X_train = array[0: half, :]

        # If we should evaluate with cross session data,
        # use features from session2 (df2), otherwise
        # take the second half of session1 (df1)
        if CROSS_SESSION == False:
            X_test = array[half:numSamples, :]
        else:
            user_test_data = df2.loc[df2.iloc[:, -1].isin([userids[i]])]
            user_test_data = user_test_data.drop(
                user_test_data.columns[-1], axis=1)
            X_test = user_test_data.values

        if ADAPTED_GMM == True:
            # MAP adaptation of the UBM using the user's training data
            gmm = copy.deepcopy(gmm_ubm)
            gmm_map_mean_adaptation(gmm, X_train)
        else:
            gmm = GaussianMixture(
                n_components=NUM_USER_MIXTURES, 
                covariance_type=COVAR_TYPE,
                random_state=RANDOM_STATE)
            gmm.fit(X_train)

        # Measure the log-likelihood differences for authentication:
        # If value is positive, it belongs to the user model, otherwise
        # it's "closer" to the UBM
        positive_scores = gmm.score_samples(X_test)
        num_positive_scores_before_average = len(positive_scores)
        background_scores = gmm_ubm.score_samples(X_test)
        positive_scores -= background_scores

        # Recalculate score averages for multiple cycles
        if NUM_CYCLES > 1:
            pscores = []
            for j in range(0, len(positive_scores) - NUM_CYCLES):
                avg = sum(positive_scores[j:j + NUM_CYCLES]) / NUM_CYCLES
                pscores.append(avg)
            positive_scores = pscores

        positive_labels = np.full(len(positive_scores), 1)
        for pscore in positive_scores:
            scorefile.write( "1," + str(pscore) + "\n")

        # Take negative samples (impostors) from either the set of
        # registered (session1) or unregistered (session0) users.
        if REGISTERED_NEGATIVES == True:
            negativesamples= select_negatives_from_other_users(df1, 'u%03d' % (i+1), num_positive_scores_before_average)
        else:
            negative_test_samples = unreg_negative_samples(df0)
            negative_samples = negative_test_samples()
            negativesamples = select_negative_samples_numsamples(negative_test_samples, num_positive_scores_before_average)
        X_negative_test = negativesamples.values[:, 0:numFeatures - 1]

        # negative_scores
        negative_scores = gmm.score_samples(X_negative_test)
        bg_scores = gmm_ubm.score_samples(X_negative_test)
        negative_scores -= bg_scores
        if NUM_CYCLES > 1:
            pscores = []
            for j in range(0, len(negative_scores) - NUM_CYCLES):
                sump = 0
                for k in range(0,NUM_CYCLES):
                    sump += negative_scores[j+k]
                pscores.append(sump/NUM_CYCLES)
            negative_scores = pscores

        # negative_scores = preprocessing.scale(negative_scores)
        negative_labels = np.full(len(negative_scores),0)
        for j in range(0, len(negative_scores)):
            scorefile.write("0," + str(negative_scores[j]) + "\n")

        scores = np.concatenate((positive_scores, negative_scores), axis=0)
        labels = np.concatenate((positive_labels, negative_labels), axis=0)

        system_positive_scores.extend(positive_scores)
        system_negative_scores.extend(negative_scores)

        # AUC
        try:
            auc =   metrics.roc_auc_score(labels, scores )
            auc_list.append(auc)
        except:
            print('Exception at user ', i)
            print("NEGATIVE", negative_scores)
            print("POSITIVE", positive_scores)
        # FPR, TPR
        fpr, tpr, thresholds = metrics.roc_curve(labels, scores, pos_label=1)
        # EER
        eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
        eer_list.append(eer)

        print(userids[i], auc, eer)
        # plot_scores(userids[ i ], negative_scores, positive_scores)
    
    m_auc = np.mean(auc_list)
    sd_auc = np.std(auc_list)
    print("User AUC (mean, stdev): "+str(m_auc)+", "+str(sd_auc))
    m_eer = np.mean(eer_list)
    sd_eer = np.std(eer_list)
    print("User EER (mean, stdev): "+str(m_eer)+", "+str(sd_eer))
    scorefile.close()
    plotAUC("scores.csv")
    plot_scores("All users: u001-u040", system_negative_scores, system_positive_scores)

