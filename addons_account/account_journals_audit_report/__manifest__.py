# -*- coding: utf-8 -*-
{
    'name': "Account Journals Audit Report",

    'summary': """
    Print Account code-Account Name in Journals Audit report.
""",

    'description': """
        Print Account code-Account Name in Journals Audit report.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_journal.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
