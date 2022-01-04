# -*- coding : utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderUpdate(models.Model):
	_inherit = 'sale.order'

	invoiced_amount = fields.Float('Project Invoiced Value' ,compute ='_compute_invoice_amount')
	invoiced_amount_due = fields.Float('Invoiced Amount Due',compute ='_compute_invoiced_amount_due')
	remaining_value = fields.Float('Remaining Value',compute ='_compute_remaining_value', help='SO value(untaxed) - Invoiced Value')
	paid_amount = fields.Float('Paid Amount',compute ='_compute_amount_paid')
	amount_paid_percent = fields.Float(compute = 'action_amount_paid')

	def _compute_invoice_amount(self):
		for record in self:
			invoices = self.env['account.move'].search(['&',('invoice_origin','=', record.name),'|',('state','=','draft'),('state','=','posted'),('payment_state', 'not in', ['reversed', 'invoicing_legacy'])])
			total = 0

			if invoices:
				for invoice in invoices:
					total += invoice.amount_untaxed
					record.invoiced_amount = total
			else:
				record.invoiced_amount = total


	@api.depends('paid_amount','invoiced_amount', 'invoiced_amount_due')
	def _compute_invoiced_amount_due(self):
		for record in self:
			invoices = self.env['account.move'].search(['&',('invoice_origin','=', record.name),'|',('state','=','draft'),('state','=','posted'),('payment_state', 'not in', ['reversed', 'invoicing_legacy'])])
			amount = 0

			if invoices:
				for inv in invoices:
					if inv.amount_residual !=0 and inv.amount_tax>0:
						amount  += inv.amount_residual - inv.amount_tax
					else:
						amount += inv.amount_residual

					record.invoiced_amount_due = amount
			else:
				record.invoiced_amount_due = amount



	@api.onchange('invoiced_amount','amount_due')
	def _compute_amount_paid(self):
		self.paid_amount = float(self.invoiced_amount) - float(self.invoiced_amount_due)

	@api.onchange('amount_untaxed','invoiced_amount')
	def _compute_remaining_value(self):
		self.remaining_value = float(self.amount_untaxed) - float(self.invoiced_amount)


	@api.depends('paid_amount','invoiced_amount')
	def action_amount_paid(self):
		if self.invoiced_amount :
			self.amount_paid_percent = round(100 * self.paid_amount / self.invoiced_amount, 3)
		return self.amount_paid_percent

