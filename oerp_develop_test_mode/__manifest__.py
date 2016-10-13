# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{
    'name': 'OpenERP - Develop - Test Mode',
    'version': '10.0.0',
    "author": "Ruchir Shukla (Bizzappdev)",
    "website": "http://bizzappdev.com",
    "category": "GenericModules",
    'sequence': 20,
    'summary': 'OpenERP - Develop Test Mode',
    'description': """
OpenERP - Develop - Test Mode
=====================

OpenERP / Odoo Module which help you to set the database for Test or Development mode.

Features:
---------

    * Set-up Test or Development environment at the level of database.
    * Provides unique mode-bar for notifying either database is in Develop mode or Test mode.
    * Mail restriction for outgoing mails.


    """,
    'images': [],
    'depends': ["web", "mail", "fetchmail"],
    'data': [
        "view/res_config_view.xml",
        "view/oerp_develope_js.xml",
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': True,
    'application': False,
    'license': 'Other proprietary',
    'js': [],
    'qweb': [
        'static/src/xml/mode.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
