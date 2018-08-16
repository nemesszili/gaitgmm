import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture

from util.const import *

##
#  Train the Universal Background Model (UBM) with data from session0
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

# gmm - an initial GMM
# X - training data OR data used for adaptation
# Explanation
# K - number of components
# nDim - dimension of feature vectors
# Reynolds GMM - MAP adaptation
# Only the means are adapted
# Natalia Neverova, PhD, Lyon INSA, 2016
def gmm_map_mean_adaptation( gmm, X ):
    K, nDim = gmm.means_.shape
    T = len(X)
    numIterations = 10
    for iter in range(0,numIterations):
        # print("Iteration: ", iter)
        w = gmm.weights_
        w_update = np.empty([K])
        mu = np.empty([K, nDim])
        mu_update = np.empty([K, nDim])

        for k in range(0, K):
             mu[k] = gmm.means_[k]

        # posterior probability of each component
        pcompx = gmm.predict_proba(X)
        # n_i: sum of posterior probabilities for each component
        n_i = np.sum(pcompx, axis=0)
        for i in range(0, K):
            if (n_i[i] < EPS):
                n_i[i] = SMALLVALUE
        ALPHA = n_i/(n_i+r)
        # means
        for i in range(0,K):
            for j in range(0, nDim):
                mu_update[i][j] = 0
                for t in range(0,T):
                    mu_update[i][j]+=pcompx[t][i]*X[t][j]
                mu_update[i][j]/=n_i[i]
        # means
        for i in range(0, K):
            for j in range(0, nDim):
                mu_update[i][j] =ALPHA[i]*mu_update[i][j] + (1-ALPHA[i])*mu[i][j]

        gmm.means_ = mu_update
        # score = gmm.score_samples(X)
        # print("score:", sum(score) / T)
    return