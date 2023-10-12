import pandas as pd
import numpy
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

model = CatBoostClassifier()
model.load_model('/home/rodion/PycharmProjects/coffee/training/task/quality_pred_coffee/my_catboost_model_cu.bin')
df = pd.read_csv(
    '/data/clear_data/all_data/all_data_au.csv',
    index_col=['id'])
X = df.drop('filename', axis=1)
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
y = model.predict(X)
encoder = LabelEncoder()
encoder.classes_ = numpy.load('/training/task/quality_pred_coffee/feature_importances/label_encoder.npy', allow_pickle=True)
y = encoder.inverse_transform(y)
print(y)
df['label'] = y

print(df)
df.to_csv('predicted.csv', index='id ')