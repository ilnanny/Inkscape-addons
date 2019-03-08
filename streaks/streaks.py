#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

import random
rr = random.randint(1,10)

# We will use the inkex module with the predefined Effect base class.
import inkex
# The simplestyle module provides functions for style parsing.
from simplestyle import *

class StreaksEffect(inkex.Effect):
    """
    Fill a box with vertical streaks.
    """
    def __init__(self):
        # Call the base class constructor.
        inkex.Effect.__init__(self)

        self.OptionParser.add_option('-b', '--blur', action = 'store',
          type = 'int', dest = 'blur', default = 2,
          help = 'No help')

        self.OptionParser.add_option('-l', '--linno', action = 'store',
          type = 'int', dest = 'linno', default = 50,
          help = 'No help')

        self.OptionParser.add_option('-x', '--xrand', action = 'store',
          type = 'inkbool', dest = 'xrand', default = True,
          help = 'No help')

        self.OptionParser.add_option('-p', '--pagep', action = 'store',
          type = 'inkbool', dest = 'pagep', default = True,
          help = 'No help')

        self.OptionParser.add_option('-X', '--cusx', action = 'store',
          type = 'int', dest = 'cusx', default = 500,
          help = 'No help')

        self.OptionParser.add_option('-Y', '--cusy', action = 'store',
          type = 'int', dest = 'cusy', default = 500,
          help = 'No help')

        self.OptionParser.add_option('-s', '--segLen', action = 'store',
          type = 'int', dest = 'segLen', default = 8,
          help = 'No help')

        self.OptionParser.add_option('-y', '--yrand', action = 'store',
          type = 'inkbool', dest = 'yrand', default = True,
          help = 'No help')

        self.OptionParser.add_option('-u', '--dashp', action = 'store',
          type = 'inkbool', dest = 'dashp', default = True,
          help = 'No help')

        self.OptionParser.add_option('-v', '--blankp', action = 'store',
          type = 'inkbool', dest = 'blankp', default = True,
          help = 'No help')

        self.OptionParser.add_option('-w', '--dotp', action = 'store',
          type = 'inkbool', dest = 'dotp', default = True,
          help = 'No help')

        self.OptionParser.add_option('-d', '--dits', action = 'store',
          type = 'int', dest = 'dits', default = 100,
          help = 'No help')

        self.OptionParser.add_option('', '--strokeColour', action = 'store',
          type = 'str', dest = 'strokeColour', default = 255,
          help = 'No help')

        self.OptionParser.add_option('', '--strokeWidth', action = 'store',
          type = 'int', dest = 'strokeWidth', default = 2,
          help = 'No help')

        self.OptionParser.add_option("", "--Nmain", action="store",
          type="string", dest="active_tab", default='title',
          help="Active tab.")

    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method.
        """
        blur = int( self.options.blur )
        linno = int( self.options.linno )
        xrand = bool( self.options.xrand )
        pagep = bool( self.options.pagep )
        cusx = int( self.options.cusx )
        cusy = int( self.options.cusy )
        segLen = int( self.options.segLen )
        yrand = bool( self.options.yrand )
        dashp = bool( self.options.dashp )
        blankp = bool( self.options.blankp )
        dotp = bool( self.options.dotp )
        dits = int( self.options.dits )
        strokeColour = int( self.options.strokeColour )
        strokeWidth = int( self.options.strokeWidth )

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        if pagep :
            try :
                width  = inkex.unittouu(svg.get('width'))
                height = inkex.unittouu(svg.attrib['height'])
            except AttributeError :
                width  = self.unittouu(svg.get('width'))
                height = self.unittouu(svg.attrib['height'])
#                inkex.errormsg("Page size %d %d" % (width, height))
        else :
            width = cusx
            height = cusy

            
        # Find defs node.
        for child in svg :
            if -1 != child.tag.find("defs") :
                break
        else:
            inkex.errormsg("No defs child found")
        defs = child

        if blur :
            filter = inkex.etree.SubElement(defs, "filter")
            filter.set(inkex.addNS('collect', 'inkscape'), 'always' )
            filname = self.uniqueId( 'filter' )
            filter.set('id' , filname)

            finfo = inkex.etree.SubElement(filter, 'feGaussianBlur' )
            finfo.set(inkex.addNS('collect', 'inkscape'), 'always' )
            finfo.set( 'stdDeviation', str( blur ) )

        """ Debug
        for i in xrange( len(svg)) :
            k = svg[i].attrib 
            for ky in k :
                inkex.errormsg(ky)

        # Clean any old layers
        flag = False
        for i in xrange( len(svg)) :
            dic = svg[i].attrib
            for key in dic:
                if -1 != key.find("label") :
                    if 'Streak Layer' == dic[key] :
                        del svg[i]
                        flag = True
        if flag :
            inkex.errormsg("Found old Streak layer")
        else:
            inkex.errormsg("Clean")
"""            
        # Create a new layer.
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), 'Streak Layer' )
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

        # Create path element
        path = inkex.etree.Element(inkex.addNS('path','svg'))

        alpha = strokeColour & 255
        color = ( strokeColour >> 8 ) & int( 'ffffff', 16 )
        style = {
            'stroke'        : '#%06X' % color,
            'stroke-width'  : str(strokeWidth),
            }
#        inkex.errormsg("Colour %s" % strokeColour)

        if blur : style['filter'] = 'url(#' + filname +')'


        path.set('style', formatStyle(style))
        
        pathstring = ''
        seglim = int(height / segLen)
        ditlen = int(height / dits)


        xco = 0
        while xco < width :
            y = 0
            flag = random.randint(0, 2)
            while y < height :
                if yrand :
                    yinc = random.randint(1, seglim)
                else :
                    yinc = seglim
                if flag == 1 and dashp: #Draw dash
                    pathstring += ' M '+str(xco)+','+str(y)+' L '+str(xco)+','+str(min( y + yinc, height))
                    y += yinc + ditlen
                elif flag == 2 and dotp: #Draw dots
                    ylim = min( y + yinc, height )
                    while y < ylim :
                        pathstring += ' M '+str(xco)+','+str(y)+' L '+str(xco)+','+str(min( y + ditlen, height))
                        y += 2*ditlen
                elif flag == 0 and blankp :
                    y += yinc #Adding blank space 
                elif not (dashp or dotp or blankp) : #Squiggle if user turns them off
                    sdit = str(2*ditlen)+' '
                    pathstring += ' M '+str(xco)+','+str(y)+' q '+ 2*sdit + '0 ' +sdit
                    for i in xrange(int(height/(2*ditlen))) :
                        pathstring += 't 0 '+sdit
                    y = height
                flag = (flag + 1)%3
            if xrand :
                xco += random.randint(0, int(2 * width / linno) )
            else :
                xco += width / linno
        path.set('d', pathstring )

        # Connect elements together.
        layer.append(path)

# Create effect instance and apply it.
effect = StreaksEffect()
effect.affect()
sys.exit( 0 )

