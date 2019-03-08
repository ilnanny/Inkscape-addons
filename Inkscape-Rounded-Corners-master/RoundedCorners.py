#!/usr/bin/env python 

"""
==============================================================================================
  Rounded Corners Version 1.3 by Chris Hawley
  
  This effect is designed to round off the corners on shapes made with the pencil tool.
  It will round off corners made of straight edges, while ignoring bezier lines.
  Corners that are too short for the desired radius will also be ignored.
  It does not work on Inkscape objects like the rectangle or star - 
  the user must convert objects to paths before using this extension.
  
  Usage: 
  1.  Select or create a polygon in Inkscape using the pencil tool 
  2.  Click Extensions->Modify Path->Rounded Corners.  
  3.  Fill out the options in the dialog that pop up
		- Choose the radius for rounding
		- Pick units (Inches, centimeters, etc.)
		- pick whether you want left corners, right corners, or both to be rounded
		- select "Live preview" to see how your selecttions affect the shape before applying
  4.  Click Apply.
==============================================================================================
"""

"""
The MIT License (MIT)
Copyright (c) 2019 Chris Hawley
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


"""
==============================================================================================
Vector class from https://gist.github.com/mcleonard/5351452
The MIT License (MIT)
Copyright (c) 2015 Mat Leonard
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
================================================================================================
begin Vector Class by Mat Leonard	
================================================================================================
"""	
class Vector(object):
    def __init__(self, *args):
        """ Create a vector, example: v = Vector(1,2) """
        if len(args)==0: self.values = (0,0)
        else: self.values = args
        
    def norm(self):
        """ Returns the norm (length, magnitude) of the vector """
        return math.sqrt(sum( comp**2 for comp in self ))
        
    def argument(self):
        """ Returns the argument of the vector, the angle clockwise from +y."""
        arg_in_rad = math.acos(Vector(0,1)*self/self.norm())
        arg_in_deg = math.degrees(arg_in_rad)
        arg_in_deg = math.degrees(arg_in_rad)
        if self.values[0]<0: return 360 - arg_in_deg
        else: return arg_in_deg

    def normalize(self):
        """ Returns a normalized unit vector """
        norm = self.norm()
        normed = tuple( comp/norm for comp in self )
        return Vector(*normed)
    
    def rotate(self, *args):
        """ Rotate this vector. If passed a number, assumes this is a 
            2D vector and rotates by the passed value in degrees.  Otherwise,
            assumes the passed value is a list acting as a matrix which rotates the vector.
        """
        if len(args)==1 and type(args[0]) == type(1) or type(args[0]) == type(1.):
            # So, if rotate is passed an int or a float...
            if len(self) != 2:
                raise ValueError("Rotation axis not defined for greater than 2D vector")
            return self._rotate2D(*args)
        elif len(args)==1:
            matrix = args[0]
            if not all(len(row) == len(v) for row in matrix) or not len(matrix)==len(self):
                raise ValueError("Rotation matrix must be square and same dimensions as vector")
            return self.matrix_mult(matrix)
        
    def _rotate2D(self, theta):
        """ Rotate this vector by theta in degrees.
            
            Returns a new vector.
        """
        theta = math.radians(theta)
        # Just applying the 2D rotation matrix
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc*x - ds*y, ds*x + dc*y
        return Vector(x, y)
        
    def matrix_mult(self, matrix):
        """ Multiply this vector by a matrix.  Assuming matrix is a list of lists.
        
            Example:
            mat = [[1,2,3],[-1,0,1],[3,4,5]]
            Vector(1,2,3).matrix_mult(mat) ->  (14, 2, 26)
         
        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions') 
        
        # Grab a row from the matrix, make it a Vector, take the dot product, 
        # and store it as the first component
        product = tuple(Vector(*row)*self for row in matrix)
        
        return Vector(*product)
    
    def inner(self, other):
        """ Returns the dot product (inner product) of self and other vector
        """
        return sum(a * b for a, b in zip(self, other))
    
    def __mul__(self, other):
        """ Returns the dot product of self and other if multiplied
            by another Vector.  If multiplied by an int or float,
            multiplies each component by other.
        """
        if type(other) == type(self):
            return self.inner(other)
        elif type(other) == type(1) or type(other) == type(1.0):
            product = tuple( a * other for a in self )
            return Vector(*product)
    
    def __rmul__(self, other):
        """ Called if 4*self for instance """
        return self.__mul__(other)
            
    def __div__(self, other):
        if type(other) == type(1) or type(other) == type(1.0):
            divided = tuple( a / other for a in self )
            return Vector(*divided)
    
    def __add__(self, other):
        """ Returns the vector addition of self and other """
        added = tuple( a + b for a, b in zip(self, other) )
        return Vector(*added)
    
    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        subbed = tuple( a - b for a, b in zip(self, other) )
        return Vector(*subbed)
    
    def __iter__(self):
        return self.values.__iter__()
    
    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        return self.values[key]
        
    def __repr__(self):
		return str(self.values)
	
