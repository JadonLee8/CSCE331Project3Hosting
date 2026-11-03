"""
Workload parameters for the Phase 2 data generator.

Driven by the Phase 2 assignment prompt (full text in generate_csvs.py):
"Create at least alpha weeks of sales history -- starting about one year ago
and ending about today -- ... in total have approximately beta million in
sales. Peak Days: Include phi peak(s) days ... Create inventory items for at
least delta different menu items." plus the Workload Balancing table
(team of 5: alpha=52, beta~$1.00M, phi=3, delta=20, epsilon=15, theta=4).
"""

import os
from datetime import date, timedelta

# ---------------------------------------------------------------- team size --
TEAM_SIZE = 5  # set to 3, 4, 5, or 6

WORKLOAD = {
    3: dict(weeks=26, sales_target=500_000.0,  peak_days=1, menu_items=12,
            queries=9,  special_queries=2),
    4: dict(weeks=39, sales_target=750_000.0,  peak_days=2, menu_items=16,
            queries=12, special_queries=3),
    5: dict(weeks=52, sales_target=1_000_000.0, peak_days=3, menu_items=20,
            queries=15, special_queries=4),
    6: dict(weeks=65, sales_target=1_250_000.0, peak_days=4, menu_items=24,
            queries=18, special_queries=5),
}

PARAMS = WORKLOAD[TEAM_SIZE]

# Fixed so every teammate generates identical CSVs; override with END_DATE env.
END_DATE = date.fromisoformat(os.environ.get("END_DATE", "2026-09-30"))
START_DATE = END_DATE - timedelta(weeks=PARAMS["weeks"])

INVENTORY_START_DATE = START_DATE - timedelta(days=7)

# TAMU-approximate academic calendar (drives seasonality).
FALL_2025_START = date(2025, 8, 25)   # fall 2025 semester (covers inventory start)
WINTER_BREAK_2526 = date(2025, 12, 13)   # winter break begins
SPRING_2026_START = date(2026, 1, 20)   # spring semester begins
SPRING_2026_END = date(2026, 5, 8)
SUMMER_2026_END = date(2026, 8, 25)
FALL_2026_START = date(2026, 8, 26)     # fall semester begins

IN_SESSION_WEIGHT = 1.00   # school in session
WINTER_WEIGHT = 0.35       # winter break
SUMMER_WEIGHT = 0.55       # summer

# Weekday weights, Monday .. Sunday (campus-adjacent shop: Fri/Sat busy,
# Sunday quiet).
WEEKDAY_WEIGHTS = (0.95, 0.92, 0.97, 1.02, 1.22, 1.05, 0.87)

# Store hours 11:00-22:00; orders taper toward close.
HOUR_WEIGHTS = {
    11: 0.55,  # 11am - open, slow
    12: 1.45,  # lunch rush
    13: 1.35,
    14: 1.05,
    15: 1.15,
    16: 1.30,  # afternoon rush
    17: 1.15,
    18: 0.95,
    19: 1.00,
    20: 0.60,
    21: 0.25,  # last orders before 10pm close
}

PEAK_CANDIDATES = [
    (date(2026, 1, 20), "Spring semester begins", 4.0),
    (date(2026, 8, 26), "Fall semester begins", 4.0),
    (date(2026, 4, 30), "National Bubble Tea Day", 3.5),
    (date(2025, 12, 31), "New Year's Eve", 3.0),
]

# Days after a peak keep a fraction of the boost (rush tapers off):
PEAK_DECAY = [(1, 0.4), (2, 0.2)]  # (offset_days, fraction of the boost kept)

PRICE_CHANGE_DATE = date(2026, 1, 1)
PRICE_INCREASE = 0.25

# ------------------------------------------------------------------ orders ---
ITEMS_PER_ORDER = [(1, 0.62), (2, 0.31), (3, 0.07)]  # (lines, probability)
EXTRA_UNIT_CHANCE = 0.15   # chance one line in the order is a double
PAYMENT_MIX = [("credit", 0.55), ("debit", 0.20), ("gift_card", 0.10),
               ("cash", 0.15)]
CARD_TIP_CHANCE = 0.45          # of credit/debit orders
CARD_TIP_RANGE = (0.10, 0.20)   # tip as a fraction of the subtotal
CASH_TIP_CHANCE = 0.12
CASH_TIP_RANGE = (0.50, 2.00)   # dollars

# Staff handling: chance a sale is rung up by someone other than a cashier.
SHIFT_LEAD_SALE_CHANCE = 0.04
MANAGER_SALE_CHANCE = 0.01

# Purchases are sized to cover upcoming consumption plus a waste/spoilage
# buffer (spills, spoilage).
PURCHASE_COVER_BUFFER = 1.15
STOCK_THRESHOLD_FACTOR = 1.10   # reorder when stock < this x upcoming need

# ------------------------------------------------------------------- misc ----
RANDOM_SEED = 331
CSV_DIR = "csv"
