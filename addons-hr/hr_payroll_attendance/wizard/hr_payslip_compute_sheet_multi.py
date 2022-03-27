from odoo import api, fields, models, _

class ComputeSheetMulti(models.TransientModel):
    _name = "compute.sheet.multi"
    
    # @api.multi
    def action_compute_sheet_multi(self):
        # print "inside action_compute_sheet_multi: ",self._context
        paylsip_ids = self._context.get('active_ids',False)
        if not paylsip_ids:
            return True
        
        payslips = self.env['hr.payslip'].browse(paylsip_ids)
        draft_payslips = payslips.filtered(lambda slip: slip.state == 'draft')
        draft_payslips.compute_sheet()
        return True
            