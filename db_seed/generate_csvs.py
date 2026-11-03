r"""
Entry point: writes the CSVs in csv/ for \copy into the database.
Run with `uv run seeding/generate_csvs.py` from the repo root.

--- Prompts used to generate these scripts (pi session, 2026-09-25) ---------

[1] Project 2: Phase 2 Description (pasted from Canvas; page chrome removed):

Overview

The second phase of the project will consist of building the database by
creating the ordering history and inventory data and inserting the data into
the schema you designed in Phase 1.

Your goal will be to implement and verify the validity of your design.
You will screencast a demo of the database's functionality.

Requirements

Your database system will be evaluated using a series of SQL queries to
determine its correctness and proximity to the design document.

If you had to make changes to your database design, you will need to describe
and justify these changes during your demo.
Be sure to keep your design documents up to date.

Data

You will create data to be stored in your database:

Create at least alpha weeks of sales history -- starting about one year ago
and ending about today -- to store in your database that in total have
approximately beta million in sales.
Peak Days: Include phi peak(s) days where sales are significantly higher,
which typically occur at the start of the regular semester. You might also
consider peak days like special holidays or large group events.
Create inventory items for at least delta different menu items. Remember
that a given menu item will have multiple ingredients.
Single-use Supplies: You will also need other items such as cups, straws,
napkins, bags, and so on.
Drink Toppings: Since the domain is for a bubble tea vendor, you will also
need to include bubble tea-appropriate toppings.
You are strongly encouraged to perform the following tasks in order to more
effectively import your auto-generated data into your database:

Numerical Data: Use scripting (e.g., Python) to generate your numerical data.
Non-numerical Data: Hardcode your non-numerical data (e.g., menu items,
non-menu items, employee personnel) to populate with your numerical data.

Queries

You will also create at least epsilon SQL queries that can be run as an
input file to verify the low-level design and interactions in your
database, but you are encouraged to build additional SQL queries for extra
practice.

These queries should have some examples of a desired question that can be
answered through this query.
They should also demonstrate that your database has been correctly populated
and you have supplied the additional data as requested above.
You will submit this query list on Canvas and demo these queries in lab.

Special Queries

Every team must include the first theta special queries which will be used to
verify the seeding of the database:

Special Query #1: "Weekly Sales History"
pseudocode: select count of orders grouped by week
about: given a specific week, how many orders were placed?
example: "week 1 has 98765 orders"
Special Query #2: "Peak Sales Day"
pseudocode: select top 10 sums of order total grouped by day in descending
order by order total
about: given a specific day, what was the sum of the top 10 order totals?
example: "30 August has $12345 of top sales"
Special Query #3: "Realistic Sales History"
pseudocode: select count of orders, sum of order total grouped by hour
about: given a specific hour of the day, how many orders were placed and what
was the total sum of the orders?
example: e.g., "12pm has 12345 orders totaling $86753"
Special Query #4: "Menu Item Inventory"
pseudocode: select count of inventory items from inventory and menu grouped
by menu item
about: given a specific menu item, how many items from the inventory does
that menu item use?
example: "classic milk tea uses 12 items"
Special Query #5: "Best of the Worst"
pseudocode: select bottom sum of order total, top count of menu items by day
grouped by week
about: given a specific week, what day had the lowest sales, what were the
sales numbers, and what was the top seller that day?
example: "12 December has lowest sales of $4321 for week 18 with match milk
tea as top seller"
These theta special queries count towards the requirement of the minimum
epsilon required SQL queries (i.e., teams must have at least
(epsilon - theta) more queries).

Workload Balancing

SYMBOL  TEAM OF 3  TEAM OF 4  TEAM OF 5  TEAM OF 6  DESCRIPTION
alpha       26         39         52         65  Number of weeks.
beta    ~$500K     ~$750K    ~$1.00M    ~$1.25M  Amount of sales.
phi         1          2          3          4  Number of peak days.
delta       12         16         20         24  Number of menu items.
epsilon      9         12         15         18  Number of required queries.
theta       2          3          4          5  First nth special queries.

Important Additional Considerations

Temporal data: Take into account temporal-related data such as:
time of orders
price of item when purchased
Data structure: Use tables instead of lists in your database.
Number of servings: Take into account the number of servings of consumable
inventory items.

Deliverables

In this phase, you will:

Populate and verify your database system with provided data.
Demo in Lab your populated database correctness, justifying any changes made
to the database design.
Submit in Canvas a TAMU GitHub release link of your demoed code.
You can find the requirement details for each of these deliverables in the
Canvas assignments.

(The Greek letters in the assignment are alpha/beta/phi/delta/epsilon/theta;
TEAM_SIZE = 5 maps to alpha=52, beta~$1.00M, phi=3, delta=20, epsilon=15,
theta=4 -- see config.py.)

[2] "Write me some scripts where we can generate these CSV's in Python"

[3] "Please reference @~/code/school/CSCE331/Project2/csce331-GUI/ for the
databse specifications"

[4] "Continue"

[5] "Can you add the necessary scripts to
~/code/school/CSCE331/Project2/project2-squad44-dunsindonuts/ ?"
---------------------------------------------------------------------------
"""

import csv
import os
from collections import Counter, defaultdict
from datetime import date

import config
from hardcoded_data import (EMPLOYEE_CSV_ROWS, MENU_ITEM_CSV_ROWS,
                             MENU_ITEM_SUPPLIES_ROWS, MENU_ITEMS, RECIPES,
                             SUPPLIES, SUPPLY_CSV_ROWS, VENDORS)
from inventory import generate_purchases
from sales_history import generate_orders

CSV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       config.CSV_DIR)

