import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import now_datetime
from frappe.utils import get_datetime, time_diff_in_seconds



class SampleRegistration(Document):

    def autoname(self):

    # Allow manual override (duplicate / clone use-case)
        if getattr(self, 'custom_generated_name', None):
            self.name = self.custom_generated_name
            return

        import frappe
        from frappe.utils import now_datetime

        customer = (self.name_of_customer or "").strip()
        company = (self.company or "").strip()
        year = now_datetime().year

        # ======================================================
        # PREFIX MAP (COMPANY + CUSTOMER)
        # ======================================================
        prefix_map = {

            # ---------- COMPANY PREFIXES ----------
            "West Coast Lubricants & Asphalts Pvt. Ltd.": "WCL",
            "Ultra Plus Lubes Pvt. Ltd": "UPL1",
            "Ultra Plus Lubes Pvt. Ltd Unit IV": "UPL4",

            # ---------- CUSTOMER PREFIXES ----------
            "Ultra Plus Lubes Pvt. Ltd.- Unit 1": "UPL1",
            "Ultra Plus Lubes Pvt. Ltd.- Unit 4": "UPL4",
            "West Coast Lubricants & Asphalts Pvt. Ltd.": "WCL",

            # ---------- OTHER CUSTOMERS ----------
            "Valvoline Cummins (I) Pvt. Ltd. (Lube oil)": "VCPLL",
            "Valvoline Cummins (I) Pvt. Ltd.  (Lube oil)": "VCPLL",
            "Petronas": "PLI",
            "Valvoline Cummins (I) Pvt. Ltd. (coolant)": "VCPLC",
            "Valvoline Cummins (I) Pvt. Ltd.  (coolant)": "VCPLC",
            "BASF (Coolant)": "BASFC",
            "G S Caltex": "GSC",
            "G S Caltex (Base Oil Trading)": "GSCT",
            "Nynas": "NYNAS",
            "Sperry": "SPERRY",
            "BASF (Brake Fluid)": "BASFB",
            "Raj Petro (Solvent)": "RPS",
            "Raj Petro (Blending)": "RPB",
            "Shell India Marketing Pvt. Ltd.": "SIMPL",
            "Castrol (I) Pvt. Ltd.": "CIL",
            "ENSOOILS": "EO",
            "Exxon Mobil": "EM",
        }

        # ======================================================
        # DUAL PREFIX COMPANY + CUSTOMER SET
        # ======================================================
        dual_prefix_companies = {
            "West Coast Lubricants & Asphalts Pvt. Ltd.",
            "Ultra Plus Lubes Pvt. Ltd",
            "Ultra Plus Lubes Pvt. Ltd Unit IV"
        }

        dual_prefix_customers = {
            "Ultra Plus Lubes Pvt. Ltd.- Unit 1",
            "Ultra Plus Lubes Pvt. Ltd.- Unit 4",
            "West Coast Lubricants & Asphalts Pvt. Ltd."
        }

        # ======================================================
        # CASE 1: DUAL PREFIX → COMPANY/CUSTOMER/YEAR/0001
        # ======================================================
        if company in dual_prefix_companies and customer in dual_prefix_customers:

            company_prefix = prefix_map.get(company)
            customer_prefix = prefix_map.get(customer)

            if not company_prefix:
                frappe.throw(f"Missing prefix mapping for Company: {company}")
            if not customer_prefix:
                frappe.throw(f"Missing prefix mapping for Customer: {customer}")

            visible_prefix = f"{company_prefix}/{customer_prefix}/{year}"

            records = frappe.db.sql("""
                SELECT name FROM `tabSample Registration`
                WHERE name LIKE %s
            """, (visible_prefix + "/%",), as_dict=True)

            max_num = 0
            for row in records:
                try:
                    max_num = max(max_num, int(row.name.split("/")[-1]))
                except:
                    pass

            self.name = f"{visible_prefix}/{str(max_num + 1).zfill(4)}"
            return

        # ======================================================
        # CASE 2: NORMAL PREFIX → PREFIX/YEAR/0001
        # ======================================================
        prefix = prefix_map.get(customer)

        if not prefix:
            prefix = "".join([w[0].upper() for w in customer.split() if w])

        visible_prefix = f"{prefix}/{year}"

        records = frappe.db.sql("""
            SELECT name FROM `tabSample Registration`
            WHERE name LIKE %s
        """, (visible_prefix + "/%",))

        max_number = 0
        for record in records:
            try:
                max_number = max(max_number, int(record[0].split("/")[-1]))
            except:
                pass

        self.name = f"{visible_prefix}/{str(max_number + 1).zfill(4)}"
    def before_submit(self):
        if self.date_of_analysis_started and self.date_of_analysis_completed: 
            start = get_datetime(self.date_of_analysis_started) 
            end = get_datetime(self.date_of_analysis_completed) 

            diff_seconds = time_diff_in_seconds(end, start)
            # Convert to minutes (integer, no seconds)
            diff_minutes = diff_seconds // 60

            # Assign directly to Int field 
            self.time_required_in_min= diff_minutes


# =================================================================
# DUPLICATE CREATION
# =================================================================
@frappe.whitelist()
def create_duplicate(docname):
    original_doc = frappe.get_doc("Sample Registration", docname)
    base_name = docname.split('-')[0]

    existing_duplicates = frappe.db.sql(
        """SELECT name FROM `tabSample Registration`
           WHERE name LIKE %s""",
        (base_name + "-%",)
    )

    max_suffix = 0
    for d in existing_duplicates:
        try:
            suffix_num = int(d[0].split('-')[-1])
            max_suffix = max(max_suffix, suffix_num)
        except:
            pass

    new_suffix = str(max_suffix + 1).zfill(2)
    final_new_name = f"{base_name}-{new_suffix}"

    new_doc = frappe.copy_doc(original_doc)
    new_doc.docstatus = 0
    
    # Get user's full name reliably
    user_fullname = frappe.session.get("user_fullname")
    if not user_fullname:
        user_fullname = frappe.db.get_value("User", frappe.session.user, "full_name")
    if not user_fullname:
        user_fullname = frappe.session.user
    
    new_doc.sample_received_by = user_fullname
    new_doc.date_of_analysis_started = frappe.utils.now_datetime()
    new_doc.date_of_sample__receipt = frappe.utils.now_datetime()
    new_doc.is_reanalysis=1
    new_doc.custom_generated_name = final_new_name
    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return new_doc.as_dict()


@frappe.whitelist()
def calculate_time_required(docname, completed_date):
	doc = frappe.get_doc("Sample Registration", docname)
	if doc.date_of_analysis_started: 
		start = get_datetime(doc.date_of_analysis_started) 
		end = get_datetime(completed_date) 
		
		diff_seconds = time_diff_in_seconds(end, start)
		# Convert to minutes (integer, no seconds)
		diff_minutes = diff_seconds // 60
	
	    # # Assign directly to Int field 
		# doc.duration_in_min = diff_minutes

		return diff_minutes