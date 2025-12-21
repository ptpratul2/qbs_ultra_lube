# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MultiTypeofSample(Document):
	pass

@frappe.whitelist()
def get_non_parent_sample_types(doctype, txt, searchfield, start, page_len, filters):
	result = frappe.db.sql("""
		SELECT st.name, st.sample_name
		FROM `tabSample Types` st
		WHERE (st.is_parent = 0 OR st.is_parent IS NULL)
		   AND (st.sample_name LIKE %s OR st.name LIKE %s)
        LIMIT %s OFFSET %s
	""", (f"%{txt}%", f"%{txt}%", int(page_len), int(start)), as_dict=True)
	
	return [[row["name"], row["sample_name"] or row["name"]] for row in result]