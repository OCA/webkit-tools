# -*- coding: utf-8 -*-
# © 2015 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Report Archive",
    "description":"""
This module extends the functionality of webkit_report and allows you to
archive the reports to be printed into the file system of the same machine
that is running the OpenERP instance. The directory must exist.

Configuration
------------
* Add the system parameter "archive_reports_path" with the path. The directory
  must exist

* Configure the reports: Go to Actions -> Reports. Two new fields will be
  displayed: "Archive the file" and "Save as File Prefix".
  Select those reports that you want to be stored by clicking
  the "Archive the File" flag and set a name for each by typing into the
  "Save as File Prefix" field.
  You can use python expression e.g. object.name.


Usage
------------
Just print the report as usual. Apart from the report returned to the
browser a copy of it will be saved in the specified directory.

Contributors
------------
 * Federico Javier Mesa Hidalgo (javier.mesa@braintec-group.com)
 * Kumar Aberer (kumar.aberer@braintec-group.com)

    """,
    "summary": """
    This module saves the PDF of any webkit report to the file system.
    """,
    "version": "1.0",
    "category": "Reports/Webkit",
    "website": "https://odoo-community.org/",
    "author": "brain-tec AG, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "images": False,
    "installable": True,
    "depends": [
        "base",
        "report_webkit",
    ],
    'data': [
        'view/ir_actions_ext.xml',
    ],
}
