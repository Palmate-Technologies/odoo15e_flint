# -*- coding: utf-8 -*-
{
    'name': "Account Invoice Qweb",

    'summary': """
        Invoice Qweb Reports
        """,

    'description': """
        Invoice Qweb Reports
    """,

    'author': "Palmate",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.0.7',

    # any module necessary for this one to work correctly
    'depends': ['base','account',
                'l10n_sa_invoice',
                'web','invoice_analytic_account',
                'invoice_line_quantity_str', # bcz of one field ie quantity_str
                'product'# bcz of adjustment line
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_invoice.xml',
        'views/report_invoice_stc.xml',
        'views/report_invoice_ericson.xml',
        'views/account_report.xml',
        'views/account_move_view.xml',
        'views/report_journal.xml',
        'views/product_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
