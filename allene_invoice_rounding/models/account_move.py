# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

from lxml import etree


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    rounding_move_line = fields.Boolean(string="Rounding Move Line", copy=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    round_off = fields.Float(string="Round Off", copy=False, compute='apply_round_off', store=True)
    value = 0.0

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
        res = super(AccountMove, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                       submenu=submenu)
        if view_type == 'form':
            enable_invoice_rounding = self.env['ir.config_parameter'].sudo().get_param('enable_amount_rounding')
            if not enable_invoice_rounding:
                doc = etree.XML(res['arch'])
                if doc.xpath("//button[@name='apply_round_off']"):
                    node = doc.xpath("//button[@name='apply_round_off']")[0]
                    node.set('invisible', '1')
                if doc.xpath("//label[@for='round_off']"):
                    node = doc.xpath("//label[@for='round_off']")[0]
                    node.set('invisible', '1')
                if doc.xpath("//field[@name='round_off']"):
                    node = doc.xpath("//field[@name='round_off']")[0]
                    node.set('invisible', '1')
                if doc.xpath("//button[@name='remove_round_off']"):
                    node = doc.xpath("//button[@name='remove_round_off']")[0]
                    node.set('invisible', '1')
                res['arch'] = etree.tostring(doc)
        return res

    def remove_round_off(self):
        self.round_off = 0.00
    
    @api.depends('amount_untaxed', 'amount_tax', 'invoice_line_ids')
    def apply_round_off(self):
        for each in self:
            invoice_line_list = []
            params = each.env['ir.config_parameter'].sudo()
            total_amount = round_off_value = 0.00
            total_amount = each.amount_untaxed + each.amount_tax
            enable_invoice_rounding = bool(params.get_param('enable_amount_rounding')),
            if enable_invoice_rounding:
                round_off_value = round(total_amount)
                print(round_off_value, total_amount)
                each.round_off = (round_off_value - total_amount)

    def action_post(self):
        invoice_line_list = []
        account_id = int(self.env['ir.config_parameter'].sudo().get_param('account_id'))
        credit = debit = 0.0
        if not self.round_off == 0.00:
            if not account_id:
                raise UserError(_('Please select rounding account from accounting settings.'))
            if self.round_off > 0:
                credit = self.round_off
            elif self.round_off < 0:
                debit = self.round_off
            if credit or debit:
                invoice_line_list.append((0, 0, {'name': 'Rounding Amount',
                                                 'account_id': account_id,
                                                 'tax_ids': [(6, 0, [])],
                                                 'price_unit': debit or credit,
                                                 'quantity': 1.00}))
                self.update({
                    'invoice_date': self.invoice_date,
                    'partner_id': self.partner_id,
                    'invoice_line_ids': invoice_line_list,
                })

                for line in self.line_ids:
                    if line.account_id.id == account_id:
                        line.rounding_move_line = True

        return self._post(soft=False)
