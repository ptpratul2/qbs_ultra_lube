# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, get_first_day, get_last_day, getdate
from frappe.utils.dashboard import cache_source

# Import color map from the other dashboard chart source
from qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.dashboard_chart_source.total_samples_per_customer.total_samples_per_customer import (
	SAMPLE_TYPE_COLORS,
	normalize_sample_type,
	get_sample_type_color
)


@frappe.whitelist()
@cache_source
def get(
	chart_name=None,
	chart=None,
	no_cache=None,
	filters=None,
	from_date=None,
	to_date=None,
	timespan=None,
	time_interval=None,
	heatmap_year=None,
):
	"""
	Bar Chart - This Month's Samples by Type
	Shows distribution of sample types for selected date range
	Filterable by date range, customer, and sample type
	"""
	filters = frappe.parse_json(filters) or {}
	
	# Get date range from filters or default to current month
	first_day = filters.get("from_date") or from_date or get_first_day(today())
	last_day = filters.get("to_date") or to_date or get_last_day(today())
	
	# Build WHERE conditions and values for parameterized query
	conditions = [
		"docstatus < 2",
		"type_of_sample IS NOT NULL",
		"DATE(date_of_sample__receipt) BETWEEN %s AND %s"
	]
	
	values = [first_day, last_day]
	
	# Add customer filter if provided
	if filters.get("name_of_customer"):
		conditions.append("name_of_customer = %s")
		values.append(filters.get("name_of_customer"))
	
	# Add type_of_sample filter if provided
	if filters.get("type_of_sample"):
		conditions.append("type_of_sample = %s")
		values.append(filters.get("type_of_sample"))
	
	where_clause = " AND ".join(conditions)
	
	# Query to get sample counts by type
	query = f"""
		SELECT 
			type_of_sample,
			COUNT(*) as count
		FROM `tabSample Registration`
		WHERE {where_clause}
		GROUP BY type_of_sample
		ORDER BY count DESC
	"""
	
	data = frappe.db.sql(query, values=tuple(values), as_dict=True)
	
	if not data:
		return {
			"labels": [_("No Data")],
			"datasets": [{"name": _("Count"), "values": [0]}],
			"type": "bar"
		}
	
	# Build labels, values, and colors
	labels = []
	chart_values = []
	colors = []
	
	for row in data:
		sample_type = normalize_sample_type(row.type_of_sample)
		labels.append(_(sample_type))
		chart_values.append(row.count)
		colors.append(get_sample_type_color(sample_type))
	
	return {
		"labels": labels,
		"datasets": [{
			"name": _("Sample Count"),
			"values": chart_values,
			"chartType": "bar"
		}],
		"colors": colors,
		"type": "bar"
	}




