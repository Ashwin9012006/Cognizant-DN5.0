-- Hands-On 4
-- Query Optimization
-- Vehicle Service Management System

EXPLAIN FORMAT=JSON
SELECT CONCAT(c.first_name,' ',c.last_name) AS customer_name,
       v.vehicle_name,
       sr.service_type
FROM service_records sr
JOIN vehicles v
ON sr.vehicle_id = v.vehicle_id
JOIN customers c
ON v.customer_id = c.customer_id;

CREATE INDEX idx_vehicle_name
ON vehicles(vehicle_name);

CREATE INDEX idx_service_type
ON service_records(service_type);

SHOW INDEX FROM vehicles;

SHOW INDEX FROM service_records;

EXPLAIN FORMAT=JSON
SELECT CONCAT(c.first_name,' ',c.last_name) AS customer_name,
       v.vehicle_name,
       sr.service_type
FROM service_records sr
JOIN vehicles v
ON sr.vehicle_id = v.vehicle_id
JOIN customers c
ON v.customer_id = c.customer_id;
