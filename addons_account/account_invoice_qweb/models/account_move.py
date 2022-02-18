# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('line_ids')
    def _get_adjustment_amount(self):
        for move in self:
            amount = 0.0
            for line in move.line_ids:
                if not line.product_id.adjustment_product:
                    continue
                amount += (line.quantity*line.price_unit)
            move.adjustment_amount_calc = amount

    period_of_supply = fields.Char(string='Period of Supply', copy=False)
    internal_ref = fields.Char(string='Internal Reference', copy=False)
    contract_no = fields.Char(string='Contract No', copy=False)
    # adjustment_amount_cal = fields.Float(string='Adjustment Amount', digits='Product Price')
    adjustment_amount_calc = fields.Monetary(string='Adjustment Amount', store=True, readonly=True,
        compute='_get_adjustment_amount')

    def get_usd_amount(self, amount):
        us_currency = self.env['res.currency'].search([('name','=','USD')], limit=1)
        if us_currency and (self.currency_id.id != us_currency.id):
            if amount and us_currency.rate:
                amount = float(round(amount * us_currency.rate, us_currency.decimal_places))
        return amount

    def get_sar_amount(self, amount):
        sar_currency = self.env['res.currency'].search([('name','=','SAR')], limit=1)
        if sar_currency and (self.currency_id.id != sar_currency.id):
            if amount and sar_currency.rate:
                amount = float(round(amount / self.currency_id.rate, sar_currency.decimal_places))
        amount = '{:,.2f}'.format(amount)
        return str(amount)+' '+sar_currency.name

    def get_sequence(self):
        seq = self.internal_ref or ''
        if self.name and seq:
            seq = str(seq) +"/"+ str(self.name.split("/")[2])
        return seq

    def get_untaxed_amount_without_adjustment(self):
        total_untaxed = 0.0
        for line in self.line_ids:
            if not line.exclude_from_invoice_tab and not line.product_id.adjustment_product:
                # Untaxed amount.
                total_untaxed += (line.quantity * line.price_unit)
        return total_untaxed



