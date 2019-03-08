#!/usr/bin/env python
#-*- coding: utf-8 -*-

import inkex
import simplestyle
import re
import random

class JitterGradients(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option(
            '-j', 
            '--jitter_amount', 
            action='store', 
            type='int', 
            dest='jitterAmount',
            default=10, 
            help='Relative to distance between gradient nodes'
            )

    def getUrlFromString(self, text):
        pattern = re.compile(r"url\(#([a-zA-Z0-9_-]+)\)")
        result = re.search(pattern, text)
        if (result):
            return result.group(1)
        else:
            return 0;

    def getFill(self, element):
        if(element.get('fill') and self.getUrlFromString(element.get('fill'))):
            return self.getUrlFromString(element.get('fill'))
        elif (element.get('style') and simplestyle.parseStyle(element.get('style'))['fill'] and self.getUrlFromString(simplestyle.parseStyle(element.get('style'))['fill'])):
            return self.getUrlFromString(simplestyle.parseStyle(element.get('style'))['fill'])
        else:
            return None

    def getGradientFromId(self, elementId):
        #svg = self.document.getroot()
        element = self.getElementById(elementId)
        #inkex.debug(element.tag)
        if (element is not None and element.tag.find("linearGradient") >= 0):
            return element
        else:
            return None

    def effect(self):
        option = self.options.jitterAmount
        
        self._main_function(option)

    def _main_function(self, amount):
        for id, node in self.selected.iteritems():
            fillId = self.getFill(node)
            if (fillId is None): 
                continue
              
            gradient = self.getGradientFromId(fillId)
            if (gradient is None): 
                continue
          
            x1 = self.unittouu(gradient.get("x1"))
            y1 = self.unittouu(gradient.get("y1"))
            x2 = self.unittouu(gradient.get("x2"))
            y2 = self.unittouu(gradient.get("y2"))
            
            x1 += random.uniform(-amount, amount)
            y1 += random.uniform(-amount, amount)
            x2 += random.uniform(-amount, amount)
            y2 += random.uniform(-amount, amount)
            
            gradient.set('x1', str(self.uutounit(x1, self.getDocumentUnit())) + self.getDocumentUnit())
            gradient.set('y1', str(self.uutounit(y1, self.getDocumentUnit())) + self.getDocumentUnit())
            gradient.set('x2', str(self.uutounit(x2, self.getDocumentUnit())) + self.getDocumentUnit())
            gradient.set('y2', str(self.uutounit(y2, self.getDocumentUnit())) + self.getDocumentUnit())

if __name__ == '__main__':
    ExtenObj = JitterGradients()
    ExtenObj.affect()

'''
    def effect(self):
        #self.duplicateNodes(self.selected)
        self.expandGroupsUnlinkClones(self.selected, True)
        self.expandGroups(self.selected, True)
        self.objectsToPaths(self.selected, True)
        self.bbox=computeBBox(self.selected.values())
        for id, node in self.selected.iteritems():
            if node.tag == inkex.addNS('path','svg') or node.tag=='path':
                d = node.get('d')
                p = cubicsuperpath.parsePath(d)

                for sub in p:
                    for ctlpt in sub:
                        self.applyDiffeo(ctlpt[1],(ctlpt[0],ctlpt[2]))

                node.set('d',cubicsuperpath.formatPath(p))
'''

'''
import inkex

class C(coloreffect.ColorEffect):
  def __init__(self):
    coloreffect.ColorEffect.__init__(self)
    #self.OptionParser.add_option("-j", "--jitter_amount", action="store", type="int", dest="jitter_amount", default="10", help="Relative to distance between gradient nodes")
    
  def colmod(self,r,g,b):
    this_color = '%02x%02x%02x' % (r, g, b)

    fir = self.options.first_color.strip('"').replace('#', '').lower()
    sec = self.options.second_color.strip('"').replace('#', '').lower()
       
    #inkex.debug(this_color+"|"+fir+"|"+sec)
    if this_color == fir:
      return sec
    elif this_color == sec:
      return fir
    else:
      return this_color

c = C()
c.affect()
'''
