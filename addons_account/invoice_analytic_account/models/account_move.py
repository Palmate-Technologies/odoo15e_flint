# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'


    # @api.depends('invoice_line_ids.analytic_account_id')
    # def _compute_analytic_account_from_lines(self):
    #     for record in self:
    #         analytic_account_id = False
    #         analytic_accounts = record.invoice_line_ids.mapped('analytic_account_id')
    #         if analytic_accounts:
    #             analytic_account_id = analytic_accounts[0].id
    #         record.analytic_account_id = analytic_account_id

    # def _set_analytic_account_from_lines(self):
    #     for record in self:
    #         if record.analytic_account_id:
    #             record.invoice_line_ids.write({'analytic_account_id':record.analytic_account_id and record.analytic_account_id.id or False})


    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account",
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True,
        help="Analytic account to which this invoice is linked for financial management. "
             "Use an analytic account to record cost and revenue on your project.")
    # compute='_compute_analytic_account_from_lines', inverse='_set_analytic_account_from_lines',
