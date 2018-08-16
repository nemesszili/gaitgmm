import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn import model_selection, metrics


def plotAUC(scorefilename ):
    data = pd.read_csv(scorefilename, names=['label','score'])
    labels = data['label']
    scores = data['score']
    labels = [int(e)   for e in labels]
    scores = [float(e) for e in scores]
    auc_value =   metrics.roc_auc_score(np.array(labels), np.array(scores) )

    fpr, tpr, thresholds_no = metrics.roc_curve(labels, scores, pos_label=1)
    eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    print("System AUC:"+str(auc_value))
    print("System EER:"+str(eer))
    # thresh_no = interp1d(fpr_no, thresholds_no)(eer_no)

    plt.figure()
    lw = 2
    plt.plot(fpr,     tpr,     color='black', lw=lw, label='AUC = %0.4f, EER= %0.4f' % (auc_value, eer))
    plt.plot([0, 1], [0, 1], color='darkorange', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('AUC')
    plt.legend(loc="lower right")
    plt.show()
    return

def plot_scores(userid, impostor_scores, genuine_scores):
    plt.figure()
    print(len(genuine_scores),len(impostor_scores))
    print('Positive scores: ', np.histogram(genuine_scores))
    print('Negative scores: ', np.histogram(impostor_scores))
    # plt.title(userid, fontsize=8)
    # plt.hist(impostor_scores, bins=10, label='Impostors', color='C1', alpha=0.5)
    # plt.hist(genuine_scores, bins=10, label='Genuine', color='C0', alpha=0.5)

    min_value = np.min(impostor_scores)
    max_value = np.max(genuine_scores)
    bins = np.linspace(min_value, max_value, 100)
    plt.hist(impostor_scores, bins, label='Impostors', color='C1', alpha=0.5)
    plt.hist(genuine_scores, bins, label='Genuine', color='C0', alpha=0.5)

    plt.legend(fontsize=8)
    plt.yticks([], [])
    plt.show()





# plots several ROC curves
def plot_cycles_ROC( ):
    scorefilename_1 = 'scores_sameday_1cycle.csv'
    data_1 = pd.read_csv(scorefilename_1, names=['label','score'])
    labels_1 = data_1['label']
    scores_1 = data_1['score']
    labels_1 = [int(e)   for e in labels_1]
    scores_1 = [float(e) for e in scores_1]
    auc_value_1 =   metrics.roc_auc_score(np.array(labels_1), np.array(scores_1) )

    fpr_1, tpr_1, thresholds_1 = metrics.roc_curve(labels_1, scores_1, pos_label=1)
    eer_1 = brentq(lambda x: 1. - x - interp1d(fpr_1, tpr_1)(x), 0., 1.)
    thresh_no = interp1d(fpr_1, thresholds_1)(eer_1)

    scorefilename_2 = 'scores_sameday_5cycles.csv'
    data_2= pd.read_csv(scorefilename_2, names=['label', 'score'])
    labels_2 = data_2['label']
    scores_2 = data_2['score']
    labels_2 = [int(e) for e in labels_2]
    scores_2 = [float(e) for e in scores_2]
    auc_value_2 = metrics.roc_auc_score(np.array(labels_2), np.array(scores_2))

    fpr_2, tpr_2, thresholds_2 = metrics.roc_curve(labels_2, scores_2, pos_label=1)
    eer_2 = brentq(lambda x: 1. - x - interp1d(fpr_2, tpr_2)(x), 0., 1.)
    thresh_2 = interp1d(fpr_2, thresholds_2)(eer_2)

    scorefilename_3 = 'scores_crossday_1cycle.csv'
    data_3 = pd.read_csv(scorefilename_3, names=['label', 'score'])
    labels_3 = data_3['label']
    scores_3 = data_3['score']
    labels_3 = [int(e) for e in labels_3]
    scores_3 = [float(e) for e in scores_3]
    auc_value_3 = metrics.roc_auc_score(np.array(labels_3), np.array(scores_3))

    fpr_3, tpr_3, thresholds_3 = metrics.roc_curve(labels_3, scores_3, pos_label=1)
    eer_3 = brentq(lambda x: 1. - x - interp1d(fpr_3, tpr_3)(x), 0., 1.)
    thresh_3 = interp1d(fpr_3, thresholds_3)(eer_3)

    scorefilename_4 = 'scores_crossday_5cycles.csv'
    data_4 = pd.read_csv(scorefilename_4, names=['label', 'score'])
    labels_4 = data_4['label']
    scores_4 = data_4['score']
    labels_4 = [int(e) for e in labels_4]
    scores_4 = [float(e) for e in scores_4]
    auc_value_4 = metrics.roc_auc_score(np.array(labels_4), np.array(scores_4))

    fpr_4, tpr_4, thresholds_4 = metrics.roc_curve(labels_4, scores_4, pos_label=1)
    eer_4 = brentq(lambda x: 1. - x - interp1d(fpr_4, tpr_4)(x), 0., 1.)
    thresh_4 = interp1d(fpr_4, thresholds_4)(eer_4)



    plt.figure()
    lw = 2
    # plt.plot(fpr_1, tpr_1,     color='r', lw=lw, label='1 step cycle (AUC = %0.4f)' % auc_value_1)
    # plt.plot(fpr_2, tpr_2, color='g', lw=lw, label='5 step cycles (AUC = %0.4f)' % auc_value_2)

    plt.plot(fpr_1, tpr_1, color='k', lw=lw, label='same day, 1 cycle', linestyle='solid')
    plt.plot(fpr_2, tpr_2, color ='k', lw=lw, label='same day, 5 cycles', linestyle ='--' )
    plt.plot(fpr_3, tpr_3, color='k', lw=lw, label='cross day, 1 cycle', linestyle='-.')
    plt.plot(fpr_4, tpr_4, color='k', lw=lw, label='cross day, 5 cycles', linestyle=':')

    plt.plot([0, 1], [0, 1], color='darkorange', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curves')
    plt.legend(loc="lower right")
    plt.show()
    # end plot
    return


def plot_cycles_ROC_1_10( ):
    scorefilename_1 = 'scores_sameday_1cycle.csv'
    data_1 = pd.read_csv(scorefilename_1, names=['label','score'])
    labels_1 = data_1['label']
    scores_1 = data_1['score']
    labels_1 = [int(e)   for e in labels_1]
    scores_1 = [float(e) for e in scores_1]
    auc_value_1 =   metrics.roc_auc_score(np.array(labels_1), np.array(scores_1) )

    fpr_1, tpr_1, thresholds_1 = metrics.roc_curve(labels_1, scores_1, pos_label=1)
    eer_1 = brentq(lambda x: 1. - x - interp1d(fpr_1, tpr_1)(x), 0., 1.)
    thresh_no = interp1d(fpr_1, thresholds_1)(eer_1)

    scorefilename_2 = 'scores_sameday_10cycles.csv'
    data_2= pd.read_csv(scorefilename_2, names=['label', 'score'])
    labels_2 = data_2['label']
    scores_2 = data_2['score']
    labels_2 = [int(e) for e in labels_2]
    scores_2 = [float(e) for e in scores_2]
    auc_value_2 = metrics.roc_auc_score(np.array(labels_2), np.array(scores_2))

    fpr_2, tpr_2, thresholds_2 = metrics.roc_curve(labels_2, scores_2, pos_label=1)
    eer_2 = brentq(lambda x: 1. - x - interp1d(fpr_2, tpr_2)(x), 0., 1.)
    thresh_2 = interp1d(fpr_2, thresholds_2)(eer_2)

    scorefilename_3 = 'scores_crossday_1cycle.csv'
    data_3 = pd.read_csv(scorefilename_3, names=['label', 'score'])
    labels_3 = data_3['label']
    scores_3 = data_3['score']
    labels_3 = [int(e) for e in labels_3]
    scores_3 = [float(e) for e in scores_3]
    auc_value_3 = metrics.roc_auc_score(np.array(labels_3), np.array(scores_3))

    fpr_3, tpr_3, thresholds_3 = metrics.roc_curve(labels_3, scores_3, pos_label=1)
    eer_3 = brentq(lambda x: 1. - x - interp1d(fpr_3, tpr_3)(x), 0., 1.)
    thresh_3 = interp1d(fpr_3, thresholds_3)(eer_3)

    scorefilename_4 = 'scores_crossday_10cycles.csv'
    data_4 = pd.read_csv(scorefilename_4, names=['label', 'score'])
    labels_4 = data_4['label']
    scores_4 = data_4['score']
    labels_4 = [int(e) for e in labels_4]
    scores_4 = [float(e) for e in scores_4]
    auc_value_4 = metrics.roc_auc_score(np.array(labels_4), np.array(scores_4))

    fpr_4, tpr_4, thresholds_4 = metrics.roc_curve(labels_4, scores_4, pos_label=1)
    eer_4 = brentq(lambda x: 1. - x - interp1d(fpr_4, tpr_4)(x), 0., 1.)
    thresh_4 = interp1d(fpr_4, thresholds_4)(eer_4)



    plt.figure()
    lw = 2
    # plt.plot(fpr_1, tpr_1,     color='r', lw=lw, label='1 step cycle (AUC = %0.4f)' % auc_value_1)
    # plt.plot(fpr_2, tpr_2, color='g', lw=lw, label='5 step cycles (AUC = %0.4f)' % auc_value_2)

    plt.plot(fpr_1, tpr_1, color='k', lw=lw, label='same day, 1 cycle', linestyle='solid')
    plt.plot(fpr_2, tpr_2, color ='k', lw=lw, label='same day, 10 cycles', linestyle ='--' )
    plt.plot(fpr_3, tpr_3, color='k', lw=lw, label='cross day, 1 cycle', linestyle='-.')
    plt.plot(fpr_4, tpr_4, color='k', lw=lw, label='cross day, 10 cycles', linestyle=':')

    plt.plot([0, 1], [0, 1], color='darkorange', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curves')
    plt.legend(loc="lower right")
    plt.show()
    # end plot
    return

