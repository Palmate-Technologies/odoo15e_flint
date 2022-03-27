from odoo import api, fields, models, _

# class RefreshHrPayslip(models.TransientModel):
#     _name = "refresh.hr.payslip"
    
    # @api.multi
    # def action_refresh_payslip(self):
    #     # print "inside action_refresh_payslip: ",self._context
    #     paylsip_ids = self._context.get('active_ids',False)
    #     if not paylsip_ids:
    #         return True
    #
    #     payslips = self.env['hr.payslip'].browse(paylsip_ids)
    #     for payslip in payslips:
    #         payslip.refresh_payslip()
    #     return True
            