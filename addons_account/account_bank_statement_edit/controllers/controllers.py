# -*- coding: utf-8 -*-
# from odoo import http


# class BankStatementEdit(http.Controller):
#     @http.route('/bank_statement_edit/bank_statement_edit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bank_statement_edit/bank_statement_edit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bank_statement_edit.listing', {
#             'root': '/bank_statement_edit/bank_statement_edit',
#             'objects': http.request.env['bank_statement_edit.bank_statement_edit'].search([]),
#         })

#     @http.route('/bank_statement_edit/bank_statement_edit/objects/<model("bank_statement_edit.bank_statement_edit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bank_statement_edit.object', {
#             'object': obj
#         })
