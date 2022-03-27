import xlrd
import base64
from odoo.exceptions import UserError
from odoo import fields, models, api
from datetime import timedelta


def date_range(date_from, date_to):
    delta = date_to - date_from
    dates = [date_from + timedelta(days=i) for i in range(delta.days + 1)]
    return dates


# class HrAttendanceImport(models.TransientModel):
#     _inherit = 'hr.attendance.import'
#
#     def _get_contract_date_from(self):
#         return self.env['hr.payslip']._get_contract_date_from()
#
#     def _get_contract_date_to(self):
#         return self.env['hr.payslip']._get_contract_date_to()
#
#     date_from = fields.Date('Date From', required=True, default=_get_contract_date_from)
#     date_to = fields.Date('Date To', required=True, default=_get_contract_date_to)


class HrAttendanceSummaryImport(models.Model):
    _name = 'hr.attendance.summary.import'
    _description = 'Attendance Summary Import'

    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    excel_file = fields.Binary(string="Excel File")

    def action_import(self):
        self.ensure_one()
        book = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = book.sheet_by_index(0)

        for row in range(1, sheet.nrows):
            emp_code = sheet.cell(row, 0)

            if emp_code.ctype is xlrd.XL_CELL_NUMBER:
                emp_code = str(int(emp_code.value))
            employee = self.env['hr.employee'].search([('registration_number', '=', emp_code)])
            if not employee:
                raise UserError("Employee not found. Code: %s." % emp_code)

            vals = {
                'employee_id': employee.id,
                'date_from': self.date_from,
                'check_date': self.date_to,
            }

            lines = []
            for col in range(1, sheet.ncols):
                label = sheet.cell(0, col).value
                value = sheet.cell(row, col).value
                work_entry_type_id = self.env['hr.work.entry.type'].search([('code', '=', label)])

                if not work_entry_type_id:
                    raise UserError("Can't find work entry type \'%s\'" % label)

                lines.append((0, 0, {'work_entry_type_id': work_entry_type_id.id, 'no_of_hours': value}))

            vals['manual_line_ids'] = lines

            to_delete_summary = self.env['hr.attendance.summary'].search(
                [('employee_id', '=', employee.id), ('date_from', '=', self.date_from),
                 ('check_date', '=', self.date_to)])
            to_delete_summary.unlink()
            self.env['hr.attendance.summary'].create(vals)






        # hr_employee = self.env['hr.employee']
        # vals = []
        # employee_ids = []

        # data = []
        # for sheet in book.sheets():
        #     for row in range(1, sheet.nrows):
        #         values = []
        #         for col in range(sheet.ncols):
        #             value = sheet.cell(row, col)
        #             values.append(value)
        #
        #         data.append(values)
        #
        # for row in data:
        #
        #     emp_code = row[1].value
        #     if row[0].ctype is xlrd.XL_CELL_NUMBER:
        #         emp_code = str(int(row[0].value))
        #
        #     employee = hr_employee.search([('registration_number', '=', emp_code)])
        #
        #     if not employee:
        #         raise UserError("Employee not found. Code: %s." % emp_code)
        #
        #     employee_ids.append(employee.id)
        #
        #     # Empty Lines
        #     # lines = []
        #     # dates = date_range(self.date_from, self.date_to)
        #
        #     # for each in dates:
        #     #     lines.append((0, 0, {'attendance_date': each}))
        #
        #     vals.append({
        #         'employee_id': employee.id,
        #         # 'weekdays_overtime_hours': row[1].value,
        #         # 'weekend_overtime_hours': row[2].value,
        #         # 'public_holiday_overtime_hours': row[3].value,
        #         # 'summary_lines': lines,
        #         'date_from': self.date_from,
        #         'check_date': self.date_to,
        #
        #         # 'manual_line_ids': [
        #         #     (0, 0, {'work_entry_type_id': })
        #         # ]
        #
        #     })
        #
        # attendance_summary = self.env['hr.attendance.summary']
        #
        # to_delete_summary = attendance_summary.search(
        #     [('employee_id', 'in', employee_ids), ('date_from', '=', self.date_from), ('check_date', '=', self.date_to)])
        # to_delete_summary.unlink()
        # attendance_summary.create(vals)

        # block

