CREATE USER 'test_user'@'%';
CREATE DATABASE IF NOT EXISTS test_db; 
GRANT ALL PRIVILEGES ON test_db.* TO 'test_user'@'%';
FLUSH PRIVILEGES;