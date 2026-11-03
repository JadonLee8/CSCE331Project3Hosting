"""
Sales history generation for the Phase 2 data generator.

Driven by the Phase 2 assignment prompt (full text in generate_csvs.py):
"Numerical Data: Use scripting (e.g., Python) to generate your numerical
data." and "Create at least alpha weeks of sales history -- starting about
one year ago and ending about today -- ... approximately beta million in
sales. Peak Days: Include phi peak(s) days where sales are significantly
higher ..." plus the temporal considerations (time of orders, price of item
when purchased).

Numerical data generation: the sales history (Phase 2 requirement:
"Use scripting (e.g., Python) to generate your numerical data").

Produces, for every day in [START_DATE, END_DATE]:
  * a realistic number of orders - TAMU session calendar seasonality,
    weekday pattern, and phi peak days (semester starts / Bubble Tea Day)
    with a two-day decay
  * realistic order times within store hours (lunch + afternoon rushes)
  * 1-3 menu items per order, sampled by popularity
  * sale_price (items subtotal) and sale_tip, per payment type
  * price_at_purchase per order line (prices were $0.25 lower before
    Jan 1, 2026)
  * per-day per-supply consumption, derived from the recipes, which the
    inventory generator uses to schedule purchases

`generate_orders()` is deterministic for a given (base_rate, seed).
"""

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from random import Random

import config
from hardcoded_data import EMPLOYEES, MENU_ITEMS, POPULARITY, RECIPES

_MENU_IDS = [m[0] for m in MENU_ITEMS]
_MENU_PRICES = {m[0]: float(m[2]) for m in MENU_ITEMS}
_MENU_POP = [POPULARITY[mid] for mid in _MENU_IDS]

_OPENERS = [e[0] for e in EMPLOYEES if e[4] == "A"]    # shift A cashiers
_EVENING = [e[0] for e in EMPLOYEES if e[4] == "B"]    # shift B cashiers
_LEADS = [e[0] for e in EMPLOYEES if e[3] == "Shift Lead"]
_MANAGER = [e[0] for e in EMPLOYEES if e[3] == "Manager"][0]


def season_weight(d):
    """Traffic multiplier by TAMU academic calendar."""
    if d < config.FALL_2025_START:
        return config.SUMMER_WEIGHT       # (covers team-of-6's summer 2025)
    if d < config.WINTER_BREAK_2526:
        return config.IN_SESSION_WEIGHT    # fall 2025 in session
    if d < config.SPRING_2026_START:
        return config.WINTER_WEIGHT        # winter break
    if d <= config.SPRING_2026_END:
        return config.IN_SESSION_WEIGHT    # spring 2026
    if d <= config.SUMMER_2026_END:
        return config.SUMMER_WEIGHT        # summer 2026
    return config.IN_SESSION_WEIGHT        # fall 2026


def chosen_peaks():
    """First `peak_days` candidates inside the sales window."""
    picked = [p for p in config.PEAK_CANDIDATES
              if config.START_DATE <= p[0] <= config.END_DATE]
    return picked[:config.PARAMS["peak_days"]]


def peak_multipliers(peaks):
    """date -> extra traffic multiplier (peaks + two-day decay)."""
    mult = {}
    for peak_date, _name, m in peaks:
        mult[peak_date] = mult.get(peak_date, 1.0) * m
        for offset, keep in config.PEAK_DECAY:
            d = peak_date + timedelta(days=offset)
            mult[d] = mult.get(d, 1.0) * (1.0 + (m - 1.0) * keep)
    return mult


def price_at(menu_id, d):
    """Menu price charged on date d. menu_items.price is the CURRENT price;
    before the Jan 2026 increase everything was $0.25 cheaper."""
    base = _MENU_PRICES[menu_id]
    return base - (config.PRICE_INCREASE if d < config.PRICE_CHANGE_DATE else 0.0)


def _order_time(rng, d):
    hour = rng.choices(list(config.HOUR_WEIGHTS),
                       weights=list(config.HOUR_WEIGHTS.values()))[0]
    return datetime(d.year, d.month, d.day, hour, rng.randint(0, 59), rng.randint(0, 59))


def _pick_employee(rng, hour):
    r = rng.random()
    if r < config.MANAGER_SALE_CHANCE:
        return _MANAGER
    if r < config.MANAGER_SALE_CHANCE + config.SHIFT_LEAD_SALE_CHANCE:
        return rng.choice(_LEADS)
    return rng.choice(_OPENERS if hour <= 15 else _EVENING)


def _pick_payment(rng):
    kinds, weights = zip(*config.PAYMENT_MIX)
    return rng.choices(kinds, weights=weights)[0]


def _tip(rng, payment, subtotal):
    if payment in ("credit", "debit") and rng.random() < config.CARD_TIP_CHANCE:
        raw = subtotal * rng.uniform(*config.CARD_TIP_RANGE)
    elif payment == "cash" and rng.random() < config.CASH_TIP_CHANCE:
        raw = rng.uniform(*config.CASH_TIP_RANGE)
    else:
        return 0.0
    return round(round(raw * 4) / 4, 2)  # round to the nearest quarter


def generate_orders(base_rate, seed):
    """Generate the full sales history.

    Returns (sales_rows, line_rows, consumption, peaks) where
      sales_rows  = [(sale_id, sale_date 'YYYY-MM-DD HH:MM:SS', sale_price,
                      sale_tip, payment_type, sale_employee_id)]
      line_rows   = [(sale_id, menu_item_id, quantity, price_at_purchase)]
      consumption = {date: {supply_id: units consumed that day}}
    """
    rng = Random(seed)
    start, end = config.START_DATE, config.END_DATE
    peaks = chosen_peaks()
    mult = peak_multipliers(peaks)

    line_counts, line_probs = zip(*config.ITEMS_PER_ORDER)
    sales_rows, line_rows = [], []
    consumption = defaultdict(Counter)

    sale_id = 0
    d = start
    while d <= end:
        weight = (season_weight(d)
                  * config.WEEKDAY_WEIGHTS[d.weekday()]
                  * mult.get(d, 1.0))
        count = max(0, round(base_rate * weight * rng.gauss(1.0, 0.08)))
        for _ in range(count):
            sale_id += 1
            dt = _order_time(rng, d)
            emp = _pick_employee(rng, dt.hour)
            payment = _pick_payment(rng)

            n_lines = rng.choices(line_counts, weights=line_probs)[0]
            picked = rng.choices(_MENU_IDS, weights=_MENU_POP, k=n_lines)
            items = Counter(picked)
            if rng.random() < config.EXTRA_UNIT_CHANCE:
                items[next(iter(items))] += 1

            subtotal = 0.0
            for menu_id, qty in items.items():
                unit_price = price_at(menu_id, d)
                subtotal += qty * unit_price
                line_rows.append((sale_id, menu_id, qty, round(unit_price, 2)))
                for supply_id, servings in RECIPES[menu_id]:
                    consumption[d][supply_id] += servings * qty

            subtotal = round(subtotal, 2)
            sales_rows.append((sale_id, dt.strftime("%Y-%m-%d %H:%M:%S"),
                               subtotal, _tip(rng, payment, subtotal), payment, emp))
        d += timedelta(days=1)

    return sales_rows, line_rows, consumption, peaks
