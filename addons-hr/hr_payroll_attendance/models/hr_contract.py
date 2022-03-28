from odoo import api, fields, models, _
from datetime import datetime, timedelta
from itertools import compress
import calendar

# import pandas as pd

class Contract(models.Model):
    _inherit = 'hr.contract'
    
#     working_hours = fields.Many2one('resource.calendar', string='Working Schedule', required=True)
    attendance_mode = fields.Selection([
        ('strict','Strict'),
        ('flexible','Flexible'),
        ('na','Not Applicable')
    ], string="Mode", default='flexible', required=True)
    ot_ded_calc_cycle = fields.Selection([
        ('daily', 'Daily'), ### Take into consideration lag time
        ('monthly', 'Monthly'), ### Does calculation on monthly basis
    ], string="Calc. Cycle", default='daily', required=True)
    # wage_gross = fields.Float('Gross Wage', digits=(16, 2), required=True, help="Gross Salary of the employee")
    overtime_calc = fields.Boolean(string='Overtime Calculation')
    overtime_lag = fields.Float(string='Lag (minutes)')
    deduction_calc = fields.Boolean(string='Deduction Calculation')
    deduction_lag = fields.Float(string='Ded Lag (minutes)')
    # calc_days = fields.Integer(string='Calculation Days')
    # attendance_policy_id = fields.Many2one("hr.attendance.policy")
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours',
                               help='Total hours based on Salary structure type for the employee.')

    def _compute_total_hours(self):
        for contract in self:
            if contract.resource_calendar_id and contract.resource_calendar_id.no_of_days_in_month:
                days = contract.resource_calendar_id.no_of_days_in_month
                if days == 'standard_30':
                    days = 30
                elif days == 'calendar_30':
                    today = fields.Date.today()
                    days = calendar.monthrange(today.year, today.month)
                    days = days[1]
                else:   # TODO: need to get working days here
                    days = 30
                contract.total_hours = days * 8

    def _calculate_ot_ded_hours(self, worked_hours, working_hours):
        overtime_hours = deduction_hours = 0.0
        # if self.attendance_mode == 'flexible':
        if worked_hours > 0.0: ### If not worked hours, then it will be counted as absent
            difference_in_hours = worked_hours - working_hours
            if self.overtime_calc:
                overtime_lag = self.overtime_lag / 60.0
                if difference_in_hours >= overtime_lag:
                    overtime_hours = difference_in_hours
            if self.deduction_calc:
                deduction_lag = self.deduction_lag / 60.0
                if (difference_in_hours * -1) >= deduction_lag:
                    deduction_hours = difference_in_hours * -1

        return overtime_hours, deduction_hours

    def get_non_working_intervals_data(self, interval_data):
        non_working_interval_data = []
        if not interval_data:
            return non_working_interval_data

        count = 1
        for each_interval_data in interval_data:
            if count == 1:
                day_begin_dt = each_interval_data[0].replace(hour=0, minute=0, second=0)
                if (each_interval_data[0] - day_begin_dt).seconds / 60 > 0:
                    non_working_interval_data.append((day_begin_dt, each_interval_data[0] - timedelta(minutes=1)))

            count += 1




    def get_working_intervals_data(self, date_from, date_to):
        def was_on_leave_interval(employee_id, date_from, date_to):
            date_from = fields.Datetime.to_string(date_from)
            date_to = fields.Datetime.to_string(date_to)
            return self.env['hr.holidays'].search([
                ('state', '=', 'validate'),
                ('employee_id', '=', employee_id),
                ('type', '=', 'remove'),
                ('date_from', '<=', date_from),
                ('date_to', '>=', date_to)
            ], limit=1)

        interval_data = []
        day_from = fields.Datetime.from_string(date_from)
        day_to = fields.Datetime.from_string(date_to)
        nb_of_days = (day_to - day_from).days + 1

        # Gather all intervals and holidays
        for day in range(0, nb_of_days):
            working_intervals_on_day = self.employee_id.calendar_id.get_working_intervals_of_day(
                start_dt=day_from + timedelta(days=day))
            for interval in working_intervals_on_day:
                interval_data.append(
                    (interval, was_on_leave_interval(self.employee_id.id, interval[0], interval[1])))

        return interval_data

    def _get_flexi_worked_hours(self, attendances, working_hours):
        net_worked_hours = sum(attendances.mapped('worked_hours'))
        flex_break_hours = self.working_hours.flexible_daily_break
        if flex_break_hours:
            first_in_dt = fields.Datetime.from_string(attendances[0].check_in)
            last_out_dt = fields.Datetime.from_string(attendances[-1].check_out)
            gross_worked_hours = (last_out_dt - first_in_dt).seconds / 3600.0
            if gross_worked_hours > working_hours:
                break_taken_hours = gross_worked_hours - net_worked_hours
                if break_taken_hours < flex_break_hours:
                    net_worked_hours -= (flex_break_hours - break_taken_hours)
        return net_worked_hours

    def _get_strict_worked_hours(self, attendances, interval_data, working_hours):
        if not interval_data:
            return sum(attendances.mapped('worked_hours'))

        # working_hours = working_hours - self.grace_period / 60.0 ### Already deducted from calling function
        ### Form pandas interval array
        clean_interval_data = []
        interval_position_dict = {}
        count = 1
        for each_interval_data in interval_data[0]:
            clean_interval_data.append(each_interval_data[0:-1])
            interval_position_dict[each_interval_data[-2]] = count
            count += 1
        intervals_pd = pd.arrays.IntervalArray.from_tuples(clean_interval_data)

        final_worked_hours = 0.0
        overtime_hours = 0.0
        for attendance in attendances:
            check_in_dt = fields.Datetime.from_string(attendance.check_in)
            check_out_dt = fields.Datetime.from_string(attendance.check_out)
            overlap_interval_mask = intervals_pd.overlaps(pd.Interval(check_in_dt, check_out_dt))
            applicable_intervals = list(compress(clean_interval_data, overlap_interval_mask))

            for applicable_interval in applicable_intervals:
                interval_start = applicable_interval[0]
                interval_end = applicable_interval[1]
                last_interval = interval_position_dict[interval_end] == len(interval_data[0])
                strict_check_in_dt = check_in_dt
                strict_check_out_dt = check_out_dt

                if check_in_dt < interval_start:
                    strict_check_in_dt = interval_start

                if check_out_dt > interval_end:
                    strict_check_out_dt = interval_end

                    if last_interval and self.overtime_calc:
                        overtime_hours +=  (check_out_dt - interval_end).seconds / 3600.0

                final_worked_hours += (strict_check_out_dt - strict_check_in_dt).seconds / 3600.0

        # if final_worked_hours < working_hours:
        final_worked_hours = min(working_hours, final_worked_hours)

        return final_worked_hours + overtime_hours
