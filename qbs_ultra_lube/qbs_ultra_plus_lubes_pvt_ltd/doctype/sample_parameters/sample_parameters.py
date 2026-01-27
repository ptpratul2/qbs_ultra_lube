# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SampleParameters(Document):
      pass

@frappe.whitelist()
def set_customer_as_per_item(start, page_len, code):
    if not code:
        return ""
    
    # Query Multi Customer table for the given item code
    # Check for Item parenttype, or if not set, just match by parent
    result = frappe.db.sql("""
        SELECT mc.customer_name
        FROM `tabMulti Customer` mc
        WHERE mc.parent = %s
        AND (mc.parenttype = 'Item' OR mc.parenttype IS NULL OR mc.parenttype = '')
        AND mc.customer_name IS NOT NULL
        AND mc.customer_name != ''
        ORDER BY mc.idx, mc.name
        LIMIT 1
    """, (code,), as_dict=True)
    
    # Return the first customer name if found
    if result and result[0].get("customer_name"):
        customer_name = result[0]["customer_name"].strip()
        if customer_name:
            return customer_name
    
    return ""