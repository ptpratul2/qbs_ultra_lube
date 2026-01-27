// Copyright (c) 2025, Swarada and contributors
// For license information, please see license.txt

const dataFields = {
    "Appearance": "section_break_vzyx",
    "Color (ASTM D1500)": "section_break_vzyx",
    "Colour (Visual)": "section_break_vzyx",
    "Crackle Test": "section_break_vzyx",
    "Odour": "section_break_vzyx",
    "Container Sr. No.": "section_break_vzyx",
    "Viscosity Index": "viscosity_index_astm_d2270_section",
    "KV@-40°C in Cst  (ISO 3104)": "kv_minus40c_section",
    "TAN (ASTM D664)": "total_acid_number_astm_d664_section",
    "Cloud Point": "cloud_point_astm_d2500_section",
    "Rust Prevention": "rust_prevention_astm_d665_section",
    "FTIR": "ftir_comparison_with_std_section",
    "RPVOT (ASTM D2272)": "rpvot_astm_d2272_section",
    "Total Dissolve Solid  (ISO 3696)": "coolant_section",
    "Conductivity @25°C (ISO 3696)": "conductivity__25c_iso_3696_section",
    "Refractive Index": "refract_index",
    "Refractive Index 20C": "refractive_index_20c_astm_d1747_section",
    "Aniline Point": "aniline_point_astm_d611_section",
    "Solubility in Water (Inhouse)": "section_break_nqnd",
    "Suspended Matter (Visual)": "section_break_nqnd",
    "Freezing Point": "freezing_point_astm_d3321astm_d1177_section",
    "Freezing Point 50% Dil.": "freezing_point_50_dil_astm_d3321astm_d1177_section",
    "Ash (ASTM D482)": "ash_section",
    "Dewatering Property with 3% Nacl Solution": "dewatering_property_with_3_nacl_solution_ihtp_q13_section",
    "Dewatering Property with DM Water": "dewatering_property_with_dm_water_ihtp_q13_section",
    "Sulphated Ash": "sulphated_ash_astm_d874_section",
    "Filterability Factor (TMS 371)": "filterability_factor_section",
    "Refractive Index @ 20°C (ASTM D1218)": "refractive_index_astm_d1218_section",
    "Viscosity @ 100°C (After 120 shear cycles)": "viscosity_100_deg_c_astm_d6278_section",
    "Sulphur (ASTM D4294)": "sulphur_astm_d4294_section",
    "Saponification Value (ASTM D94)": "saponification_value_astm_d94_section"
}

const dataMapping = {
    //"Raw Data Field Lable": "Sample Parameter Fieldname",
    "Appearance": "appearance_visual",
    "Color (ASTM D1500)": "colour_astm_d1500",
    "Colour (Visual)": "colour_visual",
    "Crackle Test": "crackle",
    "Odour": "odour",
    "Container Sr. No.": "srno_of_pack",
    "Viscosity Index": "viscosity_index",
    "KV@-40°C in Cst  (ISO 3104)": "kv",
    "TAN (ASTM D664)": "average_total_acid_number",
    "Cloud Point": "cloud_point_astm_d2500_c",
    "Rust Prevention": "rust_preventive_astm_d665b",
    "FTIR": "ftir_comparison_with_std",
    "RPVOT (ASTM D2272)": "rpvot_astm_d2272_min",
    "Total Dissolve Solid  (ISO 3696)": "total_dissolve_solid__iso_3696_mgl",
    "Conductivity @25°C (ISO 3696)": "conductivity_25c_iso_3696_µscm",
    "Refractive Index": "refractive_index",
    "Refractive Index 20C": "refractive_index_200c_astm_d1747",
    "Aniline Point": "aniline_point_astm_d611_c",
    "Solubility in Water (Inhouse)": "solubility_in_water_inhouse",
    "Suspended Matter (Visual)": "suspended__matter_visual",
    "Freezing Point": "freezing_point_point_astm_d3321astm_d1177_c",
    "Freezing Point 50% Dil.": "freezing_point_50_dil_astm_d3321astm_d1177",
    "Ash (ASTM D482)": "ash_astm_d482",
    "Dewatering Property with 3% Nacl Solution": "dewatering_property_with_3_nacl_solution_ihtp_q13",
    "Dewatering Property with DM Water": "dewatering_property_with_dm_water_ihtp_q13",
    "Sulphated Ash": "sulphated_ash__wt_astm_d874",
    "Filterability Factor (TMS 371)": "filterability_factor_tms_371",
    "Refractive Index @ 20°C (ASTM D1218)": "refractive_index__20c_astm_d1218",
    "Viscosity @ 100°C (After 120 shear cycles)": "viscosity__100_deg_c_astm_d6278",
    "Sulphur (ASTM D4294)": "sulphur_astm_d_4294",
    "Saponification Value (ASTM D94)": "saponification_value_astm_d94"
}

