import time
from datetime import datetime,timedelta
from dateutil import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import ValidationError
import babel

from odoo import api, fields, models, tools, _

import logging

_logger = logging.getLogger(__name__)


class HrPayslipAttendance(models.Model):
    _name = 'hr.payslip.attendance'
    _description = 'Payslip Attendance'
    _order = 'payslip_id, sequence'

    name = fields.Char(string='Description', required=True)
    payslip_id = fields.Many2one('hr.payslip', string='Pay Slip', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(required=True, index=True, default=10)
    code = fields.Char(required=True, help="The code that can be used in the salary rules")
    number_of_days = fields.Float(string='Number of Days')
    number_of_hours = fields.Float(string='Number of Worked Hours')
    number_of_ot_hours = fields.Float(string='Number of Overtime Hours')
    number_of_ded_hours = fields.Float(string='Number of Deduction Hours')
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True,
        help="The contract for which applied this input")

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    date_start = fields.Date(string='Date From', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, default=lambda self: self.env['hr.payslip']._get_contract_date_from())
    date_end = fields.Date(string='Date To', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env['hr.payslip']._get_contract_date_to())
    journal_id = fields.Many2one('account.journal', 'Salary Journal', states={'draft': [('readonly', False)]}, readonly=True,
        required=True, default=lambda self: self.env['account.journal'].search([('name', 'ilike', 'salary')], limit=1))

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # @api.multi
    # def compute_sheet(self):
    #     for payslip in self:
    #         attendance_summaries = self.env['hr.attendance.summary'].search([
    #             ('employee_id', '=', payslip.employee_id.id),
    #             ('date_from', '>=', payslip.date_from),
    #             ('check_date', '<=', payslip.date_to),
    #             ('state','=','draft')
    #         ])
    #         payslip.attendance_summary_ids = [(6, 0, attendance_summaries.ids)]
    #         payslip.update_worked_days_lines()
    #
    #     res = super(HrPayslip, self).compute_sheet()
    #     return res

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        # res = super(HrPayslip, self)._onchange_employee()
        for payslip in self:
            attendance_summaries = self.env['hr.attendance.summary'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('date_from', '>=', payslip.date_from),
                ('check_date', '<=', payslip.date_to),
                ('state', '=', 'draft')
            ])
            payslip.attendance_summary_ids = [(6, 0, attendance_summaries.ids)]
            payslip.update_worked_days_lines()

        return {}

    def update_worked_days_lines(self):
        self.ensure_one()

        if not self.contract_id:
            return

        attendance_summaries = self.attendance_summary_ids
        # weekdays_overtime_hours = sum(attendance_summaries.mapped('weekdays_overtime_hours'))
        # weekend_overtime_hours = sum(attendance_summaries.mapped('weekend_overtime_hours'))
        # public_holiday_overtime_hours = sum(attendance_summaries.mapped('public_holiday_overtime_hours'))

        # weekdays_ot_work_entry = self.env.ref('hr_payroll_attendance.hr_work_entry_type_weekdays_overtime')
        # weekend_ot_work_entry = self.env.ref('hr_payroll_attendance.hr_work_entry_type_weekend_overtime')
        # public_holiday_ot_work_entry = self.env.ref('hr_payroll_attendance.hr_work_entry_type_public_holiday_overtime')

        # Remove Existing
        for summary in attendance_summaries:
            for line in summary.manual_line_ids:
                existing = self.worked_days_line_ids.filtered(lambda x: x.work_entry_type_id.id == line.work_entry_type_id.id)
                existing.unlink()

        # Insert New
        lines = []
        for summary in attendance_summaries:
            for line in summary.manual_line_ids:
                lines.append({
                    'sequence': line.work_entry_type_id.sequence,
                    'work_entry_type_id': line.work_entry_type_id.id,
                    'number_of_days': 0,
                    'number_of_hours': line.no_of_hours,
                    'calc_rate': line.work_entry_type_id.is_calculation and line.work_entry_type_id.calc_rate or 0,
                })

        self.write({'worked_days_line_ids': [(0, 0, x) for x in lines]})

    # @api.multi
    # def refresh_payslip(self):
    #     # print "refresh_payslip claled ***********************"
    #     old_input_lines = self.env['hr.payslip'].browse(self.id).input_line_ids
    #     old_values = {}
    #     for old_input_line in old_input_lines:
    #         old_values[old_input_line.code] = old_input_line.amount
    #
    #     self.onchange_employee()
    #
    #     for input_line in self.input_line_ids:
    #         input_line.write({'amount': old_values.get(input_line.code,0.0) })
    #
    #     return True
    
    def _get_payslip_days(self):
        company_id = self.env.user.company_id.id
        # ir_values = self.env['ir.values']
        # payslip_day_from = ir_values.get_default('hr.payroll.config.settings', 'payslip_day_from_setting', company_id=company_id)
        # payslip_day_to = ir_values.get_default('hr.payroll.config.settings', 'payslip_day_to_setting', company_id=company_id)

        payslip_day_from = self.env['ir.config_parameter'].sudo().get_param('payslip_day_from_setting')
        payslip_day_to = self.env['ir.config_parameter'].sudo().get_param('payslip_day_to_setting')

        return payslip_day_from, payslip_day_to
    
    def _get_contract_date_from(self):
        user_obj = self.env['res.users']
        date_from = time.strftime('%Y-%m-01')
        
        payslip_day_from, payslip_day_to = self._get_payslip_days()
        if payslip_day_from and payslip_day_to:
            if int(payslip_day_from) < int(payslip_day_to):
                date_from = time.strftime('%Y-%m-' + payslip_day_from)
            else:
                date_from = str(datetime.now() + relativedelta.relativedelta(months=-1, day=int(payslip_day_from)))[:10]
        return date_from
    
    def _get_contract_date_to(self):
        user_obj = self.env['res.users']
        date_to = str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
        
        payslip_day_from, payslip_day_to = self._get_payslip_days()
        if payslip_day_from and payslip_day_to:
            date_to = time.strftime('%Y-%m-' + payslip_day_to)

        return date_to


    date_from = fields.Date(string='Date From', readonly=True, required=True,
        default=_get_contract_date_from, states={'draft': [('readonly', False)]})
    date_to = fields.Date(string='Date To', readonly=True, required=True,
        default=_get_contract_date_to,
        states={'draft': [('readonly', False)]})
    attendance_line_ids = fields.One2many('hr.payslip.attendance', 'payslip_id',
        string='Payslip Attendance', copy=True, readonly=True,
        states={'draft': [('readonly', False)]})
    journal_id = fields.Many2one('account.journal', 'Salary Journal', readonly=True, required=True,
        states={'draft': [('readonly', False)]}, default=lambda self: self.env['account.journal'].search([('name', 'ilike', 'salary')], limit=1))
    # attendance_summary_id = fields.Many2one('hr.attendance.summary', string='Attendance Summary')
    attendance_summary_ids = fields.One2many('hr.attendance.summary', 'payslip_id', string='Attendance Summary', copy=False)

    # def _get_worked_day_lines(self, domain=None, check_out_of_contract=True):
    #     res = super(HrPayslip, self)._get_worked_day_lines(domain=domain, check_out_of_contract=check_out_of_contract)
    #
    #
    #
    #
    #     # block
    #
    #     return res

    # @api.model
    # def get_worked_day_lines(self, contract_ids, date_from, date_to):
    #     res = super(HrPayslip, self).get_worked_day_lines(contract_ids, date_from, date_to)
    #
    #     for contract in self.env['hr.contract'].browse(contract_ids).filtered(lambda contract: contract.working_hours):
    #         attendance_summaries = self.attendance_summary_ids
    #         print(attendance_summaries)
    #         if not attendance_summaries:
    #             attendance_summaries = self.env['hr.attendance.summary'].search([
    #                 ('employee_id', '=', contract.employee_id.id),
    #                 ('date_from', '>=', date_from),
    #                 ('check_date', '<=', date_to),
    #                 ('state', '=', 'draft')
    #             ])
    #         if not attendance_summaries:
    #             if contract.attendance_mode != 'na':
    #                 attendances = {
    #                     'name': _("Absent Days"),
    #                     'sequence': 5,
    #                     'code': 'ABSENT',
    #                     'number_of_days': contract.calc_days,
    #                     'number_of_hours': 0.0,
    #                     'contract_id': contract.id,
    #                 }
    #                 res.append(attendances)
    #             continue
    #
    #         worked_days = sum(attendance_summaries.mapped('worked_days'))
    #         worked_hours_total_compute = sum(attendance_summaries.mapped('worked_hours_total_compute'))
    #         absent_days = sum(attendance_summaries.mapped('absent_days'))
    #         overtime_hours_compute = sum(attendance_summaries.mapped('overtime_hours_compute'))
    #         deduction_hours_compute = sum(attendance_summaries.mapped('deduction_hours_compute'))
    #
    #         weekdays_overtime_hours = sum(attendance_summaries.mapped('weekdays_overtime_hours'))
    #
    #         if worked_days:
    #             for each_res in res:
    #                 if each_res['code'] != 'WORK100':
    #                     continue
    #
    #                 each_res['name'] = 'Worked Days'
    #                 each_res['number_of_days'] = worked_days
    #                 each_res['number_of_hours'] = worked_hours_total_compute
    #
    #         if absent_days:
    #             attendances = {
    #                 'name': _("Absent Days"),
    #                 'sequence': 5,
    #                 'code': 'ABSENT',
    #                 'number_of_days': absent_days,
    #                 'number_of_hours': 0.0,
    #                 'contract_id': contract.id,
    #             }
    #             res.append(attendances)
    #
    #         if overtime_hours_compute:
    #             attendances = {
    #                 'name': _("Overtime Hours"),
    #                 'sequence': 10,
    #                 'code': 'OT',
    #                 'number_of_days': 0.0,
    #                 'number_of_hours':overtime_hours_compute,
    #                 'contract_id': contract.id,
    #             }
    #             res.append(attendances)
    #
    #         if deduction_hours_compute:
    #             attendances = {
    #                 'name': _("Deduction Hours"),
    #                 'sequence': 15,
    #                 'code': 'DED',
    #                 'number_of_days': 0.0,
    #                 'number_of_hours': deduction_hours_compute,
    #                 'contract_id': contract.id,
    #             }
    #             res.append(attendances)
    #
    #     return res

    def action_payslip_done(self):
        attendance_summaries = self.mapped('attendance_summary_ids')
        holidays = attendance_summaries.mapped('summary_lines').mapped('holiday_id')
        holidays.write({'payslip_status': True})
        attendance_summaries.write({'state': 'validated'})
        return super(HrPayslip, self).action_payslip_done()

    # @api.multi
    def unlink(self):
        attendance_summaries = self.mapped('attendance_summary_ids')
        holidays = attendance_summaries.mapped('summary_lines').mapped('holiday_id')
        holidays.write({'payslip_status': False})
        attendance_summaries.write({'state': 'draft'})
        return super(HrPayslip, self).unlink()
        

    
    # @api.multi
    # def onchange_employee_id(self, date_from, date_to, employee_id=False, contract_id=False):
    #     ### Customize: 1. Month name based on to date
    #     res = super(HrPayslip, self).onchange_employee_id(date_from, date_to, employee_id, contract_id)
    #
    #     ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_to, "%Y-%m-%d")))
    #     employee = self.env['hr.employee'].browse(employee_id)
    #     locale = self.env.context.get('lang') or 'en_US'
    #
    #     res['value'].update({
    #         'name': _('Salary Slip of %s for %s') % (
    #             employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))),
    #     })
    #     return res


class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    calc_rate = fields.Float(string="Overtime Rate")



