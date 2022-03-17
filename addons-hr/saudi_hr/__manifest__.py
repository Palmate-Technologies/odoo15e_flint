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
{
    'name': 'HR Saudi',
    'version': '1.0.0.1',
    'summary': """""",
    'description': """""",
    'category': 'Base',
    'author': 'Palmate',
    'website': "",
    'license': 'AGPL-3',

    'depends': ['hr_contract', 'analytic'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_sponsor.xml',
        'views/hr_contract.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
