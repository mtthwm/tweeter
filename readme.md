#Tweeter

##Running the app

###Basic
Activate your virtual environment

#####Windows
```
cd virtual
scripts/activate
cd ..
```

#####Linux
```
source ./virtual/bin/activate
```

Then run
```python
python manage.py runserver
```

###Celery
Start the Redis server
```
redis-server
```

Start the celery worker
```
celery -A tweeter beat -l info
```


###SCSS Compiling
To allow scss files to automatically be compiled to css, make sure you have the django-sass package installed via pip, then run
```
python manage.py sass homepage/static/homepage/css homepage/static/homepage/scss --watch
```
