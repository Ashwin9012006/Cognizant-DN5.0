-- HANDS ON 1
-- Vehicle Service Management System

CREATE DATABASE vehicle_service_db;

USE vehicle_service_db;

CREATE TABLE service_centers(
center_id INT AUTO_INCREMENT PRIMARY KEY,
center_name VARCHAR(100) NOT NULL,
manager_name VARCHAR(100),
budget DECIMAL(12,2)
);

CREATE TABLE customers(
customer_id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
phone VARCHAR(15),
center_id INT,
FOREIGN KEY(center_id)
REFERENCES service_centers(center_id)
);

CREATE TABLE vehicles(
vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
vehicle_name VARCHAR(100),
vehicle_number VARCHAR(30) UNIQUE,
model_year INT,
customer_id INT,
FOREIGN KEY(customer_id)
REFERENCES customers(customer_id)
);

CREATE TABLE service_records(
service_id INT AUTO_INCREMENT PRIMARY KEY,
vehicle_id INT,
service_date DATE,
service_type VARCHAR(100),
service_status VARCHAR(20),
FOREIGN KEY(vehicle_id)
REFERENCES vehicles(vehicle_id)
);

CREATE TABLE mechanics(
mechanic_id INT AUTO_INCREMENT PRIMARY KEY,
mechanic_name VARCHAR(100),
email VARCHAR(100) UNIQUE,
center_id INT,
salary DECIMAL(10,2),
FOREIGN KEY(center_id)
REFERENCES service_centers(center_id)
);

-- 1NF
-- All attributes contain atomic values.

-- 2NF
-- All non-key attributes depend completely on the primary key.

-- 3NF
-- No transitive dependencies exist.

ALTER TABLE service_centers
ADD max_capacity INT DEFAULT 100;

ALTER TABLE service_centers
RENAME COLUMN manager_name TO center_manager;
