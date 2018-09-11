import click
import warnings
warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

from util.settings import *
from util.process import load, train_evaluate, evaluate
from util.myplots import plot_scores, plotAUC, plot_cycles_ROC_1_10

@click.command()
@click.option('--plot', is_flag=True,
              help='Generate figure 3 from the paper')
@click.option('--plot-auc', is_flag=True,
              help='Plot system AUC for current settings')
@click.option('--plot-hist', is_flag=True,
              help='Plot system histogram for current settings')
@click.option('--no-config', is_flag=True,
              help='Override settings.py with command-line options')
@click.option('--cross-session/--same-session', default=False,
              help='Evaluate with data from session 2')
@click.option('--cycle/--fixed', default=True,
              help='Segment the data based on annotation')
@click.option('--num-cycles', default=10,
              help='Number of consecutive cycles used for evaluation')
@click.option('--adapted-gmm/--classic-gmm', default=True,
              help='Use MAP adapted GMMs')
@click.option('--reg-negatives/--unreg-negatives', default=False,
              help='Use registered negatives')
def main(plot, plot_auc, plot_hist, no_config, cross_session, cycle, 
         num_cycles, adapted_gmm, reg_negatives):
    if plot:
        plot_cycles_ROC_1_10()
        return

    if no_config:
        params = (cross_session, cycle, num_cycles, 
                  adapted_gmm, reg_negatives)
        dataframes = load(cycle)
    else:
        params = (CROSS_SESSION, CYCLE, NUM_CYCLES, 
                  ADAPTED_GMM, REGISTERED_NEGATIVES)
        dataframes = load(CYCLE)

    print()
    print('Running evaluation with:')
    print(' - cross session: {}'.format(params[0]))
    print(' - cycle:         {}'.format(params[1]))
    print(' - num cycles:    {}'.format(params[2]))
    print(' - adapted gmm:   {}'.format(params[3]))
    print(' - reg negatives: {}'.format(params[4]))
    print()
    print('Plots:')
    print(' - AUC:           {}'.format(plot_auc))
    print(' - Histogram:     {}'.format(plot_hist))
    print()
    
    neg_scores, pos_scores = train_evaluate(
        dataframes, params, 'scores.csv')
    tpr, fpr, auc_value, eer = evaluate('scores.csv')

    if plot_auc:
        plotAUC('scores.csv')
    if plot_hist:
        plot_scores('All users: u001-u040', neg_scores, pos_scores)

if __name__ == '__main__':
    main()