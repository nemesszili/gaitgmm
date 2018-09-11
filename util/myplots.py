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
             label='System AUC = %0.4f, System EER= %0.4f' % (auc_value, eer))
    plt.plot([0, 1], [0, 1], color='darkorange', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC')
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
    print('Evaluating same day 1 cycle')
    params = (False, True, 1, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_1, fpr_1, auc_1, eer_1 = evaluate('temp_scores.csv')
    print('System AUC: {}'.format(auc_1))
    print('System EER: {}'.format(eer_1))
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass
    print()

    print('Evaluating same day 10 cycles')
    params = (False, True, 10, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_2, fpr_2, auc_2, eer_2 = evaluate('temp_scores.csv')
    print('System AUC: {}'.format(auc_2))
    print('System EER: {}'.format(eer_2))
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass
    print()

    print('Evaluating cross day 1 cycle')
    params = (True, True, 1, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_3, fpr_3, auc_3, eer_3 = evaluate('temp_scores.csv')
    print('System AUC: {}'.format(auc_3))
    print('System EER: {}'.format(eer_3))
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass
    print()
    
    print('Evaluating cross day 10 cycles')
    params = (True, True, 10, True, False)
    train_evaluate(load(params[1]), params, 'temp_scores.csv')
    tpr_4, fpr_4, auc_4, eer_4 = evaluate('temp_scores.csv')
    print('System AUC: {}'.format(auc_4))
    print('System EER: {}'.format(eer_4))
    try:
        os.remove('temp_scores.csv')
    except OSError:
        pass
    print()

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
