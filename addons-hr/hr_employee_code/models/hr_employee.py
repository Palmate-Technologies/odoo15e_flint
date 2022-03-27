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
    _inherit = 'hr.employee'
    
    registration_number = fields.Char('Code')

    def name_get(self):
        res = []
        for employee in self:
            res.append((employee.id, '%s%s' % (employee.registration_number and '[%s] ' % employee.registration_number or '', employee.name)))
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('registration_number', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    def set_partner_employee_codes(self):
        for employee in self:
            partner_id = employee.address_home_id
            if not partner_id:
                continue
            partner_id.write({'ref': employee.registration_number})

    @api.model
    def create(self, values):
        res = super(HrEmployee, self).create(values)
        res.set_partner_employee_codes()
        return res

    def write(self, values):
        res = super(HrEmployee, self).write(values)
        if "registration_number" in values or "address_home_id" in values:
            self.set_partner_employee_codes()
        return res

