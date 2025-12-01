# -*- coding: utf-8 -*-


from odoo import models, api


class AgentPaymentTemplate(models.AbstractModel):
    _name = 'report.agent_commission.payment_report_template'
    _description = 'Payment Report Template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not docids:
            docids = self.env['agent.commission.payment'].browse(self.env.context.get('active_ids'))
        return {
            'data': data['commission'],
            'doc_model': 'agent.commission.payment',
            'docs': docids,
            'docs_ids': docids.ids
        }
