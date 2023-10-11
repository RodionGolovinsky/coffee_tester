from catboost import CatBoostClassifier, Pool
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

model = CatBoostClassifier()
model.load_model(
    "/home/rodion/PycharmProjects/coffee/classification/task/quality_pred_coffee/res/catboost_cu_quality.bin")

df = pd.read_csv('/classification/datasets_classification/dataset_good_bad_coffee/cu_good_bad_classification.csv', index_col=['number_of_sample'])
X = df.drop('quality', axis=1)
y = df['quality']
encoder = LabelEncoder().fit(y)
y = pd.Series(encoder.transform(y))
scaler = MinMaxScaler()
X = pd.DataFrame(scaler.fit_transform(X))
X_train, X_test, y_train, y_test = train_test_split(X, y.ravel(), test_size=0.2, shuffle=True, stratify=y,
                                                        random_state=42)
y_pred = model.predict(X_test)
classification_report(y, y_pred)