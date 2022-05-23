# -*- coding: utf-8 -*-
{
    'name': "HR Payroll Analytic Expense Only",

    'summary': """
    """,

    'description': """
The journal entry of a payslip will select analytic account only if the corresponding general account is not of receivable or payable nature.
    """,

    'author': "Aasim Ahmed Ansari",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payroll',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
