# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AgentCommission(models.Model):
    _name = 'agent.commission'

    name = fields.Char('Reference')
    agent_id = fields.Many2one('res.partner', string='Agent Commission')
    date = fields.Date(string='Date')
    amount = fields.Float(string='Amount')
    state = fields.Selection([('draft', 'Draft'),
                              ('paid', 'Paid'),
                              ('cancelled', 'Cancelled')], string='State')

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('agent.commission')
        return super(AgentCommission, self).create(values)

    def cancel_commission(self):
        if self.state == 'draft':
            self.state = 'cancelled'
