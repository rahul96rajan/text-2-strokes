"""
Expect IAM online handwriting dataset to be placed under ./data/
in the following order
    text-2-strokes
    │
    └──data
        |
        └──original-xml-part
            |
            └──original
                | a01
                | a02
                | a03
                | ...
"""

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


def extract_data(path='./data/original-xml-part/'):
    files_paths = glob.glob(path + '**/*.xml', recursive=True)
    file_no = 0
    sentences_all = []
    strokes_all = []
    for file in files_paths:
        file_no += 1
        xml = ElementTree.parse(file).getroot()
        transcription = xml.findall('Transcription')
        if not transcription:
            print(f'[INFO] Skipped file {file}')
            continue
        textslines = [html.unescape(tl.get('text'))
                      for tl in transcription[0].findall('TextLine')]
        points_set = [strk.findall('Point')
                      for strk in xml.findall('StrokeSet/Stroke')]
        parsed_points_set = []
        mid_points = []
        for points in points_set:
            parsed_points = [[0, int(pt.get('x')), int(pt.get('y'))]
                             for pt in points]
            parsed_points[-1][0] = 1
            parsed_points_set.append(parsed_points)
            mid_points.append(get_midpoints(parsed_points))

        distances = [-(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
                     for p1, p2 in zip(mid_points, mid_points[1:])]
        splits = sorted(np.argsort(distances)[:len(textslines) - 1] + 1)

        strokes_wrt_textlines = []
        for strt_idx, end_idx in zip([0] + splits,
                                     splits + [len(parsed_points_set)]):
            strokes_wrt_textlines.append(parsed_points_set[strt_idx: end_idx])
        # list of (eos,x,y) makes stroke, list of strokes make sentence,
        # list of sentence make total textlines in the file
        # i.e; strokes_wrt_texlines.

        assert len(strokes_wrt_textlines) == len(textslines),\
            f"Strokes Segregation doesn't match with textlines "\
            f"{len(strokes_wrt_textlines)} != {len(textslines)}"

        # We want list of (eos, x, y) wrt textlines,
        # hence unravel list of strokes
        textlines_seq = []
        for line in strokes_wrt_textlines:
            indiv_line_seq = []
            for strokes in line:
                indiv_line_seq += strokes
            indiv_line_seq = np.asarray(indiv_line_seq, dtype=np.float32)
            indiv_line_seq = change_coord_to_offsets(indiv_line_seq)
            textlines_seq.append(indiv_line_seq)

        strokes_all.extend(textlines_seq)
        sentences_all.extend(textslines)
        print(f'[{file_no:4d}] File: ./{file} -- '
              f'TextLines: {len(textlines_seq)}')

    assert len(sentences_all) == len(strokes_all)

    return strokes_all, sentences_all


if __name__ == "__main__":
    strokes, sents = extract_data()
