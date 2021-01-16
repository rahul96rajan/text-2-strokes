"""
Expect IAM online handwriting dataset to be placed under ./data/
in the following order
    text-2-strokes
    │
    └──data
        |
        └──original-xml-part
            | a01
            | a02
            | a03
            | ...
"""

import os
import glob
import xml.etree.ElementTree as ElementTree
import html
import numpy as np


def get_midpoints(pts):
    """
    Calculate midpoint of `x` and `y` co-ordinates as the mean of max and min
    values.
    params : ndarray (nested) of points
    Returns: list of mid points for x and y
    """
    xmax, ymax = max(pts, key=lambda x: x[1])[
        0], max(pts, key=lambda x: x[2])[1]
    xmin, ymin = min(pts, key=lambda x: x[1])[
        0], min(pts, key=lambda x: x[2])[1]
    return [(xmax + xmin)/2., (ymax + ymin)/2.]


def change_coord_to_offsets(stroke, norm_factor=20):
    """
    Dataset stores actual pen points, but we will train on differences
    between consecutive points(offsets)
    And since the recording device was place at the top corner of whiteboard
    y component is inverted.

    params :
        stroke (ndarray)  : array of points in format [eos, x, y]
        norm_factor (int) : arbitrary value to normalize offsets.

    Returns :
        ndarray of format [eos, x-offset, y-offset]
    """
    eos = stroke[1:, 0]
    offs = stroke[1:, 1:] - stroke[:-1, 1:]
    offs = offs/norm_factor
    stroke_offed = np.hstack((eos.reshape(-1, 1), offs))
    stroke_offed[:, 2] = - stroke_offed[:, 2]

    return np.vstack(([0, 0, 0], stroke_offed)).astype('float32')
