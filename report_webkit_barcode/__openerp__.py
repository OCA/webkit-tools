# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Webkit Report Barcode',
    'version': '0.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'FIXMEFIXMEFIXME',
    'summary': 'Adds a barcode helper to webkit reports',
    'description': """
Add barcodes in webkit reports
==============================

Usage
-----
To embed a barcode image in a webkit report, use ``${helper.barcode(value)}``.
Depending on template filtering, you might need to force not to use any filter
by doing ``${helper.barcode(value) | u}``

The function is defined as::
  barcode(value, code='Code128', drawOpts=None, htmlAttrs=None)

Parameters
---------
value
  Value for barcode as expected by barcode type. Code128 takes a number or
  numeric string
code
  barcode type. ReportLab 2.5 has the following codes: Codabar, Code11,
  Code128, EAN13, EAN8, Extended39, Extended93, FIM, I2of5, MSI, POSTNET, QR,
  Standard39, Standard93, USPS_4State
drawOpts
  dictionary of options for reportlab graphic. Depends on barcode type. Use
  *format* to specify image format (default png), *width* to specify image
  width in pixels (int), *height* to specify image height in pixels (int)
htmlAttrs
  dictionary of html attributes

Requirements
------------
This module depends on reportlab and lxml, which are both part of the odoo
installation.

Contributors
------------
* Vincent Vinet (vincent.vinet@savoirfairelinux.com)
""",
    'depends': [
        'report_webkit',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
