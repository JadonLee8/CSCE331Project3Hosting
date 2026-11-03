"""
Hardcoded non-numerical data for the Phase 2 data generator.

Driven by the Phase 2 assignment prompt (full text in generate_csvs.py):
"Non-numerical Data: Hardcode your non-numerical data (e.g., menu items,
non-menu items, employee personnel) to populate with your numerical data."
Also: "Drink Toppings: Since the domain is for a bubble tea vendor, you will
also need to include bubble tea-appropriate toppings."
"""

import hashlib


# --------------------------------------------------------------- employees --
def _hash(first, last):
    """Deterministic placeholder password hash. Scheme (for the GUI demo):
    sha256("<first>.<last>-331"), e.g. sha256("dana.whitfield-331")."""
    return hashlib.sha256(f"{first.lower()}.{last.lower()}-331".encode()).hexdigest()


# (employee_id, first_name, last_name, role, shift)
# shift "A" = opening shift (11:00-15:59), "B" = evening (16:00-close),
# "all" = full-day shift (manager / shift lead).
# If the team already has an employees.csv elsewhere, put that roster here
# instead - sales.sale_employee_id must reference this table.
EMPLOYEES = [
    (1, "Dana", "Whitfield", "Manager", "all"),
    (2, "Marcus", "Chen", "Shift Lead", "all"),
    (3, "Priya", "Raghavan", "Shift Lead", "all"),
    (4, "Jonah", "Reyes", "Cashier", "A"),
    (5, "Amara", "Osei", "Cashier", "A"),
    (6, "Ellie", "Tran", "Cashier", "A"),
    (7, "Diego", "Fuentes", "Cashier", "A"),
    (8, "Nia", "Coleman", "Cashier", "A"),
    (9, "Owen", "Barrett", "Cashier", "B"),
    (10, "Sofia", "Petrov", "Cashier", "B"),
    (11, "Caleb", "Mensah", "Cashier", "B"),
    (12, "Ruby", "Nakamura", "Cashier", "B"),
]

EMPLOYEE_CSV_ROWS = [
    # DB roles are only Manager/Cashier; shift leads are stored as Cashier
    (e[0], e[1], e[2], _hash(e[1], e[2]),
     "Cashier" if e[3] == "Shift Lead" else e[3]) for e in EMPLOYEES
]


# ----------------------------------------------------------------- vendors --
# (vendor_id, vendor_name, vendor_phone, vendor_email, delivery_info)
VENDORS = [
    (1, "Lone Star Tea Imports", "(979) 555-0114",
     "orders@lonestartea.example.com", "Weekly delivery, Tuesdays"),
    (2, "Gulf Coast Dairy & Creamer Co.", "(979) 555-0173",
     "sales@gulfcoastdairy.example.com", "Twice weekly, Mon/Thu"),
    (3, "Boba Bros Wholesale", "(713) 555-0286",
     "wholesale@bobabros.example.com", "Weekly delivery, Wednesdays"),
    (4, "EcoSip Packaging Supply", "(979) 555-0411",
     "orders@ecosip.example.com", "Biweekly delivery, Fridays"),
    (5, "Sweet Syrup Solutions", "(281) 555-0399",
     "supply@sweetsyrup.example.com", "Monthly delivery, first Monday"),
]

# Weekday(s) each vendor delivers (Monday=0 .. Sunday=6) - used to snap
# purchase dates onto realistic delivery days.
VENDOR_DELIVERY_DAYS = {1: (1,), 2: (0, 3), 3: (2,), 4: (4,)}


