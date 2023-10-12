import os
import sys
import time
from datetime import datetime

sys.path.append('/secondary_functions')
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from paths import get_project_path

names_in_english = {'Интенсивность_горечи': 'bitterness', 'Интенсивность_сладости': 'sweetness',
                    'Интенсивность_кислотности': 'acidity', 'quality': 'quality'}
extra_names = ['Интенсивность_горечи', 'Интенсивность_сладости',
               'Интенсивность_кислотности']


def catboost_grid(target_col, catboost_model, dataset_path):
    dataset = pd.read_csv(dataset_path)
    X = dataset.drop(extra_names, axis=1)
    y = dataset[target_col]
    X = pd.DataFrame(StandardScaler().fit_transform(X))
    X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.2, shuffle=True, stratify=y,
                                                        random_state=42)
    start = time.time()
    grid_search_results = catboost_model.grid_search(grid, X=X_train, y=y_train, cv=5, refit=True,
                                                     train_size=0.1)
    print(grid_search_results)
    end = time.time()
    material = dataset_path.split(os.sep)[-1].split("_")[0]
    y_pred = catboost_model.predict(X_test)
    scores = cross_val_score(catboost_model, X, y.values.ravel(), cv=5, scoring="accuracy")
    catboost_model.save_model(f'catboost_{names_in_english[target_col]}_{material}.bin')
    best_params = catboost_model.get_params()

    with open(f'report_catboost_{material}_{names_in_english[target_col]}.txt',
              'a') as f:
        f.write(f'Grid Search for catboost {names_in_english[target_col]}, {datetime.now()}\n')
        f.write(
            f'Accuracy for easy cross_validation for model {catboost_model.__class__.__name__}: %0.2f (+/- %0.2f)' % (
                scores.mean(), scores.std() * 2))
        f.write(f'Program runtime: {(end - start):.2f}\n')
        f.write(
            f'Classification_report:\n{classification_report(y_test, y_pred)}')
        f.write(f'Best params:\n{best_params}\n')


grid = {
    'iterations': [2500, 5000, 7500, 10000],
    'learning_rate': [0.05, 0.025, 0.005, 0.0001],
    'depth': [1, 2, 3, 4, 5, 6, 7],
    'l2_leaf_reg': [1, 5],
    'early_stopping_rounds': [500],
    'verbose': [500]
}
file2 = 'data/datasets_classification/dataset_3_classes/gc_for_classification.csv'
catboost_grid('Интенсивность_сладости',
                  CatBoostClassifier(task_type="GPU", bootstrap_type='Poisson', subsample=0.4),
                  os.path.join(get_project_path(), file2))
