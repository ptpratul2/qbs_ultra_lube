
// const THERMOMETER_FIELDS = [
// 	"thermometer_id_kv_100c",
// 	"thermometer_id_kv_40c",
// 	"thermometer_id_kv_blend__100c",
// 	"thermometer_id_kv_378c",
// 	"thermometer_id_foaming",
// 	"thermometer_id_foaming_astm_d1881",
// 	"thermometer_id_demulsibility",
// 	"thermometer_id_pour_point",
// 	"thermometer_id_flash_point",
// 	"thermometer_id_fp",
// 	"thermometer_id",
// 	"thermometer_id_ar",
// 	"thermometer_id_ap"
// ];

// /**
//  * Format thermometer field display to show name and ID in a single line
//  * @param {Object} frm - Frappe form object
//  * @param {string} fieldname - Name of the thermometer field
//  */
// function format_thermometer_display(frm, fieldname) {
// 	// Debug log
// 	// console.log(`[ThermometerUtils] Formatting ${fieldname}... Val: ${frm.doc[fieldname]}`);

// 	// Fetch thermometer details and format display
// 	if (!frm.doc[fieldname]) {
// 		return;
// 	}

// 	frappe.db.get_value("Thermometers", frm.doc[fieldname], ["equipment_id", "name_of_equipment"])
// 		.then(r => {
// 			if (r && r.message) {
// 				const doc = r.message;
// 				const displayText = `${doc.name_of_equipment || ''} - ${doc.equipment_id || ''}`.trim();
// 				// console.log(`[ThermometerUtils] Display Text for ${fieldname}: ${displayText}`);

// 				// Update the field display - try multiple approaches for compatibility
// 				const field = frm.get_field(fieldname);
// 				if (field) {
// 					// Wait for field to be fully rendered
// 					setTimeout(() => {
// 						// Try to find the field wrapper using different methods
// 						const $fieldWrapper = field.disp_area
// 							? $(field.disp_area)
// 							: $(`[data-fieldname="${fieldname}"]`).closest('.form-group, .frappe-control');

// 						if ($fieldWrapper.length) {
// 							// console.log(`[ThermometerUtils] Found wrapper for ${fieldname}, applying text.`);
// 							// Update the main link text (for link fields)
// 							const $linkContent = $fieldWrapper.find('.link-content, .control-value, .static-value');
// 							if ($linkContent.length) {
// 								$linkContent.text(displayText);
// 								$linkContent.attr('title', displayText);
// 							} else {
// 								// console.warn(`[ThermometerUtils] Link content not found for ${fieldname}`);
// 							}

// 							// Hide the description line and merge it with the name
// 							const $description = $fieldWrapper.find('.help-box, .description, .small, .text-muted');
// 							if ($description.length) {
// 								$description.hide();
// 							}

// 							// Update input field attributes if present
// 							const $input = $fieldWrapper.find(`input[data-fieldname="${fieldname}"], input[name="${fieldname}"]`);
// 							if ($input.length) {
// 								$input.attr('data-display-value', displayText);
// 								$input.attr('title', displayText);
// 								// Force value for visual confirmation (experimental)
// 								// $input.val(displayText); 
// 							}

// 							// Also try to update any label or display element
// 							const $display = $fieldWrapper.find('.control-value-wrapper, .link-btn');
// 							if ($display.length) {
// 								$display.attr('title', displayText);
// 							}
// 						} else {
// 							console.warn(`[ThermometerUtils] Wrapper not found for ${fieldname}`);
// 						}
// 					}, 500); // Increased timeout to 500ms
// 				} else {
// 					console.warn(`[ThermometerUtils] Field object not found: ${fieldname}`);
// 				}
// 			}
// 		})
// 		.catch(err => {
// 			console.error(`[ThermometerUtils] Failed to format ${fieldname} display:`, err);
// 		});
// }

// /**
//  * Setup thermometer fields for a form
//  * This function sets up queries and event handlers for all thermometer fields
//  * @param {Object} frm - Frappe form object
//  * @param {Array} field_list - Optional array of field names. If not provided, uses default THERMOMETER_FIELDS
//  */
// function setup_thermometer_fields(frm, field_list = null) {
// 	const fields = field_list || THERMOMETER_FIELDS;
// 	// console.log("[ThermometerUtils] Setting up fields...", fields);

// 	// Set custom query and event handlers for all thermometer fields
// 	fields.forEach(fieldname => {
// 		// console.log(`[ThermometerUtils] Processing field: ${fieldname}`);
// 		try {
// 			frm.set_query(fieldname, () => {
// 				return {
// 					query: "qbs_ultra_lube.thermometer_utils.get_thermometer_with_name"
// 				};
// 			});

// 			// Attach change handler to trigger formatting when value changes
// 			// This is crucial for new/unsaved documents
// 			// We use a flag 'is_thermometer_handler' to avoid multiple wrappings on repeated refreshes
// 			if (!frm.cscript[fieldname]) {
// 				// console.log(`[ThermometerUtils] Attaching new handler for ${fieldname}`);
// 				// RENAME inner frm to doc to avoid shadowing
// 				frm.cscript[fieldname] = function (doc, cdt, cdn) {
// 					setTimeout(() => {
// 						format_thermometer_display(frm, fieldname);
// 					}, 100);
// 				};
// 				frm.cscript[fieldname].is_thermometer_handler = true;
// 			} else if (!frm.cscript[fieldname].is_thermometer_handler) {
// 				// If a handler exists but isn't ours, wrap it
// 				// console.log(`[ThermometerUtils] Wrapping existing handler for ${fieldname}`);
// 				const old_handler = frm.cscript[fieldname];
// 				// RENAME inner frm to doc
// 				frm.cscript[fieldname] = function (doc, cdt, cdn) {
// 					if (typeof old_handler === 'function') {
// 						old_handler(doc, cdt, cdn);
// 					}
// 					setTimeout(() => {
// 						format_thermometer_display(frm, fieldname);
// 					}, 100);
// 				};
// 				frm.cscript[fieldname].is_thermometer_handler = true;
// 			} else {
// 				// console.log(`[ThermometerUtils] Handler already attached for ${fieldname}`);
// 			}
// 		} catch (e) {
// 			console.error(`[ThermometerUtils] Error setting up ${fieldname}:`, e);
// 		}
// 	});

// 	// Return empty handlers object as we attached them directly
// 	return {};
// }

// /**
//  * Format all thermometer fields on form refresh
//  * @param {Object} frm - Frappe form object
//  * @param {Array} field_list - Optional array of field names. If not provided, uses default THERMOMETER_FIELDS
//  */
// function refresh_thermometer_fields(frm, field_list = null) {
// 	const fields = field_list || THERMOMETER_FIELDS;
// 	// console.log("[ThermometerUtils] Refreshing fields...", fields);

// 	// Format all thermometer field displays to show name and ID in single line
// 	fields.forEach(fieldname => {
// 		format_thermometer_display(frm, fieldname);
// 	});
// }

