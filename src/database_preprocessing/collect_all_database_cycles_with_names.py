import os
import pandas as pd
from src.secondary_functions.concat_id_number_of_sample import concat_id_number_of_sample
from src.secondary_functions.convet_data_to_csv_cycles import convert_to_csv_from_edf_cycles


def collect_names_for_cycles_database(path_cycles, path_coffee_names, path_id_and_numbers,
                                      column_for_merge_id_nOfSam='number_of_sample'):
    names_df = concat_id_number_of_sample(path_coffee_names, path_id_and_numbers, column_for_merge_id_nOfSam)
    for root, dirs, files in os.walk(path_cycles):
        for dir in dirs:
            current_dir = os.path.join(root, dir)
            for file in os.listdir(current_dir):
                if file.endswith('names.csv'):
                    pass
                else:
                    current_table = pd.read_csv(os.path.join(current_dir, file), index_col=[0])
                    id = current_table['id'].tolist()
                    current_table = current_table.merge(names_df, on='id')
                    current_table['coffee_grind_and_roast'].fillna('-', inplace=True)
                    id_new = current_table['id'].tolist()
                    if len(id) != len(id_new):
                        diff = list(set(id).difference(set(id_new)))
                        print(f'File {file}\n in new database was deleted following values: {diff}')
                    print(current_table)
                    new_name = file.split('.csv')[0] + '_with_names.csv'
                    current_table.to_csv(os.path.join(current_dir, new_name), index=False)

# TODO: Change paths in all file!
path_cycles = '/data/clear_data/by_cycles'
path_coffee_names = '/data/clear_data/coffee_names.csv'
path_id_and_numbers = '/data/clear_data/id_and_numberOfSample.csv'
path_edf = '/data/raw_edf'
path_csv_dir_cycles = '/data/clear_data/by_cycles'
convert_to_csv_from_edf_cycles(path_edf, path_csv_dir_cycles)
collect_names_for_cycles_database(path_cycles, path_coffee_names, path_id_and_numbers)
