#!/usr/bin/env python 
'''
Copyright (C) 2013 Carl Sorensen carl.d.sorensen@gmail.com
Derived from grid_cartesian.py copyright (C) 2007 John Beard john.j.beard@gmail.com


##This extension allows you to draw a two-point perspective grid in Inkscape.
##There is a wide range of options including subdivision, subsubdivions
##and angles of the triangular axes.
##Custom line widths are also possible.
##All elements are grouped with similar elements (eg all x-subdivs)

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

import inkex
import simplestyle, sys
from math import *

def draw_SVG_line(x1, y1, x2, y2, width, stroke, name, parent):
    style = { 'stroke': stroke, 'stroke-width':str(width), 'fill': 'none' }
    line_attribs = {'style':simplestyle.formatStyle(style),
                    inkex.addNS('label','inkscape'):name,
                    'd':'M '+str(x1)+','+str(y1)+' L '+str(x2)+','+str(y2)}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )
    
def draw_SVG_rect(x,y,w,h, width, stroke, fill, name, parent):
    style = { 'stroke': stroke, 'stroke-width':str(width), 'fill':fill}
    rect_attribs = {'style':simplestyle.formatStyle(style),
                    inkex.addNS('label','inkscape'):name,
                    'x':str(x), 'y':str(y), 'width':str(w), 'height':str(h)}
    inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), rect_attribs )

def colorString(pickerColor):
    longcolor = long(pickerColor)
    if longcolor < 0:
        longcolor = longcolor & 0xFFFFFFFF
    return '#' + format(longcolor/256, '06X')


class Grid_Perspective(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--size_unit",
                        action="store", type="string", 
                        dest="size_unit", default="",
                        help="Units for geometry")
        self.OptionParser.add_option("--width",
                        action="store", type="int", 
                        dest="width", default=500,
                        help="Width of grid window")
        self.OptionParser.add_option("--height",
                        action="store", type="int", 
                        dest="height", default=300,
                        help="Height of grid window")
        self.OptionParser.add_option("--p_divs",
                        action="store", type="int", 
                        dest="p_divs", default=10,
                        help="Number of divisions in perspective angle")
        self.OptionParser.add_option("--horizon",
                        action="store", type="float", 
                        dest="horizon", default=150,
                        help="Y coordinate of horizon")
        self.OptionParser.add_option("--left_x",
                        action="store", type="float", 
                        dest="left_x", default=-250,
                        help="X coordinate of left perspective point")
        self.OptionParser.add_option("--right_x",
                        action="store", type="float", 
                        dest="right_x", default=750,
                        help="X coordinate of right perspective point")
        self.OptionParser.add_option("--div_th",
                        action="store", type="float", 
                        dest="div_th", default=2,
                        help="Grid division line thickness")
        self.OptionParser.add_option("--div_color",
                        action="store", type="int", 
                        dest="div_color", 
                        help="Grid division line color")
        self.OptionParser.add_option("--border_th",
                        action="store", type="float", 
                        dest="border_th", default=3,
                        help="Border Line thickness")

    def EdgePoints(self,x0, y0, theta):
        #  find the intersection points of the line with the extended
        #  grid bounding box.
        #  Note that y is positive DOWN, not up
        #  Grid bounding box goes from (0,0) to (self.xmax, self.ymax)
        theta_r = radians(theta)
        if theta_r == 0:
	    return [[0,y0],[self.xmax,y0],
                    [-100, self.ymax], [self.xmax+100,0]] 
        r_bot = (self.ymax-y0)/sin(theta_r)
        r_top = -y0/sin(theta_r)
        r_left = -x0/cos(theta_r)
        r_right = (self.xmax-x0)/cos(theta_r)
        return [[0,y0+r_left*sin(theta_r)], # left
                [self.xmax, y0+r_right*sin(theta_r)], # right
                [x0+r_bot*cos(theta_r), self.ymax], #bottom
               [x0+r_top*cos(theta_r), 0]] #top

    def trimmed_coords(self, x1, y1, theta):
	#find the start and end coordinates for a grid line
	#starting at (x1, y1) with an angle of theta
	border_points = self.EdgePoints(x1, y1, theta)
        left = 0
        right = 1
        top = 3
        bottom = 2
        x=0
        y=1
	if theta > 0:
            if border_points[left][y] < 0:
		start_x = border_points[top][x]
                start_y = border_points[top][y]
            else:
		start_x = border_points[left][x]
                start_y = border_points[left][y]
            if border_points[right][y] > self.ymax:
		end_x = border_points[bottom][x]
                end_y = border_points[bottom][y]
            else:
		end_x = border_points[right][x]
                end_y = border_points[right][y]
        else:
            if border_points[left][y] > self.ymax:
		start_x = border_points[bottom][x]
                start_y = border_points[bottom][y]
            else:
		start_x = border_points[left][x]
                start_y = border_points[left][y]
            if border_points[right][y] < 0:
		end_x = border_points[top][x]
                end_y = border_points[top][y]
            else:
		end_x = border_points[right][x]
                end_y = border_points[right][y]
	return [[start_x,start_y],[end_x, end_y]]

    def drawAngledGridLine (self, x1, y1, theta, thickness, color, 
                            label, groupName):
        end_points = self.trimmed_coords(x1, y1, theta)
        x_start = end_points[0][0]
        y_start = end_points[0][1]
        x_end = end_points[1][0]
        y_end = end_points[1][1]

        if (x_start >= 0 and x_start <= self.xmax and 
                y_start >= 0 and y_start <= self.ymax and
                x_end >= 0 and x_end <= self.xmax and 
                y_end >= 0 and y_end <= self.ymax):
            draw_SVG_line(x_start, y_start,
                          x_end, y_end,
                          thickness, colorString(color), label, groupName)
	
    def perspective_intersection(self, left_theta, right_theta):
        if right_theta == 0 or left_theta == 0 or left_theta == right_theta:
            return -100   # outside of bounding box
        r=(self.right_x - self.left_x)/(sin(right_theta)/tan(left_theta)-cos(right_theta))
        y_int = self.horizon + r*sin(right_theta)
        if y_int < 0 or y_int > self.ymax :
            return -100 #above or below bounding box
        return self.right_x + r*cos(right_theta)

    def effect(self):
        
        #find the pixel dimensions of the overall grid
        self.ymax = self.unittouu(str(self.options.height)+self.options.size_unit)
        self.xmax = self.unittouu(str(self.options.width)+self.options.size_unit)
        self.horizon = self.unittouu(str(self.options.horizon)+self.options.size_unit)
        self.left_x = self.unittouu(str(self.options.left_x)+self.options.size_unit)
        self.right_x = self.unittouu(str(self.options.right_x)+self.options.size_unit)
       

        # Embed grid in group
        #Put in in the centre of the current view
        t = 'translate(' + str( self.view_center[0]- self.xmax/2.0) + ',' + \
                           str( self.view_center[1]- self.ymax/2.0) + ')'
        g_attribs = {inkex.addNS('label','inkscape'):'Grid_Perspective:Size' + \
                     str( self.xmax)+'x'+str(self.ymax) +
                     ':Horizon'+str(self.horizon) +
                     ':LeftX'+str(self.left_x) +
                     ':RightX'+str(self.right_x),
                     'transform':t }
        grid = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)
        
        #Group for vertical gridlines
        g_attribs = {inkex.addNS('label','inkscape'):'VerticalGridlines'}
        gv = inkex.etree.SubElement(grid, 'g', g_attribs)

        #Group for left point gridlines
        g_attribs = {inkex.addNS('label','inkscape'):'LeftPointGridlines'}
        glp = inkex.etree.SubElement(grid, 'g', g_attribs)
        
        #Group for right point gridlines
        g_attribs = {inkex.addNS('label','inkscape'):'RightPointGridlines'}
        grp = inkex.etree.SubElement(grid, 'g', g_attribs)
        
        draw_SVG_rect(0, 0, self.xmax, self.ymax, self.options.border_th,
                      colorString(self.options.div_color), 'none',
                      'Border', grid) #border rectangle
        

        # Calculate the extreme angles for the left and right points
        if self.horizon < 0 :
            left_theta_min = atan((self.horizon-0)/(0-self.right_x))
            left_theta_max = atan((self.ymax - self.horizon)/
                                   (0-self.left_x))
            right_theta_min = atan((0-self.horizon)/
                                    (self.left_x-self.xmax))
            right_theta_max = atan((self.horizon - self.ymax)/
                                    (self.right_x - self.xmax ))
        elif self.horizon < self.ymax :
            left_theta_min = atan((self.horizon-0)/(self.left_x-0))
            left_theta_max = atan((self.ymax - self.horizon)/
                                   (0-self.left_x))
            right_theta_min = atan((self.horizon-0)/
                                    (self.right_x-self.xmax))
            right_theta_max = atan((self.horizon - self.ymax)/
                                    (self.right_x - self.xmax ))
        else:
            left_theta_min = atan((self.horizon-0)/(self.left_x-0))
            left_theta_max = atan((self.ymax - self.horizon)/
                                   (0-self.right_x))
            right_theta_min = atan((self.horizon-0)/
                                    (self.right_x-self.xmax))
            right_theta_max = atan((self.horizon - self.ymax)/
                                    (self.left_x - self.xmax ))

        left_dtheta = (left_theta_max - left_theta_min)/float(self.options.p_divs)

        right_dtheta = (right_theta_max - right_theta_min)/float(self.options.p_divs)
        mid_index = self.options.p_divs/2
        left_mid_theta = left_theta_min + mid_index * left_dtheta
        right_mid_theta = right_theta_min + mid_index * right_dtheta

 
        #DO THE PERSPECTIVE DIVISONS========================================
        for i in range(0,self.options.p_divs+1): 
            left_theta = left_theta_min + i * left_dtheta
            right_theta = right_theta_min + i * right_dtheta
            self.drawAngledGridLine(self.left_x, self.horizon, 
                               degrees(left_theta),
                               self.options.div_th,
                               self.options.div_color,
                               'LeftDivPersp'+str(i),
                               glp)
            self.drawAngledGridLine(self.right_x, self.horizon, 
                               degrees(right_theta),
                               self.options.div_th,
                               self.options.div_color,
                               'RightDivPersp'+str(i),
                               grp)
            intersection = self.perspective_intersection(left_theta,
                                                  right_theta_max - i * right_dtheta)
            if intersection > 0 and intersection < self.xmax:
                draw_SVG_line(intersection, 0,
                              intersection, self.ymax,
                              self.options.div_th,
                              colorString(self.options.div_color),
                              'VerticalDiv'+str(i), gv)
            comment = """
            intersection = self.perspective_intersection(left_theta, right_mid_theta)
            if intersection > 0 and intersection < self.xmax:
                draw_SVG_line(intersection, 0,
                              intersection, self.ymax,
                              self.options.div_th,
                              colorString(self.options.div_color),
                              'VerticalDiv'+str(i), gv)
            intersection = self.perspective_intersection(left_theta, right_theta)
            if intersection > 0 and intersection < self.xmax:
                draw_SVG_line(intersection, 0,
                              intersection, self.ymax,
                              self.options.div_th,
                              colorString(self.options.div_color),
                              'VerticalDiv'+str(i), gv)
            """

        intersection = self.perspective_intersection(left_mid_theta, right_mid_theta)
        if intersection > 0 and intersection < self.xmax:
            draw_SVG_line(intersection, 0,
                          intersection, self.ymax,
                          self.options.div_th,
                          colorString(self.options.div_color),
                          'VerticalDiv'+str(i), gv)



if __name__ == '__main__':
    e = Grid_Perspective()
    e.affect()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 encoding=utf-8 textwidth=99
