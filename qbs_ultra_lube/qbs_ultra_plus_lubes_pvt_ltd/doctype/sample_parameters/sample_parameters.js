// // Copyright (c) 2025, Astha and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Sample Parameters", {
	item_code: function(frm){
        if(frm.doc.item_code){
            frappe.call({
                method: "qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.doctype.sample_parameters.sample_parameters.set_customer_as_per_item",
                args: { 
                    start: 0,
                    page_len: 20,
                    code: frm.doc.item_code
                },
                callback: function(r) {
                    if (r && r.message && r.message.trim() !== "") {
                        frm.set_value("customer", r.message);
                        frm.refresh_field("customer");
                    } else {
                        // Clear customer field if no customer found
                        frm.set_value("customer", "");
                        frm.refresh_field("customer");
                    }
                },
                error: function(r) {
                    console.error("Error fetching customer:", r);
                    frappe.show_alert({
                        message: __("Error fetching customer information"),
                        indicator: "red"
                    }, 3);
                }
            })
        } else {
            // Clear customer field if item_code is cleared
            frm.set_value("customer", "");
            frm.refresh_field("customer");
        }
    }
});
