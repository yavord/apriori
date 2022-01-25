import pandas as pd
import numpy as np
from dataclasses import make_dataclass


# Sample data set
df = pd.DataFrame(np.array([
    'b,a,c',
    'a,c',
    'b,c',
    'c'
]), columns=['items'])

class Apriori:
    pass

def find_support(
    pd_series: pd.Series,
    min_support: int = 1,
    index_type: str = 'str'
) -> pd.DataFrame:
    """
    pd_series: iterate through sets and find the support for each item in the item set
    min_support: minimum support threshold for final item sets
    index_type: based on input data and if the user would like it to be encoded as int for ex
    output (L): pd.DataFrame with support counts that pass threshold and displays set size
    """
    split = pd_series.str.split(',', expand=True)
    support = split.apply(pd.value_counts).sum(axis=1).where(lambda value: value > min_support).dropna()
    L = pd.DataFrame(
    {
        'items': support.index.astype(index_type),
        'support_count': support.values,
        'set_size': 1
    })
    return(L)
