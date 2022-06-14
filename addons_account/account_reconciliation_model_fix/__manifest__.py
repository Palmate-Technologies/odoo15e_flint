# -*- coding: utf-8 -*-
{
    'name': "Account Reconciliation Model Fix",

    'summary': """
    If tax is selected and then removed in reconciliation window, then the tax grid is not updated.
    This module is written to fix this issue.
    """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_accountant'],

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
    'assets': {
        'web.assets_backend': [
            'account_reconciliation_model_fix/static/src/js/reconciliation/reconciliation_model.js',
        ]
    }
    
}
