# We make a qr code for easier payment and store it in the database
# 
# 1. generate_and_save_epc_qr_code() at the very bottom...
# a) compiles the data in a string with build_epc_qr_string()
# b) build_epc_qr_string() uses get_company_bank_data() 
# 2. it then calls
# - make_qr_base64()
# and saves it's output in db field custom_qr_code_base64


import frappe
import qrcode
import base64
import logging
from io import BytesIO

logger = frappe.logger("erpnext_epc_codes_for_invoices")
logger.setLevel("INFO")

def get_company_bank_data(company_name):
    """Return a dict with account_name and iban for the company's bank account"""
    bank_account = frappe.get_all(
        "Bank Account",
        filters={"company": company_name},
        fields=["account_name", "iban"],
        limit_page_length=1
    )
    if not bank_account:
        frappe.throw(f"No primary bank account found for company {company_name}")

    return bank_account[0]

def build_epc_qr_string(invoice):
    company = invoice.company
    company_doc = frappe.get_doc("Company", company)
    bank = get_company_bank_data(company)
    name = (company_doc.company_name)[:70]
    iban = bank["iban"]
    bic = "" # no longer necessary for sepa credit transfer since version 002 bank["bic"]

    if not iban:
        frappe.throw("IBAN missing for company bank account")

    amount = f"{invoice.grand_total:.2f}"
    reference = invoice.name[:35]
    info = f"{invoice.customer_name or ''}".strip()[:70]

    payload = "\n".join([
        "BCD",
        "001",
        "1",
        "SCT",
        bic,
        name,
        iban,
        f"EUR{amount}",
        "",             # purpose (optional)
        reference,
        info
    ])
    return payload

def make_qr_base64(data):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def generate_and_save_epc_qr_string(doc, method):
#    logger.info(f"generate_and_save_epc_qr_string: {method} {doc.doctype} {doc.name}")
    payload = build_epc_qr_string(doc)
    qstring = make_qr_base64(payload)
    logger.info(qstring)
    doc.db_set("custom_qr_code_base64", "data:image/png;base64," + qstring)

