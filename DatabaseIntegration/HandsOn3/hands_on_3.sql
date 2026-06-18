-- HANDS ON 3

SELECT *
FROM mechanics m1
WHERE salary=
(
SELECT MAX(salary)
FROM mechanics m2
WHERE m1.center_id=m2.center_id
);

CREATE VIEW vw_customer_summary AS
SELECT
customer_id,
CONCAT(first_name,' ',last_name)
AS customer_name
FROM customers;

SELECT *
FROM vw_customer_summary;

DROP VIEW vw_customer_summary;

DELIMITER $$

CREATE PROCEDURE sp_add_service(
IN p_vehicle_id INT,
IN p_service_date DATE,
IN p_service_type VARCHAR(100),
IN p_status VARCHAR(20)
)
BEGIN

INSERT INTO service_records
(vehicle_id,service_date,service_type,service_status)
VALUES
(p_vehicle_id,p_service_date,p_service_type,p_status);

END$$

DELIMITER ;

START TRANSACTION;

UPDATE service_centers
SET budget=budget+10000
WHERE center_id=1;

ROLLBACK;