"""
================================================================================================
end Vector Class by Mat Leonard	
================================================================================================
"""	





"""
================================================================================================
Begin Rounded Corners By Chris Hawley
================================================================================================
"""	
import inkex
import simplepath
import re
import math
import sys

class RoundedCorners(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--RCradius",
				action="store", type="float", 
				dest="RCradius", default=1.0,
				help="Radius for rounded corners")
		self.OptionParser.add_option("--units", action="store",
                                     type="string", dest="units",
                                     default="25.4/96") # Inches
		
		
		self.OptionParser.add_option("--LeftCorners", action="store",
							 type="string", dest="LeftCorners",
							 default=True) 
							 
		self.OptionParser.add_option("--RightCorners", action="store",
							 type="string", dest="RightCorners",
							 default=True) 							 
							 
		self.newPath = []


	def effect(self):
		foundPath = False
		succeededRounding = False
		selection = self.selected
		if (selection):
			for id, node in selection.iteritems():
				if node.tag == inkex.addNS('path','svg'):
					succeededRounding = self.MakeRound(node) or succeededRounding
					foundPath = True
			if foundPath == False:
				inkex.errormsg("Suitable path not found.  Try converting to path first using the menu item 'Path->Object to Path'.")
			elif not succeededRounding:
				inkex.errormsg("Couldn't find any suitable corners to round.  Try decreasing the Rounded Corner Radius.")
		else:
			inkex.errormsg("Please select an object.")
	
	
	def RoundCorner(self, cursorIndex, line1Index, arcIndex, line2Index):
		#
		#    p2 _________ p3
		#      |
		#      |    p0
		#   p1 |
		
		#sys.stderr.write(str((cursorIndex, line1Index, arcIndex, line2Index)))
		
		
		#radius. defined by user dialog
		r=self.options.RCradius
		
		roundLeft = self.options.LeftCorners.lower() == 'true'
		roundRight = self.options.RightCorners.lower() == 'true'
		
		if (not roundLeft) and (not roundRight):
			return True
		
		scale = eval(self.options.units)
		if not scale:
			scale = 25.4/96     
		scale /= self.unittouu('1px')
		r /= scale

		p1 = Vector( self.newPath[cursorIndex][1][-2], self.newPath[cursorIndex][1][-1] )
		p2 = Vector( self.newPath[line1Index][1][-2], self.newPath[line1Index][1][-1] )
		p3 = Vector( self.newPath[line2Index][1][-2], self.newPath[line2Index][1][-1] )

		if (p1-p2).norm() < .0001:
			return
		if (p2-p3).norm() < .0001:
			return
		
		
		#L20 = bisecting line. 320 and 120 are right triangles
		
		#point on line L12 that is 1 unit away from p2 (normalized)
		n1 = (p1 - p2).normalize() + p2
		n3 = (p3 - p2).normalize() + p2
		
		
		p0 = n1 + n3
		p0 = p0 / 2.0
		

		#V vectors are normalized lines translated to the origin
		V12 = (p2 - p1).normalize()
		V12angle = math.atan2(V12[1], V12[0])
		V12PerpRightx = math.cos(V12angle + math.pi/2)
		V12PerpRighty = math.sin(V12angle + math.pi/2)


		V23 = (p3 - p2).normalize()
		V23angle = math.atan2(V23[1], V23[0])
		V23PerpRightx = math.cos(V23angle + math.pi/2)
		V23PerpRighty = math.sin(V23angle + math.pi/2)

		V13 = p3 - p1

		#dot product of V13 and the vector perpendicular to V12
		facingRight = (V12PerpRightx * V13[0] + V12PerpRighty * V13[1]) > 0

		#distance from point p0 to line L12
		p0x = p0[0]
		p0y = p0[1]
		p1x = p1[0]
		p1y = p1[1]
		p2x = p2[0]
		p2y = p2[1]
		
		p0Dist = abs((p2y - p1y)*p0x - (p2x - p1x)*p0y + p2x * p1y - p2y*p1x)/math.sqrt((p2y-p1y)**2 + (p2x-p1x)**2)
		multiplier = r/p0Dist

		#p5 on the line L20, but the correct distance so that it is r away from the other lines
		#it is the center point for the circle of radius r that touches the other 2 lines
		p5 = (p0-p2)*multiplier + p2

		#Tangent1: where circle with radius r, centered on p5 touches the line L12. Tangent 2 is where circle touches L23
		V12PerpRight = Vector(V12PerpRightx, V12PerpRighty)
		V23PerpRight = Vector(V23PerpRightx, V23PerpRighty)
		
		if facingRight:
			Tangent1 = p5 - V12PerpRight * r
			Tangent2 = p5 - V23PerpRight * r
		
		else: 
			Tangent1 = p5 + V12PerpRight * r
			Tangent2 = p5 + V23PerpRight * r

		#check that [tangent points are closer to p2] than p1 and p3 are
		#if so, replace line from p1 to p1, and line from p2 to p3 with:
		#arc, starting on tangent1, centered at p5, radius r, ending on tangent2
		#A rx ry x-axis-rotation large-arc-flag sweep-flag x y
		
		allowed = True
		
		if facingRight and (not roundRight):
			allowed = False;
			
		if (not facingRight) and (not roundLeft):
			allowed = False;
		
		if ((Tangent1 - p2).norm() > (p1 - p2).norm() + 0.001) or ((Tangent2 - p2).norm() > (p3 - p2).norm() + 0.001):
			allowed = False
			
		if allowed:
			
			#line from p1 to tangent 1
			self.newPath[line1Index] = ("L", [Tangent1[0], Tangent1[1]])
			if facingRight:
				self.newPath[arcIndex] = ("A", [ r,r,0,0,1,Tangent2[0],Tangent2[1]])
			else:
				self.newPath[arcIndex] = ("A", [ r,r,0,0,0,Tangent2[0],Tangent2[1]])
				
		return allowed
	
	def MakeRound(self, node):
		dArr = simplepath.parsePath(node.get('d'))
		dLen = len(dArr)
		
		if dLen < 3:
			return 
		
		self.newPath = []
		isClosed = False
		
		#make a new list of tupples. each tupple is a letter string, and a list of parameters
		#every other tupple will start blank to make room for adding possible arcs as curved corners
		
		for i in range(dLen):
			cmd, params = dArr[i]
			if cmd != "Z":
				self.newPath.append((cmd, params))
				self.newPath.append(("",[]))
			else:
				isClosed = True
			
		if isClosed:
			endIndex = len(self.newPath) - 1
		else:
			endIndex = len(self.newPath) - 4
		
		npLen = len(self.newPath)
		
		succeeded = False
		
		debuglog = ""
		
		for n in range(0, endIndex, 2):
			#get first point of possible corner
			if self.newPath[(n+1) % npLen][0] != '':
				cursorIndex = (n+1) % npLen
			else:
				cursorIndex = n
		
			#check if other 2 points are L, M, or Z commands. if so we have a corner
			if self.newPath[(n+2) % npLen][0] in "LMZ" and self.newPath[(n+4) % npLen][0] in "LMZ":
				
				succeeded = self.RoundCorner(cursorIndex, (n+2) % npLen, (n+3) % npLen, (n+4) % npLen) or succeeded
			
		firstCommand, firstArgs = self.newPath[0]
		self.newPath[0] = ('M', [firstArgs[-2], firstArgs[-1]]);
		
		
		newDString = ""
		
		for cmd, params in self.newPath:
			if cmd != '':
				newDString += (cmd + " ")
				newDString += ",".join(map (str, params))
				newDString += "\n"
		
		if isClosed:
			newDString += "Z\n"
		
		if succeeded:
			node.set('d', newDString)

		return succeeded



if __name__ == '__main__':
	e = RoundedCorners()
	e.affect()

	
	
	
	

