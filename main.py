import click
import warnings
warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

from util.settings import *
from util.process import load, train_evaluate, evaluate
from util.myplots import plot_scores, plotAUC, plot_cycles_ROC_1_10

@click.command()
@click.option('--force-extract', is_flag=True,
              help='Force feature re-extraction')
def main(force_extract):
    dataframes = load(CYCLE)
    params = (CROSS_SESSION, CYCLE, NUM_CYCLES, 
              ADAPTED_GMM, REGISTERED_NEGATIVES)
    neg_scores, pos_scores = train_evaluate(
        dataframes, params, 'scores.csv')
    tpr, fpr, _ = evaluate('scores.csv')

    # plotAUC('scores.csv')
    # plot_scores('All users: u001-u040', neg_scores, pos_scores)
    # plot_cycles_ROC_1_10()

if __name__ == '__main__':
    main()