CREATE DATABASE keycloak;
CREATE USER keycloak_user WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak_user;