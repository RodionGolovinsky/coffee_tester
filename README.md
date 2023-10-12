<h1 align="center">Электронный дегустатор кофе ☕</h1>
<img align="center"
  src="models/media/picture1.jpg"
  alt="Coffee process"
  style="display: inline-block; margin: 0 auto; max-width: 1000px">


Проект, объединяющий подходы, связанные с электрохимическим анализом и применением методов машинного обучения для определения вкусовых характеристик и качества кофе.
##  Usage ##
Сделайте локальную копию репозитория
```bash
git clone https://github.com/RodionGolovinsky/coffee_tester.git
```
Перейдите в директорию проекта 
```bash
cd путь_к_папке_проекта
```
Создайте в каталоге проекта новое виртуальное окружение 
```bash
python -m venv venv
```
или 
```bash
python3 -m venv venv
```
Активируйте виртуальное окружение 
- Mac/Linux
```bash
source venv/bin/activate
```
- Windows
```bash
venv\Scripts\activate.bat
```
Установите все необходимые бибилиотеки 
```bash
pip install -r requirements.txt
```
Запустите веб-интерфейс 
```bash
python -m streamlit run web.py
```
<p align="center">
    <img width="900" src="models/media/screencast.gif">
</p>

## Acknowledgment ## 
This project was carried out with the support of the Blue Sky Research grant. 