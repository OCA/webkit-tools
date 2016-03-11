# -*- coding: utf-8 -*-
# © 2015 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""
@author: brain-tec AG
"""
from openerp.addons.report_webkit.webkit_report import WebKitParser
from openerp import pooler
import logging
from openerp.tools.translate import _
import time

_logger = logging.getLogger(__name__)


def __new_create(old_func):
    """
    @author: brain-tec AG
    """

    def __create_pdf(self, cursor, uid, ids, data, context=None):
        """
        @author: brain-tec AG
        """
        # creating the PDF
        (pdf_binary, type_of_file) = old_func(self,
                                              cursor,
                                              uid,
                                              ids,
                                              data,
                                              context=None)
        # getting the report
        report_obj = self.pool.get('ir.actions.report.xml')
        report_xml_ids = report_obj.search(cursor,
                                       uid,
                                       [('report_name', '=', self.name[7:])],
                                       context=context)
        if report_xml_ids:
            report_xml = report_obj.browse(cursor,
                                       uid,
                                       report_xml_ids[0],
                                       context=context)
            if report_xml.is_archive and report_xml.archive_attachment:
                #get the object to be saved
                obj = self.getObjects(cursor, uid, ids, context)[0]
                attachment_name = eval(report_xml.archive_attachment, {'object':obj, 'time':time})

                # get path to save the file
                archive_reports_path = self.pool.get('ir.config_parameter').get_param(cursor, uid,
                                                                                      'archive_reports_path')
                if archive_reports_path:
                    try:
                        pdf_file = open('{path}{name}'.format(
                            path=archive_reports_path,
                            name=attachment_name), 'w+b')
                        pdf_file.write(pdf_binary)
                        pdf_file.close()
                        _logger.info(_('Success, saved report PDF "%s" in "%s/%s"' %(report_xml.name,
                                                                                     archive_reports_path,attachment_name)))
                    except Exception:
                        _logger.info(_('Failed, saving report PDF "%s" in "%s/%s"' %(report_xml.name,
                                                                                     archive_reports_path,attachment_name)), exc_info=True)

                else:
                    _logger.debug(_('No path configured for report: %s' %report_xml.name))
        return (pdf_binary, type_of_file)

    return __create_pdf

WebKitParser.create = __new_create(WebKitParser.create)
