# -*- coding: utf-8 -*-
{
    'name': "HR Generate Payslips Filter",

    'summary': """
        This module adds different filters in Generate Payslips wizard in Payslip Batches
    """,

    'description': """
        This module adds different filters in Generate Payslips wizard in Payslip Batches
    """,

    'author': "Aasim Ahmed Ansari",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payroll',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/hr_payroll_payslips_by_employees_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license':'LGPL-3'
}
