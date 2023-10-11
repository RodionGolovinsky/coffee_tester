import numpy as np
import os

import pandas as pd


def load_card(path):
    df = pd.read_csv(path)
    df.rename({'№': 'number_of_sample'}, inplace=True, axis=1)
    # df.drop('были уже внесены в excel с печатных дегустационных листов', axis=1, inplace=True)
    for col in df.columns.values:
        if 'Unnamed' in col:
            df.drop(col, axis=1, inplace=True)
    return df
