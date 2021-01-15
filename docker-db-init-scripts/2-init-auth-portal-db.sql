CREATE DATABASE auth_portal;

CREATE USER auth_portal_admin;
CREATE DATABASE auth_portal_admin;

ALTER USER auth_portal_admin WITH PASSWORD 'admin';

GRANT ALL PRIVILEGES ON DATABASE auth_portal TO auth_portal_admin;