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
{
    'name': 'Webkit Setup',
    'version': '7.0.1.0.0',
    'author': 'initOS GmbH, Odoo Community Association (OCA)',
    'category': '',
    'description': """
Webkit Setup Module
==========================================================

This module allows to configure the webkit path by a wizard during setup.
All wkhtmltopdf binaries in the PATH will be suggested in the wizard
drop down field.
If the webkit path is already configured,
its value will be used as a default value for the
webkit path field in the wizard.
""",
    'website': 'http://www.initos.com',
    'license': 'AGPL-3',
    'images': [],
    'depends': [
        'base'
    ],
    'data': [
        'webkit_setup_view.xml',
    ],
    'js': [
    ],
    'qweb': [
    ],
    'css': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
