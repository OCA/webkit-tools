{
    "name" : "Report Archive",
    "summary": "This module saves the reports to be printed in a directory specified in the system parameters.",
    "version" : "1.0",
    "category" : "Uncategorized",
    "website": "https://odoo-community.org/",
    "author" : "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends" : [
                 "base",
                 "report_webkit",
    ],
    'data': [
             'view/ir_actions_ext.xml'
    ]
}
