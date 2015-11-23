# -*- coding: utf-8 -*-
# © 2015 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Report Archive",
    "summary": """
    This module saves the reports to be printed
    in a directory specified in the system parameters.
    """,
    "version": "1.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "brain-tec AG, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "report_webkit",
    ],
    'data': [
        'view/ir_actions_ext.xml',
    ],
}
