#!/usr/bin/perl
#
# Copyright (C) 2016 Kie Brooks
# Distributed under GPLv3 or later.
# draw_ratchet
# version 0.1
#
#   This file is part of draw_ratchet
#
#   draw_ratchet is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# description :
# draw ratchet gears to arbitrary sizes and precision
#
# I am not an engineer, I am sure this little program could be improved or made much more complex,
# it may contain horrible flaws but it fills my current need and should be easy to improve on.
# Alternatively pay me some money and I might do it for you ;P
#
# This program is used by inkscape.
# It can be found in the menu :  extensions -> render -> ratchet
# see file draw_ratch.inx
# (directory ~/.config/inkscape/extensions/)

use strict;
use warnings;

use Getopt::Long;

my $teeth;
my ($centre_hole, $centre_hole_diam, $c_x, $c_y);
my ($diam_in, $diam_out);
my ($vtooth_shape, $htooth_shape);
#  <param name="teeth" type="int" min="2" max="300" gui-text="Number of teeth">12</param>
#  <param name="centre_hole" type="boolean" gui-text="Centre hole">true</param>
#  <param name="centre_hole_diam" type="float" precision="3" min="0" max="50" gui-text="Centre hole size">1.000</param>
#  <param name="diam_in" type="float" precision="3" min="0" max="200" gui-text="Outside diameter">30.000</param>
#  <param name="diam_out" type="float" precision="3" min="0" max="200" gui-text="Inside diameter">28.000</param>
#  <param name="vtooth_shape" type="optiongroup" _gui-text="Vertical tooth line:">
#      <option value="straight">straight</option>
#      <option value="curve">curve</option></param>
#   <param name="htooth_shape" type="optiongroup" _gui-text="Horizontal tooth line:">
#     <option value="straight">straight</option>
#     <option value="curve">curve</option></param>
my $arguments = GetOptions (
    "teeth=i" => \$teeth,                       # integer
    "centre_hole=s" => \$centre_hole, # boolean flag (but actually gets passed the option true or false
    "centre_hole_diam=f" => \$centre_hole_diam, # floating point
    "diam_in=f" => \$diam_in,# floating point
    "diam_out=f" => \$diam_out, # floating point
    "vtooth_shape=s" => \$vtooth_shape, # string
    "htooth_shape=s" => \$htooth_shape #string
    );

#(alternative look at @ARGV)


my @svg_constr;
my $svg_count = 0;
my $line;

### default values #############################################
# set number of teeth (int)
unless ($teeth) {
    $teeth = 24;
}

# set centre hole on / off (boolean) but we will go with "true/false" as passed by inkscape
#$centre_hole = 1;
# set centre position cx, cy, default 0,0, (float)
$c_x = 0;
$c_y = 0;
unless ($centre_hole) {
	$centre_hole = "true";
}
unless ($centre_hole_diam) {
	$centre_hole_diam = 10;
}

# set outside diameter (some arbitrary value) (unsigned float)
unless ($diam_out) {
    $diam_out  = 15.75;
}

# set inside diameter (outside diameter - hole depth)
# this should be less than the outer diameter but that's up to you! (unsigned float)
unless ($diam_in) {
    $diam_in = 14.5;
}

unless ($vtooth_shape) {
    $vtooth_shape = "straight";
}
unless ($htooth_shape) {
    $htooth_shape = "straight";
}
#########################################################


# begin  SVG print
$line = '<svg xmlns="http://www.w3.org/2000/svg"';
$svg_constr[$svg_count++] = $line;
print "$line\n";

$line = ' xmlns:xlink="http://www.w3.org/1999/xlink">'."\n";
$svg_constr[$svg_count++] = $line;
print "$line\n";

if ($centre_hole eq "true") {
    $line = '<circle cx="'.$c_x.'" cy="'.$c_y.'" r="'.$centre_hole_diam.'" stroke="black" stroke-width="0.1" fill="none" />';
    $svg_constr[$svg_count++] = $line;
    print "$line\n";
}

