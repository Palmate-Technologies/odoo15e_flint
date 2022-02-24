# -*- coding: utf-8 -*-
# from odoo import http


# class AccountJournalsAuditReport(http.Controller):
#     @http.route('/account_journals_audit_report/account_journals_audit_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_journals_audit_report/account_journals_audit_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_journals_audit_report.listing', {
#             'root': '/account_journals_audit_report/account_journals_audit_report',
#             'objects': http.request.env['account_journals_audit_report.account_journals_audit_report'].search([]),
#         })

#     @http.route('/account_journals_audit_report/account_journals_audit_report/objects/<model("account_journals_audit_report.account_journals_audit_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_journals_audit_report.object', {
#             'object': obj
#         })