const dataFieldname = {
    "Appearance": "appearance_visual",
    "Color (ASTM D1500)": "colour_astm_d1500",
    "Colour (Visual)": "colour_visual",
    "Crackle Test": "crackle",
    "Odour": "odour",
    "Container Sr. No.": "container_sr_no",
    "Solubility in Water (Inhouse)": "solubility_in_water_inhouse",
    "Suspended Matter (Visual)": "suspended_matter_visual",
}

function hasRequiredData(frm) {
    return frm.doc.sample_name && frm.doc.type_of_sample && frm.doc.name_of_customer;
}

async function ensureTables(frm) {
    if (!hasRequiredData(frm) || frm.__tables_in_progress) {
        return;
    }

    frm.__tables_in_progress = true;
    try {
        await getAllTables(frm);
    } finally {
        frm.__tables_in_progress = false;
    }
}

frappe.ui.form.on("Raw Data Sample", {
    refresh: async function (frm) {
        await ensureTables(frm);

        // Only add confirm logic if the doc is not yet submitted
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            // Override the standard submit button
            frm.page.set_primary_action(__('Submit'), function () {
                frappe.confirm(
                    'Are you sure you want to submit this record?',
                    function () {
                        // If confirmed, call the standard submit
                        // frm.set_value('date_of_analysis_completed', frappe.datetime.now_datetime());
                        frm.save('Submit');
                    },
                    function () {
                        frappe.show_alert('Submission cancelled');
                    }
                );
            });
        }
    },
    onload_post_render: async function (frm) {
        // // Get all fields from the Doctype metadata
        const fields = frm.meta.fields;

        // console.log("---- TAB BREAKS ----");
        // // Filter fields of type "Tab Break"
        const tabBreaks = fields.filter(f => f.fieldtype === "Tab Break");
        tabBreaks.forEach(tab => {
            // console.log("Tab Label:", tab.label, "| Fieldname:", tab.fieldname);
            if (tab.fieldname === "details" && tab.fieldname === "other_tab" && frm.tabs.tabs.details) {
                $(frm.tabs.tabs.details.wrapper).show();
            } else if (frm.fields_dict[tab.fieldname]) {
                frm.fields_dict[tab.fieldname].tab.hide();
            }
        });

        // console.log("---- SECTION BREAKS ----");
        // // Filter fields of type "Section Break"
        const sectionBreaks = fields.filter(f => f.fieldtype === "Section Break");
        sectionBreaks.forEach(section => {
            // console.log("Section Label:", section.label, "| Fieldname:", section.fieldname);
            if (section.fieldname === "__section_1" || section.fieldname === "section_break_vzyx" || section.fieldname === "section_break_zifa" || section.fieldname === "other_1_section" || section.fieldname === "other_2_section") {
                frm.set_df_property(section.fieldname, "hidden", 0);
            } else {
                frm.set_df_property(section.fieldname, "hidden", 1);
            }
        });
        await ensureTables(frm);
    },
    sample_name: async function (frm) {
        await ensureTables(frm);
        // frm.refresh_fields();

        frm.set_df_property("section_break_vzyx", "hidden", 0);
        frm.set_df_property("other_1_section", "hidden", 0);
        frm.set_df_property("other_2_section", "hidden", 0);
        frm.set_df_property("section_break_zifa", "hidden", 0);
    },

});

