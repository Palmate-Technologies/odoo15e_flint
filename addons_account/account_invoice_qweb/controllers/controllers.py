# -*- coding: utf-8 -*-
# from odoo import http


# class AccountInvoiceQweb(http.Controller):
#     @http.route('/account_invoice_qweb/account_invoice_qweb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_qweb/account_invoice_qweb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_qweb.listing', {
#             'root': '/account_invoice_qweb/account_invoice_qweb',
#             'objects': http.request.env['account_invoice_qweb.account_invoice_qweb'].search([]),
#         })

#     @http.route('/account_invoice_qweb/account_invoice_qweb/objects/<model("account_invoice_qweb.account_invoice_qweb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_qweb.object', {
#             'object': obj
#         })
