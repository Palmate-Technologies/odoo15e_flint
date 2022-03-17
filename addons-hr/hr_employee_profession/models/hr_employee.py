# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class HrEmployee(models.Model):

    _inherit = "hr.employee"

    profession_id = fields.Many2one('employee.profession', 'Profession', groups="hr.group_hr_user")
