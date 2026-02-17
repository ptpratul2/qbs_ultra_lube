// Copyright (c) 2026, Astha and contributors
// For license information, please see license.txt

frappe.query_reports["Pivot Table Raw Data"] = {
    "filters": [
        {
            fieldname: "name_of_customer",
            label: __("Name of Customer"),
            fieldtype: "Link",
            options: "Customer",
            reqd: 0
        },
        {
            fieldname: "type_of_sample",
            label: __("Type of Sample"),
            fieldtype: "Link",
			options: "Sample Types",
            reqd: 0
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 0
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 0
        }
    ],

    onload: function(report) {
        // Optional: add a custom button to download pivoted Excel directly
        report.page.add_inner_button(__("Download Excel"), function() {
            // frappe.call({
            //     method: "custom_app.custom_app.report.pivot_table_raw_data.pivot_table_raw_data.download_pivoted_excel",
            //     args: { filters: report.get_values() }
            // });
			const filters = report.get_values(); 
			const url = `/api/method/qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.report.pivot_table_raw_data.pivot_table_raw_data.download_pivoted_excel?filters=${encodeURIComponent(JSON.stringify(filters))}`;
			window.open(url);
        });
    }
};