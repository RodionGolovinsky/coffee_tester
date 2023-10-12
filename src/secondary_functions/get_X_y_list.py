import os

import pandas as pd


def get_X_y_list(path_dataset, cycles, target_name, *extra_columns):
    X_list = []
    y_list = []
    names = []
    for root, dirs, files in os.walk(path_dataset):
        for file in files:
            if file.endswith('.csv'):
                if cycles:
                    material = '_'.join(file.split('_')[:2])
                    print(material)
                else:
                    material = file.split('_')[0]
                df = pd.read_csv(os.path.join(root, file), index_col=['number_of_sample'])
                X = df.drop([target_name, *extra_columns], axis=1)
                y = df[[target_name]]
                X_list.append(X)
                y_list.append(y)
                names.append(material)

    data = dict(zip(names, X_list))
    targets = dict(zip(names, y_list))
    return data, targets
