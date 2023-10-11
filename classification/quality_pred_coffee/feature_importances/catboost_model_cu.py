import os

from catboost import CatBoostClassifier, Pool
import pandas as pd
import numpy
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from paths import get_project_path
import scikitplot as skplt
import matplotlib.pyplot as plt

model = CatBoostClassifier()
model.load_model(os.path.join(get_project_path(), 'classification/task/quality_pred_coffee/res/catboost_cu_quality.bin'))
df = pd.read_csv(os.path.join(get_project_path(), 'classification/datasets_classification/dataset_good_bad_coffee/cu_good_bad_classification.csv'), index_col=['number_of_sample'])
X = df.drop('quality', axis=1)
y = df['quality']
encoder = LabelEncoder().fit(y)
numpy.save('classes.npy', encoder.classes_)
y = pd.Series(encoder.transform(y))
scaler = MinMaxScaler()
X = pd.DataFrame(scaler.fit_transform(X))
X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.2, shuffle=True, stratify=y,
                                                        random_state=42)
y_pred = encoder.inverse_transform(model.predict(X))
y_true = encoder.inverse_transform(y_test)
skplt.metrics.plot_confusion_matrix(y_true, y_pred, normalize=True)
plt.show()
print(classification_report(y_true, y_pred))