# -*- coding: utf-8 -*-
{
    'name': 'Agent Commission',
    'version': '1.0.1',
    'summary': 'It will allows you to Define the Agent and also allows to give the Commission to that agent',
    'sequence': 15,
    'website': 'https://www.fiverr.com/hardikgajera82?up_rollout=true',
    'price': 30,
    'currency': 'EUR',
    "license": "LGPL-3",
    'author': 'Allene Software',
    'description': """
It will allows you to Define the Agent and also allows to give the Commission to that agent.
    """,
    'category': 'General',
    'images': ['static/description/odoo14_03_calculation.png'],
    'depends': ['base', 'sale', 'account', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/agent_commission_view.xml',
        'wizard/commission_payment_view.xml',
        'wizard/commission_payment_report_view.xml',
        'report/payment_report_template.xml',
        'report/report_agent_payment.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
