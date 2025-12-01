# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
{
    'name': 'Access Restriction Using IP',
    'version': '1.0.1',
    'summary': 'It will allows only specific IP Address to logged in',
    'sequence': 15,
    'website': 'https://www.fiverr.com/hardikgajera82?up_rollout=true',
    'price': 10,
    'currency': 'EUR',
    "license": "LGPL-3",
    'author': 'Allene Software',
    'description': """
It will allows only specific IP Address to logged in
    """,
    'category': 'General',
    'images': ['static/description/main_screenshot.png'],
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/allowed_ips_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
