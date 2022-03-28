# -*- coding: utf-8 -*-
{
    'name': "HR Payroll linked with Attendance",

    'summary': """
    """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Aasim Ahmed Ansari",
    'website': "http://aasimania.wordpress.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '14.0.3',

    # any module necessary for this one to work correctly
    'depends': [
        'hr_attendance',
        'hr_payroll',
        'account',
        # 'hr_base',
        'hr_holidays'

    ],

    # always loaded
    'data': [
        'data/hr_work_entry_type.xml',
        'security/ir.model.access.csv',
        'security/hr_security.xml',
        'wizard/hr_attendance_update_view.xml',
        # 'wizard/hr_payslip_compute_sheet_multi_view.xml',
        'wizard/refresh_payslip_view.xml',
        'views/views.xml',
        'views/hr_payroll_views.xml',
        'views/res_config_view.xml',
        'views/hr_contract_views.xml',
        'views/hr_attendance_summary_view.xml',
        'views/hr_attendance_view.xml',
        'views/hr_attendance_adjustment_view.xml',
        'views/hr_attendance_summary_report_template.xml',
        'views/reports.xml',
        'views/resource_views.xml',
        'wizard/hr_attendance_summary_import.xml',
        'views/hr_attendance_policy.xml',
        'views/hr_work_entry_type.xml',
    ],
    # only loaded in demonstration mode
    'license':'LGPL-3'

}