async function getAllTables(frm) {
    if (!frm.doc.sample_name || !frm.doc.type_of_sample || !frm.doc.name_of_customer) {
        return;
    }


    frm.set_df_property("section_break_vzyx", "hidden", 0);
    frm.set_df_property("other_1_section", "hidden", 0);
    frm.set_df_property("other_2_section", "hidden", 0);
    frm.set_df_property("section_break_zifa", "hidden", 0);

    const sampleType = frm.doc.type_of_sample;

    let isInternalClient = 0;

    if (frm.doc.name_of_customer) {
        const res = await frappe.db.get_value("Customer", { name: frm.doc.name_of_customer }, "custom_is_internal_client");
        if (res.message) {
            isInternalClient = res.message.custom_is_internal_client;
        }
    }



    const name_of_sample = frm.doc.sample_name;


    if(sampleType == "Empty Tanker IN"){
        Object.keys(dataFields).forEach(field => {
            if(field == "Appearance" || field == "Color (ASTM D1500)" || field == "Crackle Test"){
                if (dataFields[field] === "section_break_vzyx") {
                    frm.set_df_property("section_break_vzyx", "hidden", 0);
                    if (dataFieldname[field]) {
                        frm.set_df_property(dataFieldname[field], "hidden", 0);
                    }     
                } else if (dataFieldname[field]) {
                    frm.set_df_property(dataFields[field], "hidden", 0);
                    frm.set_df_property(dataFieldname[field], "hidden", 0);
                    // console.log("fieldname: " + dataFieldname[field] + " Hide: " + hide);
                }else{
                    frm.set_df_property(dataFieldname[field], "hidden", 1);
                }
            }
            else{
                frm.set_df_property(dataFieldname[field], "hidden", 1);
            }
        })
    }


    if (sampleType == "Other" || isInternalClient == 1 || sampleType == "Lab Blend" || sampleType == "Tanker Flushing") {
        const response = await frm.call("preload_all_tables_for_internal", {
        });

        const tableMap = response.message;

        Object.entries(tableMap).forEach(([fieldname, wasPopulated]) => {
            const field = frm.fields_dict[fieldname];
            if (!field) return;

            // ✅ Find section by scanning backwards
            const fields = frm.meta.fields;
            let sectionFieldname = null;

            const currentIndex = fields.findIndex(f => f.fieldname === fieldname);
            if (currentIndex !== -1) {
                for (let i = currentIndex - 1; i >= 0; i--) {
                    const prevField = fields[i];
                    if (prevField.fieldtype === "Section Break") {
                        sectionFieldname = prevField.fieldname;
                        break;
                    }
                }
            }

            // ✅ Unhide the table field
            frm.set_df_property(fieldname, "hidden", 0);

            // ✅ Unhide its parent section
            if (sectionFieldname) {
                // console.log(`✅ Showing section before ${fieldname}: ${sectionFieldname}`);
                frm.set_df_property(sectionFieldname, "hidden", 0);
                frm.set_df_property("other_1_section", "hidden", 0);
                frm.set_df_property("other_2_section", "hidden", 0);
                frm.set_df_property("section_break_zifa", "hidden", 0);
                frm.set_df_property("section_break_vzyx", "hidden", 0);
            }
        });

        Object.keys(dataFields).forEach(field => {
            if(sampleType == "Tanker Flushing"){
                if(field == "Appearance" || field == "Color (ASTM D1500)" || field == "Colour (Visual)" || field == "Crackle Test"){
                    if (dataFields[field] === "section_break_vzyx") {
                        frm.set_df_property("section_break_vzyx", "hidden", 0);
                        if (dataFieldname[field]) {
                            frm.set_df_property(dataFieldname[field], "hidden", 0);
                        }     
                    } else if (dataFieldname[field]) {
                        frm.set_df_property(dataFields[field], "hidden", 0);
                        frm.set_df_property(dataFieldname[field], "hidden", 0);
                        // console.log("fieldname: " + dataFieldname[field] + " Hide: " + hide);
                    }else{
                        frm.set_df_property(dataFieldname[field], "hidden", 1);
                    }
                }
                else{
                    frm.set_df_property(dataFieldname[field], "hidden", 1);
                }
            }else{
                let fieldTab = dataFields[field];

                frm.set_df_property(fieldTab, "hidden", 0);
            }
        })
    }
    // console.log(sampleName);
    else {
    let sampleName = "";
    if (name_of_sample) {
        const res = await frappe.db.get_value("Item", name_of_sample, "item_name");
        if (res.message) {
            sampleName = res.message.item_name;
        }
    }

    const sampleParamList = await frappe.db.get_list('Sample Parameters', {
        filters: {
            item_code: name_of_sample,
            item_name: sampleName,
            sample_types: sampleType,
            customer: frm.doc.name_of_customer,
        },
        limit: 1
    });
    if (!sampleParamList.length) {
        frappe.msgprint(`Sample Parameters not found for ${sampleName} (${sampleType})`);
        return;
    }
    const samplePara = await frappe.db.get_doc('Sample Parameters', sampleParamList[0].name);

    if (!samplePara) {
        frappe.error(`There is no record of "${sampleName}" in Sample Parameters`);
    } else {
        frm.sample_para = samplePara;
        console.log(samplePara);
    }
    const response = await frm.call("preload_all_tables", {
        samplePara: JSON.stringify(frm.sample_para),
    });

    const tableMap = response.message;

    // console.log(tableMap);

    // Step 4: Populate and show only relevant tables
    Object.entries(tableMap).forEach(([fieldname, wasPopulated]) => {
        const field = frm.fields_dict[fieldname];
        if (!field) return;

        // ✅ Find section by scanning backwards
        const fields = frm.meta.fields;
        let sectionFieldname = null;

        const currentIndex = fields.findIndex(f => f.fieldname === fieldname);
        if (currentIndex !== -1) {
            for (let i = currentIndex - 1; i >= 0; i--) {
                const prevField = fields[i];
                if (prevField.fieldtype === "Section Break") {
                    sectionFieldname = prevField.fieldname;
                    break;
                }
            }
        }

        // ✅ Unhide the table field
        frm.set_df_property(fieldname, "hidden", 0);

        // ✅ Unhide its parent section
        if (sectionFieldname) {
            // console.log(`✅ Showing section before ${fieldname}: ${sectionFieldname}`);
            frm.set_df_property(sectionFieldname, "hidden", 0);
            frm.set_df_property("other_1_section", "hidden", 0);
            frm.set_df_property("other_2_section", "hidden", 0);
            frm.set_df_property("section_break_zifa", "hidden", 0);
            frm.set_df_property("section_break_vzyx", "hidden", 0);
        }
    });

    //loop through all detaField list
    Object.keys(dataFields).forEach(field => {
        //check if the field value is NA or blank then hide the field


        let sampleField = dataMapping[field];
        // console.log(sampleField);
        let sampleVal = frm.sample_para[sampleField];
        // console.log(sampleVal);

        const hide = !sampleVal || sampleVal.toLowerCase() === "na";

        // Always keep section_break_vzyx visible
        if (dataFields[field] === "section_break_vzyx") {
            frm.set_df_property("section_break_vzyx", "hidden", 0);
            if (dataFieldname[field]) {
                frm.set_df_property(dataFieldname[field], "hidden", hide ? 1 : 0);
            }
        } else if (dataFieldname[field]) {
            frm.set_df_property(dataFields[field], "hidden", hide ? 1 : 0);
            frm.set_df_property(dataFieldname[field], "hidden", hide ? 1 : 0);
            // console.log("fieldname: " + dataFieldname[field] + " Hide: " + hide);
        } else {
            let fieldTab = dataFields[field];
            frm.set_df_property(fieldTab, "hidden", hide ? 1 : 0);
            // console.log("fieldTab: " + fieldTab + " Hide: " + hide);
        }

        if (!hide) {
            frm.set_df_property("other_1_section", "hidden", 0);
            frm.set_df_property("other_2_section", "hidden", 0);
            frm.set_df_property("section_break_zifa", "hidden", 0);
            frm.set_df_property("section_break_vzyx", "hidden", 0);
        }
    })
} 
    // Ensure section_break_vzyx is always visible
    frm.set_df_property("section_break_vzyx", "hidden", 0);
};