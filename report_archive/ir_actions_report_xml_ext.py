# -*- coding: utf-8 -*-
# © 2015 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields



class ir_actions_report_xml_ext(osv.Model):
    _inherit = 'ir.actions.report.xml'
    
    _columns = {
        'is_archive': fields.boolean('Archive the File'),
        'archive_attachment': fields.char('Attachment Name when Archiving'),
    }