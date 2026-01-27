
import frappe
from frappe import _
from frappe.utils import get_first_day, get_last_day, getdate, today

def execute(filters=None):
    if not filters:
        filters = {}
        
    columns = get_columns()
    conditions, values = get_conditions(filters)
    data = get_data(filters, conditions, values)
    
    if data:
        data = add_total_row(data)

    chart = get_chart_data(data, filters)
    
    return columns, data, None, chart

def get_columns():
    return [
        { "label": _("Customer Name"), "fieldname": "customer_name", "fieldtype": "Link", "options": "Customer", "width": 250 },
        { "label": _("Sample Type"), "fieldname": "type_of_sample", "fieldtype": "Data", "width": 200 },
        { "label": _("TD"), "fieldname": "created_today", "fieldtype": "Int", "width": 180 },
        { "label": _("MTD"), "fieldname": "created_this_month", "fieldtype": "Int", "width": 200 },
        { "label": _("YTD"), "fieldname": "created_this_year", "fieldtype": "Int", "width": 180 }
    ]

def get_conditions(filters):
    conditions = ["docstatus = 1"]
    values = {}

    if filters.get("company"):
        conditions.append("company = %(company)s")
        values["company"] = filters.get("company")
        
    if filters.get("customer"):
        customer_list = filters.get("customer")
        if isinstance(customer_list, str):
            customer_list = [c.strip() for c in customer_list.split(",") if c.strip()]
        conditions.append("name_of_customer IN %(customer)s")
        values["customer"] = customer_list

    if filters.get("type_of_sample"):
        conditions.append("type_of_sample = %(type_of_sample)s")
        values["type_of_sample"] = filters.get("type_of_sample")

    # If dates are provided, optimize the query range
    if filters.get("from_date") and filters.get("to_date"):
        f_date = getdate(filters.get("from_date"))
        t_date = getdate(filters.get("to_date"))
        values["query_start"] = f"{f_date.year}-01-01"
        values["query_end"] = f"{t_date.year}-12-31"
        conditions.append("DATE(date_of_sample__receipt) BETWEEN %(query_start)s AND %(query_end)s")
    
    return conditions, values

def get_data(filters, conditions, values):
    # FALLBACK LOGIC: If no filter, use Today's date for logic
    raw_from = filters.get("from_date") or today()
    raw_to = filters.get("to_date") or today()
    
    f_date = getdate(raw_from)
    t_date = getdate(raw_to)

    # MTD logic: If filters are available, use the filter range; else use current month
    if filters.get("from_date") and filters.get("to_date"):
        # Use the filter date range for MTD
        mtd_start = f_date
        mtd_end = t_date
        # YTD: Use the year of the selected date range
        ytd_year = f_date.year
    else:
        # Use current month if no filters
        today_date = getdate(today())
        mtd_start = get_first_day(today_date)
        mtd_end = get_last_day(today_date)
        # YTD: Use current year
        ytd_year = today_date.year

    # Set boundaries for the SQL CASE statements
    values.update({
        "td_date": t_date,
        "mtd_start": mtd_start,
        "mtd_end": mtd_end,
        "ytd_start": f"{ytd_year}-01-01",
        "ytd_end": f"{ytd_year}-12-31"
    })
    
    sql_query = f"""
        SELECT
            name_of_customer AS customer_name,
            type_of_sample,
            SUM(CASE WHEN DATE(date_of_sample__receipt) = %(td_date)s THEN 1 ELSE 0 END) AS created_today,
            SUM(CASE WHEN DATE(date_of_sample__receipt) BETWEEN %(mtd_start)s AND %(mtd_end)s THEN 1 ELSE 0 END) AS created_this_month,
            SUM(CASE WHEN DATE(date_of_sample__receipt) BETWEEN %(ytd_start)s AND %(ytd_end)s THEN 1 ELSE 0 END) AS created_this_year
        FROM `tabSample Registration`
        WHERE {" AND ".join(conditions)}
        GROUP BY name_of_customer, type_of_sample
        ORDER BY name_of_customer, type_of_sample
    """
    return frappe.db.sql(sql_query, values, as_dict=True)

def add_total_row(data):
    total_td = sum(d.get("created_today", 0) for d in data)
    total_mtd = sum(d.get("created_this_month", 0) for d in data)
    total_ytd = sum(d.get("created_this_year", 0) for d in data)

    data.append({
        "customer_name": "Total",
        "type_of_sample": "",
        "created_today": total_td,
        "created_this_month": total_mtd,
        "created_this_year": total_ytd
    })
    return data

def get_chart_data(data, filters=None):
    if not data:
        return None
    
    chart_rows = [d for d in data if d.get("customer_name") != "Total"]
    if not chart_rows: return None
    
    customers = sorted(list(set(d['customer_name'] for d in chart_rows if d.get('customer_name'))))
    sample_types = sorted(list(set(d['type_of_sample'] for d in chart_rows if d.get('type_of_sample'))))

    pivot_data = {}
    for row in chart_rows:
        cust = row['customer_name']
        stype = row['type_of_sample']
        if not cust or not stype: continue
        if cust not in pivot_data: pivot_data[cust] = {}
        pivot_data[cust][stype] = row.get('created_this_year', 0)

    datasets = []
    for st in sample_types:
        datasets.append({
            "name": st,
            "values": [pivot_data.get(c, {}).get(st, 0) for c in customers]
        })

    return {
        "data": {"labels": customers, "datasets": datasets},
        "type": "bar",
        "stacked": 1,
        "height": 300
    }