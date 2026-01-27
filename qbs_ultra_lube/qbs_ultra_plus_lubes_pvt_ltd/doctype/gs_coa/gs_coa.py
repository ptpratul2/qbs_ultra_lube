# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GSCOA(Document):
	pass


@frappe.whitelist()
def get_gscaltex_approved_blending_samples():
    result = frappe.db.sql("""
        SELECT DISTINCT sr.batch_no
        FROM `tabSample Registration` sr
        WHERE
            sr.type_of_sample = 'Blending'
            AND sr.name_of_customer = 'G S Caltex'
            AND sr.sample_status = 'Approved'
            AND sr.batch_no IS NOT NULL
            AND sr.batch_no != ''
        ORDER BY sr.creation DESC
    """, as_dict=True)

    # Return array with all unique batch_no values (for Select field compatibility)
    return [row["batch_no"] for row in result if row.get("batch_no")]