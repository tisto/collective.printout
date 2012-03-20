# -*- coding: utf-8 -*-

import os
import sys

from util import newTempfile, runcmd

from collective.printout import log


class Fop(object):

    def convert(self, fo_filename, output_filename=None):

        if not output_filename:
            output_filename = newTempfile(suffix='.pdf')

        cmd = 'fop -fo "%s" -pdf "%s"' % (fo_filename, output_filename)

        status, output = runcmd(cmd)
        if status != 0:
            raise RuntimeError('Error executing: %s\n\n%s' % (cmd, output))
        log.info("\n")

        return output_filename
