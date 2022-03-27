# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    is_calculation = fields.Boolean(string="Calculation", default=False)
    calc_rate = fields.Float(string="Calculation Rate")