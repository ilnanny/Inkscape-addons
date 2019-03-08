#! /usr/bin/python
# -*- coding: cp1252 -*-
"""
graphviz.py
This extension renders DOT files to SVG paths.

Copyright (C) 2017 Thomas Flynn <tflynn@gradcenter.cuny.edu>

Based on EqTexSvg by Julien Vitard <julienvitard@gmail.com>

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

"""

import inkex, os, tempfile, sys, xml.dom.minidom

class DOTSVG(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        # The one option is 'dotfile', the filename that is passed to dot.
        self.OptionParser.add_option("-f", "--dotfile",
                        action="store", type="string",
                        dest="dotfile", default="",
                        help="DOT file")
        
    #effect: this function provides the main feature of the plugin.
    #it calls dot with the users' file and imports the resulting svg
    #onto the inkscape canvas.
    def effect(self):
        base_dir = tempfile.mkdtemp("", "inkscape-");
        svg_file = os.path.join(base_dir, "eq.svg") #svg output from DOT
        out_file = os.path.join(base_dir, "eq.out") #stdout messages from DOT
        err_file = os.path.join(base_dir, "eq.err") #stderr messages from DOT

        # Clean: remove temporary files generated during plugin execution.
        def clean():
            if os.path.exists(svg_file):
                os.remove(svg_file)
            if os.path.exists(out_file):
                os.remove(out_file)
            if os.path.exists(err_file):
                os.remove(err_file)
            os.rmdir(base_dir)

        # Execute the dot command, to generate the svg from the users file.
        os.system('dot "%s" -Tsvg:cairo -o "%s" > "%s" 2> "%s"' \
                  % (self.options.dotfile, svg_file, out_file, err_file))
        
        #if there was no output svg_file, tell the user
        try:
            os.stat(svg_file)
        except OSError:
            print >>sys.stderr, "Invalid DOT input:"
            print >>sys.stderr, self.options.dotfile
            print >>sys.stderr, "temporary files were left in:", base_dir
            sys.exit(1)

        if os.path.exists(err_file):
            err_stream = open(err_file, 'r')
            for line in err_stream:
                sys.stderr.write(line + '\n')
            err_stream.close()
            
        # Attempt to open the svg and place it on the inkscape canvas.
        doc = inkex.etree.parse(svg_file)
        svg = doc.getroot()
        self.current_layer.append(svg)

        # Finish up
        clean()

if __name__ == '__main__':
    e = DOTSVG()
    e.affect()
