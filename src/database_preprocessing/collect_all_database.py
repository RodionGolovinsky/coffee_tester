from src.secondary_functions.convert_data_to_csv import convert_to_csv_from_edf
from src.secondary_functions.get_summery_tables import get_summery_tables
from src.secondary_functions.organize_files_into_folders import organize_files_into_folders

# TODO: Change paths in all file!
# use it to sort data to specific folders
target_paths = {"cu": '/home/rodion/PycharmProjects/coffee/data/clear_data/every_electrode/cu',
                "ni": '/home/rodion/PycharmProjects/coffee/data/clear_data/every_electrode/ni',
                "gc": '/home/rodion/PycharmProjects/coffee/data/clear_data/every_electrode/gc',
                "au": '/home/rodion/PycharmProjects/coffee/data/clear_data/every_electrode/au'}

path_edf_dir = '/data/raw_edf'
path_all_csv_data = '/data/clear_data/all_csv_data_from_edf'
path_all_data = '/data/clear_data/all_data'
print('Converting edf data to csv format in progress...')
convert_to_csv_from_edf(path_edf_dir, path_all_csv_data)
print('Organizing all csv data to specific folders in progress...')
organize_files_into_folders(target_paths, path_all_csv_data)
print('Collect all data in database...')
get_summery_tables(target_paths['cu'][:-3], path_all_data)


