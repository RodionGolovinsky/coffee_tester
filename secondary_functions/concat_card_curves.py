import os

import pandas as pd


def concat_card_curves(df_card, path_curves_dir):
    electrodes = []
    tables = []
    for root, dirs, files in os.walk(path_curves_dir):
        for file in files:
            if 'with' in file:
                electrode = file.split('.csv')[0].split('_')[2]
                electrodes.append(electrode)
                curves = pd.read_csv(os.path.join(root, file))
                curves.drop(curves.columns[[0, -1, -2, -4]], axis=1, inplace=True)
                df_card['number_of_sample'] = df_card['number_of_sample'].astype('str')
                curves['number_of_sample'] = curves['number_of_sample'].astype('str')
                df_new = curves.merge(df_card, on='number_of_sample', how='inner')
                tables.append(df_new)
    return dict(zip(electrodes, tables))
