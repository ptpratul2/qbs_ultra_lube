
frappe.query_reports["Sample Reg"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "MultiSelectList",
            "options": "Customer",
            "get_data": function (txt) {
                return frappe.db.get_link_options("Customer", txt);
            }
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date"
        },
        {
            "fieldname": "type_of_sample",
            "label": __("Sample Type"),
            "fieldtype": "Link",
            "options": "Sample Types",
        }
    ]
};