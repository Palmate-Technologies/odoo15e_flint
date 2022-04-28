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
    'name': 'HR Allowance Deduction',
    'version': '15.0.0.3',
    'summary': """ Allows to add adjustments in payslip ex Loan deduction, Traffic violation penalty etc """,
    'description': """ Allows to add adjustments in payslip ex Loan deduction, Traffic violation penalty etc """,
    'category': 'Human Resources/Payroll',
    'author': 'Palmate',
    'website': "",
    'license': 'AGPL-3',

    'depends': [
                'hr_payroll',
                'hr_work_entry_contract_enterprise',
                'hr_salary_rule_global'
                ],

    'data': [
        'security/ir.model.access.csv',
        # 'data/hr_adjustment_data.xml',
        'views/other_hr_payslip.xml',
        'views/hr_payslip_view.xml',
        'wizard/mass_approve_adjustment.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}