#begin polygon drawing
#    <path d="M50,50 A30,50 0 0,1 100,100"
#          style="stroke:#660000; fill:none;"/>
# L - line : x posn, y posn
# A - arc : radius x, radius y, x-axis rotation, large arc flag, sweep flag
#
# points on the ratchet
#
#    b
#    |\
#    |  \    |\
# \  |    \  |  \
#  \ |      \|    \
#    a     c      \
#

my $begin_polygon = 1;
for (my $i = 0; $i < $teeth ; $i++) {
    my ($x_a, $x_b, $x_c); # x coordinates
    my ($y_a, $y_b, $y_c); # y coordinates
    my ($angle, $angle_next);

    # oh , perl uses radians instead of degrees.
    my $pi = 3.14159265358979;
    # sub deg_to_rad { ($_[0]/180) * $pi }

    $angle = $i * 360 / $teeth;
    $angle = deg_to_rad($angle);

    $x_a = $diam_in * cos($angle) ;
    $y_a = $diam_in * sin($angle);
    $x_b = $diam_out * cos($angle);
    $y_b = $diam_out * sin($angle);

    if ($begin_polygon) {
	$line = '<path d="M'.$x_a." ".$y_a;
	$svg_constr[$svg_count++] = $line;
	print "$line\n";
	$begin_polygon = 0;
    }

    # draw_straight_line(x_a,y_a,x_b,y_b); // draw straight line
    if ($vtooth_shape eq "straight") {
	$line = ' L'.$x_b.' '.$y_b;
#	$line = ' L'.$x_b.' '.$y_b.' stroke="black" stroke-width="1" fill="none"';
    } else {
	# (rx ry x-axis-rotation large-arc-flag sweep-flag x y)
	$line = ' A'.' '.$diam_in.', '.$diam_in.' 0 0, 0 '.$x_b.', '.$y_b;
    }
    $svg_constr[$svg_count++] = $line;
    print "$line\n";

    $angle_next = ($i+1) * 360 / $teeth;
    $angle_next = deg_to_rad($angle_next);

    $x_c = $diam_in * cos($angle_next);
    $y_c = $diam_in * sin($angle_next);

    #//ok, let's work out the center of the circle, xc, yc
    #//
#    my $dbc = (($x_b-$x_c)^2 + ($y_b-$y_c)^2)^1/2;   # distance from a to b
#    my $dbch = $dbc/2;                                                        # half the distance from a to b
#    my $x_m = ($x_b + $x_c)/2;                                         # x midpoint
#    my $y_m = ($y_b + $y_c)/2;                                         # y midpoint
#    my $h = ($x_b - $x_c) / ($y_c - $y_b);                        # gradient from center of circle to midpoint
#    my $a = ($diam_in^2 - $dbch^2)^(1/2);                      # distance from center of circle to a or b
#    my $x_centre = $x_m + $a * ($y_b - $y_c) / $dbc;
#    my $y_centre = $y_m + $a * ($x_c - $x_b) / $dbc;
#    my $x_c2 = $x_m - a * ($y_b - $y_c)/$dbc; # other x centre point
#    my $y_c2 = $y_m - a * ($x_c - $x_b)/$dbc; # other y centre point

    # draw arc
    # radius x, radius y x-axis rotation large arc flag, sweep flag, end_point x, endpoint y
    if ($htooth_shape eq "straight") {
	$line = ' L'.$x_c.' '.$y_c.' ';
    } else { # value curve
	$line = ' A'.' '.$diam_in.', '.$diam_in.' 0 0, 1 '.$x_c.', '.$y_c;
    }
    $svg_constr[$svg_count++] = $line;
    print "$line\n";

}

#finish polygon drawing
$line = '" style="stroke: black; stroke-width: 0.1; join: round; fill: none" />';
#$line = '"/>';
$svg_constr[$svg_count++] = $line;
print "$line\n";

$line = '</svg>';
$svg_constr[$svg_count++] = $line;
print "$line\n";

# print out @svg_construction
#foreach (@svg_constr) {
#  print "$_\n";
#}



### subroutines #####################################################

sub deg_to_rad {
    my $pi = 3.14159265358979;
    return ($_[0]/180) * $pi;
}

exit 1;
