from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError

class HrSalaryIncrementLine(models.Model):
    _name = "hr.salary.increment.line"
    _description = "Hr Salary Increment Line"
    _rec_name= "old_value"

    @api.depends('old_value', 'new_value')
    def compute_is_changed(self):
        for line in self:
            is_changed = False
            if line.old_value != line.new_value:
                is_changed = True
            line.is_changed = is_changed

    increment_field_id = fields.Many2one('hr.salary.parameter', string='Salary Parameter', ondelete='restrict', readonly=True)
    old_value = fields.Float(string='Old Amount', digits='Payroll', readonly=True)
    new_value = fields.Float(string='New Amount', digits='Payroll')
    increment_id = fields.Many2one('hr.salary.increment', string='Salary Increment', required=True, ondelete='cascade', index=True, copy=False)
    is_changed = fields.Boolean(compute='compute_is_changed', store=True)


class HrSalaryIncrement(models.Model):
    _name = "hr.salary.increment"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = "Hr Salary Increment"

    name = fields.Char(string="Name", required=True, index=True, copy=False, readonly=True, states={'draft': [('readonly', False)]})
    effective_date = fields.Date(string="Effective Date", default=fields.Datetime.now, required=True, readonly=True, states={'draft': [('readonly', False)]},tracking=1)
    state = fields.Selection(
        [('draft', 'Draft'), ('to_approve', 'To approve'), ('approved', 'Approved'), ('cancel', 'Cancel')],
        default='draft',tracking=1)
    employee_id = fields.Many2one('hr.employee', string='Employee ID', required=True, readonly=True, states={'draft': [('readonly', False)]},tracking=1)
    contract_id = fields.Many2one(related='employee_id.contract_id', string='Contract')
    salary_structure_updated = fields.Boolean(string='Structure Updated', readonly=True)
    increment_lines = fields.One2many('hr.salary.increment.line', 'increment_id', string='Increment Lines', copy=True, readonly=True, states={'draft': [('readonly', False)]}, auto_join=True)

    @api.constrains('effective_date')
    def _constrains_effective_date(self):
        for record in self:
            if int(record.effective_date.strftime("%d")) == 31:
                raise UserError(_('Increment can not happen on 31st of month'))


    def get_increment_lines(self):
        parameters = self.env['hr.salary.parameter'].search([])
        for increment in self:
            increment.sudo().increment_lines.unlink()
            lines = []
            contract = increment.contract_id
            for parameter in parameters:
                lines.append((0, 0, {'old_value': getattr(contract, parameter.field_id.name),
                                     'new_value': getattr(contract, parameter.field_id.name),
                                     'increment_field_id':parameter.id,
                                     }))
            increment.increment_lines = lines
        return True

    # cron function, to check if increment is set for a date, update its values in Contract
    def update_increment_in_contract_cron(self):
        increments = self.search([
                ('effective_date','>=',date.today()),
                ('effective_date','<=',date.today()),
                ('salary_structure_updated','!=',True),
                ('state','=','approved'),
            ])
        print("increments: ",increments)
        for increment in increments:
            contract = increment.contract_id
            for line in increment.increment_lines:
                setattr(contract, line.increment_field_id.field_id.name, line.new_value)
                print("updated")
            increment.salary_structure_updated = True

        return True

    def action_submit(self):
        for increment in self:
            if increment.increment_lines.filtered(lambda l: l.is_changed):
                # raise UserError(_('Old value and New value can not be same.'))
                increment.write({'state':'to_approve'})
        return True

    def action_approve(self):
        self.write({'state': 'approved'})
        return True

    def action_cancel(self):
        for record in self:
            if record.salary_structure_updated:
                raise UserError(_('Salary structure updated with these new values, can not cancel now.'))
        self.write({'state': 'cancel'})
        return True

    def action_reset_draft(self):
        self.write({'state': 'draft'})
        return True

