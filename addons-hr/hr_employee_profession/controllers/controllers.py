# -*- coding: utf-8 -*-
# from odoo import http


# class HrEmployeeProfession(http.Controller):
#     @http.route('/hr_employee_profession/hr_employee_profession', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_employee_profession/hr_employee_profession/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_employee_profession.listing', {
#             'root': '/hr_employee_profession/hr_employee_profession',
#             'objects': http.request.env['hr_employee_profession.hr_employee_profession'].search([]),
#         })

#     @http.route('/hr_employee_profession/hr_employee_profession/objects/<model("hr_employee_profession.hr_employee_profession"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_employee_profession.object', {
#             'object': obj
#         })
