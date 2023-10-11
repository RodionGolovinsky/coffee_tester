import os
import time

from catboost import CatBoostClassifier, Pool
import pandas as pd
import numpy
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from paths import get_project_path
import matplotlib.pyplot as plt
import pickle

catboost_model = CatBoostClassifier(
    **{'subsample': 0.4, 'depth': 1, 'od_wait': 500, 'verbose': 250,
       'l2_leaf_reg': 1, 'iterations': 2500, 'learning_rate': 0.05}

)
path_df = os.path.join(get_project_path(),
                       'data/datasets_classification/dataset_good_bad_coffee/ni_good_bad_classification.csv')
dataset = pd.read_csv(path_df, index_col=['number_of_sample'])
X = dataset.drop('quality', axis=1)
y = dataset['quality']
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
X = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.2, shuffle=True, stratify=y,
                                                    random_state=42)
start = time.time()
catboost_model.fit(X_train, y_train)
end = time.time()
catboost_model.save_model(
    os.path.join(get_project_path(), f'demo_apps/catboost_{path_df.split(os.sep)[-1].split("_")[0]}.bin'))
y_pred = catboost_model.predict(X_test)
catboost_model.plot_tree(tree_idx=0)
plt.show()
print(catboost_model.predict(X[2, :]))
print(catboost_model.predict_proba(X[2, :]))
print(catboost_model.predict(X[60, :]))
print(catboost_model.predict(X[50, :]))
print(catboost_model.predict(X[30, :]))
print(catboost_model.predict_proba(X[60, :]))
print(classification_report(y_test, y_pred))
