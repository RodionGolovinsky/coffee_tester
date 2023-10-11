import os
import pandas as pd
from secondary_functions.load_card import load_card


def get_dataset_for_classification(path_card, path_all_data_with_names, target_columns: list, path_for_dataset):
    testing_card = load_card(path_card)
    data = testing_card[testing_card['Дегустатор'] == 'Леонова Т.']
    data = data[['number_of_sample', *target_columns]]
    data = data.replace([0.0, 1.0, 2.0, 3.0, 4.0], ['low', 'middle', 'middle', 'high', 'high'])
    data['number_of_sample'] = data['number_of_sample'].astype('str')
    electrodes = []
    tables = []
    for root, dirs, files in os.walk(path_all_data_with_names):
        for file in files:
            if 'with' in file:
                electrode = file.split('.csv')[0].split('_')[2]
                electrodes.append(electrode)
                curves = pd.read_csv(os.path.join(root, file), index_col=['id'])
                curves.drop(['filename', 'name', 'coffee_grind_and_roast'], axis=1,
                            inplace=True)
                curves['number_of_sample'] = curves['number_of_sample'].astype('str')
                df_new = curves.merge(data, on='number_of_sample', how='inner')
                tables.append(df_new)
            dictionary = dict(zip(electrodes, tables))
    for key in dictionary.keys():
        filename = key + '_for_classification.csv'
        print(dictionary[key])
        dictionary[key].to_csv(os.path.join(path_for_dataset, filename), index=False)
        print('Files saved!')
    return True


path_card = '/data/clear_data/Дегустация кофе 20.07 - Лист1.csv'
path_all_data_with_names = '/data/clear_data/all_data_with_names'
target_columns = ['Интенсивность_кислотности', 'Интенсивность_сладости', 'Интенсивность_горечи']
path_for_dataset = '/classification/datasets_classification/dataset_3_classes'
print(get_dataset_for_classification(path_card, path_all_data_with_names, target_columns, path_for_dataset))
