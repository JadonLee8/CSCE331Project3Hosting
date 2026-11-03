create table employees(
    employee_id int primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    password_hash varchar(255) not null,
    employee_role varchar(50) not null check (employee_role in ('Manager', 'Cashier')) -- cashier could be any employee that is not manager
);

create table supplies(
    supply_id int primary key,
    item_name varchar(255) not null,
    category varchar(50) not null,
    quantity int not null default 0
);

create table vendors(
    vendor_id int primary key,
    vendor_name varchar(255) not null,
    vendor_phone varchar(50),
    vendor_email varchar(255),
    delivery_info varchar(255)
);

create table purchases(
    purchase_id int primary key,
    purchase_date date not null,
    vendor_id int,
    constraint fk_vendor_id
        foreign key (vendor_id)
        references vendors (vendor_id)
);

create table purchase_supplies(
    purchase_supply_id int primary key,
    purchase_id int not null,
    supply_id int not null,
    purchase_quantity int not null,
    constraint fk_purchase_id
        foreign key (purchase_id)
        references purchases (purchase_id),
    constraint fk_supply_id
        foreign key (supply_id)
        references supplies (supply_id)
);

create table menu_items(
    menu_item_id int primary key,
    menu_item_name varchar(255),
    price decimal(10,2) not null,
    image_url varchar(255),
    season_start date,
    season_end date
);

create table sales(
    sale_id int primary key,
    sale_date timestamp not null,
    sale_price decimal(10,2) not null,
    sale_tip decimal(10,2) not null,
    sale_employee_id int not null,
    constraint fk_staff_id
        foreign key (sale_employee_id)
        references employees (employee_id)
);

create table menu_item_supplies(
    menu_item_id int not null,
    supply_id int not null,
    quantity int not null,
    primary key (menu_item_id, supply_id),
    constraint fk_mis_menu_item_id
        foreign key (menu_item_id)
        references menu_items (menu_item_id),
    constraint fk_mis_supply_id
        foreign key (supply_id)
        references supplies (supply_id)
);

create table sale_menu_items(
    sale_menu_item_id int generated always as identity primary key,
    sale_id int not null,
    menu_item_id int not null,
    quantity int not null,
    price_at_purchase decimal(10,2) not null,
    constraint fk_sale_id
        foreign key (sale_id)
        references sales (sale_id),
    constraint fk_menu_item_id
        foreign key (menu_item_id)
        references menu_items (menu_item_id)
);
