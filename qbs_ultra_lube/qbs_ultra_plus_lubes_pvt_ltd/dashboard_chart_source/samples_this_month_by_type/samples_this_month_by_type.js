frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Samples This Month by Type"] = {
	method: "qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.dashboard_chart_source.samples_this_month_by_type.samples_this_month_by_type.get",
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
			fieldname: "name_of_customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		},
		{
			fieldname: "type_of_sample",
			label: __("Type of Sample"),
			fieldtype: "Link",
			options: "Sample Types"
		}
	]
};
