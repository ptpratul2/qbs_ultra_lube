# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SampleParameters(Document):
      pass

@frappe.whitelist()
def set_customer_as_per_item(start, page_len, code):
    result = frappe.db.sql("""
        SELECT mc.customer_name
        FROM `tabMulti Customer` mc
        WHERE mc.parent = %s
        ORDER BY mc.idx, mc.name
    """, (code,), as_dict=True)
    if len(result) == 1 and result[0].get("customer_name"):
        return result[0]["customer_name"]
    return ""