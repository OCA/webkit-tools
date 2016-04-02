# -*- coding: utf-8 -*-
# © 2014 Savoir-faire Linux
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openerp.addons.report_webkit.report_helper import WebKitHelper


_logger = logging.getLogger(__name__)


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
            if k in drawOpts and k not in attrs:
                attrs[k] = "{0}px".format(drawOpts[k])
            elif k in attrs and k not in drawOpts:
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
