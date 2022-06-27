# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import tools
from psycopg2 import sql
import calendar
from datetime import datetime
from odoo import api, fields, models


class HrPayrollReport2(models.Model):
    _name = "hr.payroll.report2"

    employee_id = fields.Many2one('hr.employee', string='Employee')
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule')
    amount = fields.Float(string='Amount')
    slip_id = fields.Many2one('hr.payslip', string='Pay Slip')




    # def init(self):
    #     query = """
    #         SELECT
    #             p.id as id,
    #             e.id as employee_id
    #         FROM
    #             (SELECT * FROM hr_payslip) p
    #                 left join hr_employee e on (p.employee_id = e.id)
    #
    #         """
    #     #
    #     # print(122)
    #     tools.drop_view_if_exists(self.env.cr, self._table)
    #     self.env.cr.execute(sql.SQL("CREATE or REPLACE VIEW {} as ({})").format(sql.Identifier(self._table), sql.SQL(query)))


class HrPayrollReportWizard(models.TransientModel):
    _name = "hr.payroll.report2.wizard"

    def _get_default_vals(self):
        today = datetime.now().date()
        return {
            'date_from': today.replace(day=1),
            'date_to': today.replace(day=calendar.monthrange(today.year, today.month)[1]),
        }

    date_from = fields.Date(string='From', default=lambda self: self._get_default_vals()['date_from'])
    date_to = fields.Date(string='To', default=lambda self: self._get_default_vals()['date_to'])

    def button_open_report(self):
        action = self.env.ref('hr_payroll_report.payroll_report_action2').read()[0]
        self.sudo().setup_report()
        return action

    def setup_report(self):
        _table = self.env['hr.payroll.report2']._table

        self._cr.execute("DELETE FROM {};".format(_table))

        self._cr.execute("SELECT id,employee_id,date_from,date_to,state FROM hr_payslip;")

        for slip in self._cr.fetchall():
            slip_id = slip[0]
            employee_id = slip[1]
            date_from = slip[2]
            date_to = slip[3]
            state = slip[4]

            if state in ['cancel']:
                continue

            if all([
                date_from < self.date_from,
                date_to < self.date_from,
            ]):
                continue

            if all([
                date_from > self.date_to,
                date_to > self.date_to,
            ]):
                continue

            self._cr.execute("SELECT id,salary_rule_id,total FROM hr_payslip_line WHERE slip_id={};".format(slip_id))
            for line in self._cr.fetchall():
                line_id, salary_rule_id, amount = line

                query = "INSERT INTO {}(slip_id,employee_id,salary_rule_id,amount) VALUES ({},{},{},{});".format(_table, slip_id, employee_id, salary_rule_id, amount)
                self._cr.execute(query)

