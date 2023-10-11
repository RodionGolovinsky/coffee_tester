import os
import pickle
from datetime import datetime

from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from colorama import init, Fore
from colorama import Style

from secondary_functions.get_X_y_list import get_X_y_list

names_in_english = {'Интенсивность_горечи': 'bitterness',
                    'Интенсивность_сладости': 'sweetness',
                    'Интенсивность_кислотности': 'acidity',
                    'quality': 'quality'}


def classification(target_names, path_dataset, preprocessor, model, params_grid, results_dir, cycles: bool = False):
    init(autoreset=True)
    for target in target_names:
        if os.path.exists(path_dataset):
            print(Fore.CYAN + Style.BRIGHT + f'Start work with {target}')
        else:
            print(Fore.RED + Style.BRIGHT + f'Not such directory with dataset {path_dataset}')
            exit()
        current_extra_columns = target_names.copy()
        current_extra_columns.remove(target)
        X_list, y_list = get_X_y_list(path_dataset, cycles, target, *current_extra_columns)
        materials = list(X_list.keys())
        print(materials)
        for material in tqdm(materials):
            X = X_list[material]
            y = y_list[material]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True,
                                                                random_state=42, stratify=y)
            scaler = preprocessor.fit(X_train)
            X_train = preprocessor.transform(X_train)
            X_test = preprocessor.transform(X_test)
            scores = cross_val_score(model, X, y.values.ravel(), cv=5, scoring="accuracy")
            grid = GridSearchCV(model, params_grid, cv=5, verbose=False)
            grid.fit(X_train, y_train.values.ravel())
            best_model = grid.best_estimator_
            reports_path = results_dir + os.sep + material + os.sep + 'reports'
            models_path = results_dir + os.sep + material + os.sep + 'models'
            existence_reports = os.path.exists(reports_path)
            existence_models = os.path.exists(models_path)
            if existence_reports:
                pass
            else:
                os.makedirs(reports_path)
            if existence_models:
                pass
            else:
                os.makedirs(models_path)
            with open(os.path.join(reports_path,
                                   f"report_{material}_{model.__class__.__name__}_{names_in_english[target]}.txt"),
                      "a") as file:
                file.write(
                    f'Accuracy for easy cross_validation for model {model.__class__.__name__}: %0.2f (+/- %0.2f)' % (
                        scores.mean(), scores.std() * 2))
                file.write(f'\nGridSearch - {datetime.now()}')
                file.write(f'Preprocessor - {scaler.__class__.__name__}\n')
                file.write(
                    f'Classification report for {model.__class__.__name__}: \n Best estimator metrics: \n {classification_report(y_test, best_model.predict(X_test))}')
                file.write(f'Best model parameters: \n{grid.best_params_}\n\n')
            filename_model = f'{names_in_english[target]}' + f'_{material}_' + str(model.__class__.__name__) + '.pkl'
            pickle.dump(best_model,
                        open(os.path.join(models_path, filename_model), 'wb'))


path_dataset = '/classification/dataset_3_classes'

target_names = ['Интенсивность_горечи', 'Интенсивность_сладости', 'Интенсивность_кислотности']
