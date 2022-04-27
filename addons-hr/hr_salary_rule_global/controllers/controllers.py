# -*- coding: utf-8 -*-
# from odoo import http


# class HrPayrollStructureGlobal(http.Controller):
#     @http.route('/hr_payroll_structure_global/hr_payroll_structure_global/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payroll_structure_global/hr_payroll_structure_global/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payroll_structure_global.listing', {
#             'root': '/hr_payroll_structure_global/hr_payroll_structure_global',
#             'objects': http.request.env['hr_payroll_structure_global.hr_payroll_structure_global'].search([]),
#         })

#     @http.route('/hr_payroll_structure_global/hr_payroll_structure_global/objects/<model("hr_payroll_structure_global.hr_payroll_structure_global"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payroll_structure_global.object', {
#             'object': obj
#         })
