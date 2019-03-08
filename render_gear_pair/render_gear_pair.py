#! /usr/bin/env python
'''
Abe Karnik 2017 ("Do what you like with it, no liability" license)
Based on Aaron Spike  (aaron @ ekips.org) and Tavmjong Bah (tavmjong @ free.fr) 'Render Gear'

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import inkex
import simplestyle, sys
from math import *
import string
from fractions import Fraction

def involute_intersect_angle(Rb, R):
    Rb, R = float(Rb), float(R)
    return (sqrt(R**2 - Rb**2) / (Rb)) - (acos(Rb / R))

def point_on_circle(radius, angle):
    x = radius * cos(angle)
    y = radius * sin(angle)
    return (x, y)

def points_to_svgd(p):
    f = p[0]
    p = p[1:]
    svgd = 'M%.5f,%.5f' % f
    for x in p:
        svgd += ' L%.5f,%.5f' % x
    svgd += 'z'
    return svgd
    
def make_gear_path(pitch, angle, teeth):
    two_pi = 2.0 * pi

    # Pitch (circular pitch): Length of the arc from one tooth to the next)
    # Pitch diameter: Diameter of pitch circle.
    pitch_diameter = float( teeth ) * pitch / pi
    pitch_radius   = pitch_diameter / 2.0

    # Base Circle
    base_diameter = pitch_diameter * cos( radians( angle ) )
    base_radius   = base_diameter / 2.0

    # Diametrial pitch: Number of teeth per unit length.
    pitch_diametrial = float( teeth )/ pitch_diameter

    # Addendum: Radial distance from pitch circle to outside circle.
    addendum = 1.0 / pitch_diametrial

    # Outer Circle
    outer_radius = pitch_radius + addendum
    outer_diameter = outer_radius * 2.0

    # Tooth thickness: Tooth width along pitch circle.
    tooth  = ( pi * pitch_diameter ) / ( 2.0 * float( teeth ) )

    # Undercut?
    undercut = (2.0 / ( sin( radians( angle ) ) ** 2))
    needs_undercut = teeth < undercut


    # Clearance: Radial distance between top of tooth on one gear to bottom of gap on another.
    clearance = 0.0

    # Dedendum: Radial distance from pitch circle to root diameter.
    dedendum = addendum + clearance

    # Root diameter: Diameter of bottom of tooth spaces. 
    root_radius =  pitch_radius - dedendum
    root_diameter = root_radius * 2.0

    half_thick_angle = two_pi / (4.0 * float( teeth ) )
    pitch_to_base_angle  = involute_intersect_angle( base_radius, pitch_radius )
    pitch_to_outer_angle = involute_intersect_angle( base_radius, outer_radius ) - pitch_to_base_angle

    centers = [(x * two_pi / float( teeth) ) for x in range( teeth ) ]

    points = []

    for c in centers:

        # Angles
        pitch1 = c - half_thick_angle
        base1  = pitch1 - pitch_to_base_angle
        outer1 = pitch1 + pitch_to_outer_angle

        pitch2 = c + half_thick_angle
        base2  = pitch2 + pitch_to_base_angle
        outer2 = pitch2 - pitch_to_outer_angle

        # Points
        b1 = point_on_circle( base_radius,  base1  )
        p1 = point_on_circle( pitch_radius, pitch1 )
        o1 = point_on_circle( outer_radius, outer1 )

        b2 = point_on_circle( base_radius,  base2  )
        p2 = point_on_circle( pitch_radius, pitch2 )
        o2 = point_on_circle( outer_radius, outer2 )

        if root_radius > base_radius:
            pitch_to_root_angle = pitch_to_base_angle - involute_intersect_angle(base_radius, root_radius )
            root1 = pitch1 - pitch_to_root_angle
            root2 = pitch2 + pitch_to_root_angle
            r1 = point_on_circle(root_radius, root1)
            r2 = point_on_circle(root_radius, root2)
            p_tmp = [r1,p1,o1,o2,p2,r2]
        else:
            r1 = point_on_circle(root_radius, base1)
            r2 = point_on_circle(root_radius, base2)
            p_tmp = [r1,b1,p1,o1,o2,p2,b2,r2]

        points.extend( p_tmp )

    path = points_to_svgd( points )
    return path

def ratioMatch(pair1, pair2, gR): #smallest positive number
    pair1R= (gR-(pair1[1]/pair1[0]))
    pair2R= (gR-(pair2[1]/pair2[0]))
    #print(pair1R, pair2R)
    if(0 <= pair1R):
        if(pair1R <= pair2R):
            return pair1
        else:
            if(pair2R < 0):
                return pair1
            else:
                return pair2
    else:
        return pair2
    return pair1
  
  
def add_gear_path_to_sketch(group, gear_idx, teeth, path, centerdiameter,  units):
    #t = 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')'
    
    #group g contains one gear each
    #g = inkex.etree.SubElement(current_layer, 'g'+str(gear_idx), g_attribs)

    if gear_idx == 1:
        fillGear = '#ffff00'
    else:
        fillGear = '#00ff00'
        
        
    # Create SVG Path for gear, since it is to be laser cut, the stroke is fine
    style = { 'stroke': '#000000', 'fill': fillGear, 'stroke-width': units }
    gear_attribs = {'style':simplestyle.formatStyle(style), 'd':path}
    #add the gear path to the group 'g'
    gear = inkex.etree.SubElement(group, inkex.addNS('path','svg'), gear_attribs )
    styleHole = { 'stroke': '#000000', 'fill': '#ff0000', 'stroke-width': units }
    if(centerdiameter > 0.0):
        center_attribs = {'style':simplestyle.formatStyle(styleHole), 
            inkex.addNS('cx','sodipodi')        :'0.0',
            inkex.addNS('cy','sodipodi')        :'0.0',
            inkex.addNS('rx','sodipodi')        :str(centerdiameter/2),
            inkex.addNS('ry','sodipodi')        :str(centerdiameter/2),
            inkex.addNS('type','sodipodi')      :'arc'
    }
    center = inkex.etree.SubElement(group, inkex.addNS('path','svg'), center_attribs )
    return 0

class Gears(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        #self.OptionParser.add_option("-t", "--teeth",
        #                action="store", type="int",
        #                dest="teeth", default=24,
        #                help="Number of teeth")
        self.OptionParser.add_option("-t", "--teethG1",
                        action="store", type="int",
                        dest="teethG1", default=24,
                        help="Gear 1 tooth count")
        self.OptionParser.add_option("-y", "--teethG2",
                        action="store", type="int",
                        dest="teethG2", default=24,
                        help="Gear 2 tooth count")
        self.OptionParser.add_option("-d", "--distance",
                        action="store", type="float",
                        dest="distance", default=24,
                        help="Center to center distance")
        self.OptionParser.add_option("-p", "--pitch",
                        action="store", type="float",
                        dest="pitch", default=3.0,
                        help="Circular Pitch (length of arc from one tooth to next)")
        self.OptionParser.add_option("-a", "--angle",
                        action="store", type="float",
                        dest="angle", default=20.0,
                        help="Pressure Angle (common values: 14.5, 20, 25 degrees)")
        self.OptionParser.add_option("-c", "--centerdiameterG1",
                        action="store", type="float",
                        dest="centerdiameterG1", default=10.0,
                        help="Diameter of central hole - 0.0 for no hole")
        self.OptionParser.add_option("-v", "--centerdiameterG2",
                        action="store", type="float",
                        dest="centerdiameterG2", default=10.0,
                        help="Diameter of central hole - 0.0 for no hole")
        self.OptionParser.add_option("-b", "--basis",
                        action="store", type="string",
                        dest="calculationBasis", default="dx",
                        help="Fixed CP or fixed distance")
        self.OptionParser.add_option("-u", "--unit",
                        action="store", type="string",
                        dest="unit", default="mm",
                        help="unit of measure for circular pitch and center diameter")
    def effect(self):

        #start modification
        
        #capture G1 params
        teethG1 = self.options.teethG1
        centerdiameterG1 = self.unittouu( str(self.options.centerdiameterG1) + self.options.unit)
        
        #capture G2 params
        teethG2 = self.options.teethG2
        centerdiameterG2 = self.unittouu( str(self.options.centerdiameterG2) + self.options.unit)
        
        #capture common params
        #pitch = self.unittouu( str(self.options.pitch) + self.options.unit)
        pitch = self.options.pitch
        angle = self.options.angle  # Angle of tangent to tooth at circular pitch wrt radial line.
        distance = self.options.distance
        calculationBasis = self.options.calculationBasis
        
        #gear ratio (GR): N2/N1
        #diametral pitch (dP) is fixed (and related to CP)
        #pitch diameter (PD) = N/dP
        # PD1 + PD2 = distance * 2
        # N1/dP1 + N2/dP2 = distance * 2
        # N1/dP + GR*N1/dP = distance * 2
        # (1+GR)*N1/dP = distance * 2
        # dP = (1+GR)*N1/(distance * 2)
        # CP = pi/dP
        # CP = pi*(distance*2)/((1+GR)*N1)
        # OR
        # distance = CP*(1+GR)*N1/(2*PI)
        # OR
        # N1 = D*2*PI/(CP*(1+GR)) # N2 = GR*N1
        
        gearRatio = teethG2/(teethG1*1.0)
        if(calculationBasis == 'dx'):  #CP can be changed, distance is as is
            pitchUU = self.unittouu( str((pi * 2 * distance)/((1+gearRatio)*teethG1)) + self.options.unit)
            distanceUU = self.unittouu(str(distance)+self.options.unit)
        elif (calculationBasis == 'gr'):
            pitchUU = self.unittouu(str(pitch)+self.options.unit)
            distanceUU = self.unittouu(str(distance)+self.options.unit)
            tempT1 = distanceUU*2*pi/(pitchUU*(1+gearRatio))
            intT1 = int(tempT1)
            tempT2 = gearRatio*tempT1
            intT2 = int(tempT2)
            gr1 = ratioMatch((intT1,intT2),(intT1,intT2+1),gearRatio)
            gr2 = ratioMatch((intT1-1,intT2),(intT1-1,intT2+1),gearRatio)
            grFinal = ratioMatch(gr1,gr2, gearRatio)
            teethG1 = grFinal[0]
            teethG2 = grFinal[1]
            gearRatioNew = teethG2/(teethG1*1.0)
        else:
            distanceUU = self.unittouu(str(pitch*(1+gearRatio)*teethG1/(2*pi))+self.options.unit)
            pitchUU = self.unittouu(str(pitch)+self.options.unit)
        # print >>sys.stderr, "Teeth: %s\n"        % teeth
        
        pathG1 = make_gear_path(pitchUU, angle, teethG1)
        pathG2 = make_gear_path(pitchUU, angle, teethG2)
        
        t1 = 'translate(' + str( self.view_center[0] ) + ',' + str( self.view_center[1] ) + ')'
        g1_attribs = {inkex.addNS('label','inkscape'):'Gear1' + str( teethG1 ), 'transform':t1 }
        
        t2 = 'translate(' + str( self.view_center[0] + distanceUU ) + ',' + str(self.view_center[1]) + ')'
        g2_attribs = {inkex.addNS('label','inkscape'):'Gear1' + str( teethG2 ), 'transform':t2 }
        
        gear1Grp = inkex.etree.SubElement(self.current_layer, 'g', g1_attribs)
        gear2Grp = inkex.etree.SubElement(self.current_layer, 'g', g2_attribs)
        
        ret1 = add_gear_path_to_sketch(gear1Grp, 1, teethG1, pathG1, centerdiameterG1,str(self.unittouu('0.001 mm')))
        ret2 = add_gear_path_to_sketch(gear2Grp, 2, teethG2, pathG2, centerdiameterG2,str(self.unittouu('0.001 mm')))
        
        #add text indicating cp value
        t3 = 'translate(' + str( self.view_center[0]  ) + ',' + str(self.view_center[1] + distanceUU) + ')'
        t3_attribs = {inkex.addNS('label','inkscape'):'CPText', 'transform':t3  }
        
        t3Text = inkex.etree.SubElement(self.current_layer, inkex.addNS('text','svg'),t3_attribs)
        txt_attribs = {'font-family':'Courier New', 'font-weight':'bold', 'font-style':'normal','font-size':'10 px','fill':'#0000ff'}
        
        tAdd = inkex.etree.SubElement(t3Text, inkex.addNS('tspan','svg'), txt_attribs )
        if(calculationBasis == 'dx'):
            tAdd.text = "CP=" + str('%.3f'%self.uutounit(pitchUU, self.options.unit)) + self.options.unit
        elif(calculationBasis == 'gr'):
            tAdd.text = "GR(new)=" + str('%.2f'%gearRatioNew) +" GR=" + str('%.2f'%gearRatio) 
            #t3 = 'translate(' + str( 0 ) + ',' + str(self.unittouu("15px")) + ')'
            txt_attribs2 = {'font-family':'Courier New', 'font-weight':'bold', 'font-style':'normal','font-size':'10 px','fill':'#0000ff','x':str(self.unittouu("0 px")),'dy':str(self.unittouu("15 px"))}
            tAdd2 = inkex.etree.SubElement(t3Text, inkex.addNS('tspan','svg'), txt_attribs2 )
            tAdd2.text =  "T1=" + str(teethG1) + " T2=" + str(teethG2) + " Err=" + str('%.1f'%(100*(gearRatioNew-gearRatio)/gearRatio)) +"%" 
        else:
            tAdd.text = "Distance=" + str('%.2f'%self.uutounit(distanceUU, self.options.unit)) + self.options.unit
        
if __name__ == '__main__':
    e = Gears()
    e.affect()



# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
