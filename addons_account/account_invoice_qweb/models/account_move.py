# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    period_of_supply = fields.Char(string='Period of Supply', copy=False)
    internal_ref = fields.Char(string='Internal Reference', copy=False)

    # def _get_name_invoice_report(self):
    #     self.ensure_one()
    #     return 'account.report_invoice_document'

