# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author Camptocamp. Copyright Camptocamp SA
##############################################################################
import logging
from report_webkit import report_helper

chapter_logger = logging.getLogger('chapter server')


class chapter_server(object):

    @classmethod
    def __init__(self):
        self.stack = [0]

    @classmethod
    def get_structure(self, level):
        while len(self.stack) < level:
            self.stack.append(0)
        while len(self.stack) > level:
            self.stack = self.stack[:level]
        try:
            self.stack[len(self.stack) - 1] += 1
        except:
            chapter_logger.error(self.stack)
        return ".".join("%s" % s for s in self.stack) + "."

report_helper.WebKitHelper.chapter = chapter_server
