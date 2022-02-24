# -*- coding: utf-8 -*-
{
    'name': "Account Bank Statement Edit",

    'summary': """
    Allow to edit unreconciled bank statement line in Processing state.
""",

    'description': """
        Allow to edit unreconciled bank statement line in Processing state.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_bank_statement_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
