FLASK_APP=src
FLASK_ENV=development
FLASK_RUN_PORT=8088

SQLALCHEMY_DATABASE_URI=postgresql://tempuser_local:temppassword_local@127.0.0.1:9908/local_testdb
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ECHO=True

JWT_SECRET_KEY=local_test_jwt_secret_key