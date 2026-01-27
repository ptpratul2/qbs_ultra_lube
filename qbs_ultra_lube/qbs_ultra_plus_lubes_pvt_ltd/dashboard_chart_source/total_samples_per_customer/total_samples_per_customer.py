# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, get_first_day, get_last_day
from frappe.utils.dashboard import cache_source
import hashlib

# -------------------------------------------------------------------
# FIXED COLOR MAP (single source of truth)
# IMPORTANT: use ONLY normal hyphen "-" in keys
# -------------------------------------------------------------------

SAMPLE_TYPE_COLORS = {
    "Internal Sample": "#6c757d",
    "Receipt - Packing Material": "#20c997",
    "Blending- Premix": "#6610f2",
    "Blending": "#e83e8c",
    "Lab Blend": "#17a2b8",
    "Tanker Flushing": "#fd7e14",
    "Other": "#adb5bd",
    "Empty Tanker IN": "#ffc107",
    "Receipt - Base oil": "#0d6efd",
    "Base Oil": "#0b5ed7",
    "Receipt - MEG": "#198754",
    "Process Water": "#0dcaf0",
    "Bulk Filling Tanker OUT - Base oil": "#dc3545",
    "BK Flushing": "#adb5bd",
    "Blending Kettle Flushing": "#6f42c1",
    "Additives": "#ff922b",
    "Receipt - Additive": "#ffa94d",
    "SFG": "#845ef7",
    "Receipt - SFG": "#9775fa",
    "FFS": "#f03e3e",
    "FFS Break": "#c92a2a",
    "Storage Tank flushing": "#868e96",
    "Filling Line Tea Break Sample": "#74c0fc",
    "Filling Line Lunch Break Sample": "#4dabf7",
    "Filling Line End Sample": "#228be6",
    "Filling Line Break Sample": "#1864ab",
    "Filling Line Dinner Break Sample": "#1c7ed6",
    "Bulk Filling Tanker OUT- Blending": "#fa5252",
    "Finished Good Storage Tank Sample": "#51cf66",
    "First Filled sample": "#94d82d",
    # Additional entries to handle variations
    "Blending , Blending-Premix , FirstFill Sample , Receipt-SFG": "#b197fc",
}

# -------------------------------------------------------------------
# NORMALIZATION (fix Unicode dash issues)
# -------------------------------------------------------------------

def normalize_sample_type(sample_type):
    if not sample_type:
        return sample_type
    return (
        sample_type
        .replace("–", "-")   # en dash
        .replace("—", "-")   # em dash
        .strip()
    )

# -------------------------------------------------------------------
# COLOR RESOLVER (global + fallback)
# -------------------------------------------------------------------

def get_sample_type_color(sample_type):
    sample_type = normalize_sample_type(sample_type)

    if sample_type in SAMPLE_TYPE_COLORS:
        return SAMPLE_TYPE_COLORS[sample_type]

    # deterministic fallback with vibrant colors
    h = hashlib.md5(sample_type.encode()).hexdigest()
    # Extract RGB components and ensure they're vibrant (not too dark)
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    
    # If the color is too dark (all components < 100), brighten it
    if r < 100 and g < 100 and b < 100:
        # Boost all components proportionally
        max_component = max(r, g, b, 1)  # Avoid division by zero
        scale = 150 / max_component
        r = min(int(r * scale), 255)
        g = min(int(g * scale), 255)
        b = min(int(b * scale), 255)
    
    return f"#{r:02x}{g:02x}{b:02x}"

# -------------------------------------------------------------------
# DASHBOARD CHART SOURCE
# -------------------------------------------------------------------

@frappe.whitelist()
@cache_source
def get(
    chart_name=None,
    chart=None,
    no_cache=None,
    filters=None,
    from_date=None,
    to_date=None,
    timespan=None,
    time_interval=None,
    heatmap_year=None,
):
    """
    Stacked Bar Chart - Total Samples per Customer (by Type)
    X-axis: Customer Name
    Y-axis: Total Sample Registrations (stacked by type)
    """

    filters = frappe.parse_json(filters) or {}

    # Get date range from filters or default to current month
    first_day = filters.get("from_date") or from_date or get_first_day(today())
    last_day = filters.get("to_date") or to_date or get_last_day(today())

    # Build WHERE conditions and values for parameterized query
    conditions = [
        "docstatus < 2",
        "name_of_customer IS NOT NULL",
        "type_of_sample IS NOT NULL",
        "DATE(date_of_sample__receipt) BETWEEN %s AND %s"
    ]
    
    values = [first_day, last_day]
    
    # Add type_of_sample filter if provided
    if filters.get("type_of_sample"):
        conditions.append("type_of_sample = %s")
        values.append(filters.get("type_of_sample"))

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            name_of_customer,
            type_of_sample,
            COUNT(*) AS count
        FROM `tabSample Registration`
        WHERE {where_clause}
        GROUP BY name_of_customer, type_of_sample
        ORDER BY name_of_customer, count DESC
    """

    data = frappe.db.sql(query, values=tuple(values), as_dict=True)

    # ---------------------------------------------------------------
    # Customers (Top 10)
    # ---------------------------------------------------------------

    customer_totals = {}
    for row in data:
        customer_totals[row.name_of_customer] = (
            customer_totals.get(row.name_of_customer, 0) + row.count
        )

    customers = [
        c[0] for c in sorted(
            customer_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
    ]

    # ---------------------------------------------------------------
    # Sample types (all)
    # ---------------------------------------------------------------

    sample_types = sorted({
        normalize_sample_type(row.type_of_sample) for row in data
    })

    # ---------------------------------------------------------------
    # Build datasets
    # ---------------------------------------------------------------

    datasets = []

    for sample_type in sample_types:
        values = []
        for customer in customers:
            values.append(
                sum(
                    row.count for row in data
                    if row.name_of_customer == customer
                    and normalize_sample_type(row.type_of_sample) == sample_type
                )
            )

        datasets.append({
            "name": _(sample_type),
            "values": values,
            "color": get_sample_type_color(sample_type),
        })

    return {
        "labels": customers,
        "datasets": datasets,
        "type": "bar",
    }
