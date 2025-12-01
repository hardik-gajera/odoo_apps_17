# -*- coding: utf-8 -*-

{
    'name': 'Invoice Amount Rounding',
    'version': '1.0',
    'category': 'account',
    'summary': 'Rounding Invoice Amount',
    'description': """
        This module allows you to round the total amount of invoice.
        """,
    'price': 15.00,
    'currency': 'EUR',
    "license": "LGPL-3",
    'author': 'Allene Software',
    'website': 'https://www.fiverr.com/hardikgajera82?up_rollout=true',
    'depends': ['base', 'account'],
    "data": [
        'views/res_config_view.xml',
        'views/account_view.xml',
    ],
    'images': ['static/description/odoo14_2_invoice_ss.png'],
    'installable': True,
    'auto_install': False,
}