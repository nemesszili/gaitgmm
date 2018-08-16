import numpy as np

# Constants used for GMM model adaptation
EPS = 0.0000001
SMALLVALUE = 0.00001
r = 0

# GMM parameters
COVAR_TYPE = 'diag'
NUM_UBM_MIXTURES = 8 
NUM_USER_MIXTURES = 8

# Directory where feature CSVs are stored
FEAT_DIR = 'features'

# Range of users from session0 for training the UBM
UBM_USER_RANGE = range(1, 12)

# Range of users from session0 to be used as negative samples
NEG_USER_RANGE = range(12, 23)

# Total number of users
NUM_USERS = 153

# Random state for reproducibility
RANDOM_STATE = np.random.seed(0)