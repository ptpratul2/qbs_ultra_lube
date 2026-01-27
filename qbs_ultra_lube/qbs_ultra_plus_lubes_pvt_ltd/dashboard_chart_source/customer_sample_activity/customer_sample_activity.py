# Copyright (c) 2025, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, getdate, add_days
from frappe.utils.dashboard import cache_source
import hashlib

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
	Customer Sample Activity - Shows customer activity over recent period
	X-axis: Customer Name
	Y-axis: Number of Recent Registrations
	Color/Group: Type of Sample
	"""
	filters = frappe.parse_json(filters) or {}
	
	# Get date range from filters or default to last 7 days
	to_date_val = filters.get("to_date") or to_date or getdate(today())
	from_date_val = filters.get("from_date") or from_date or add_days(to_date_val, -7)
	
	# Build WHERE conditions and values for parameterized query
	conditions = [
		"docstatus < 2",
		"name_of_customer IS NOT NULL",
		"DATE(date_of_sample__receipt) BETWEEN %s AND %s"
	]
	
	values = [from_date_val, to_date_val]
	
	# Add type_of_sample filter if provided
	if filters.get("type_of_sample"):
		conditions.append("type_of_sample = %s")
		values.append(filters.get("type_of_sample"))
	
	# Add customer filter if provided
	if filters.get("name_of_customer"):
		conditions.append("name_of_customer = %s")
		values.append(filters.get("name_of_customer"))
	
	where_clause = " AND ".join(conditions)
	
	# Query recent activity
	query = f"""
		SELECT 
			name_of_customer,
			type_of_sample,
			COUNT(*) as count,
			MAX(DATE(date_of_sample__receipt)) as last_date
		FROM `tabSample Registration`
		WHERE {where_clause}
		GROUP BY name_of_customer, type_of_sample
		ORDER BY count DESC
		LIMIT 50
	"""
	
	data = frappe.db.sql(query, values=tuple(values), as_dict=True)
	
	if not data:
		return {
			"labels": [],
			"datasets": [],
			"type": "bar"
		}
	
	# Get top customers by total count
	customer_totals = {}
	for row in data:
		customer_totals[row.name_of_customer] = customer_totals.get(row.name_of_customer, 0) + row.count
	
	# Sort customers by total count and get top 15
	all_customers = [
		c[0] for c in sorted(
			customer_totals.items(),
			key=lambda x: x[1],
			reverse=True
		)[:15]
	]
	
	# Group by sample type for visualization
	type_groups = {}
	for row in data:
		# Skip if customer not in top 15
		if row.name_of_customer not in all_customers:
			continue
			
		sample_type = normalize_sample_type(row.type_of_sample or "Other")
		if sample_type not in type_groups:
			type_groups[sample_type] = {}
		
		type_groups[sample_type][row.name_of_customer] = row.count
	
	# Build datasets with colors
	datasets = []
	for sample_type in sorted(type_groups.keys()):
		values = []
		for customer in all_customers:
			values.append(type_groups[sample_type].get(customer, 0))
		
		datasets.append({
			"name": _(sample_type),
			"values": values,
			"color": get_sample_type_color(sample_type)
		})
	
	return {
		"labels": all_customers,
		"datasets": datasets,
		"type": "bar"
	}





