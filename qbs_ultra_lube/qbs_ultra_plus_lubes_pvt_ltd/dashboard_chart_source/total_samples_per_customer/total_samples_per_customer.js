frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Total Samples per Customer"] = {
	method: "qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.dashboard_chart_source.total_samples_per_customer.total_samples_per_customer.get",
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_start()
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_end()
		},
		{
			fieldname: "type_of_sample",
			label: __("Type of Sample"),
			fieldtype: "Link",
			options: "Sample Types"
		}
	]
};





