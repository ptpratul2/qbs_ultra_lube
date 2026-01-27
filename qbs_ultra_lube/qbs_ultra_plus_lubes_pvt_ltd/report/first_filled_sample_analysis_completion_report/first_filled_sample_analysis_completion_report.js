// Copyright (c) 2025, Astha and contributors
// For license information, please see license.txt

frappe.query_reports["First Filled Sample Analysis Completion Report"] = {
	"filters": [
      {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company"
      },
      {
      fieldname: "customer",
      label: __("Customer"),
      fieldtype: "MultiSelectList",
      options: "Customer",
      get_data: function (txt) {
        return frappe.db.get_link_options("Customer", txt);
      }
    },
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date"
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date"
    }
	]
};
