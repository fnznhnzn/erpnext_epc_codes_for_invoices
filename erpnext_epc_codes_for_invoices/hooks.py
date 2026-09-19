app_name = "erpnext_epc_codes_for_invoices"
app_title = "ERPNext EPC codes for invoices"
app_publisher = "fnznhnzn"
app_description = "Generate code as base64 and store it in tabSales Order"
app_email = "90838602+fnznhnzn@users.noreply.github.com"
app_license = "mit"

doc_events = {
    "Sales Invoice": {
        "before_save": "erpnext_epc_codes_for_invoices.api.generate_and_save_epc_qr_string"
    }
}
