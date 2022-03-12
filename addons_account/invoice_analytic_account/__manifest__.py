# -*- coding: utf-8 -*-
{
    'name': "Invoice Analytic Account",

    'summary': """
    -Added Analytic account field in Invoice.
""",

    'description': """
        -Added Analytic account field in Invoice.
    """,

    'author': "Palmate",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account','analytic'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
