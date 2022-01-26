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


def remove_decimal_zeros_from_number(num):
    decimal = num - int(num)
    if not decimal:
        return int(num)
    return num


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('quantity')
    def _compute_quantity_str(self):
        for record in self:
            record.quantity_str = str(remove_decimal_zeros_from_number(record.quantity))

    quantity_str = fields.Char(string='Quantity Str',compute="_compute_quantity_str")