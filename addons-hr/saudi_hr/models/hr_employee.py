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
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    visa_no = fields.Char('Iqama Number', groups="hr.group_hr_user", tracking=True)
    visa_expire = fields.Date('Iqama Expiry Date', groups="hr.group_hr_user", tracking=True)
    work_permit_expiration_date_hijri = fields.Char('Work Permit Expiration Date (Hijri)', groups="hr.group_hr_user",
                                                    tracking=True)

    # employee_no = fields.Char(string="Employee ID")
    # name = fields.Char(translate=True)
    blood_group = fields.Char('Blood Group')
    iqama_occupation = fields.Char('Iqama Occupation')
    actual_work_trade = fields.Char('Actual Work Trade')
    actual_work_trade_arabic = fields.Char('Actual Work Trade Arabic')
    personal_email = fields.Char('Personal Email')

    # name_ar = fields.Char(string="Name in Arabic")
    # hr_responsible_id = fields.Many2one('res.users', "HR Responsible", tracking=True)
    # analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    # iqama_number = fields.Char(string="Iqama Number")
    # iqama_expiry_date = fields.Date(string="Iqama Expiry")
    # iqama_expiry_date_hijri = fields.Char(string="Iqama Expiry (Hijri)")
    # gosi_number = fields.Char(string="Gosi Number")
    # sponsor_id = fields.Many2one('hr.sponsor')

