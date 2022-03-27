from datetime import datetime, timedelta
from odoo import models, fields, api, _
# from odoo.tools import convert_utc_date_to_current
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError

from collections import defaultdict

class HrAttendanceSummaryLine(models.Model):
    _name = "hr.attendance.summary.line"
    _description = "HR Attendance Summary Lines"

    @api.depends('working_hours','worked_hours','adjustment_ids.state')
    def _compute_worked_hours_summary_line(self):
        for summary_line in self:
            summary = summary_line.summary_id
            overtime_hours = deduction_hours = 0.0
            if summary.contract_id.attendance_mode != 'na':
                if summary.ot_ded_calc_cycle == 'daily' and not summary_line.holiday_id:
                    overtime_hours, deduction_hours = summary.contract_id._calculate_ot_ded_hours(summary_line.worked_hours + summary_line.adjustment_hours, summary_line.working_hours)

            summary_line.update({
                'overtime_hours': overtime_hours,
                'deduction_hours': deduction_hours
            })

    @api.depends('adjustment_ids.state')
    def _compute_adjustment_hours(self):
        for summary_line in self:
            if summary_line.summary_id.contract_id.attendance_mode == 'na':
                continue
            approved_adjustments = summary_line.adjustment_ids.filtered(lambda a: a.state == 'approved')
            summary_line.adjustment_hours = sum(approved_adjustments.mapped('additional_hours'))

    @api.depends('working_hours','holiday_id','worked_hours','adjustment_hours')
    def _compute_status(self):
        for summary_line in self:
            status = 'attendance'
            # if summary_line.public_holiday_line_id:
            #     status = 'holiday'

            # elif summary_line.holiday_id:
            if summary_line.holiday_id:
                status = summary_line.holiday_id.holiday_status_id.name.lower().strip() == 'unpaid' and 'unpaid' or 'leave'

            elif summary_line.working_hours == 0.0:
                status = 'weekend'

            elif summary_line.worked_hours + summary_line.adjustment_hours == 0.0:
                status = 'absent'
            summary_line.status = status

    attendance_date = fields.Date(string='Date')
    dayofweek = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ], 'Day of Week', required=True, default='6')
    working_hours = fields.Float(string='Working Hours', help="Workig hours based on resource calendar.")
    worked_hours = fields.Float(string='Worked Hours')
    overtime_hours = fields.Float(string='Overtime Hours', compute='_compute_worked_hours_summary_line', store=True)
    deduction_hours = fields.Float(string='Deduction Hours', compute='_compute_worked_hours_summary_line', store=True)
    adjustment_hours = fields.Float(string='Adjustment Hours', compute='_compute_adjustment_hours', store=True,
                                    help="Adjustment hours subject to manager approval.")
    status = fields.Selection([('attendance','Attendance'),('weekend','Weekend'),('absent','Absent'),
        ('leave','Paid Leave'),('unpaid','Unpaid Leave'),('holiday','Public Holiday')],
        'Status', compute='_compute_status', store=True)
    attendance_ids = fields.One2many('hr.attendance', 'attendance_summary_line_id', string='Attendance')
    # holiday_id = fields.Many2one('hr.holidays', string='Paid Leaves')
    holiday_id = fields.Many2one('hr.leave', string='Paid Leaves')
    # public_holiday_line_id = fields.Many2one('hr.holidays.public.line', string='Public Holiday Line')
    adjustment_ids = fields.One2many('hr.attendance.adjustment', 'summary_line_id', string='Adjustments')
    summary_id = fields.Many2one('hr.attendance.summary', 'Attendance Summary', required=True, ondelete='cascade')
    state = fields.Selection([
		('draft', 'Draft'),
		('validated', 'Validated')
    ], related='summary_id.state', string='Status', readonly=True, copy=False, store=True, default='draft')

    # def get_convert_utc_date_to_current_attendance_ids_check_in(self):
    #     dt = convert_utc_date_to_current(sorted(self.attendance_ids, key=lambda at: at.check_in)[0].check_in, self.env.user.tz or self.env.context.get('tz', 'Asia/Riyadh'))
    #     tm = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    #     return tm.strftime('%H:%M:%S')
    #
    # def get_convert_utc_date_to_current_attendance_ids_check_out(self):
    #     dt = convert_utc_date_to_current(sorted(self.attendance_ids, key=lambda at: at.check_in)[-1].check_out, self.env.user.tz or self.env.context.get('tz', 'Asia/Riyadh'))
    #     tm = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    #     return tm.strftime('%H:%M:%S')

    def create_adjustment_entry(self):
        if self.summary_id.contract_id.attendance_mode == 'na':
            raise UserError(_("You cannot create adjustment entries for NA attendance mode."))

        view_id = self.env.ref('hr_payroll_attendance.view_attendance_adjustment_form').id
        context = self._context.copy()
        context.update({
            'default_adjustment_date': self.attendance_date,
            'default_employee_id': self.summary_id.employee_id.id,
            'default_summary_line_id': self.id,
            'editing_summary': True
        })
        return {
            'name': 'Attendance Adjustment',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'hr.attendance.adjustment',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            # 'res_id': self.id,
            # 'target': 'new',
            'context': context,
        }


