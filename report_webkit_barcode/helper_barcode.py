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

import logging
_logger = logging.getLogger(__name__)

from openerp.addons.report_webkit.report_helper import WebKitHelper


def patch_helper():
    try:
        # Reportlab also has createBarcodeDrawingInMemory. Unfortunately, it
        # is broken in 2.5, so we'll have to do the same thing it does in 3.0
        from reportlab.graphics.barcode import createBarcodeDrawing
        from lxml.etree import tostring as HTML, Element
    except ImportError, e:
        _logger.warn("Failed to import required dependency: %s", e[0])
        return

    def barcode(self, value, code='Code128', drawOpts=None, htmlAttrs=None):
        """ Generate a <img /> tag with embedded barcode

        Params:
        - value: barcode value, must be valid for barcode type
        - code: barcode type, as per reportlab.graphics.barcode.getCodes()
        - drawOpts: options for the reportlab barcode
        - htmlAttrs: attributes for <img /> tag
        """
        drawOpts = (drawOpts or {})
        imgtype = drawOpts.pop('format', 'png')
        attrs = (htmlAttrs or {})
        drawOpts['value'] = value
        for k in ('width', 'height'):
            # Attempt to unify drawing and image sizes to prevent accidental
            # scaling, and reduce parameter duplication
            if k in drawOpts and not k in attrs:
                attrs[k] = "{0}px".format(drawOpts[k])
            elif k in attrs and not k in drawOpts:
                # reportlab expects a float
                value = str(attrs[k])
                if value.endswith("px"):
                    value = value[:-2].strip()
                try:
                    value = float(value)
                except ValueError:
                    # Ignore values that we can't handle
                    pass
                else:
                    drawOpts[k] = value

        data = createBarcodeDrawing(code, **drawOpts).asString(imgtype)
        attrs['src'] = "data:image/{1};base64,{0}".format(
            data.encode('base64'), imgtype,
        )
        return HTML(Element('img', attrs))


    WebKitHelper.barcode = barcode
