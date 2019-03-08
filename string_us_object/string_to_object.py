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

import inkex,sys
from lxml import etree

class objectToString(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)
    self.OptionParser.add_option('--useId', action = 'store', 
            type = 'string', dest = 'useId', default = 'false', 
            help = 'ID to overwrite')
    self.OptionParser.add_option('--outerSvg', action = 'store', 
        type = 'string', dest = 'outerSvg', default = 'false', 
        help = 'Data to replace')
    self.OptionParser.add_option("-d", "--useSelection",
        action="store", type="inkbool", 
        dest="useSelection", default=False,
        help="Use current selection")

  def effect(self):
    saveout = sys.stdout
    sys.stdout = sys.stderr
    svg = self.document.getroot()
    if self.options.useSelection == True:
        if len(self.selected) > 1 or len(self.selected) == 0:
            print "Select one"
            sys.stdout = saveout
            return;
        for id, node in self.selected.iteritems():
            parentEl = node.getparent()
            parsedData = etree.fromstring(self.options.outerSvg)
            c = 0
            for child in parentEl:
                if child == node:
                    parentEl.remove(child)
                    parentEl.insert(c, parsedData);
                c = c+1
    else:
        xpathStr = '//svg:*[@id="' + self.options.useId + '"]'
        el = svg.xpath(xpathStr, namespaces=inkex.NSS)
        if el == []:
            print "This ID dont exist"
            sys.stdout = saveout
        else:
            parentEl = el[0].getparent()
            parsedData = etree.fromstring(self.options.outerSvg)
            c = 0
            for child in parentEl:
                if child == el[0]:
                    parentEl.remove(child)
                    parentEl.insert(c, parsedData);
                c = c+1
    sys.stdout = saveout
c =  objectToString()
c.affect()
