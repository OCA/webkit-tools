# -*- coding: utf-8 -*-
# © 2015 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""
@author: brain-tec AG
"""
from openerp.addons.report_webkit.webkit_report import WebKitParser
from openerp import pooler


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
        pool = pooler.get_pool(cursor.dbname)
        ir_obj = pool.get('ir.actions.report.xml')
        report_xml_ids = ir_obj.search(cursor,
                                       uid,
                                       [('report_name', '=', self.name[7:])],
                                       context=context)
        if report_xml_ids:
            report_xml = ir_obj.browse(cursor,
                                       uid,
                                       report_xml_ids[0],
                                       context=context)
            if report_xml.is_archive and report_xml.archive_attachment:
                # get path to save the file
                ir_config_parameter_pool = self.pool.get('ir.config_parameter')
                archive_reports_path_ids = ir_config_parameter_pool.search(
                    cursor,
                    uid,
                    [('key', '=', 'archive_reports_path')])
                if archive_reports_path_ids:
                    archive_reports_path = ir_config_parameter_pool.browse(
                        cursor,
                        uid,
                        archive_reports_path_ids[0],
                        context=context)
                    pdf_file = open('{path}/{name}.pdf'.format(
                        path=archive_reports_path.value,
                        name=report_xml.archive_attachment), 'w+b')
                    pdf_file.write(pdf_binary)
                    pdf_file.close()
        return (pdf_binary, type_of_file)

    return __create_pdf

WebKitParser.create = __new_create(WebKitParser.create)
