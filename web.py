import os
import pickle
import time

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from catboost import CatBoostClassifier

st.write("""
# Электронный дегустатор кофе ☕ #
""")
st.markdown("### Выберите edf-файл ###")
uploaded_file = st.file_uploader("", type=['edf'])
while (uploaded_file is None):
    time.sleep(1)
if uploaded_file is not None:
    times, currents, voltages = [], [], []
    for line in uploaded_file:
        line = line.decode('latin-1')  # Декодируйте строку,
        one_string = line.split(' ')
        norm_string = ' '.join(one_string).split()
        if len(norm_string) == 4:
            times.append(float(norm_string[1]))
            voltages.append(float(norm_string[2]))
            currents.append(float(norm_string[3]))
    df = pd.DataFrame(list(zip(times, currents, voltages)), columns=['Time', 'Current', 'Voltage'])
st.markdown("### Выберите материал электрода: ###")
electrode = st.radio(
    "",
    ["Au", "Cu", "GC", "Ni"],
    captions=["Золотой", "Медный", "Стеклоуглеродный", "Никелевый"])
current_path = os.getcwd()

electrode = electrode.lower()
model_path_quality = os.path.join(current_path, f'demo_app/models_quality/catboost_{electrode}.bin')
model_path_acidity = os.path.join(current_path, f'demo_app/models_taste/catboost_acidity_{electrode}.bin')
model_path_bitterness = os.path.join(current_path, f'demo_app/models_taste/catboost_bitterness_{electrode}.bin')
model_path_sweetness = os.path.join(current_path, f'demo_app/models_taste/catboost_sweetness_{electrode}.bin')
class_coffee = {0: 'Плохой', 1: 'Хороший'}
model_quality = CatBoostClassifier().load_model(model_path_quality)
model_acidity = CatBoostClassifier().load_model(model_path_acidity)
model_bitterness = CatBoostClassifier().load_model(model_path_bitterness)
model_sweetness = CatBoostClassifier().load_model(model_path_sweetness)
X = df['Current'].to_numpy().reshape((1, -1))
with open('demo_app/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
X = scaler.transform(X).reshape(-1)
probability = model_quality.predict_proba(X.reshape((1, -1)))
st.write(
    '### Качество кофе: ###')
st.write(f'**{class_coffee[np.argmax(probability)]}** кофе с вероятностью {round(max(*probability), 2)}')
st.write('### Вкусовые характеристики кофе: ###')
st.write(f'Кислотность: {model_acidity.predict(X.reshape((1, -1)))[0][0]} с вероятностью {round(max(*model_acidity.predict_proba(X.reshape((1, -1)))), 2)}')
st.write(f'Сладость: {model_sweetness.predict(X.reshape((1, -1)))[0][0]} с вероятностью {round(max(*model_sweetness.predict_proba(X.reshape((1, -1)))), 2)}')
st.write(f'Горечь: {model_bitterness.predict(X.reshape((1, -1)))[0][0]} с вероятностью {round(max(*model_bitterness.predict_proba(X.reshape((1, -1)))), 2)}')
st.markdown('### Вольтамперная характеристика ###')
fig = px.line(df, x='Voltage', y='Current', title='',
              labels={'x': 'Напряжение', 'y': 'Сила тока'})
fig.update_traces(line=dict(width=0.5))  # Change 'width' to set the line thickness

st.plotly_chart(fig)
st.write("### Содержимое файла: ###")
st.dataframe(df)
