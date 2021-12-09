# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    period_of_supply = fields.Char(string='Period of Supply', copy=False)
    internal_ref = fields.Char(string='Internal Reference', copy=False)

    # def _get_name_invoice_report(self):
    #     self.ensure_one()
    #     return 'account.report_invoice_document'

    def get_usd_amount(self, amount):
        us_currency = self.env['res.currency'].search([('name','=','USD')], limit=1)
        if us_currency and (self.currency_id.id != us_currency.id):
            if amount and us_currency.rate:
                amount = float(round(amount * us_currency.rate,2))
        return amount

    def get_sar_amount(self, amount):
        sar_currency = self.env['res.currency'].search([('name','=','SAR')], limit=1)
        if sar_currency and (self.currency_id.id != sar_currency.id):
            if amount and sar_currency.rate:
                amount = float(round(amount / self.currency_id.rate,2))
        return amount

