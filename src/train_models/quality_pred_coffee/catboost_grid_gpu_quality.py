import time
from datetime import datetime

import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from src.secondary_functions import names_in_english


def catboost_grid(target_col, catboost_model, dataset_path):
    dataset = pd.read_csv(dataset_path)
    X = dataset.drop(target_col, axis=1)
    y = dataset[target_col]
    encoder = LabelEncoder().fit(y)
    y = pd.Series(encoder.transform(y))
    scaler = MinMaxScaler()
    X = pd.DataFrame(scaler.fit_transform(X))
    X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.2, shuffle=True, stratify=y,
                                                        random_state=42)
    start = time.time()
    grid_search_results = catboost_model.grid_search(grid, X=X_train, y=y_train, cv=5, refit=True,
                                                     train_size=0.1)
    end = time.time()
    # sorted_feature_importance = catboost_model.feature_importances_.argsort()
    y_pred = encoder.inverse_transform(catboost_model.predict(X_test))
    catboost_model.save_model(
        f'catboost_{dataset_path.split("/")[-1].split("_")[0]}_{names_in_english[target_col]}.bin')
    best_params = catboost_model.get_params()

    with open(
            f'/home/rodion/PycharmProjects/coffee/train_models/task/quality_pred_coffee/res/report_catboost_{dataset_path.split("/")[-1].split("_")[0]}_{names_in_english[target_col]}.txt',
            'a') as f:
        f.write(f'Grid Search for catboost {names_in_english[target_col]}, {datetime.now()}\n')
        f.write(f'Preprocessor - {scaler.__class__.__name__}\n')
        f.write(f'Program runtime: {(end - start):.2f}\n')
        f.write(
            f'Classification_report:\n{classification_report(encoder.inverse_transform(y_test), y_pred)}')
        f.write(f'Best params:\n{best_params}\n')
        # print(sorted_feature_importance)
    # np.savetxt(fname=f'feature_importances_catboost_{dataset_path.split("/")[-1].split("_")[0]}_{names_in_english[target_col]}.txt', X=sorted_feature_importance.tolist())


target_col = 'quality'

grid = {
    'iterations': [1000, 2500, 5000, 10000],
    'learning_rate': [0.05, 0.005, 0.0001],
    'depth': [1, 2, 3, 4, 5, 6, 7],
    'l2_leaf_reg': [1, 5, 15, 20, 25],
    'early_stopping_rounds': [500],
    'verbose': [250]
}
grid = {
    'iterations': [250, 500, 1000],
    'learning_rate': [0.05, 0.005, 0.0001],
    'depth': [1, 2, 3, 4, 5, 6, 7],
    'l2_leaf_reg': [1, 5, 15, 20, 25],
    'early_stopping_rounds': [500],
    'verbose': [250]
}

# for file in tqdm(os.listdir(root)):
# TODO: PATHS!
catboost_grid(target_col, CatBoostClassifier(task_type="GPU", bootstrap_type='Poisson', subsample=0.4),
              '/train_models/datasets_classification/dataset_summary_data/all_materials_dataset_quality.csv')
