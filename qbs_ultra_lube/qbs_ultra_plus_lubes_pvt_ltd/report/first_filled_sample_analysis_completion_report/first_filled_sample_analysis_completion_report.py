import frappe
from frappe import _
import json

@frappe.whitelist()
def execute(filters=None):
    if filters and isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            filters = {}

    # Reference date filter se uthayenge, nahi toh aaj ki date
    ref_date = filters.get("to_date") or frappe.utils.today()

    columns = get_columns()
    conditions, values = get_conditions(filters)
    data = get_data(conditions, values, ref_date)

    if data:
        total_td = sum(row.get("created_today", 0) for row in data)
        total_mtd = sum(row.get("created_this_month", 0) for row in data)
        total_ytd = sum(row.get("created_this_year", 0) for row in data)

        data.append({
            "customer_name": "Total",
            "type_of_sample": "",
            "created_today": total_td,
            "created_this_month": total_mtd,
            "created_this_year": total_ytd
        })

    chart = get_chart_data(data)
    return columns, data, None, chart

def get_columns():
    return [
        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 250
        },
        {
            "label": _("Sample Type"),
            "fieldname": "type_of_sample",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("TD"),
            "fieldname": "created_today",
            "fieldtype": "Int",
            "width": 180
        },
        {
            "label": _("MTD"),
            "fieldname": "created_this_month",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "label": _("YTD"),
            "fieldname": "created_this_year",
            "fieldtype": "Int",
            "width": 180
        }
    ]

def get_conditions(filters):
    conditions = [
        "docstatus = 1",
        "type_of_sample = 'First Filled sample'",
        """
        TIMESTAMPDIFF(
            MINUTE,
            date_of_analysis_started,
            date_of_analysis_completed
        ) <= 30
        """
    ]

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

    if filters.get("from_date"):
        conditions.append("DATE(date_of_analysis_completed) >= %(from_date)s")
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions.append("DATE(date_of_analysis_completed) <= %(to_date)s")
        values["to_date"] = filters.get("to_date")

    return conditions, values

def get_data(conditions, values, ref_date):
    # Reference date ko values dictionary mein add kiya
    values["ref_date"] = ref_date

    query = f"""
        SELECT
            name_of_customer AS customer_name,
            type_of_sample,

            SUM(
                CASE
                    WHEN DATE(date_of_analysis_completed) = %(ref_date)s
                    THEN 1 ELSE 0
                END
            ) AS created_today,

            SUM(
                CASE
                    WHEN YEAR(date_of_analysis_completed) = YEAR(%(ref_date)s)
                     AND MONTH(date_of_analysis_completed) = MONTH(%(ref_date)s)
                    THEN 1 ELSE 0
                END
            ) AS created_this_month,

            SUM(
                CASE
                    WHEN YEAR(date_of_analysis_completed) = YEAR(%(ref_date)s)
                    THEN 1 ELSE 0
                END
            ) AS created_this_year

        FROM `tabSample Registration`
        WHERE {" AND ".join(conditions)}
        GROUP BY name_of_customer, type_of_sample
        ORDER BY name_of_customer
    """

    return frappe.db.sql(query, values, as_dict=True)

def get_chart_data(data):
    if not data:
        return None

    data = [d for d in data if d.get("customer_name") != "Total"]

    labels = [d["customer_name"] for d in data]
    values = [d["created_this_year"] for d in data]

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "First Filled Sample (≤ 30 min)",
                    "values": values
                }
            ]
        },
        "type": "bar",
        "height": 500
    }