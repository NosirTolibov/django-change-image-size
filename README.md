##Инструкцию по развороту и запуску проекта
- Python 3.9.0
- Django 3.2

####Клонирование проекта:
```bash
git clone https://github.com/Golhoper/test-for-IdaProject.git
```

####Вход в виртуальное окружение: 
```bash
python3 -m venv venv
source venv/bin/activate
```

####Установка компонентов:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

####Создание папки медиа:
```bash
mkdir media
```

####Запуск проекта
```bash
cd change_img_size
python manage.py migrate
python manage.py runserver
```