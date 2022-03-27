from odoo import models, fields, api, _
from odoo.exceptions import UserError
from collections import defaultdict
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HrAttendanceUpdate(models.TransientModel):
    _name = "hr.attendance.update"
    _description = 'HR Attendance Update'
    
    employee_filter = fields.Selection([('all','All'),('emp','Employee')],string="Filter",default="all")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    date_from = fields.Date(string='Date From',default= lambda self: self.env['hr.payslip']._get_contract_date_from(), required=True)
    date_to = fields.Date(string='Date To', default= lambda self: self.env['hr.payslip']._get_contract_date_to(), required=True)
    
    
    # @api.multi
    def action_update_attendance(self):
        # print "inside action_update_attendance"
        attendance_obj = self.env['hr.attendance']
        attendance_summary = self.env['hr.attendance.summary']

        date_from = self.date_from
        date_to = (datetime.strptime(self.date_to, DEFAULT_SERVER_DATE_FORMAT) + timedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT)
        utc_company_date_from = attendance_obj._convert_to_utc_company_datetime(date_from)
        utc_company_date_to = attendance_obj._convert_to_utc_company_datetime(date_to)

        domain = [('check_in','>=',utc_company_date_from),('check_out','<',utc_company_date_to)]
        domain_summary = [('date_from','>=',self.date_from),('date_from','<=',self.date_to)] # Deals with only date
        conflict_test_domain = ['|', '&', '&',
            ('check_in', '>=', utc_company_date_from), ('check_in', '<', utc_company_date_to), ('check_out', '=', False),
            '&', '&',
            ('check_out', '>=', utc_company_date_from), ('check_out', '<', utc_company_date_to),('check_in', '=', False)
        ]

        if self.employee_filter == 'emp':
            domain.append(('employee_id','=',self.employee_id.id))
            domain_summary.append(('employee_id','=',self.employee_id.id))
            conflict_test_domain.append(('employee_id','=',self.employee_id.id))

        ### Search for conflict
        ### Test start
        # domain.append(('employee_id','in',(7576,8221)))
        # domain_summary.append(('employee_id','in',(7576,8221)))
        # conflict_test_domain.append(('employee_id','in',(7576,8221)))
        ### Test end
        conflict_attendances = attendance_obj.search(conflict_test_domain)
        if conflict_attendances:
            raise UserError(_('Conflict exist in attendance!!!'))
        attendances = attendance_obj.search(domain, order='employee_id, check_in')

        emp_attendance_data = defaultdict(lambda: self.env['hr.attendance'])
        for attendance in attendances:
            emp_attendance_data[attendance.employee_id] |= attendance

        attendance_summary._update_attendance_summary(domain_summary, emp_attendance_data, self.date_from, self.date_to)

        return {
            'name': _('Attendance Summary'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'hr.attendance.summary',
            'view_id': self.env.ref('hr_payroll_attendance.view_attendance_summary_tree').id,
            'type': 'ir.actions.act_window',
            # 'context': context,
            # 'target': 'new'
        }
        
    
