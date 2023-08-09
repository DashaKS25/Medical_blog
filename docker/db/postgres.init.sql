-- initialize postgresql database for the django project
CREATE ROLE mmed WITH ENCRYPTED PASSWORD '123' LOGIN;
CREATE DATABASE med2 OWNER mmed;
