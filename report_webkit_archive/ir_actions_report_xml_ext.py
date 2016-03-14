# -*- coding: utf-8 -*-
# © 2015 brain-tec AG
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""
@author: brain-tec AG
"""


from openerp.osv import osv, fields


class IrActionsReportXmlExt(osv.Model):
    """
    @author: brain-tec AG
    """
    _inherit = 'ir.actions.report.xml'

    _columns = {
        'is_archive': fields.boolean('Archive the File'),
        'archive_attachment': fields.char('Save as File Prefix',
                                          help='This is the filename of the report. '
                                               'You can use a python expression with the object and time variables.')
    }
