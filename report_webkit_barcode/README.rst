.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================
Webkit Report Barcode
=====================

This module Add barcodes in webkit reports

Usage
=====

To embed a barcode image in a webkit report, use ``${helper.barcode(value)}``.
Depending on template filtering, you might need to force not to use any filter
by doing ``${helper.barcode(value) | safe}``

The function is defined as:

  barcode(value, code='Code128', drawOpts=None, htmlAttrs=None)

Parameters
----------
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

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/163/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/webkit-tools/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
webkit-tools/issues/new?body=module:%20
report_webkit_barcode%0Aversion:%20
8%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Vincent Vinet <vincent.vinet@savoirfairelinux.com>
* Cristian Salamea <ovnicraft@gmail.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
