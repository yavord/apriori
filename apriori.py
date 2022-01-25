import pandas as pd
import numpy as np
from dataclasses import make_dataclass

df = pd.DataFrame(np.array([
    'b,a,c',
    'a,c',
    'b,c',
    'c'
]), columns=['items'])


def find_support(
    pd_series: pd.Series,
    min_support: int = 1,
    index_type: str = 'str'
):
    split = pd_series.str.split(',', expand=True)
    support = split.apply(pd.value_counts).sum(axis=1).where(lambda value: value > min_support).dropna()
    L = pd.DataFrame(
    {
        'items': support.index.astype(index_type),
        'support_count': support.values,
        'set_size': 1
    })
    return(L)

x = find_support(df['items'])
df['set_size'] = df['items'].str.count(',') + 1
df['items'] = df['items'].apply(lambda row: set(map(str, row.split(","))))
