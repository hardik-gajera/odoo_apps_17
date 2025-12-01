# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_ids = fields.One2many('commission.calculation', 'sale_id', string='Commission', compute='calculate_agent_commission', store=True)
    agent_id = fields.Many2one('res.partner', string='Agent', domain=[('is_agent', '=', True)])

    @api.depends('agent_id', 'order_line')
    def calculate_agent_commission(self):
        if self.agent_id and self.agent_id.commission_ids:
            amount = (self.amount_total * self.agent_id.commission_ids[0].amount)/100 if self.agent_id.commission_ids[0].calculation == 'percentage' else self.agent_id.commission_ids[0].amount
            if not self.commission_ids:
                self.commission_ids = [(0, 0, {'calculation': self.agent_id.commission_ids[0].calculation,
                                               'amount': amount})]
            else:
                self.commission_ids.calculation = self.agent_id.commission_ids[0].calculation
                self.commission_ids.amount = amount

    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        if self.agent_id:
            commission = self.env['agent.commission'].sudo().create({'date': datetime.now().date(),
                                                                        'agent_id': self.agent_id.id,
                                                                        'amount': self.commission_ids[0].amount,
                                                                        'state': 'draft'})



class CommissionCalculation(models.Model):
    _name = 'commission.calculation'

    sale_id = fields.Many2one('sale.order')
    calculation = fields.Selection([('percentage', 'Percentage'),
                                    ('fixed', 'Fixed')], string="Calculation Based")
    amount = fields.Float("Amount")