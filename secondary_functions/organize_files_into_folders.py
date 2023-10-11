import os
from tqdm import tqdm

def organize_files_into_folders(target_path, source_path):
    materials = []
    for root, dirs, files in os.walk(source_path):
        for file in tqdm(files):
            if file.endswith(".csv"):
                length_array = len(file.split('_'))
                material = 'error'
                if length_array == 3:
                    material = file.split('_')[1]
                if length_array == 2:
                    material = file.split('.csv')[0].split('_')[-1]
                if length_array == 4:
                    material = file.split('_')[2]
                if length_array == 5:
                    material = file.split('_')[1]
                try:
                    material = material.lower()
                    materials.append(material)
                    if not os.path.isfile(os.path.join(target_path[material], file)):
                        os.rename(os.path.join(root, file), os.path.join(target_path[material], file))
                except:
                    print(os.path.join(root, file))
    print(*set(materials), sep=' ')
