import pandas as pd
import numpy as np
from itertools import combinations
from operator import itemgetter


# import sample data
# combinations of individual items coded as str -> list of ints
df = pd.read_csv('sample_data.csv')

class Apriori:
    pass

def find_support(
    pd_series: pd.Series,
    min_support: int = len(df)*0.25,
    index_type: str = 'int'
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
        'support': support.values,
        'set_size': 1
    })
    return(L)

def find_subset_support(
    data: pd.DataFrame = df,
    min_support: int = len(df)*0.25,
) -> pd.DataFrame:
    """
    calculate the support for all possible subsets
    """
    L = find_support(data['items'], min_support=min_support)
    data['set_size'] = data['items'].str.count(",") + 1
    # change map based on data type, ideally should be int
    data['items'] = data['items'].apply(lambda row: set(map(int, row.split(','))))
    L_set = set(L['items'])

    for length in range(2, len(L_set)+1):
        data = data[data['set_size']>= length]
        d = data['items'] \
            .apply(lambda st: pd.Series(s if set(s).issubset(st) else None for s in combinations(L_set, length))) \
            .apply(lambda col: [col.dropna().unique()[0], col.count()] if col.count() >= min_support else None).dropna()
        if d.empty:
            break

        L = L.append(pd.DataFrame({
            'items': list(map(itemgetter(0), d.values)),
            'support': list(map(itemgetter(1), d.values)),
            'set_size': length
             }), ignore_index=True)

        return(L)

def find_confidence(
    data: pd.DataFrame = find_subset_support(),
    min_confidence: float = 0.5
) -> pd.DataFrame:
    """
    calculate confidence using support of all sets passing min_support threshold
    """
    s = data[data['set_size'] < 2]
    m = data[data['set_size'] >= 2]

    m['confidence'] = m['support'] / s.loc[s['items'] == m['items'].values[0][0], ['support']].values[0]
    m = m[m['confidence'] >= min_confidence]

    return(m)