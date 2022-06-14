# -*- coding: utf-8 -*-
# from odoo import http


# class AccountReconciliationModelFix(http.Controller):
#     @http.route('/account_reconciliation_model_fix/account_reconciliation_model_fix', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_reconciliation_model_fix/account_reconciliation_model_fix/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_reconciliation_model_fix.listing', {
#             'root': '/account_reconciliation_model_fix/account_reconciliation_model_fix',
#             'objects': http.request.env['account_reconciliation_model_fix.account_reconciliation_model_fix'].search([]),
#         })

#     @http.route('/account_reconciliation_model_fix/account_reconciliation_model_fix/objects/<model("account_reconciliation_model_fix.account_reconciliation_model_fix"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_reconciliation_model_fix.object', {
#             'object': obj
#         })
