# sample flask api template


## Todo
* [ ] project structure
* [ ] replace flask-SQLAlchemy with SQLAlchemy
* [ ] use marshmallow for request params validation


## Table of contents
* environment settings
* folder structures
* application structures
* database settings
* authentication
* authorization
* error handling
* logging
* documentations


## application structures
* python blueprints for large application
* sqlalchemy as orm lib to access data


## environment setting and basic command
``` bash

pip3 install virtualenv


virtualenv venv


source venv/bin/activate

deactivate 

#in virtual env, pip stands for pip3
pip list

#install all packages in the file
pip install -r requirements.txt

# environment variables file that need to be set, python-dotenv package will pick up values from these files

#.env
SECRET_KEY
JWT_SECRET_KEY

# .flaskenv
export FLASK_ENV
export FLASK_APP
export SQLALCHEMY_DATABASE_URI
export SQLALCHEMY_TRACK_MODIFICATIONS

# run app
flask run
```

### commands for db table setup
``` bash
 
# interact with item through terminal
flask shell

from src.db.database import db

# only create tables(should create db first, check connection string)
db.create_all()

db.drop_all()
```


## references
1. [AUTOMATICALLY LOAD ENVIRONMENT VARIABLES IN FLASK](https://prettyprinted.com/tutorials/automatically_load_environment_variables_in_flask)
2. [flask tutorials](https://www.youtube.com/watch?v=WFzRy8KVcrM&t=606s)
3. [marshmallow for request validation](https://www.cameronmacleod.com/blog/better-validation-flask-marshmallow)
4. [flask sqlalchemy basic usage](https://kknews.cc/code/8gyampn.html)
5. [flask sqlalchemy basic usage -1](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
6. [use sqlalchemy instead of flask-sqlalchemy](https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4)
7. [build issues for flask in mac ](https://lifesaver.codes/answer/psycopg2-binary-fails-to-install-on-macos-big-sur-11-0-1-and-python-3-9-0-with-possible-workaround-1200)

