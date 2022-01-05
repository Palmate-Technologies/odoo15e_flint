# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        self.ensure_one()
        res = super()._prepare_invoice()
        if self.analytic_account_id:
            res['analytic_account_id'] = self.analytic_account_id and self.analytic_account_id.id or False
        return res
