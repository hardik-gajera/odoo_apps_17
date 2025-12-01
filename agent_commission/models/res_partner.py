# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_agent = fields.Boolean('Agent')
    commission_ids = fields.One2many('commission.define', 'agent_id', string='Commission')


class CommissionDefine(models.Model):
    _name = 'commission.define'

    calculation = fields.Selection([('percentage', 'Percentage'),
                                    ('fixed', 'Fixed')], string="Calculation Based")
    amount = fields.Float("Amount")
    agent_id = fields.Many2one('res.partner', "Agent")

    @api.constrains('amount')
    def check_amount_value(self):
        if self.calculation == 'percentage' and not 0 < self.amount < 100:
            raise Warning(_('Please enter the valid percentage.'))