# ---------------------------------------------------------------- supplies --
# (supply_id, item_name, category, vendor_id, restock_cadence_days)
# category: tea_base | powder | dairy | sweetener | fruit_syrup | topping | single_use
SUPPLIES = [
    # --- tea bases (dry leaves; vendor 1) ---
    (1, "Assam Black Tea Leaves", "tea_base", 1, 30),
    (2, "Oolong Tea Leaves", "tea_base", 1, 30),
    (3, "Jasmine Green Tea Leaves", "tea_base", 1, 30),
    (4, "Green Tea Leaves", "tea_base", 1, 30),
    (5, "Earl Grey Tea Leaves", "tea_base", 1, 30),
    (6, "Thai Tea Mix", "tea_base", 1, 30),
    # --- powders (vendor 5) ---
    (7, "Taro Powder", "powder", 5, 30),
    (8, "Matcha Green Tea Powder", "powder", 5, 30),
    (9, "Cocoa Powder", "powder", 5, 30),
    (10, "Hokkaido Creamer Powder", "powder", 5, 30),
    (11, "Non-Dairy Creamer", "powder", 2, 30),
    (12, "Cheese Foam Powder", "powder", 5, 30),
    # --- dairy / liquids ---
    (13, "Whole Milk", "dairy", 2, 7),
    (14, "Brown Sugar Syrup", "sweetener", 5, 30),
    (15, "Cane Sugar Syrup", "sweetener", 5, 30),
    (16, "Honey", "sweetener", 5, 30),
    # --- fruit syrups & purees (vendor 5) ---
    (17, "Mango Syrup", "fruit_syrup", 5, 30),
    (18, "Lychee Syrup", "fruit_syrup", 5, 30),
    (19, "Strawberry Puree", "fruit_syrup", 5, 30),
    (20, "Passionfruit Syrup", "fruit_syrup", 5, 30),
    (21, "Grapefruit Syrup", "fruit_syrup", 5, 30),
    (22, "Honeydew Syrup", "fruit_syrup", 5, 30),
    (23, "Winter Melon Syrup", "fruit_syrup", 5, 30),
    (24, "Peach Syrup", "fruit_syrup", 5, 30),
    # --- drink toppings (vendor 3) ---
    (25, "Classic Tapioca Pearls (Boba)", "topping", 3, 14),
    (26, "Brown Sugar Tapioca Pearls", "topping", 3, 14),
    (27, "Mango Popping Boba", "topping", 3, 14),
    (28, "Strawberry Popping Boba", "topping", 3, 14),
    (29, "Lychee Jelly", "topping", 3, 14),
    (30, "Grass Jelly", "topping", 3, 14),
    (31, "Coffee Jelly", "topping", 3, 14),
    (32, "Egg Pudding", "topping", 3, 14),
    (33, "Red Bean", "topping", 3, 14),
    (34, "Aloe Vera", "topping", 3, 14),
    (35, "Oreo Cookie Crumbs", "topping", 3, 14),
    # --- single-use supplies (vendor 4) ---
    (36, "16 oz Polypropylene Cups", "single_use", 4, 14),
    (37, "22 oz Polypropylene Cups", "single_use", 4, 14),
    (38, "Flat Lids (16 oz)", "single_use", 4, 14),
    (39, "Dome Lids (22 oz)", "single_use", 4, 14),
    (40, "Cup Sealing Film", "single_use", 4, 14),
    (41, "Wide Boba Straws", "single_use", 4, 14),
    (42, "Regular Straws", "single_use", 4, 14),
    (43, "Napkins", "single_use", 4, 14),
    (44, "Paper Carrier Bags", "single_use", 4, 14),
    (45, "Food-Grade Gloves", "single_use", 4, 30),
]

SUPPLY_CSV_ROWS = [(s[0], s[1], s[2]) for s in SUPPLIES]


# -------------------------------------------------------------- menu items --
# Supply ID shorthand for the recipes below.
(ASSAM, OOLONG, JASMINE_TEA, GREEN_TEA, EARL_GREY, THAI_TEA) = (1, 2, 3, 4, 5, 6)
(TARO_PWD, MATCHA_PWD, COCOA_PWD, HOKKAIDO_PWD, CREAMER, CHEESEFOAM_PWD) = (7, 8, 9, 10, 11, 12)
(MILK, BROWN_SUGAR, CANE_SYRUP, HONEY) = (13, 14, 15, 16)
(MANGO_SYRUP, LYCHEE_SYRUP, STRAWBERRY_PUREE, PASSIONFRUIT_SYRUP,
 GRAPEFRUIT_SYRUP, HONEYDEW_SYRUP, WINTERMELON_SYRUP, PEACH_SYRUP) = (17, 18, 19, 20, 21, 22, 23, 24)
