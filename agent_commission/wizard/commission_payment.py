# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api


class CommissionPayment(models.TransientModel):
    _name = 'commission.payment'

    agent_id = fields.Many2one('res.partner', 'Agent')
    commission_ids = fields.Many2many('agent.commission', 'agent_commission_rel', string='Commissions')

    @api.onchange('agent_id')
    def _onchange_agent(self):
        if self.agent_id:
            commission_ids = self.env['agent.commission'].sudo().search([('agent_id', '=', self.agent_id.id), ('state', '=', 'draft')])
            self.commission_ids = [(6, 0, commission_ids.ids)]

    def confirm_payment(self):
        amount = sum(self.commission_ids.mapped('amount'))
        journal_id = self.env['account.journal'].search(
            [('type', '=', 'bank')], limit=1)
        invoice_id = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.agent_id.id,
            'invoice_date': date.today(),
            'date': date.today(),
            'invoice_line_ids': [(0, 0, {
                'quantity': 1,
                'name': 'Agent Commission',
                'price_unit': amount,
            })]
        })
        if invoice_id:
            invoice_id.sudo().action_post()
            payment_vals = {'date': date.today(),
                            'amount': amount,
                            'payment_type': 'outbound',
                            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                            'partner_type': 'supplier',
                            'ref': invoice_id.name,
                            'journal_id': journal_id.id,
                            'partner_id': self.agent_id.id,
                            'reversal_move_id': [(4, invoice_id.id)]
                            }
            payment = self.env['account.payment'].create(payment_vals)
            payment.action_post()
            for each in self.commission_ids:
                each.state = 'paid'