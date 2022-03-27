from odoo import fields, models, api, _
from lxml import etree
# from odoo.osv.orm import setup_modifiers
from collections import defaultdict
from odoo.exceptions import UserError


class HrAttendanceAdjustment(models.Model):
    _name = "hr.attendance.adjustment"
    _description = "Attendance Adjustment"
    _order = "adjustment_date desc"

    # @api.multi
    @api.depends('adjustment_date', 'employee_id')
    def name_get(self):
        result = []
        for adjustment in self:
            name = adjustment.employee_id.name + ': ' + str(adjustment.adjustment_date)
            result.append((adjustment.id, name))
        return result

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    adjustment_date = fields.Date(string="Date", default=fields.Datetime.now, required=True)
    creating_user_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    approved_user_id = fields.Many2one('res.users', 'Approved By')
    additional_hours = fields.Float('Additional Hours')
    reason = fields.Text('Reason')
    summary_line_id = fields.Many2one('hr.attendance.summary.line', string='Summary Line')
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved')], string='Status',
        required=True, readonly=True, copy=False, default='draft')

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(HrAttendanceAdjustment, self).fields_view_get(
    #         view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #
    #     if view_type == 'form':
    #         if self._context.get('editing_summary',False):
    #             doc = etree.XML(res['arch'])
    #             node_employee = doc.xpath("//field[@name='employee_id']")[0]
    #             node_employee.set('readonly', "1")
    #             setup_modifiers(node_employee, res['fields']['employee_id'])
    #
    #             node_adjustment_date = doc.xpath("//field[@name='adjustment_date']")[0]
    #             node_adjustment_date.set('readonly', "1")
    #             setup_modifiers(node_adjustment_date, res['fields']['adjustment_date'])
    #
    #             res['arch'] = etree.tostring(doc)
    #     return res

    # @api.multi
    def approve(self):
        for adjustment in self:
            adjustment.write({'state': 'approved', 'approved_user_id': self.env.user.id})

        return True

    # @api.multi
    def set_to_draft(self):
        for adjustment in self:
            adjustment.write({'state': 'draft', 'approved_user_id': False})

    # @api.multi
    def unlink(self):
        for adjustment in self:
            if adjustment.state in ('approved'):
                raise UserError(_('Cannot delete adjustment(s) which are approved.'))
        return super(HrAttendanceAdjustment, self).unlink()

    def _fetch_adjustment_data_dict(self, day_from, day_to):
        adjustments = self.search([
            ('adjustment_date', '>=', day_from),
            ('adjustment_date', '<=', day_to)
        ])
        employees = adjustments.mapped('employee_id')
        res = {}
        for employee in employees:
            adjustment_dict = defaultdict(lambda: self.env['hr.attendance.adjustment'])
            for adjustment in adjustments.filtered(lambda a: a.employee_id == employee):
                adjustment_dict[adjustment.adjustment_date] |= adjustment

            res[employee.id] = adjustment_dict

        return res


