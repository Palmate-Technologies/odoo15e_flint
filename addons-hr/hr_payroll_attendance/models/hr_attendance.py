from odoo import fields, models, api, _
from odoo.exceptions import UserError

# def float_hour(dt):
#     minute = dt.strftime('%M')
#     minute = round(float(minute) / 60.0, 2)
#     return float(dt.strftime('%H')) + minute

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    attendance_summary_line_id = fields.Many2one('hr.attendance.summary.line', string='Summary Lines')

    # @api.multi
    def unlink(self):
        for attendance in self:
            if attendance.attendance_summary_line_id.state == 'validated':
                raise UserError(_('You cannot delete an entry which has been recorded with the payslip.'))
        super(HrAttendance, self).unlink()

