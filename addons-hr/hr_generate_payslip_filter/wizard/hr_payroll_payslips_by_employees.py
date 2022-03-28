from odoo import fields, models, api
from odoo.osv import expression


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    # employee_ids = fields.Many2many(compute='_compute_employee_ids', store=True, readonly=False)
    # employee_ids = fields.Many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees',
    #                                 default=lambda self: self._get_employees(), required=True,
    #                                 compute='_compute_employee_ids', store=True, readonly=False)
    # department_id = fields.Many2one('hr.department')
    analytic_account_id = fields.Many2one('account.analytic.account')

    @api.depends('department_id','analytic_account_id')
    def _compute_employee_ids(self):
        hr_employees = self.env['hr.employee']
        for wizard in self.filtered(lambda w: w.department_id):
            hr_employees |= self.env['hr.employee'].search(expression.AND([
                wizard._get_available_contracts_domain(),
                [('department_id', 'ilike', self.department_id.name)]
            ]))
            
        for wizard in self.filtered(lambda w: w.analytic_account_id):
            hr_employees |= self.env['hr.employee'].search(expression.AND([
                wizard._get_available_contracts_domain(),
                [
                    # ('contract_id.analytic_account_id', 'child_of', self.analytic_account_id.id),
                    ('contract_id.analytic_account_id', '=', self.analytic_account_id.id),
                    ('contract_id.state', '=', 'open')
                ]
            ]))

        wizard.employee_ids = hr_employees
