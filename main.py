import click
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from util.settings import *
from util.process import extract_load_feat, train_evaluate

@click.command()
@click.option('--force-extract', is_flag=True,
              help='Force feature re-extraction')
def main(force_extract):
    df0, df1, df2 = extract_load_feat(force_extract, CYCLE)
    train_evaluate(df0, df1, df2)

if __name__ == '__main__':
    main()