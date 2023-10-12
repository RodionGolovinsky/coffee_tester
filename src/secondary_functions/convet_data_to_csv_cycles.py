import pandas as pd
import os
from tqdm import tqdm


def convert_to_csv_from_edf_cycles(path_edf_dir, path_csv_dir_cycles):
    cycles = []
    all_files = []
    file_names = []
    for root, dirs, files in os.walk(path_edf_dir):
        for file in tqdm(files):
            if file.endswith('.edf'):
                with open(os.path.join(root, file), "rt", encoding="latin-1") as f:
                    text = f.read()
                    f.close()
                strings = text.splitlines()
                times, currents, voltages = [], [], []
                for string in strings:
                    one_string = string.split(' ')
                    norm_string = ' '.join(one_string).split()
                    if len(norm_string) == 4:
                        times.append(float(norm_string[1]))
                        voltages.append(float(norm_string[2]))
                        currents.append(float(norm_string[3]))
                    else:
                        tmp_df = pd.DataFrame(data={
                            'Time': times,
                            'Voltage': voltages,
                            'Current': currents
                        })
                        if not tmp_df.empty:
                            cycles.append(tmp_df)
                            times = []
                            currents = []
                            voltages = []
                all_files.append(cycles)
                file_names.append(os.path.join(root, file))
                cycles = []
    for i in range(5):
        ni, cu, gc, au = [], [], [], []
        for f, filename in zip(all_files, file_names):
            current_file = filename.split(os.sep)[-1]
            try:
                cycle = f[i]['Current'].tolist()
                if len(cycle) == 1140:
                    cycle.pop(-1)
                if len(cycle) != 1139:
                    print(f'Length incorrect for file - {filename}: {len(cycle)}')
                    cycle = cycle[:1139]
                cycle.append(current_file)
                cycle.append(current_file.split('c_')[0])
            except IndexError:
                print(f'{filename} ошибка в количестве циклов!')
            if 'ni' in current_file:
                ni.append(cycle)
            elif 'cu' in current_file:
                cu.append(cycle)
            elif 'gc' in current_file:
                gc.append(cycle)
            elif 'au' in current_file:
                au.append(cycle)
        df_ni = pd.DataFrame(data=ni)
        df_cu = pd.DataFrame(data=cu)
        df_gc = pd.DataFrame(data=gc)
        df_au = pd.DataFrame(data=au)
        number_of_cycle = i + 1
        dfs = [df_cu, df_au, df_gc, df_ni]
        for dataframe in dfs:
            dataframe.rename({1139: 'filename', 1140: 'id'}, inplace=True, axis=1)
            # print(dataframe)
        df_ni.to_csv(os.path.join(path_csv_dir_cycles, f'cycle{number_of_cycle}', f'ni_cycle{number_of_cycle}.csv'), index=False)
        df_cu.to_csv(os.path.join(path_csv_dir_cycles, f'cycle{number_of_cycle}', f'cu_cycle{number_of_cycle}.csv'), index=False)
        df_gc.to_csv(os.path.join(path_csv_dir_cycles, f'cycle{number_of_cycle}', f'gc_cycle{number_of_cycle}.csv'), index=False)
        df_au.to_csv(os.path.join(path_csv_dir_cycles, f'cycle{number_of_cycle}', f'au_cycle{number_of_cycle}.csv'), index=False)