class HrAttendanceSummary(models.Model):
    _name = "hr.attendance.summary"
    _description = "HR Attendance Summary"
    _order = "check_date desc, id"

    # @api.multi
    @api.depends('check_date', 'employee_id')
    def name_get(self):
        result = []
        for summary in self:
            name = summary.employee_id.name + ': ' + str(summary.check_date)
            result.append((summary.id, name))
        return result
    
    @api.depends('summary_lines', 'summary_lines.adjustment_hours')
    def _compute_worked_hours_summary(self):
        # print "inside _compute_worked_hours_summary: ",self.overtime_hours, self.deduction_hours
        for attendance_summary in self:
            summary_lines = attendance_summary.summary_lines
            contract = attendance_summary.contract_id
            overtime_hours = deduction_hours = 0.0
            total_worked_hours = sum(summary_lines.mapped('worked_hours')) + \
                                 sum(summary_lines.mapped('adjustment_hours'))
            worked_days = len(summary_lines.filtered(lambda l: l.status not in ('absent','unpaid')))
            absent_days = len(attendance_summary.summary_lines.filtered(lambda l: l.status in ('absent')))
            if contract.attendance_mode == 'na':
                overtime_hours = deduction_hours = 0.0
                absent_days = 0

            elif contract.ot_ded_calc_cycle == 'monthly':
                total_working_hours = sum(attendance_summary.summary_lines.
                    filtered(lambda l: l.status not in ('absent','leave','unpaid')).mapped('working_hours'))
                overtime_hours, deduction_hours = contract._calculate_ot_ded_hours(total_worked_hours, total_working_hours)

            elif contract.ot_ded_calc_cycle == 'daily':
                overtime_hours = sum(attendance_summary.summary_lines.mapped('overtime_hours'))
                deduction_hours = sum(attendance_summary.summary_lines.mapped('deduction_hours'))

            attendance_summary.update({
                'worked_hours_total_compute': total_worked_hours,
                'overtime_hours_compute': overtime_hours,
                'deduction_hours_compute': deduction_hours,
                'worked_days': worked_days,
                'absent_days': absent_days
            })

    date_from = fields.Date(string='Date From', readonly=True)
    check_date = fields.Date(string="Date To", readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    contract_id = fields.Many2one('hr.contract', string='Contract', related='employee_id.contract_id')
    attendance_mode = fields.Selection([
        ('strict', 'Strict'),
        ('flexible', 'Flexible'),
        ('na', 'Not Applicable')
    ], string="Mode", related='contract_id.attendance_mode')
    ot_ded_calc_cycle = fields.Selection(string="Calc. Cycle", related='contract_id.ot_ded_calc_cycle')
    worked_hours_total_compute = fields.Float(string='Worked Hours', compute='_compute_worked_hours_summary', store=True)
    overtime_hours_compute = fields.Float(string='Overtime Hours', compute='_compute_worked_hours_summary', store=True)
    deduction_hours_compute = fields.Float(string='Deduction Hours', compute='_compute_worked_hours_summary', store=True)
    ### Old fields
    worked_hours_total = fields.Float(string='Worked Hours')
    overtime_hours = fields.Float(string='Overtime Hours')
    deduction_hours = fields.Float(string='Deduction Hours')

    # Overtime
    # weekdays_overtime_hours = fields.Float(string="Overtime Hours (Weekdays)")
    # weekend_overtime_hours = fields.Float(string="Overtime Hours (Weekend)")
    # public_holiday_overtime_hours = fields.Float(string="Overtime Hours (Public Holiday)")
    manual_line_ids = fields.One2many("hr.attendance.summary.manual", "summary_id")

    ### Old fields
    worked_days = fields.Integer(string='Worked Days', compute='_compute_worked_hours_summary', store=True)
    absent_days = fields.Integer(string='Absent Days', compute='_compute_worked_hours_summary', store=True)
    company_id = fields.Many2one('res.company', 'Company',store=True)
    summary_lines = fields.One2many('hr.attendance.summary.line', 'summary_id', string='Summary Lines')
    payslip_id = fields.Many2one('hr.payslip', string='Pay Slip', ondelete='set null', index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
    ], string='Status', readonly=True, copy=False, index=True, default='draft')
    
    _sql_constraints = [
        ('check_date_employee_id_uniq', 'unique (check_date, employee_id)', 'The summary date and employee must be unique !'),
    ]

    def _update_attendance_summary(self, domain_summary, emp_attendance_data, date_from, date_to):
        ### Delete already existing summary data during that range
        unlink_summary = self.search(domain_summary)
        unlink_summary.unlink()

        day_from = fields.Datetime.from_string(date_from)
        day_to = fields.Datetime.from_string(date_to)
        nb_of_days = (day_to - day_from).days + 1
        payslip_years = list(set([day_from.strftime("%Y"), day_to.strftime("%Y")]))

        attendance_start_hour = self.env['ir.values'].get_default(
            'hr.attendance',
            'attendance_start_hour_setting',
            company_id=self.env.user.company_id.id
        ) or 0.0
        td = timedelta(hours=attendance_start_hour)

        ### Existing Adjustments
        adjustment_dict = self.env['hr.attendance.adjustment']._fetch_adjustment_data_dict(day_from, day_to)

        for employee, attendances in emp_attendance_data.iteritems():
            contract = employee.contract_id
            att_day_wise = defaultdict(lambda: self.env['hr.attendance'])
            for attendance in attendances:
                check_in_user_tz = convert_utc_date_to_current(attendance.check_in, self.env.context.get('tz', 'Asia/Riyadh'))
                key = (datetime.strptime(check_in_user_tz, DEFAULT_SERVER_DATETIME_FORMAT) - td).strftime(DEFAULT_SERVER_DATE_FORMAT)
                # key = datetime.strptime(check_in_user_tz, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                att_day_wise[key] |= attendance

            summary_lines_vals = []
            interval_data = contract.get_working_intervals_data(date_from, date_to)
            interval_data_dict = defaultdict(lambda: [[], self.env['hr.holidays']])
            for i in interval_data:
                interval_data_dict[i[0][0].strftime('%Y-%m-%d')][0].append(i[0])
                interval_data_dict[i[0][0].strftime('%Y-%m-%d')][1] |= i[1]

            ### Get Public Holiday
            holidays_public = self.env['hr.holidays.public']
            holidays_public_line = self.env['hr.holidays.public.line']
            # for payslip_year in payslip_years:
            #     holidays_public_line |= holidays_public.get_holidays_list(payslip_year, employee.id)

            # public_holidays_dict = {l.date: l for l in holidays_public_line}

            for day in range(0, nb_of_days):
                start_dt = day_from + timedelta(days=day)
                start_dt_str = start_dt.strftime('%Y-%m-%d')

                holiday_id = public_holiday_line_id = False
                # if start_dt_str in public_holidays_dict.keys():
                #     public_holiday_line_id = public_holidays_dict[start_dt_str].id

                ### Working Hours and Holiday
                each_interval_data = interval_data_dict.get(start_dt_str, [])
                working_hours = 0.0
                if each_interval_data:
                    intervals = each_interval_data[0]
                    holidays = each_interval_data[1]  ### Extract the first holiday

                    working_hours = 0.0
                    for interval in intervals:
                        working_hours += (interval[1] - interval[0]).total_seconds() / 3600.0

                    if holidays:
                        holiday_id = holidays[0].id
                        working_hours = 0.0

                ### Worked Hours
                start_dt_attendances = att_day_wise.get(start_dt_str, False)

                if contract.attendance_mode != 'strict':
                    worked_hours = start_dt_attendances and contract._get_flexi_worked_hours(start_dt_attendances, working_hours) or 0.0
                else:

                    worked_hours = start_dt_attendances and contract._get_strict_worked_hours(start_dt_attendances, each_interval_data, working_hours) or 0.0

                ### Check if there is any worked hours during holiday
                if holiday_id and worked_hours > 0.0:
                    raise UserError(_("There should not be any attendance record during leave period. \nEmployee: %s \nDate: %s") % (employee.display_name, start_dt_str))

                if public_holiday_line_id:
                    working_hours = 0.0
                    holiday_id = False

                ### Check for adjustments
                adjustment_ids = adjustment_dict.get(employee.id, {}).get(start_dt_str,False)

                summary_lines_vals.append((0, 0, {
                    'attendance_date': start_dt_str,
                    'dayofweek': str(start_dt.weekday()),
                    'working_hours': working_hours,
                    'worked_hours': worked_hours,
                    'holiday_id': holiday_id,
                    # 'public_holiday_line_id': public_holiday_line_id,
                    'attendance_ids': start_dt_attendances and [(6, 0, start_dt_attendances.ids)],
                    'adjustment_ids': adjustment_ids and [(6,0,adjustment_ids.ids)] or False
                }))

            self.create({
                'date_from': date_from,
                'check_date': date_to,
                'employee_id': employee.id,
                'company_id': employee.company_id.id,
                'summary_lines': summary_lines_vals
            })


class HrAttendanceSummaryManual(models.Model):
    _name = 'hr.attendance.summary.manual'
    _description = 'Hr Attendance Summary Manual'

    work_entry_type_id = fields.Many2one('hr.work.entry.type')
    no_of_days = fields.Float(string="No Of Days")
    no_of_hours = fields.Float(string="No Of Hours")
    summary_id = fields.Many2one("hr.attendance.summary")