(BOBA, BS_BOBA, MANGO_POP, STRAWBERRY_POP, LYCHEE_JELLY, GRASS_JELLY,
 COFFEE_JELLY, EGG_PUDDING, RED_BEAN, ALOE, OREO) = (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35)
(CUP16, CUP22, FLAT_LID, DOME_LID, SEALING_FILM, BOBA_STRAW, REG_STRAW,
 NAPKIN, BAG, GLOVES) = (36, 37, 38, 39, 40, 41, 42, 43, 44, 45)

# (menu_item_id, menu_item_name, price, image_url)
# image_url = direct image file for each source page in img/menu/CREDITS.md.
# IDs 1-24 and prices mirror menu_seed.sql exactly - keep in sync.
# price = the CURRENT menu price; historical charged prices are derived from
# it by sales_history.price_at (they were PRICE_INCREASE lower before
# config.PRICE_CHANGE_DATE).
MENU_ITEMS = [
    (1, "Brown Sugar Boba Milk", 5.75,
     "https://live.staticflickr.com/65535/52253683954_db5da3d6d8_b.jpg"),
    (2, "Chocolate Milk Tea", 5.25,
     "https://live.staticflickr.com/7098/7281244558_65df00abed_b.jpg"),
    (3, "Classic Pearl Milk Tea", 5.25,
     "https://live.staticflickr.com/2653/4000461186_aa159096b3_b.jpg"),
    (4, "Cookies & Cream Milk Tea", 5.75,
     "https://live.staticflickr.com/6038/6390616297_6d5bc41757_z.jpg"),
    (5, "Grapefruit Green Tea", 5.25,
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Grapefruit_Tea_1_2019-10-12.jpg/960px-Grapefruit_Tea_1_2019-10-12.jpg"),
    (6, "Hokkaido Milk Tea", 5.75,
     "https://live.staticflickr.com/3481/3892617380_283ce19770_b.jpg"),
    (7, "Honey Earl Grey Milk Tea", 5.75,
     "https://live.staticflickr.com/4014/4568009448_4e5253ba0a_b.jpg"),
    (8, "Honeydew Milk Tea", 5.25,
     "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/BubbleTeaHoneydewMapleStreet20July2008.jpg/960px-BubbleTeaHoneydewMapleStreet20July2008.jpg"),
    (9, "Jasmine Milk Tea", 5.25,
     "https://live.staticflickr.com/7334/8726115061_729f11d5ae_z.jpg"),
    (10, "Lychee Green Tea", 5.25,
     "https://live.staticflickr.com/8490/8281726583_02c58572e9_b.jpg"),
    (11, "Mango Green Tea", 5.25,
     "https://live.staticflickr.com/7030/6729845499_6d92590021_b.jpg"),
    (12, "Mango Milk Tea", 5.25,
     "https://live.staticflickr.com/1138/1153763213_737578bc1f_b.jpg"),
    (13, "Matcha Cheese Foam Tea", 6.25,
     "https://live.staticflickr.com/65535/54520707640_aefb05bc42_b.jpg"),
    (14, "Matcha Milk Tea", 5.75,
     "https://live.staticflickr.com/552/31378506724_80d9e2d4c4_b.jpg"),
    (15, "Oolong Milk Tea", 5.25,
     "https://live.staticflickr.com/2918/14130060306_06d9f85741_z.jpg"),
    (16, "Passionfruit Green Tea", 5.25,
     "https://live.staticflickr.com/2936/14203087184_6cea0cee9b_b.jpg"),
    (17, "Peach Green Tea", 5.25,
     "https://live.staticflickr.com/4330/36285239046_3b127ff160_b.jpg"),
    (18, "QQ Happy Family Milk Tea", 6.25,
     "https://live.staticflickr.com/1370/626245963_45390ac8ea_b.jpg"),
    (19, "Strawberry Green Tea", 5.25,
     "https://live.staticflickr.com/7202/6940033043_26b146c919_b.jpg"),
    (20, "Strawberry Matcha Latte", 6.25,
     "https://live.staticflickr.com/65535/54520354151_f4ef8a9dc5_b.jpg"),
    (21, "Taro Milk Tea", 5.75,
     "https://live.staticflickr.com/5171/5460596042_5b23fec1f3_z.jpg"),
    (22, "Thai Milk Tea", 5.75,
     "https://live.staticflickr.com/6125/6005706023_380f58a067_b.jpg"),
    (23, "Thai Tea Boba Supreme", 6.25,
     "https://live.staticflickr.com/2659/4103465807_44931f1115_z.jpg"),
    (24, "Winter Melon Tea", 5.25,
     "https://live.staticflickr.com/7086/7156838856_9532b96f5d_b.jpg"),
]

MENU_ITEM_CSV_ROWS = [
    (m[0], m[1], f"{m[2]:.2f}", m[3]) for m in MENU_ITEMS
]


# --------------------------------------------------------- recipe mapping ---
# menu_item_id -> [(supply_id, servings consumed per drink ordered), ...]
# Every drink uses one cup + film/lid + straw + napkin; specials also use a
# carrier bag. Drinks with pearls/jelly get the wide boba straw.
RECIPES = {
    1: [(ASSAM, 1), (MILK, 1), (BROWN_SUGAR, 1), (BS_BOBA, 1),
        (CUP22, 1), (SEALING_FILM, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    2: [(ASSAM, 1), (COCOA_PWD, 1), (MILK, 1), (CANE_SYRUP, 1),
        (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    3: [(ASSAM, 1), (CREAMER, 1), (CANE_SYRUP, 1), (BOBA, 1),
        (CUP22, 1), (SEALING_FILM, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    4: [(ASSAM, 1), (COCOA_PWD, 1), (MILK, 1), (CANE_SYRUP, 1), (OREO, 1), (BOBA, 1),
        (CUP22, 1), (DOME_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1), (BAG, 1)],
    5: [(GREEN_TEA, 1), (GRAPEFRUIT_SYRUP, 1), (CANE_SYRUP, 1),
        (CUP16, 1), (FLAT_LID, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    6: [(OOLONG, 1), (HOKKAIDO_PWD, 1), (MILK, 1), (CANE_SYRUP, 1),
        (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    7: [(EARL_GREY, 1), (HONEY, 1), (MILK, 1),
        (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    8: [(GREEN_TEA, 1), (HONEYDEW_SYRUP, 1), (MILK, 1), (CANE_SYRUP, 1),
        (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    9: [(JASMINE_TEA, 1), (CREAMER, 1), (CANE_SYRUP, 1),
        (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    10: [(GREEN_TEA, 1), (LYCHEE_SYRUP, 1), (CANE_SYRUP, 1), (LYCHEE_JELLY, 1),
         (CUP16, 1), (FLAT_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    11: [(GREEN_TEA, 1), (MANGO_SYRUP, 1), (CANE_SYRUP, 1), (MANGO_POP, 1),
         (CUP16, 1), (FLAT_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    12: [(GREEN_TEA, 1), (MANGO_SYRUP, 1), (MILK, 1), (CANE_SYRUP, 1), (MANGO_POP, 1),
         (CUP22, 1), (SEALING_FILM, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    13: [(GREEN_TEA, 1), (MATCHA_PWD, 1), (CHEESEFOAM_PWD, 1), (MILK, 1), (BS_BOBA, 1),
         (CUP22, 1), (DOME_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1), (BAG, 1)],
    14: [(GREEN_TEA, 1), (MATCHA_PWD, 1), (MILK, 1), (CANE_SYRUP, 1),
         (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    15: [(OOLONG, 1), (MILK, 1), (CANE_SYRUP, 1),
         (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    16: [(GREEN_TEA, 1), (PASSIONFRUIT_SYRUP, 1), (CANE_SYRUP, 1), (ALOE, 1),
         (CUP16, 1), (FLAT_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    17: [(GREEN_TEA, 1), (PEACH_SYRUP, 1), (CANE_SYRUP, 1), (ALOE, 1),
         (CUP16, 1), (FLAT_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    18: [(ASSAM, 1), (CREAMER, 1), (CANE_SYRUP, 1), (BOBA, 1), (EGG_PUDDING, 1),
         (LYCHEE_JELLY, 1), (CUP22, 1), (DOME_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1),
         (BAG, 1)],
    19: [(GREEN_TEA, 1), (STRAWBERRY_PUREE, 1), (CANE_SYRUP, 1), (STRAWBERRY_POP, 1),
         (CUP16, 1), (FLAT_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
    20: [(GREEN_TEA, 1), (MATCHA_PWD, 1), (STRAWBERRY_PUREE, 1), (MILK, 1),
         (CANE_SYRUP, 1), (STRAWBERRY_POP, 1), (CUP22, 1), (DOME_LID, 1),
         (BOBA_STRAW, 1), (NAPKIN, 1), (BAG, 1)],
    21: [(ASSAM, 1), (TARO_PWD, 1), (MILK, 1), (CANE_SYRUP, 1),
         (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    22: [(THAI_TEA, 1), (CREAMER, 1), (CANE_SYRUP, 1),
         (CUP22, 1), (SEALING_FILM, 1), (REG_STRAW, 1), (NAPKIN, 1)],
    23: [(THAI_TEA, 1), (CREAMER, 1), (CANE_SYRUP, 1), (BOBA, 1), (EGG_PUDDING, 1),
         (CUP22, 1), (DOME_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1), (BAG, 1)],
    24: [(OOLONG, 1), (WINTERMELON_SYRUP, 1), (GRASS_JELLY, 1), (RED_BEAN, 1),
         (CUP16, 1), (FLAT_LID, 1), (BOBA_STRAW, 1), (NAPKIN, 1)],
}

MENU_ITEM_SUPPLIES_ROWS = [
    (mid, sid, servings)
    for mid, recipe in RECIPES.items()
    for (sid, servings) in recipe
]

# Relative popularity of each menu item (drives the item mix in orders).
POPULARITY = {
    1: 11,   # Brown Sugar Boba Milk
    2: 4,    # Chocolate Milk Tea
    3: 12,   # Classic Pearl Milk Tea
    4: 3,    # Cookies & Cream Milk Tea
    5: 4,    # Grapefruit Green Tea
    6: 4,    # Hokkaido Milk Tea
    7: 3,    # Honey Earl Grey Milk Tea
    8: 3,    # Honeydew Milk Tea
    9: 6,    # Jasmine Milk Tea
    10: 6,   # Lychee Green Tea
    11: 5,   # Mango Green Tea
    12: 5,   # Mango Milk Tea
    13: 3,   # Matcha Cheese Foam Tea
    14: 7,   # Matcha Milk Tea
    15: 5,   # Oolong Milk Tea
    16: 5,   # Passionfruit Green Tea
    17: 4,   # Peach Green Tea
    18: 5,   # QQ Happy Family Milk Tea
    19: 6,   # Strawberry Green Tea
    20: 3,   # Strawberry Matcha Latte
    21: 9,   # Taro Milk Tea
    22: 5,   # Thai Milk Tea
    23: 4,   # Thai Tea Boba Supreme
    24: 4,   # Winter Melon Tea
}
