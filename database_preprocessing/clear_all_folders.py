import os
from paths import path_all_data, path_electrodes, path_cycles, path_all_data_with_names, path_all_csv_data


def cleaning(*paths):
    """
        Clear all files in directories which you enter in args

        :param paths: paths to all cleanup folders.
        """
    for path in [*paths]:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))
    print('Cleaned!')


cleaning(path_cycles, path_electrodes, path_all_data, path_all_csv_data, path_all_data_with_names)
