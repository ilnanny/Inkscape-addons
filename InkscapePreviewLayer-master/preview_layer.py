#!/usr/bin/env python

# These two lines are only needed if you don't put the script directly into
# the installation directory
import sys
sys.path.append('/usr/share/inkscape/extensions')

# We will use the inkex module with the predefined Effect base class
import inkex
# The simplestyle module provides functions for style parsing
import simplestyle



class AddPreviewLayer(inkex.Effect):
    """
    Creates a new preview layer with black or white background color.
    """
    def __init__(self):
        """
        Constructor.
        Defines the "--bgcolor" option of a script.
        """
        # Call the base class constructor
        inkex.Effect.__init__(self)

        # Define string option "--bgcolor" with "-b" shortcut and default value "#000000"
        self.OptionParser.add_option('-b', '--bgcolor', action = 'store',
          type = 'string', dest = 'bgcolor', default = '#000000',
          help = 'Background color')



    def draw_SVG_square(self, (w,h), (x,y), parent):
        """
        Method to draw rectangles.
        """

        # Get script's "--bgcolor" option value
        what = self.options.bgcolor


        style = {   'stroke'        : 'none',
                    'stroke-width'  : '1',
                    'fill'          : '%s' % what
                }
                    
        attribs = {
            'style'     : simplestyle.formatStyle(style),
            'height'    : str(h),
            'width'     : str(w),
            'x'         : str(x),
            'y'         : str(y)
                }
        circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attribs )

    
    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts new preview layer.
        """
        # Get script's "--bgcolor" option value
        what = self.options.bgcolor

        # Get access to main SVG document element and get its dimensions
        svg = self.document.getroot()

        # Get document dimentions
        width  = self.unittouu(svg.get('width'))
        height = self.unittouu(svg.get('height'))


        # Create a new layer
        preview_layer = inkex.etree.SubElement(svg, 'g')
        preview_layer.set(inkex.addNS('label', 'inkscape'), 'Preview Layer')
        preview_layer.set(inkex.addNS('id'), 'preview_layer')
        preview_layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
        preview_layer.set(inkex.addNS('insensitive', 'sodipodi'), 'true') #lock layer


        # preview layer as parent
        #parent = self.current_layer
        parent = preview_layer

        
        # draw rectangles on preview layer
        #draw_SVG_square((w,h), (x,y), parent)
        
        #left
        #self.draw_SVG_square((2000,4000), (-2000,-2000), parent)
        self.draw_SVG_square((width*2,height*5), (-width*2,-height*2), parent)

        #right        
        #self.draw_SVG_square((2000,4000), (width,-2000), parent)
        self.draw_SVG_square((width*2,height*5), (width,-height*2), parent)

        #top
        #self.draw_SVG_square((4000,2000), (-2000,-2000), parent)
        self.draw_SVG_square((width*5, height*2), (-width*2,-height*2), parent)

        #bottom
        #self.draw_SVG_square((4000,2000), (-2000,height), parent)
        self.draw_SVG_square((width*5, height*2), (-width*2, height), parent)






# Create effect instance and apply it
effect = AddPreviewLayer()
effect.affect()



