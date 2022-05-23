# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    amount_select = fields.Selection(selection_add=[('parameter', 'Parameter')],
                                     ondelete={'parameter': 'set default'})
    parameter_id = fields.Many2one('hr.salary.parameter', string='Salary Parameter', ondelete='restrict')

    def _compute_rule(self, localdict):
        precision = self.env['decimal.precision'].precision_get('Payroll')
        self.ensure_one()
        res = super(HrSalaryRule, self)._compute_rule(localdict)

        if self.amount_select == 'parameter':
            parameter = self.parameter_id
            payslip = localdict.get('payslip')
            contract = payslip.contract_id

            amount = getattr(contract, parameter.field_id.name)
            res = (amount, res[1], res[2])

            ### Check if increment line exist
            increment_lines = self.env['hr.salary.increment.line'].search([
                ('increment_field_id','=',parameter.id),
                ('is_changed','=',True),
                ('increment_id.state','=','approved'),
                # ('increment_id.salary_structure_updated','=',True),
                ('increment_id.contract_id','=',contract.id),
                ('increment_id.effective_date','>=',payslip.date_from),
                ('increment_id.effective_date','<=',payslip.date_to),
            ])

            if increment_lines:
                if not increment_lines[0].increment_id.salary_structure_updated:
                    raise UserError(_('Please run Salary Increment cron first!'))

                effective_date = increment_lines[0].increment_id.effective_date
                days = int(effective_date.strftime("%d")) - 1
                if days <= 30:
                    new_value = ((30 - days) * increment_lines[0].new_value) / 30
                    old_value = (days * increment_lines[0].old_value) / 30
                    amount = float(round(old_value + new_value, precision))

                    res = (amount, res[1], res[2])
        return res