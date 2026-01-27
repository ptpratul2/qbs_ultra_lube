# # Copyright (c) 2025, Astha and contributors
# # For license information, please see license.txt

# import frappe


# @frappe.whitelist()
# @frappe.validate_and_sanitize_search_inputs
# def get_thermometer_with_name(doctype, txt, searchfield, start, page_len, filters):
# 	"""
# 	Custom query function for Thermometers to return name and ID in a single line.
# 	Returns format: "name_of_equipment - equipment_id"
	
# 	This function can be used as a query function for any Link field pointing to Thermometers.
	
# 	Usage in JavaScript:
# 		frm.set_query("thermometer_field", () => {
# 			return {
# 				query: "qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.utils.thermometer_utils.get_thermometer_with_name"
# 			};
# 		});
# 	"""
# 	search_pattern = f"%{txt}%"
	
# 	return frappe.db.sql("""
# 		SELECT 
# 			name AS value,
# 			CONCAT(COALESCE(name_of_equipment, ''), ' - ', equipment_id) AS description
# 		FROM `tabThermometers`
# 		WHERE equipment_id LIKE %s 
# 		   OR name_of_equipment LIKE %s
# 		ORDER BY equipment_id
# 		LIMIT %s OFFSET %s
# 	""", (search_pattern, search_pattern, int(page_len), int(start)))

