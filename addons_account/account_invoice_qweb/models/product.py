# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Template(models.Model):
    _inherit = 'product.template'

    adjustment_product = fields.Boolean("Adjustment Product")