# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2015 OpenERP s.a. (<http://openerp.com>).
#    Copyright (C) 2015 initOS GmbH(<http://www.initos.com>).
#    Author Nikolina Todorova <nikolina.todorova at initos.com>
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
from openerp.osv import orm
from openerp.osv import fields
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
import openerp
import os
import subprocess
import re


class webkit_setup_config(orm.TransientModel):
    _name = 'webkit.setup.config'
    _inherit = 'res.config'

    def existing_paths(self, cr, uid, context=None):
        options = []
        lookfor = "wkhtmltopdf"
        paths = os.environ['PATH'].split(os.pathsep)
        # We don't use `find_in_path` because we want to find all
        # matching binaries.
        for path in paths:
            file_path = os.path.join(path, lookfor)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                process = subprocess.Popen(file_path, stderr=subprocess.PIPE)
                output = process.stderr.read()
                wkh_index = output.find('wkhtmltopdf')
                row = output[wkh_index:].split('\n')
                m = re.search('[0-9]+.[0-9]+.[0-9]+', row[0])
                if m:
                    options.append(
                        (file_path, 'Version ' + m.group(0) + ': ' + file_path)
                    )
        return options

    def onchange_path(self, cr, uid, ids, path, context=None):
        if path:
            return {'value': {'webkit_path': path, }, }
        return {'value': {}}

    _columns = {
        'webkit_path': fields.char('Field'),
        'existing_paths': fields.selection(existing_paths, 'Existing Paths')
    }

    def init(self, cr):
        config_parameters = self.pool.get("ir.config_parameter")
        file_path = config_parameters.get_param(cr,
                                                SUPERUSER_ID,
                                                "webkit_path")
        if file_path:
            self._defaults['webkit_path'] = file_path
        else:
            lookfor = "wkhtmltopdf"
            file_path = ''
            paths = os.environ['PATH'].split(os.pathsep)
            for path in paths:
                file_path = os.path.join(path, lookfor)
                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                    self._defaults['webkit_path'] = file_path
                    break

    def execute(self, cr, uid, ids, context=None):
        if uid != SUPERUSER_ID and \
            not self.pool['res.users'].has_group(cr,
                                                 uid,
                                                 'base.group_erp_manager'):
            raise openerp.exceptions.AccessError(_("""Only administrators
                                                   can change the settings"""))
        config_parameters = self.pool.get("ir.config_parameter")
        obj_wizard = self.browse(cr, uid, ids[0])
        webkit_path = obj_wizard.webkit_path
        config_parameters.set_param(cr,
                                    uid,
                                    "webkit_path",
                                    webkit_path or '',
                                    context=context)
