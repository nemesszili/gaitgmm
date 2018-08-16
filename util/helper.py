import pandas as pd

from util.const import *

##
#  Select features belonging to unregistered users from session0
#
def unreg_negative_samples(df):
    numFeatures = df.shape[1]
    userids = ['u%03d' % i for i in NEG_USER_RANGE]
    frames = df.loc[df.iloc[:, -1].isin(userids)]
    return frames

# select a fraction rom negatives_df dataframe (session0)
def select_negative_samples_fraction(negatives_df, fraction):
    return negatives_df.sample( frac = fraction, random_state=RANDOM_STATE)

# select numsamples negative samples from negatives_df dataframe (session0)
def select_negative_samples_numsamples(negatives_df, numsamples):
    return negatives_df.sample( numsamples, random_state=RANDOM_STATE)


# select numsamples negative samples from the other users of session1
def select_negatives_from_other_users(dataset, userid, numsamples):
    num_features = dataset.shape[1]
    other_users_data =  dataset[num_features - 1] != userid
    dataset_negatives = dataset[other_users_data].sample(numsamples, random_state=RANDOM_STATE)
    return dataset_negatives