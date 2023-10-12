import os
import pandas as pd
from src.secondary_functions.concat_id_number_of_sample import concat_id_number_of_sample
from src.utils.paths import path_coffe_names, path_id_and_number, path_all_data, path_all_data_with_names

def concat_name_id_number_of_sample(path_coffee_names, path_id_and_numbers, path_all_data, path_all_data_with_names,
                                    column_for_merge='number_of_sample'):
    """
        Сonnects the voltammetric characteristics to the names of the coffee samples

        :param path_coffee_names: File with the matching sample number and coffee name.
        :param path_id_and_numbers: File with matching sample number (number_of_sample) and experiment number (id).
        :param path_all_data: Folder with databases for all four electrodes.
        :param path_all_data_with_names: Folder where the new 4 files with databases containing the names of the coffee sample will be saved..
        """
    df = concat_id_number_of_sample(path_coffee_names, path_id_and_numbers, column_for_merge)
    for root, dirs, files in os.walk(path_all_data):
        for file in files:
            if file.endswith('.csv'):
                current_table = pd.read_csv(os.path.join(root, file))
                id = current_table['id'].tolist()
                df_result = current_table.merge(df, on='id')
                df_result['coffee_grind_and_roast'].fillna('-', inplace=True)
                id_new = df_result['id'].tolist()
                if len(id) != len(id_new):
                    diff = list(set(id).difference(set(id_new)))
                    print(f'File {file}\n in new database was deleted following values: {diff}')
                df_result.to_csv(os.path.join(path_all_data_with_names, file.split('.csv')[0] + '_with_names.csv'),
                                 index=False)


concat_name_id_number_of_sample(path_coffe_names, path_id_and_number, path_all_data, path_all_data_with_names)
