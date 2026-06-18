-- ===========================================
-- HANDS ON 1
-- Vehicle Service Management System
-- Database Design & DDL Operations
-- ===========================================

CREATE DATABASE vehicle_service_db;

USE vehicle_service_db;

-- ===========================================
-- TABLE CREATION
-- ===========================================

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
vehicle_name VARCHAR(100) NOT NULL,
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
mechanic_name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE,
center_id INT,
salary DECIMAL(10,2),
FOREIGN KEY(center_id)
REFERENCES service_centers(center_id)
);

SHOW TABLES;

DESC service_centers;
DESC customers;
DESC vehicles;
DESC service_records;
DESC mechanics;

-- ===========================================
-- NORMALIZATION ANALYSIS
-- ===========================================

-- 1NF
-- All columns contain atomic values.
-- No column stores multiple values.
-- Example violation:
-- phone = '9876543210,9876543211'

-- 2NF
-- Every non-key attribute depends fully
-- on the primary key.
-- Example:
-- email depends on customer_id.

-- 3NF
-- No transitive dependency exists.
-- Service center details are stored only
-- in service_centers table.
-- Customers reference center_id.
-- This prevents data redundancy.
-- service_records satisfies 3NF because
-- service_date, service_type and
-- service_status depend only on service_id.

-- ===========================================
-- ALTER TABLE OPERATIONS
-- ===========================================

ALTER TABLE customers
ADD emergency_contact VARCHAR(15);

ALTER TABLE service_centers
ADD max_capacity INT DEFAULT 100;

ALTER TABLE service_records
ADD CONSTRAINT chk_status
CHECK (service_status IN
('Pending','Completed','In Progress'));

ALTER TABLE service_centers
RENAME COLUMN manager_name
TO center_manager;

ALTER TABLE customers
DROP COLUMN emergency_contact;

DESC service_centers;
