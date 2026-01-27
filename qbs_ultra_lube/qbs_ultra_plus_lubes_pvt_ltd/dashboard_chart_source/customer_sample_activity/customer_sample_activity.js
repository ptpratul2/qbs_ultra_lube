frappe.provide("frappe.dashboards.chart_sources");

frappe.dashboards.chart_sources["Customer Sample Activity"] = {
	method: "qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.dashboard_chart_source.customer_sample_activity.customer_sample_activity.get",
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -7)
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		},
		{
			fieldname: "type_of_sample",
			label: __("Type of Sample"),
			fieldtype: "Link",
			options: "Sample Types"
		},
		{
			fieldname: "name_of_customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		}
	]
};

