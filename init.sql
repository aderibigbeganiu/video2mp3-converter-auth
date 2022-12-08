-- CREATE USER (admin) IDENTIFIED BY (Adeleke);
 -- CREATE DATABASE auth;
 -- GRANT ALL PRIVILEGES ON auth.* TO auth_user;
 -- USE auth;

CREATE TABLE users (id INT NOT NULL PRIMARY KEY,
                                            email VARCHAR(255) NOT NULL,
                                                               password VARCHAR(255) NOT NULL)