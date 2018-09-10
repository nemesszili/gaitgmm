##
#  Modify the values below to test the model with different parameters.
#

##
#  True  - user models are trained using data from session1 while positive
#          test samples are taken from session2 (cross-day)
#  False - user models are both trained and tested using samples from
#          samples from session1 (same-day)
CROSS_SESSION = True

##
#  True  - data is segmented using the annotated step cycle boundaries
#  False - data is segmented into fixed length frames of 128
#
CYCLE = True

##
#  Number of consecutive cycles used for evaluation
#  To be varied between 1 and 10
#
NUM_CYCLES = 5

##
#  True  - GMMs are trained by adaptation from the UBM
#  False - Classic GMMs
#
ADAPTED_GMM = True

##
#  True  - negative samples are selected from users of session1 
#          (registered)
#  False - negative samples are selected from users of session0
#          (unregistered: u11-u22)
#
REGISTERED_NEGATIVES = False