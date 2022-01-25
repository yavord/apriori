import imp
import pandas as pd
import numpy as np
from itertools import combinations
from operator import itemgetter
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
    calculate support for each item in pd_series
    output items that pass the min_support threshold
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

def find_subset_support(
    data: pd.DataFrame = df,
    min_support: int = 1,
):
    """
    calculate the support for all possible subsets
    """
    L = find_support(data['items'], min_support=min_support)
    data['set_size'] = data['items'].str.count(",") + 1
    data['items'] = data['items'].apply(lambda row: set(map(str, row.split(','))))
    L_set = set(L['items'])

    for length in range(2, len(L_set)+1):
        data = data[data['set_size']>= length]
        d = data['items'] \
            .apply(lambda st: pd.Series(s if set(s).issubset(st) else None for s in combinations(L_set, length))) \
            .apply(lambda col: [col.dropna().unique()[0], col.count()] if col.count() >= min_support else None).dropna()
        if d.empty:
            break
        print(d.values[0])
        # L = L.append(pd.DataFrame({
        #     'items': list(map(itemgetter(0), d.values)),
        #     'support': list(map(itemgetter(1), d.values)),
        #     'set_size': length
        #      }), ignore_index=True)
    