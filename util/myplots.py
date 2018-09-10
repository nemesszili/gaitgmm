import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn import model_selection, metrics
import os

from util.process import load, evaluate, train_evaluate

##
#  Plot figure for Area Under Curve based on TPR, FPR, AUC and EER.
#
#  @param[in]  scorefile  Scorefile for the system
#
def plotAUC(scorefile):
    tpr, fpr, auc_value, eer = evaluate(scorefile)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='black', lw=lw, 
             label='AUC = %0.4f, EER= %0.4f' % (auc_value, eer))
    plt.plot([0, 1], [0, 1], color='darkorange', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('AUC')
    plt.legend(loc='lower right')
    plt.show()
    return

##
#  Plot user or system specific score histogram.
#
#  @param[in]  title            Plot title
#  @param[in]  impostor_scores  0-labeled scores
#  @param[in]  genuine_scores   1-labeled scores
#
def plot_scores(title, impostor_scores, genuine_scores):
    plt.figure()
    min_value = np.min(impostor_scores)
    max_value = np.max(genuine_scores)
    bins = np.linspace(min_value, max_value, 100)
    plt.title(title, fontsize=8)
    plt.hist(impostor_scores, bins, label='Impostors', color='C1', alpha=0.5)
    plt.hist(genuine_scores, bins, label='Genuine', color='C0', alpha=0.5)

    plt.legend(fontsize=8)
    plt.yticks([], [])
    plt.show()

##
#  Plot figure for comparison of consecutive cycle AUCs (Fig.3. in paper)
#
def plot_cycles_ROC_1_10():
    params = (False, True, 1, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_1, fpr_1, auc_1, _ = evaluate('temp_scores.csv')
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass

    params = (False, True, 10, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_2, fpr_2, auc_2, _ = evaluate('temp_scores.csv')
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass

    params = (True, True, 1, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_3, fpr_3, auc_3, _ = evaluate('temp_scores.csv')
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass
    
    params = (True, True, 10, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_4, fpr_4, auc_4, _ = evaluate('temp_scores.csv')
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass

    plt.figure()
    lw = 2

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
    plt.legend(loc='lower right')
    plt.show()

    return
