# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api

        
class HrPayrollConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    # def _get_month_days(self):
    #     res = []
    #     for i in range(1,29):
    #         res.append((str(i),str(i)))
    #     return res
    
    # payslip_day_from_setting = fields.Selection(_get_month_days, string='Default Payslip From', required=True)
    # payslip_day_to_setting = fields.Selection(_get_month_days, string='Default Payslip To', required=True)

    # @api.model
    # def set_values(self):
    #     self.env['ir.config_parameter'].sudo().set_param('payslip_day_from_setting', self.payslip_day_from_setting)
    #     self.env['ir.config_parameter'].sudo().set_param('payslip_day_to_setting', self.payslip_day_to_setting)
    #
    #     res = super(HrPayrollConfigSettings, self).set_values()
    #     return res

    # @api.model
    # def get_values(self):
    #     res = super(HrPayrollConfigSettings, self).get_values()
    #
    #     res['payslip_day_from_setting'] = self.env['ir.config_parameter'].sudo().get_param('payslip_day_from_setting')
    #     res['payslip_day_to_setting'] = self.env['ir.config_parameter'].sudo().get_param('payslip_day_to_setting')
    #
    #     return res



    # @api.multi
    # # def set_payslip_day_from_defaults(self):
    #     return self.env['ir.values'].sudo().set_default(
    #         'hr.payroll.config.settings', 'payslip_day_from_setting', self.payslip_day_from_setting, company_id=self.env.user.company_id.id)
    #
    # @api.multi
    # def set_payslip_day_to_defaults(self):
    #     return self.env['ir.values'].sudo().set_default(
    #         'hr.payroll.config.settings', 'payslip_day_to_setting', self.payslip_day_to_setting, company_id=self.env.user.company_id.id)

