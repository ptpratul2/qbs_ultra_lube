// Copyright (c) 2025, Astha and contributors
// For license information, please see license.txt

frappe.ui.form.on('GS COA', {
	refresh: function(frm) {
        frappe.call({
            method: "qbs_ultra_lube.qbs_ultra_plus_lubes_pvt_ltd.doctype.gs_coa.gs_coa.get_gscaltex_approved_blending_samples",
            callback: function(r) { 
                if (r.message && r.message.length > 0) {
                    console.log("response: ", r.message);
                    // Convert array to newline-separated string for Select field
                    var options = "\n" + r.message.join("\n");
                    frm.fields_dict['batch_no'].df.options = options; 
                    frm.refresh_field('batch_no');
                } else {
                    console.log("No data received:", r);
                }
            }
        })
    }
})