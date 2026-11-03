\copy employees(employee_id, first_name, last_name, password_hash, employee_role) FROM 'seeding/csv/employees.csv' WITH (FORMAT csv, HEADER true)
\copy vendors(vendor_id, vendor_name, vendor_phone, vendor_email, delivery_info) FROM 'seeding/csv/vendors.csv' WITH (FORMAT csv, HEADER true)
\copy supplies(supply_id, item_name, category) FROM 'seeding/csv/supplies.csv' WITH (FORMAT csv, HEADER true)
\copy menu_items(menu_item_id, menu_item_name, price, image_url) FROM 'seeding/csv/menu_items.csv' WITH (FORMAT csv, HEADER true)
\copy menu_item_supplies(menu_item_id, supply_id, quantity) FROM 'seeding/csv/menu_item_supplies.csv' WITH (FORMAT csv, HEADER true)
\copy sales(sale_id, sale_date, sale_price, sale_tip, sale_employee_id) FROM 'seeding/csv/sales.csv' WITH (FORMAT csv, HEADER true)
\copy sale_menu_items(sale_id, menu_item_id, quantity, price_at_purchase) FROM 'seeding/csv/sale_menu_items.csv' WITH (FORMAT csv, HEADER true)
\copy purchases(purchase_id, purchase_date, vendor_id) FROM 'seeding/csv/purchases.csv' WITH (FORMAT csv, HEADER true)
\copy purchase_supplies(purchase_supply_id, purchase_id, supply_id, purchase_quantity) FROM 'seeding/csv/purchase_supplies.csv' WITH (FORMAT csv, HEADER true)
UPDATE supplies s
SET quantity = GREATEST(0,
  COALESCE((SELECT SUM(purchase_quantity) FROM purchase_supplies ps WHERE ps.supply_id = s.supply_id), 0) -
  COALESCE((SELECT SUM(smi.quantity * ms.quantity)
            FROM sale_menu_items smi
            JOIN menu_item_supplies ms ON ms.menu_item_id = smi.menu_item_id
            WHERE ms.supply_id = s.supply_id), 0));
INSERT INTO employees(employee_id, first_name, last_name, password_hash, employee_role) VALUES (13, 'testM', 'Test', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'Manager'), (14, 'testC', 'Test', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'Cashier');
