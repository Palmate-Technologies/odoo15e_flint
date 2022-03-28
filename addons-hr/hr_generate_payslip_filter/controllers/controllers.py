# -*- coding: utf-8 -*-
# from odoo import http


# class HrPayslipEmployeesDepartment(http.Controller):
#     @http.route('/hr_payslip_employees_department/hr_payslip_employees_department/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payslip_employees_department/hr_payslip_employees_department/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payslip_employees_department.listing', {
#             'root': '/hr_payslip_employees_department/hr_payslip_employees_department',
#             'objects': http.request.env['hr_payslip_employees_department.hr_payslip_employees_department'].search([]),
#         })

#     @http.route('/hr_payslip_employees_department/hr_payslip_employees_department/objects/<model("hr_payslip_employees_department.hr_payslip_employees_department"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payslip_employees_department.object', {
#             'object': obj
#         })
