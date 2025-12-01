# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            enable_amount_rounding=bool(params.get_param('enable_amount_rounding')),
            account_id=int(params.get_param('account_id')),
        )
        return res

    def set_values(self):
        res = super(ResConfigSetting, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('enable_amount_rounding', self.enable_amount_rounding)
        params.set_param('account_id', self.account_id.id)

    enable_amount_rounding = fields.Boolean('Enable Rounding')
    account_id = fields.Many2one('account.account', string="Rounding Account")
