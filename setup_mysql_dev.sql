-- create a database hbnb_test_db
CREATE DATABASE IF NOT hbnb_dev_db;
-- create a new user hbnb_test set password at localhost
CREATE USER 'hbnb_dev' @ 'localhost' IDENTIFIED BY "hbnb_test_pwd";
-- grant privilages
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
