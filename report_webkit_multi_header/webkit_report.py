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
import os
import shutil
import subprocess
import tempfile
from functools import partial

from mako import exceptions

from openerp.addons.report_webkit import webkit_report, report_helper
from openerp import addons
from openerp import pooler
from openerp import tools
from openerp.osv import orm
from openerp.tools.translate import _

mako_template = webkit_report.mako_template
WebKitHelper = report_helper.WebKitHelper
WebKitParser = webkit_report.WebKitParser

_logger = logging.getLogger(__name__)


def log_rmtree_error(func, path, exc_info):
    _logger.error('cannot %s %s: %s',
                  {"listdir": "list dir",
                   "remove": "delete",
                   "rmdir": "remove dir"}.get(func.__name__),
                  path, exc_info[0])


class WebKitMultiParser(WebKitParser):

    # override needed to keep the attachments storing procedure
    def create_single_pdf(self, cursor, uid, ids, data, report_xml,
                          context=None):
        """generate the PDF"""

        if context is None:
            context = {}
        if report_xml.report_type != 'webkit':
            return super(WebKitParser, self).create_single_pdf(
                cursor, uid, ids, data, report_xml, context=context)

        if not report_xml.multi_mode:
            return super(WebKitMultiParser, self).create_single_pdf(
                cursor, uid, ids, data, report_xml, context=context)

        parser_instance = self.parser(cursor,
                                      uid,
                                      self.name2,
                                      context=context)

        self.pool = pooler.get_pool(cursor.dbname)
        objs = self.getObjects(cursor, uid, ids, context)
        parser_instance.set_context(objs, data, ids, report_xml.report_type)

        template = False

        if report_xml.report_file:
            # backward-compatible if path in Windows format
            report_path = report_xml.report_file.replace("\\", "/")
            path = addons.get_module_resource(*report_path.split('/'))
            if path and os.path.exists(path):
                template = file(path).read()
        if not template and report_xml.report_webkit_data:
            template = report_xml.report_webkit_data
        if not template:
            raise orm.except_orm(_('Error!'),
                                 _('Webkit report template not found!'))
        header = report_xml.webkit_header.html
        footer = report_xml.webkit_header.footer_html
        if not header and report_xml.header:
            raise orm.except_orm(
                _('No header defined for this Webkit report!'),
                _('Please set a header in company settings.')
            )
        if not report_xml.header:
            header = ''
            default_head = addons.get_module_resource('report_webkit',
                                                      'default_header.html')
            with open(default_head, 'r') as f:
                header = f.read()
        css = report_xml.webkit_header.css
        if not css:
            css = ''

        translate_call = partial(self.translate_call, parser_instance)
        pages = []
        body_mako_tpl = mako_template(template)
        head_mako_tpl = mako_template(header)
        foot_mako_tpl = mako_template(footer) if footer else None
        helper = WebKitHelper(cursor, uid, report_xml.id, context)
        objs = parser_instance.localcontext['objects']
        parser_instance.localcontext['all_objects'] = objs
        for obj in objs:
            html, head, foot = None, None, None
            parser_instance.localcontext['objects'] = [obj]
            try:
                html = body_mako_tpl.render(helper=helper,
                                            css=css,
                                            _=translate_call,
                                            **parser_instance.localcontext)
            except Exception:
                msg = exceptions.text_error_template().render()
                _logger.error(msg)
                raise orm.except_orm(_('Webkit render!'), msg)
            try:
                head = head_mako_tpl.render(helper=helper,
                                            css=css,
                                            _=translate_call,
                                            _debug=False,
                                            **parser_instance.localcontext)
            except Exception:
                raise orm.except_orm(
                    _('Webkit render!'),
                    exceptions.text_error_template().render(),
                )

            if foot_mako_tpl:
                try:
                    foot = foot_mako_tpl.render(helper=helper,
                                                css=css,
                                                _=translate_call,
                                                **parser_instance.localcontext)
                except:
                    msg = exceptions.text_error_template().render()
                    _logger.error(msg)
                    raise orm.except_orm(_('Webkit render!'), msg)

            pages.append((html, head, foot))

        if report_xml.webkit_debug:
            try:
                deb = head_mako_tpl.render(
                    helper=helper,
                    css=css,
                    _debug=tools.ustr("\n".join(p[0] for p in pages)),
                    _=translate_call,
                    **parser_instance.localcontext)
            except Exception:
                msg = exceptions.text_error_template().render()
                _logger.error(msg)
                raise orm.except_orm(_('Webkit render!'), msg)
            return (deb, 'html')
        bin = self.get_lib(cursor, uid)
        pdf = self.generate_pdf_multi(bin, report_xml, pages)
        return (pdf, 'pdf')

    def generate_pdf_multi(self, comm_path, report_xml, pages):
        """Call webkit in order to generate pdf"""
        tmpdir = tempfile.mkdtemp(prefix='webkit_report')
        out_filename = os.path.join(tmpdir, "out.pdf")
        webkit_header = report_xml.webkit_header

        if comm_path:
            command = [comm_path]
        else:
            command = ['wkhtmltopdf']

        command.extend([
            '--encoding', 'utf-8',
            '--quiet',
        ])
        for key, val in [("--margin-top", webkit_header.margin_top),
                         ("--margin-bottom", webkit_header.margin_bottom),
                         ("--margin-right", webkit_header.margin_right),
                         ("--margin-left", webkit_header.margin_left),
                         ("--page-size", webkit_header.format),
                         ("--orientation", webkit_header.orientation)]:
            if val:
                command.extend([
                    key,
                    str(val).replace(", ", "."),
                ])

        for idx, (html, head, foot) in pages:
            body_file = os.path.join(tmpdir, "body{0}.html".format(idx))
            with open(body_file, "wb") as f:
                f.write(self._sanitize_html(html))
            command.extend(["page", body_file])

            if head:
                head_file = os.path.join(tmpdir, "head{0}.html".format(idx))
                with open(head_file, "wb") as f:
                    f.write(self._sanitize_html(head))
                command.extend(["--header-html", head_file])

            if foot:
                foot_file = os.path.join(tmpdir, "foot{0}.html".format(idx))
                with open(foot_file, "wb") as f:
                    f.write(self._sanitize_html(foot))
                command.extend(["--footer-html", foot_file])

        command.append(out_filename)
        stderr_path = os.path.join(tmpdir, "stderr.out")
        try:
            print " ".join(command)
            with open(stderr_path, "w") as stderr_fd:
                status = subprocess.call(command, stderr=stderr_fd)
            try:
                with open(stderr_path, 'r') as fobj:
                    error_message = fobj.read()
            except Exception:
                error_message = _('No diagnosis message was provided')
            else:
                error_message = _('The following diagnosis message was '
                                  'provided:\n') + error_message

            if status:
                raise orm.except_orm(
                    _('Webkit error'),
                    _("The command 'wkhtmltopdf' failed with error code = %s."
                      "Message: %s") % (status, error_message))

            with open(out_filename, 'rb') as pdf_file:
                pdf = pdf_file.read()
        finally:
            try:
                shutil.rmtree(tmpdir, log_rmtree_error)
            except Exception:
                pass
        return pdf
