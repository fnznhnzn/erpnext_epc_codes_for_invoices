### Km Invoice Helper

EPC QR codes for ERPNext. These 2d codes introduced by the European Payment Council appear on invoices to facilitate their recognition by banking apps. While those process invoices reasonably well, an EPC code improves reliability a lot.

E-Invoices make EPC codes redundant in b2b but they will stay relevant in b2c transactions. 

Contrary to other implementations, we compile the necessary data points and store the resulting png as a string in the database when the invoice is saved or submitted. 

That way, no on-the-fly generation breaks the scheduled creation of invoices such as in subscriptions or auto repeats and no extra libraries are needed either.

Turns out, payment improves with EPC codes. Less mistakes are made by the payor and more correct payment references are seen even from the sloppy of accountants (they are never sloppy, are they;)

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app git@github.com:fnznhnzn/km_invoice_helper.git --branch main
bench install-app km_invoice_helper
```
Now add a custom field "custom_qr_code_base64" to Sales Invoice, Text + Read Only

...and finally for the codes to appear in your invoices add to your print formats:
```
{% if doc.custom_qr_code_base64 %} <img src="{{ doc.custom_qr_code_base64 | safe }}" /> {% endif %}
```
And... done!

Done!


### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/km_invoice_helper
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
