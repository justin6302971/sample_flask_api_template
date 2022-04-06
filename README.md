# sample flask api template




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


## environment setting and basic command
``` bash

pip3 list

#install all packages in the file
pip3 install -r requirements.txt

#manually install certain package

# allow python to loading env setting from .env file
pip3 install python-dotenv 


# environment variables file that need to be set

#.env
SECRET_KEY
JWT_SECRET_KEY

#.flaskenv
export FLASK_ENV
export FLASK_APP
export SQLALCHEMY_DATABASE_URI
export SQLALCHEMY_TRACK_MODIFICATIONS

```


## application structures
* python blueprints for large application
* sqlalchemy as orm lib to access data
  

### commands for db table setup
``` bash
 
# interact with item through terminal
flask shell

from src.database import db

db.create_all()

db.drop_all()
```