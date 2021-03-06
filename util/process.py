import pathlib
import numpy as np
import pandas as pd
import sys
from sklearn.mixture import GaussianMixture
from sklearn import metrics
from scipy.optimize import brentq
from scipy.interpolate import interp1d
import copy
from click import progressbar

from util.const import *
from util.settings import *
from util.gmm import create_ubm_gmm, gmm_map_mean_adaptation

##
#  Load features from the appropriate CSV files for all sessions
#
#  @param[in] cycle          Flag for using features from annotated cycles
#  @return    df0, df1, df2  One dataframe for each session
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

    return (df0, df1, df2)

##
#  Calculate TPR, FPR, AUC and EER from scorefile
#
#  @param[in]  scorefile  Scorefile of the system
#  @return     Tuple of arrays and values.
#
def evaluate(scorefile):
    data = pd.read_csv(scorefile, names=['label','score'])
    labels = [int(e) for e in data['label']]
    scores = [float(e) for e in data['score']]
    fpr, tpr, _ = metrics.roc_curve(labels, scores, pos_label=1)
    auc = metrics.roc_auc_score(np.array(labels), np.array(scores))
    eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)

    return (tpr, fpr, auc, eer)

##
#  Recalculate score averages for multiple cycles.
#
#  @param[in]  scores      Array of score deltas based on proximities
#                          to own model and UBM
#  @param[in]  num_cycles  Number of consecutive cycles to be averaged
#  @return                 Averages of consecutive cycle sequences
#
def cycle_scores(scores, num_cycles):
    if num_cycles > 1:
        pscores = []
        for j in range(0, len(scores) - num_cycles):
            avg = sum(scores[j:j + num_cycles]) / num_cycles
            pscores.append(avg)
        return pscores
    return scores

##
#  Train and evaluate the model.
#
#  @return  Tuple of systemwide positive and negative scores
#
def train_evaluate(dataframes, params, scorefile):
    df0, df1, df2 = dataframes
    cross_session, cycle, num_cycles, adapted_gmm, reg_negatives = params

    # Setup
    numFeatures = df0.shape[1]
    userids  = ['u%03d' % i for i in range(1, NUM_USERS + 1)]
    auc_list = []
    eer_list = []
    system_positive_scores = []
    system_negative_scores = []

    # Unregistered negative samples
    neg_userids = ['u%03d' % i for i in NEG_USER_RANGE]
    unreg_negative_samples = df0.loc[df0.iloc[:, -1].isin(neg_userids)]

    # Global system score file
    scorefile = open(scorefile, "w")

    # Train the UBM
    gmm_ubm = create_ubm_gmm(df0)

    # Train user-specific GMMs and evaluate them
    items = range(NUM_USERS)
    with progressbar(items) as bar:
        for i in bar:
            # Select all samples that belong to current user
            user_train_data = df1.loc[df1.iloc[:, -1].isin([userids[i]])]
            numSamples = user_train_data.shape[0]

            # Select data for training
            user_train_data = user_train_data.drop(
                user_train_data.columns[-1], 
                axis=1)
            array = user_train_data.values
            half = (int)(numSamples / 2)
            X_train = array[0: half, :]

            # If we should take positive samples from cross
            # session data, use features from session2 (df2),
            # otherwise take the second half of session1 (df1)
            if cross_session == False:
                X_test = array[half:numSamples, :]
            else:
                user_test_data = df2.loc[df2.iloc[:, -1].isin([userids[i]])]
                user_test_data = user_test_data.drop(
                    user_test_data.columns[-1], 
                    axis=1)
                X_test = user_test_data.values

            if adapted_gmm == True:
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
            background_scores = gmm_ubm.score_samples(X_test)
            positive_scores -= background_scores

            # Save the number of positive samples for sampling
            # negative samples later
            num_positive_scores_orig = len(positive_scores)

            positive_scores = cycle_scores(positive_scores, num_cycles)

            # Prepare positive label array for ROC AUC evaluation
            positive_labels = np.full(len(positive_scores), 1)

            # Output scores obtained on positive samples with
            # their respective '1' label
            for pscore in positive_scores:
                scorefile.write("1," + str(pscore) + "\n")

            # Take negative samples (impostors) from either the set of
            # registered (session1) or unregistered (session0) users.
            if reg_negatives == True:
                userid = ['u%03d' % (i+1)]
                other_users_data = df1.loc[~df1.iloc[:, -1].isin(userid)]
                neg_samples = other_users_data.sample(
                    num_positive_scores_orig, 
                    random_state=RANDOM_STATE_SAMPLE)
            else:
                neg_samples = unreg_negative_samples.sample(
                    num_positive_scores_orig, 
                    random_state=RANDOM_STATE_SAMPLE)

            X_negative_test = neg_samples.drop(
                neg_samples.columns[-1],
                axis=1)

            # Measure the log-likelihood differences scores of negative samples
            negative_scores = gmm.score_samples(X_negative_test)
            bg_scores = gmm_ubm.score_samples(X_negative_test)
            negative_scores -= bg_scores

            negative_scores = cycle_scores(negative_scores, num_cycles)

            # Prepare negative label array for ROC AUC evaluation
            negative_labels = np.full(len(negative_scores), 0)

            # Output scores obtained on positive samples with
            # their respective '0' label
            for j in range(0, len(negative_scores)):
                scorefile.write("0," + str(negative_scores[j]) + "\n")

            scores = np.concatenate((positive_scores, negative_scores), axis=0)
            labels = np.concatenate((positive_labels, negative_labels), axis=0)

            system_positive_scores.extend(positive_scores)
            system_negative_scores.extend(negative_scores)

            # ROC AUC evaluation
            try:
                auc = metrics.roc_auc_score(labels, scores)
                auc_list.append(auc)
            except ValueError:
                print('Exception at user ', i)
                print("NEGATIVE", negative_scores)
                print("POSITIVE", positive_scores)
            # FPR, TPR
            fpr, tpr, thresholds = metrics.roc_curve(
                labels, scores, pos_label=1)
            # EER
            eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
            eer_list.append(eer)

    print()
    m_auc  = np.mean(auc_list)
    sd_auc = np.std(auc_list)
    print("User AUC (mean, stdev): {}, {}".format(m_auc, sd_auc))
    m_eer = np.mean(eer_list)
    sd_eer = np.std(eer_list)
    print("User EER (mean, stdev): {}, {}".format(m_eer, sd_eer))
    scorefile.close()

    return (system_negative_scores, system_positive_scores)
