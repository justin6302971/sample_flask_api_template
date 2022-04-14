CREATE DATABASE local_testdb
    WITH 
    OWNER = tempuser_local
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

CREATE SCHEMA sp
    AUTHORIZATION tempuser_local;