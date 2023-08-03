/* put database initialization script here */

-- for example
CREATE ROLE mmed WITH ENCRYPTED PASSWORD '123' LOGIN;
COMMENT ON ROLE docker IS 'docker user for tests';

CREATE DATABASE med2 OWNER mmed;
COMMENT ON DATABASE docker IS 'docker db for tests owned by docker user';
