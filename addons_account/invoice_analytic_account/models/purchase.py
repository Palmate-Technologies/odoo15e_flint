# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _prepare_invoice(self):
        self.ensure_one()
        res = super()._prepare_invoice()
        analytic_accounts = self.order_line.mapped('account_analytic_id')
        if analytic_accounts:
            res['analytic_account_id'] = analytic_accounts[0].id
        return res
