# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    @api.depends('amount_select')
    def _compute_is_global(self):
        for rule in self:
            # rule.is_global = rule.amount_select not in ('percentage','fix','code') and True or False
            rule.is_global = rule.amount_select in ('adjustment') and True or False

    is_global = fields.Boolean(compute='_compute_is_global', store=True)
    struct_id = fields.Many2one('hr.payroll.structure', string="Salary Structure", required=False)