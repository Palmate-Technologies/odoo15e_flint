# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceAnalyticAccount(http.Controller):
#     @http.route('/invoice_analytic_account/invoice_analytic_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_analytic_account/invoice_analytic_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_analytic_account.listing', {
#             'root': '/invoice_analytic_account/invoice_analytic_account',
#             'objects': http.request.env['invoice_analytic_account.invoice_analytic_account'].search([]),
#         })

#     @http.route('/invoice_analytic_account/invoice_analytic_account/objects/<model("invoice_analytic_account.invoice_analytic_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_analytic_account.object', {
#             'object': obj
#         })
