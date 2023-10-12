import os
import pandas as pd


def get_summery_tables(path_dirs_clean, path_summery_tables):
    for root, dirs, files in os.walk(path_dirs_clean):
        df_list_for_dirs = []
        for dir in dirs:
            g = locals()
            g[dir] = []
            current_path = os.path.join(root, dir)
            files_in_current_dir = os.listdir(current_path)
            for file in files_in_current_dir:
                df = pd.read_csv(os.path.join(current_path, file))
                current = df['Current'].tolist()
                id = file.split('_')[0][:-1]
                if len(current) != 5698:
                    print(f'Problems with file: {os.path.join(current_path, file)}')
                current.append(file)
                current.append(int(id))
                g[dir].append(current)
            df_one_material = pd.DataFrame(g[dir])
            df_one_material = df_one_material.sort_values(by=df_one_material.columns[-1], ignore_index=True)
            df_one_material.columns = [*list(range(5698)), 'filename', 'id']
            df_one_material.set_index(['id'], inplace=True)
            if df_one_material.isna().sum().sum() != 0:
                print(f'Empty values have been detected in the database for {dir} electrode!!!')
                break
            print(f'Database for {dir.title()} electrode:')
            print(df_one_material)
            name_for_result_file = 'all_data_' + dir + '.csv'
            df_one_material.to_csv(os.path.join(path_summery_tables, name_for_result_file))
