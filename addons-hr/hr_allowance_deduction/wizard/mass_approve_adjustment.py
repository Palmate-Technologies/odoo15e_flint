# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OtherHrPayslipApproveWizard(models.TransientModel):
    _name = 'other.hr.payslip.approve.wizard'
    _description = 'Approve Payroll Adjustments Wizard'

    def button_approve_all(self):
        self.ensure_one()
        for each in self.env[self._context['active_model']].browse(self._context['active_ids']):
            each.other_hr_payslip_done()

