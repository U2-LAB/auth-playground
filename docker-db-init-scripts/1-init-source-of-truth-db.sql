CREATE DATABASE source_of_truth;

CREATE USER source_of_truth_admin;
CREATE DATABASE source_of_truth_admin;

ALTER USER source_of_truth_admin WITH PASSWORD 'admin';

GRANT ALL PRIVILEGES ON DATABASE source_of_truth TO source_of_truth_admin;