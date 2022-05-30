# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    def _find_mail_template(self, ):
        template_id = self.env['ir.model.data']._xmlid_to_res_id('hr_payslip_send_mail.payslip_email_template',
                                                                 raise_if_not_found=False)
        return template_id

    def action_send_payslip(self):
        # sending the payslip report to employee via email
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        hst = {
            'default_model': 'hr.payslip',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'model_description': self.with_context(lang=lang)
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': hst,
        }