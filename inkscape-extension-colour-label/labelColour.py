#!/usr/bin/env python2
# -*- coding: utf-8 -*-


"""
A inkscape plugin to label features with their fill colour


Copyright (C) 2019 Christoph Fink

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


import cubicsuperpath
import inkex
import simplepath
import simplestyle
import simpletransform


class LabelColour(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        if len(self.selected) > 0:
            for id, node in self.selected.iteritems():
                self.labelFeature(node)

    def labelFeature(self, node):
        if True: #try:
            nodeStyle = simplestyle.parseStyle(node.attrib["style"])

            nodeColour, labelColour = \
                self.getNodeAndLabelColours(nodeStyle["fill"])
            nodeX, nodeY, nodeWidth, nodeHeight = \
                self.getNodeDimensions(node)

            parent = self.getParentNode(node)

            label = inkex.etree.SubElement(
                parent,
                inkex.addNS("text", "svg"),
                {
                    "x": str(nodeX + (nodeWidth/2)),
                    "y": str(nodeY + (nodeHeight/2)),
                    "dy": "0.5em",
                    "style": simplestyle.formatStyle({
                        "fill": labelColour,
                        "stroke": "none",
                        "text-anchor": "middle"
                    })
                }
            )
            labelTextSpan = inkex.etree.SubElement(
                label,
                inkex.addNS("tspan", "svg"),
                {}
            )
            labelTextSpan.text = nodeColour

        #except Exception as e:
        #    inkex.debug(str(e))

    def getNodeAndLabelColours(self, nodeStyleFill):
        if nodeStyleFill[:5] == "url(#":
            nodeFill = self.getElementById(nodeStyleFill[5:-1])
            if "Gradient" in nodeFill.tag:
                nodeColour, labelColour = \
                    self.getNodeAndLabelColourForGradient(
                        nodeFill
                    )
            else:
                nodeColour = ""
                labelColour = ""

        else:
            nodeColour = nodeStyleFill
            labelColour = self.getLabelColour(nodeColour)

        return (nodeColour, labelColour)

    def getNodeAndLabelColourForGradient(self, gradientNode):
        stops = self.getGradientStops(gradientNode)

        nodeColours = []

        for stop in stops:
            offset = float(stop[0])
            colour = stop[1]
            nodeColours.append("{colour:s}{offset:s}".format(
                colour=colour,
                offset="" if offset in (0, 1) else " ({:0.2f})".format(offset)
            ))
        nodeColour = u" ↔ ".join(nodeColours)

        avgNodeColour = [
            sum([
                simplestyle.parseColor(stop[1])[c]
                for stop in stops
            ]) / len(stops)
            for c in range(3)
        ]

        labelColour = \
            self.getLabelColour(simplestyle.formatColoria(avgNodeColour))

        return (nodeColour, labelColour)

    def getGradientStops(self, gradientNode):
        while "{http://www.w3.org/1999/xlink}href" in gradientNode.attrib:
            gradientNode = \
                self.getElementById(
                    gradientNode.attrib["{http://www.w3.org/1999/xlink}href"][1:]  # noqa:E129
                )

        stops = []

        for child in gradientNode:
            if "stop" in child.tag:
                stopStyle = simplestyle.parseStyle(child.attrib["style"])
                stops.append((child.attrib["offset"], stopStyle["stop-color"]))

        # if only opacity differs (colour == same), return one stop only:
        if len(set([s[1] for s in stops])) == 1:
            stops = [(0, stops[0][1])]

        return stops

    def getLabelColour(self, nodeColour):
        labelColour = "#000000"

        try:
            nodeColour = simplestyle.parseColor(nodeColour)
            if sum(nodeColour) / len(nodeColour) < 128:
                labelColour = "#ffffff"
        except (
            TypeError,
            ZeroDivisionError  # if parseColor returns ""
        ):
            pass

        return labelColour

    def getNodeDimensions(self, node):
        try:
            nodeX = float(node.attrib["x"])
            nodeY = float(node.attrib["y"])
            nodeWidth = float(node.attrib["width"])
            nodeHeight = float(node.attrib["height"])
        except Exception:
            try:
                (nodeMinX, nodeMaxX, nodeMinY, nodeMaxY) = \
                    simpletransform.roughBBox(node.attrib["d"])
            except Exception:
                (nodeMinX, nodeMaxX, nodeMinY, nodeMaxY) = \
                    simpletransform.roughBBox(
                        cubicsuperpath.CubicSuperPath(
                            simplepath.parsePath(node.attrib["d"])
                        )
                    )
            nodeX = nodeMinX
            nodeY = nodeMinY
            nodeWidth = nodeMaxX - nodeMinX
            nodeHeight = nodeMaxY - nodeMinY

        return nodeX, nodeY, nodeWidth, nodeHeight


labelColour = LabelColour()
labelColour.affect()
