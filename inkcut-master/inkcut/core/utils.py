"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jul 12, 2015

@author: jrm
"""
import os
import sys
import logging
from enaml.image import Image
from enaml.icon import Icon, IconImage
from enaml.application import timed_call
from enaml.qt.QtCore import QPointF
from enaml.qt.QtGui import QPainterPath
from twisted.internet.defer import Deferred
from .svg import QtSvgDoc


# -----------------------------------------------------------------------------
# Logger
# -----------------------------------------------------------------------------
log = logging.getLogger("inkcut")


def clip(s, n=1000):
    """ Shorten the name of a large value when logging"""
    v = str(s)
    if len(v) > n:
        v[:n]+"..."
    return v

# -----------------------------------------------------------------------------
# Icon and Image helpers
# -----------------------------------------------------------------------------
#: Cache for icons
_IMAGE_CACHE = {}


def icon_path(name):
    """ Load an icon from the res/icons folder using the name 
    without the .png
    
    """
    path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(path, 'res', 'icons', '%s.png' % name)


def load_image(name):
    """ Get and cache an enaml Image for the given icon name.
    
    """
    path = icon_path(name)
    global _IMAGE_CACHE
    if path not in _IMAGE_CACHE:
        with open(path, 'rb') as f:
            data = f.read()
        _IMAGE_CACHE[path] = Image(data=data)
    return _IMAGE_CACHE[path]


def load_icon(name):
    img = load_image(name)
    icg = IconImage(image=img)
    return Icon(images=[icg])


def menu_icon(name):
    """ Icons don't look good on Linux/osx menu's """
    if sys.platform == 'win32':
        return load_icon(name)
    return None


# -----------------------------------------------------------------------------
# Unit conversion
# -----------------------------------------------------------------------------
def from_unit(val, unit='px'):
    return QtSvgDoc.convertFromUnit(val, unit)


def to_unit(val, unit='px'):
    return QtSvgDoc.convertToUnit(val, unit)


def parse_unit(val):
    """ Parse a string into pixels """
    return  QtSvgDoc.parseUnit(val)


unit_conversions = QtSvgDoc._uuconv

# -----------------------------------------------------------------------------
# Async helpers
# -----------------------------------------------------------------------------
def async_sleep(ms):
    """ Sleep for the given duration without blocking. Typically this
    is used with the inlineCallbacks decorator.
    """
    d = Deferred()
    timed_call(ms, d.callback, True)
    return d


# -----------------------------------------------------------------------------
# QPainterPath helpers
# -----------------------------------------------------------------------------
def split_painter_path(path):
    """ Split a QPainterPath into subpaths. """
    if not isinstance(path, QPainterPath):
        raise TypeError("path must be a QPainterPath, got: {}".format(path))

    # Element types
    MoveToElement = QPainterPath.MoveToElement
    LineToElement = QPainterPath.LineToElement
    CurveToElement = QPainterPath.CurveToElement
    CurveToDataElement = QPainterPath.CurveToDataElement

    subpaths = []
    params = []
    e = None

    def finish_curve(p, params):
        if len(params) == 2:
            p.quadTo(*params)
        elif len(params) == 3:
            p.cubicTo(*params)
        else:
            raise ValueError("Invalid curve parameters: {}".format(params))

    for i in range(path.elementCount()):
        e = path.elementAt(i)

        # Finish the previous curve (if there was one)
        if params and e.type != CurveToDataElement:
            finish_curve(p, params)
            params = []

        # Reconstruct the path 
        if e.type == MoveToElement:
            p = QPainterPath()
            p.moveTo(e.x, e.y)
            subpaths.append(p)
        elif e.type == LineToElement:
            p.lineTo(e.x, e.y)
        elif e.type == CurveToElement:
            params = [QPointF(e.x, e.y)]
        elif e.type == CurveToDataElement:
            params.append(QPointF(e.x, e.y))

    # Finish the previous curve (if there was one)
    if params and e and e.type != CurveToDataElement:
        finish_curve(p, params)
    return subpaths


def join_painter_paths(paths):
    """ Join a list of QPainterPath into a single path """
    result = QPainterPath()
    for p in paths:
        result.addPath(p)
    return result
