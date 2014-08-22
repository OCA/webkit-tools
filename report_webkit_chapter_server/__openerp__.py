# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author Camptocamp. Copyright Camptocamp SA
##############################################################################
{
    'name': 'Chapter server helper for report webkit',
    'version': '0.1',
    'category': 'Other',
    'description': """
      Add chapter_server to report Webkit
      <% import random %>
      <%chapter = helper.chapter() %>
      % for i in xrange(100):
       <% a = random.randrange(1, 3) %>
        ${chapter.get_structure(a)}<br/>
      %endfor
    """,
    'author': 'Camptocamp',
    'website': 'http://openerp.camptocamp.com',
    'depends': ['report_webkit'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'installable': False,
    'active': False,
}
