from odoo import models, fields, api

class HrSalaryParameter(models.Model):
    _name = "hr.salary.parameter"
    _description = "Hr Salary Parameter"

    name = fields.Char(string="Name", required=True, index=True, copy=False)
    field_id = fields.Many2one('ir.model.fields', string='Field',
                               domain=[('model_id.model','=','hr.contract'),('ttype','=','monetary')], ondelete='cascade', required=True)

    _sql_constraints = [
        ('field_id', 'UNIQUE (field_id)', 'You can not have two same fields selected as parameter!')
    ]