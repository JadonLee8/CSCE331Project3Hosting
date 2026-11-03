DROP TABLE IF EXISTS sale_menu_items,
sales,
employees,
menu_item_supplies,
menu_items,
purchase_supplies,
purchases,
supplies,
vendors CASCADE;
\i seeding/schema.sql
\i seeding/seed.sql
