# -*- coding: utf-8 -*-
{
    'name': "Salary Rule Global",

    'summary': """
	""",

    'description': """
Allows creation of global rules which will be independent of any structure. These rules will be applicable to any 
payslip which has respective transactions validated.
    """,

    'author': "Palmate Technologies",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payroll',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
		# 'data/hr_payroll_data.xml',
        'views/hr_salary_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
