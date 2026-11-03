"""
Purchase/inventory generation for the Phase 2 data generator.

Driven by the Phase 2 assignment prompt (full text in generate_csvs.py):
"Create inventory items for at least delta different menu items. Remember
that a given menu item will have multiple ingredients.
Single-use Supplies: You will also need other items such as cups, straws,
napkins, bags, and so on." Also "Number of servings: Take into account the
number of servings of consumable inventory items."
"""

import math
from datetime import timedelta
from random import Random

import config
from hardcoded_data import SUPPLIES, VENDOR_DELIVERY_DAYS


def _snap_back_to_delivery_day(d, vendor_id, floor):
    """Most recent delivery day in [floor, d] (vendor 5: first Monday of
    the month; opening inventory is delivered on setup day itself)."""
    if vendor_id == 5:
        probe = d
        while True:  # walk back to a first-of-month Monday
            first = probe.replace(day=1)
            while first.weekday() != 0:
                first += timedelta(days=1)
            if floor <= first <= d:
                return first
            if first <= floor:
                return floor  # opening stock arrives on setup day
            probe = (probe.replace(day=1) - timedelta(days=1))
    for _ in range(7):
        if d.weekday() in VENDOR_DELIVERY_DAYS[vendor_id]:
            return max(d, floor)
        d -= timedelta(days=1)
    return floor


def generate_purchases(consumption, seed):
    """Build purchase rows from the per-day consumption of the sales history.

    Returns (purchase_rows, purchase_supply_rows) where
      purchase_rows       = [(purchase_id, purchase_date, vendor_id)]
      purchase_supply_rows = [(purchase_supply_id, purchase_id, supply_id,
                                purchase_quantity)]
    """
    rng = Random(seed)
    start, end = config.INVENTORY_START_DATE, config.END_DATE

    total_consumed = {}
    for day_map in consumption.values():
        for sid, units in day_map.items():
            total_consumed[sid] = total_consumed.get(sid, 0) + units

    records = []  # (purchase_date, supply_id, quantity, vendor_id)

    for sid, _name, _category, vendor_id, cadence in SUPPLIES:
        if total_consumed.get(sid, 0) == 0:
            # Standing order for back-of-house / off-menu supplies.
            d = start
            while d <= end:
                records.append((_snap_back_to_delivery_day(d, vendor_id, start),
                                 sid, 300, vendor_id))
                d += timedelta(days=30)
            continue

        stock = 0
        d = start
        while d <= end:
            # How much will be consumed over the next `cadence` days?
            # (Anchor to the first sales day: the pre-sales week consumes
            # nothing, so a naive window would under-order at setup.)
            need = 0
            probe = max(d + timedelta(days=1), config.START_DATE)
            for _ in range(cadence):
                need += consumption.get(probe, {}).get(sid, 0)
                probe += timedelta(days=1)

            if stock < need * config.STOCK_THRESHOLD_FACTOR:
                qty = max(10, math.ceil(need * config.PURCHASE_COVER_BUFFER / 10) * 10)
                records.append((_snap_back_to_delivery_day(d, vendor_id, start),
                                sid, qty, vendor_id))
                stock += qty

            stock -= consumption.get(d, {}).get(sid, 0)
            if stock < 0:
                stock = 0  # covered by the threshold reorder logic
            d += timedelta(days=1)

    # Group same-day same-vendor supply purchases into delivery events.
    events = {}
    for pd, sid, qty, vendor_id in records:
        events.setdefault((pd, vendor_id), []).append((sid, qty))

    purchase_rows = []
    purchase_supply_rows = []
    line_id = 0
    for purchase_id, ((pd, vendor_id), lines) in enumerate(
            sorted(events.items(), key=lambda kv: (kv[0][0], kv[0][1])), 1):
        purchase_rows.append((purchase_id, pd, vendor_id))
        for sid, qty in sorted(lines, key=lambda l: l[0]):
            line_id += 1
            purchase_supply_rows.append(
                (line_id, purchase_id, sid, qty))

    return purchase_rows, purchase_supply_rows
