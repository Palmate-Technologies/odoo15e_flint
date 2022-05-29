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
from odoo import api, fields, models


class HrPayrollReport2(models.Model):
    _name = "hr.payroll.report2"
    _auto = False

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
    employee_id2 = fields.Many2one('hr.employee', 'Employee', readonly=True)

    def init(self):
        query = """
            SELECT
                p.id as id,
                e.id as employee_id
            FROM
                (SELECT * FROM hr_payslip) p
                    left join hr_employee e on (p.employee_id = e.id)
                    
            """

        #
        # print(122)
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(sql.SQL("CREATE or REPLACE VIEW {} as ({})").format(sql.Identifier(self._table), sql.SQL(query)))
