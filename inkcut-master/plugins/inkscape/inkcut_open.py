#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inkcut, Plot HPGL directly from Inkscape.
   extension.py

   Copyright 2010-2018 The Inkcut Team

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
   MA 02110-1301, USA.
"""
import os
import sys
import inkex
inkex.localize()
import subprocess

from inkcut import convert_objects_to_paths

DEBUG = False
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


class InkscapeInkcutPlugin(inkex.Effect):
    def effect(self):
        """ Like cut but requires no selection and does no validation for
        text nodes.
        """
        #: If running from source
        if DEBUG:
            python = '~/inkcut/venv/bin/python'
            inkcut = '~/inkcut/main.py'
            cmd = [python, inkcut]
        else:
            cmd = ['inkcut']

        document = convert_objects_to_paths(self.args[-1], self.document)

        cmd += ['open', '-']
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=DEVNULL,
                             stderr=subprocess.STDOUT,
                             close_fds=sys.platform != "win32")
        p.stdin.write(inkex.etree.tostring(document))
        p.stdin.close()

# Create effect instance and apply it.
effect = InkscapeInkcutPlugin()
effect.affect()
