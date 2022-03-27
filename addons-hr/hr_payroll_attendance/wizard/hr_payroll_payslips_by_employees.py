from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    def _prepare_vals(self, employee, hr_payslip_batch, run_data, slip_data):
        res = {
            'employee_id': employee.id,
            'name': slip_data['value'].get('name'),
            'struct_id': slip_data['value'].get('struct_id'),
            'contract_id': slip_data['value'].get('contract_id'),
            'payslip_run_id': hr_payslip_batch.id,
            'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
            'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
            'loan_line_ids': [(0, 0, x) for x in slip_data['value'].get('loan_line_ids', [])],
            'date_from': run_data.get('date_start'),
            'date_to': run_data.get('date_end'),
            'credit_note': run_data.get('credit_note'),
        }
        return res
    
    # @api.multi
    def compute_sheet(self):
        ### Customize- Added attendance_line_ids
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        existing_payslip_employee_ids = []
        if active_id:
            hr_payslip_batch = self.env['hr.payslip.run'].browse(active_id)
            existing_payslip_employee_ids = hr_payslip_batch.slip_ids.mapped('employee_id').ids
            # print "existing_payslip_employee_ids: ",existing_payslip_employee_ids
            [run_data] = hr_payslip_batch.read(['date_start', 'date_end', 'credit_note'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))

        if set(data['employee_ids']).intersection(set(existing_payslip_employee_ids)):
            raise UserError(_("Employee(s) already selected."))

        for employee in self.env['hr.employee'].browse(data['employee_ids']):
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)
            res = self._prepare_vals(employee, hr_payslip_batch, run_data, slip_data)
            payslips += self.env['hr.payslip'].create(res)
        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
