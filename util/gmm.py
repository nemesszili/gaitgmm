import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture

from util.const import *

##
#  Train the Universal Background Model (UBM) with data from session0
#
#  @param[in]  df       Dataframe to be used for training the UBM
#  @return     gmm_ubm  Universal Background Model
#
def create_ubm_gmm(df):
    numFeatures = df.shape[1]
    userids = ['u%03d' % i for i in UBM_USER_RANGE]

    frames = df.loc[df.iloc[:, -1].isin(userids)].values
    X = frames[:, 0:numFeatures - 1]
    gmm_ubm = GaussianMixture(
        n_components=NUM_UBM_MIXTURES, 
        covariance_type=COVAR_TYPE, 
        random_state=RANDOM_STATE
    )
    gmm_ubm.fit(X)
    return gmm_ubm

##
#  Reynolds GMM - Maximum A Posteriori adaptation by adapting only 
#  mean vectors. Written by Natalia Neverova, PhD, Lyon INSA, 2016.
# 
#  @param[in]  gmm  GMM to be adapted
#  @param[in]  X    Data used for adaptation
#
def gmm_map_mean_adaptation(gmm, X):
    # K    - number of Gaussian mixtures in the model
    # nDim - dimension of feature vectors
    K, nDim = gmm.means_.shape

    T = len(X)
    numIterations = 10

    for _ in range(0, numIterations):
        mu = np.empty([K, nDim])
        mu_update = np.empty([K, nDim])

        # Initialize mean vectors for every component
        for k in range(0, K):
             mu[k] = gmm.means_[k]

        # Posterior probability of each component
        pcompx = gmm.predict_proba(X)
        # sum_i - sum of posterior probabilities for each component
        sum_i = np.sum(pcompx, axis=0)
        for i in range(0, K):
            if (sum_i[i] < EPS):
                sum_i[i] = SMALLVALUE
        alpha = sum_i / (sum_i + r)

        # Mean adjustments
        for i in range(0,K):
            for j in range(0, nDim):
                mu_update[i][j] = 0
                for t in range(0,T):
                    mu_update[i][j] += pcompx[t][i] * X[t][j]
                mu_update[i][j] /= sum_i[i]

        for i in range(0, K):
            for j in range(0, nDim):
                mu_update[i][j] = 
                    alpha[i] * mu_update[i][j] + (1 - alpha[i]) * mu[i][j]

        gmm.means_ = mu_update
