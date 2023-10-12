import os

import pandas as pd
from tqdm import tqdm

# use it to convert all data from edf to csv format
def convert_to_csv_from_edf(path_edf_dir, path_to_save_csv):
    for root, dirs, files in os.walk(path_edf_dir):
        for file in tqdm(files):
            if file.endswith('.edf'):
                with open(os.path.join(root, file), "rt", encoding="latin-1") as f:
                    text = f.read()
                    strings = text.splitlines()
                    times, currents, voltages = [], [], []
                    for string in strings:
                        one_string = string.split(' ')
                        norm_string = ' '.join(one_string).split()
                        if len(norm_string) == 4:
                            times.append(norm_string[1])
                            voltages.append(norm_string[2])
                            currents.append(norm_string[3])
                df = pd.DataFrame(list(zip(times, currents, voltages)), columns=['Time', 'Current', 'Voltage'])
                new_filename = file.split('.')[0] + '.csv'
                df.to_csv(os.path.join(path_to_save_csv, new_filename))
