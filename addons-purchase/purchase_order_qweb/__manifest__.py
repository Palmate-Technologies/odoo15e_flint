# -*- coding: utf-8 -*-
{
    'name': "Purchase Order Qweb",

    'summary': """
    Purchase order qweb reports.
""",

    'description': """
        Purchase order qweb reports.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_purchase.xml',
        'views/purchase_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
