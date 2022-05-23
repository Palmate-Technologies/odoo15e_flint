# -*- coding: utf-8 -*-
# from odoo import http


# class HrPayrollAnalyticExpenseOnly(http.Controller):
#     @http.route('/hr_payroll_analytic_expense_only/hr_payroll_analytic_expense_only/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payroll_analytic_expense_only/hr_payroll_analytic_expense_only/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payroll_analytic_expense_only.listing', {
#             'root': '/hr_payroll_analytic_expense_only/hr_payroll_analytic_expense_only',
#             'objects': http.request.env['hr_payroll_analytic_expense_only.hr_payroll_analytic_expense_only'].search([]),
#         })

#     @http.route('/hr_payroll_analytic_expense_only/hr_payroll_analytic_expense_only/objects/<model("hr_payroll_analytic_expense_only.hr_payroll_analytic_expense_only"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payroll_analytic_expense_only.object', {
#             'object': obj
#         })
