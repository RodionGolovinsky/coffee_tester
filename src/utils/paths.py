import os
from pathlib import Path
 

def get_project_path() -> str:
    """
    Create project path
    :return: str with path to project
    """
    return Path(__file__).parent


path_edf_data = os.path.join(get_project_path(), 'data', 'raw_edf')
path_all_csv_data = os.path.join(get_project_path(), 'data', 'clear_data', 'all_csv_data_from_edf')
path_all_data = os.path.join(get_project_path(), 'data', 'clear_data', 'all_data')
path_all_data_with_names = os.path.join(get_project_path(), 'data', 'clear_data', 'all_data_with_names')
path_cycles = os.path.join(get_project_path(), 'data', 'clear_data', 'by_cycles')
path_electrodes = os.path.join(get_project_path(), 'data', 'clear_data', 'every_electrode')
path_coffe_names = os.path.join(get_project_path(), 'data', 'clear_data', 'coffee_names.csv')
path_id_and_number = os.path.join(get_project_path(), 'data', 'clear_data', 'id_and_numberOfSample.csv')
path_icon_coffee = os.path.join(get_project_path(), 'gui', 'Oxygen-Icons.org-Oxygen-Apps-java.ico')
