-- HANDS ON 2

INSERT INTO service_centers
(center_name, center_manager, budget, max_capacity)
VALUES
('Chennai Central Service', 'Rajesh Kumar', 850000, 100);

UPDATE service_records
SET service_status='Completed'
WHERE service_id=3;

DELETE FROM service_records
WHERE service_status='Pending';

SELECT *
FROM customers
WHERE center_id=1;

SELECT *
FROM mechanics
WHERE salary BETWEEN 80000 AND 95000;

SELECT *
FROM customers
WHERE email LIKE '%gmail.com';

SELECT c.first_name,c.last_name,s.center_name
FROM customers c
JOIN service_centers s
ON c.center_id=s.center_id;

SELECT center_id,COUNT(*)
FROM customers
GROUP BY center_id;

SELECT center_id,COUNT(*)
FROM customers
GROUP BY center_id
HAVING COUNT(*)>2;
