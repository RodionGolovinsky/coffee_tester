from sklearn import svm
from catboost import CatBoostClassifier
from colorama import Fore
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from secondary_functions.classification_grid_and_cross import classification

path_dataset = '/classification/datasets_classification/dataset_good_bad_coffee'
target_names = ['quality']
results_dir = '/classification/results/results_quality_prediction'
preprocessor = MinMaxScaler()

mlp = MLPClassifier(max_iter=1000, random_state=42)
parameters_mlp = {'hidden_layer_sizes': [(50,), (100,), (50, 50), (100, 50)],
                  'activation': ['relu', 'tanh'],
                  'solver': ['adam', 'sgd'],
                  'alpha': [0.0001, 0.001, 0.01],
                  'learning_rate': ['constant', 'adaptive']
                  }

decision_tree_model = DecisionTreeClassifier(random_state=42)
parameters_tree = {'criterion': ['gini', 'entropy'],
                   'max_depth': [None, 10, 20, 30],
                   'min_samples_split': [2, 5, 10],
                   'min_samples_leaf': [1, 2, 4, 6],
                   'max_features': ['auto', 'sqrt', 'log2'],
                   }

log_reg = LogisticRegression(random_state=42)
parameters_log = {'penalty': ['l1', 'l2'],
                  'C': [0.01, 0.1, 1.0, 10.0],
                  'max_iter': [100, 200, 300],
                  "solver": ['liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga']}

svc = svm.SVC()
parameters_svc = {'C': [0.01, 0.1, 1.0, 10.0],
                  'gamma': [1, 0.1, 0.001, 0.0001],
                  'kernel': ['linear', 'rbf']}

catboost_model = CatBoostClassifier()
parameters_catboost = {'learning_rate': [0.03, 0.1, 0.001],
                       'depth': [*list(range(2, 100, 12))],
                       'l2_leaf_reg': [1, 3, 5, 7, 9],
                       'iterations': [*list(range(10, 300, 80))]}

xgb_model = XGBClassifier(tree_method='gpu_hist')
parameters_xgb = {
    'max_depth': range(2, 100, 2),
    'n_estimators': range(60, 200, 30),
    'learning_rate': [0.1, 0.01, 0.05, 0.001]
}
models = [mlp, decision_tree_model, log_reg, svc, catboost_model, xgb_model]
params = [parameters_mlp, parameters_tree, parameters_log, parameters_svc, parameters_catboost, parameters_xgb]
for model, parm in zip(models, params):
    print(Fore.MAGENTA + f'{model.__class__.__name__}')
    classification(target_names, path_dataset, preprocessor, model, parm, results_dir)
