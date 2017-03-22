CREATE DATABASE studybuddy_db;
CREATE USER studybuddy_user WITH PASSWORD 'muddyP3ncil71';
ALTER ROLE studybuddy_user SET client_encoding TO 'utf8';
ALTER ROLE studybuddy_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE studybuddy_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE studybuddy_db TO studybuddy_user;