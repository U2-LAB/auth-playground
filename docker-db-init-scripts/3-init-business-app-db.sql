CREATE DATABASE business_app;

CREATE USER business_app_admin;
CREATE DATABASE business_app_admin;

ALTER USER business_app_admin WITH PASSWORD 'admin';

GRANT ALL PRIVILEGES ON DATABASE business_app TO business_app_admin;