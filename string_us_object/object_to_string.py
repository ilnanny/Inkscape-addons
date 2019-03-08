#!/usr/bin/env python 
'''
This extension get the "outersvg" of selected elements.

Copyright (C) 2012 Jabiertxo Arraiza, jabier.arraiza@marker.es

Version 0.2

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import sys, inkex
from lxml import etree

class objectToString(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)

  def effect(self):
    saveout = sys.stdout
    sys.stdout = sys.stderr
    svg = self.document.getroot()
    if len(self.selected) > 1:
        print "Only select one"
        sys.stdout = saveout
        return;
    for id, node in self.selected.iteritems():
        out = etree.tostring(node)
        print out
    sys.stdout = saveout
c =  objectToString()
c.affect()