# (filename, import order) - parents before children for the FKs.
TABLES = ["employees", "vendors", "supplies", "menu_items",
          "menu_item_supplies", "sales", "sale_menu_items",
          "purchases", "purchase_supplies"]


def write_csv(filename, header, rows):
    path = os.path.join(CSV_DIR, filename)
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def calibrate_sales(target):
    """Find base_rate so the generated history lands within 0.5% of target.

    generate_orders(base_rate) scales linearly, so a few passes converge fast.
    The seed stays fixed across passes.
    """
    base_rate = 1.0
    for _ in range(6):
        sales, lines, consumption, peaks = generate_orders(base_rate, config.RANDOM_SEED)
        revenue = sum(s[2] for s in sales)
        if abs(revenue - target) <= target * 0.005:
            break
        base_rate *= target / revenue
    return sales, lines, consumption, peaks, base_rate


def fmt_money(x):
    return f"${x:,.2f}"


def main():
    p = config.PARAMS
    print(f"Team size            : {config.TEAM_SIZE}")
    print(f"Workload (alpha,beta,phi,delta) = "
          f"({p['weeks']} weeks, {fmt_money(p['sales_target'])}, "
          f"{p['peak_days']} peaks, {p['menu_items']}+ menu items)")

    sales, lines, consumption, peaks, base_rate = calibrate_sales(p["sales_target"])
    purchases, purchase_supplies = generate_purchases(consumption, config.RANDOM_SEED)

    revenue = sum(s[2] for s in sales)
    tips = sum(s[3] for s in sales)

    os.makedirs(CSV_DIR, exist_ok=True)
    counts = {
        "employees.csv": write_csv(
            "employees.csv",
            ["employee_id", "first_name", "last_name", "password_hash", "employee_role"],
            EMPLOYEE_CSV_ROWS),
        "vendors.csv": write_csv(
            "vendors.csv",
            ["vendor_id", "vendor_name", "vendor_phone", "vendor_email", "delivery_info"],
            VENDORS),
        "supplies.csv": write_csv(
            "supplies.csv",
            ["supply_id", "item_name", "category"],
            SUPPLY_CSV_ROWS),
        "menu_items.csv": write_csv(
            "menu_items.csv",
            ["menu_item_id", "menu_item_name", "price", "image_url"],
            MENU_ITEM_CSV_ROWS),
        "menu_item_supplies.csv": write_csv(
            "menu_item_supplies.csv",
            ["menu_item_id", "supply_id", "quantity"],
            MENU_ITEM_SUPPLIES_ROWS),
        "sales.csv": write_csv(
            "sales.csv",
            ["sale_id", "sale_date", "sale_price", "sale_tip", "sale_employee_id"],
            [(s[0], s[1], f"{s[2]:.2f}", f"{s[3]:.2f}", s[5]) for s in sales]),
        "sale_menu_items.csv": write_csv(
            "sale_menu_items.csv",
            # sale_menu_item_id is generated by the database (identity column)
            ["sale_id", "menu_item_id", "quantity", "price_at_purchase"],
            [(l[0], l[1], l[2], f"{l[3]:.2f}") for l in lines]),
        "purchases.csv": write_csv(
            "purchases.csv",
            ["purchase_id", "purchase_date", "vendor_id"],
            [(r[0], r[1].isoformat(), r[2]) for r in purchases]),
        "purchase_supplies.csv": write_csv(
            "purchase_supplies.csv",
            ["purchase_supply_id", "purchase_id", "supply_id",
             "purchase_quantity"],
            purchase_supplies),
    }

    # --- verification summary ------------------------------------------------
    days = (config.END_DATE - config.START_DATE).days + 1
    orders_by_day, revenue_by_day = Counter(), defaultdict(float)
    for s in sales:
        day = date.fromisoformat(s[1][:10])
        orders_by_day[day] += 1
        revenue_by_day[day] += s[2]

    print(f"\nSales window         : {config.START_DATE} .. {config.END_DATE} "
          f"({days / 7:.0f} weeks)")
    print(f"Orders               : {len(sales):,} (avg {len(sales) / days:.0f}/day, "
          f"base rate {base_rate:.1f}/in-session day)")
    print(f"Item revenue         : {fmt_money(revenue)} (target {fmt_money(p['sales_target'])})")
    print(f"Tips                 : {fmt_money(tips)} "
          f"(total collected {fmt_money(revenue + tips)})")

    print(f"\nPeak days ({len(peaks)}/{p['peak_days']}):")
    for peak_date, name, m in peaks:
        print(f"  {peak_date}  {name:<28} {m}x  "
              f"{orders_by_day[peak_date]:,} orders  {fmt_money(revenue_by_day[peak_date])}")
    if len(peaks) < p["peak_days"]:
        print("  WARNING: not enough peak candidates inside the window!")

    busiest = orders_by_day.most_common(1)[0]
    print(f"Busiest day          : {busiest[0]} ({busiest[1]:,} orders)")

    print(f"\nFiles written to {CSV_DIR}:")
    for name, n in counts.items():
        print(f"  {name:<24} {n:>7,} rows")

    avg_recipe = sum(len(r) for r in RECIPES.values()) / len(RECIPES)
    print(f"\nCatalog: {len(MENU_ITEMS)} menu items (avg {avg_recipe:.1f} supplies each), "
          f"{len(SUPPLIES)} supplies, {len(VENDORS)} vendors, "
          f"{len(EMPLOYEE_CSV_ROWS)} employees")

    print("\nLoad order (FK dependencies):")
    print("  " + " -> ".join(TABLES))
    print("  (load with seed.sql, see README.md)")


if __name__ == "__main__":
    main()
