#Tweeter

This project was essentially a Twitter clone that I worked on during the summer of 2020. At the time I still often neglected to use version control (for some reason) so I just pushed everything I did in case I ever want to go back to it.

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
