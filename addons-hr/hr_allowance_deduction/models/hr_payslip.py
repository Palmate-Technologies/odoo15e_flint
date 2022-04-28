# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import models, fields, api, _
from collections import defaultdict
from odoo.exceptions import UserError, ValidationError


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    amount_select = fields.Selection(selection_add=[('adjustment', 'Adjustment')],
                                     ondelete={'adjustment': 'set default'})

    def _compute_rule(self, localdict):
        self.ensure_one()
        if self.amount_select == 'adjustment':
            adjustment_lines = localdict['adjustments']
            rule_adjustment_lines = adjustment_lines.filtered(lambda l: l.adjustment_type_id.rule_id == self)
            total_adjustment = 0.0
            for rule_adjustment_line in rule_adjustment_lines:
                sign = 1 if rule_adjustment_line.operation_type == 'allowance' else -1
                total_adjustment += (rule_adjustment_line.amount * sign)
            return total_adjustment, 1.0, 100
        return super(HrSalaryRule, self)._compute_rule(localdict)


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def _fetch_adjustment_lines(self):
        self.ensure_one()
        return self.env['other.hr.payslip'].search([
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'done')
        ])

    def _prepare_payslip_line_vals(self, contract, rule, amount, qty, rate, localdict):
        res = super(HrPayslip, self)._prepare_payslip_line_vals(contract, rule, amount, qty, rate, localdict)
        if rule.amount_select == 'adjustment' and localdict['adjustments']:
            adjustments = localdict['adjustments']
            adjustments = adjustments.filtered(lambda line: line.adjustment_type_id.rule_id.id == rule.id)
            if adjustments:
                name = ": ".join(adjustments.mapped('name'))
                description = adjustments[0].description

                res['name'] = name
                res['note'] = description
                res['other_hr_payslip_ids'] = [(6, 0, adjustments.ids)]
        return res


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    other_hr_payslip_ids = fields.One2many('other.hr.payslip', 'payslip_line_id', string='Adjustments', copy=False)


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    def get_all_rules(self, payslip, localdict):

        all_rules, localdict = super(HrPayrollStructure, self).get_all_rules(payslip, localdict)
        adjustment_lines = payslip._fetch_adjustment_lines()

        for adjustment_line in adjustment_lines:
            all_rules |= adjustment_line.adjustment_type_id.rule_id
        localdict.update(adjustments=adjustment_line)
        return all_rules, localdict