# -*- coding: utf-8 -*-
{
    'name': "HR Payslip Send Mail",

    'summary': """
        Send payslip by email to employees.
    """,

    'description': """
        Send payslip by email to employees.
    """,

    'author': "Palmate",
    'website': "https://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payslip',
    'version': '15.0.1',
    "license": "AGPL-3",

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/hr_payslip_views.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
