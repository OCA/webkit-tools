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

from openerp.osv import orm, fields
from openerp.report.report_sxw import rml_parse
from openerp import netsvc

from .webkit_report import WebKitMultiParser


def register_report(name, model, tmpl_path, parser=rml_parse):
    """Register the report into the services"""
    name = 'report.%s' % name
    if netsvc.Service._services.get(name, False):
        service = netsvc.Service._services[name]
        if isinstance(service, WebKitMultiParser):
            #already instantiated properly, skip it
            return
        if hasattr(service, 'parser'):
            parser = service.parser
        del netsvc.Service._services[name]
    WebKitMultiParser(name, model, tmpl_path, parser=parser)

class Report(orm.Model):
    _name = _inherit = 'ir.actions.report.xml'

    _columns = {
        'multi_mode': fields.boolean(
            'Multi Mode',
            help='This mode allows rendering the header and footer for each'
                 ' object of the report.'),
    }

    def register_all(self,cursor):
        value = super(Report, self).register_all(cursor)
        cursor.execute("SELECT * FROM ir_act_report_xml WHERE report_type = 'webkit'")
        records = cursor.dictfetchall()
        for record in records:
            register_report(record['report_name'], record['model'], record['report_rml'])
        return value
