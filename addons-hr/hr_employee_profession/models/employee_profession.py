# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class EmployeeProfession(models.Model):

    _name = "employee.profession"
    _description = "Employee Profession"

    name = fields.Char(string="Name", required=True, translate=True)
