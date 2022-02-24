# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model
    def create(self, vals):
        self = self.with_context(check_move_validity=False)
        line = super(AccountBankStatementLine, self).create(vals)

        if line.state == 'posted' and line.move_id and line.move_id.state == 'draft':
            line.move_id._post(soft=False)

        return line

    def unlink(self):
        reconciled = self.filtered(lambda l: l.is_reconciled==True)
        if reconciled:
            raise UserError(_("Please Revert Reconciliation first."))
        return super().unlink()
