"""
"""

import os
import glob
import xml.etree.ElementTree as ElementTree
import html
import numpy as np
import pickle

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


def distance(p1, p2, axis=None):
    return np.sqrt(np.sum(np.square(p1 - p2), axis=axis))


def clear_middle(pts):
    """
    Clipping off any un-derised points in the middle of coninous writing.
    By calculating distance between the points in the stroke's trajectory
    points, and removing the ones with large distances.
    """

    to_remove = []
    for i in range(1, len(pts) - 1):
        p1, p2, p3 = pts[i - 1: i + 2, :2]
        dist = distance(p1, p2) + distance(p2, p3)
        if dist > 1500:
            to_remove.append(i)
    return np.delete(pts, to_remove, axis=0)


def separate(pts):
    """
    Identifying the points from where possibly a new character is begun.
    Converts the array to a nested array of
    seperate sequence(possible character or several characters)
    """
    seps = []
    for i in range(0, len(pts) - 1):
        if distance(pts[i], pts[i+1]) > 600:
            seps += [i + 1]
    return [pts[b:e] for b, e in zip([0] + seps, seps + [len(pts)])]


def get_midpoints(pts):
    """
    Calculate midpoint of `x` and `y` co-ordinates as the mean of max and min
    values.
    params : ndarray (nested) of points
    Returns: list of mid points for x and y
    """
    xmax = max(pts, key=lambda p: p[0])[0]
    ymax = max(pts, key=lambda p: p[1])[1]
    xmin,  = min(pts, key=lambda p: p[0])[0]
    ymin = min(pts, key=lambda p: p[1])[1]
    return [(xmax + xmin)/2., (ymax + ymin)/2.]


def save_data(dataset, label, trans_dict, path='data'):
    if not os.path.isdir('data'):
        os.mkdir('data')

    np.save(os.path.join(path, 'dataset'), np.array(dataset))
    np.save(os.path.join(path, 'labels'), np.array(label))
    with open(os.path.join(path, 'translation.pkl'), 'wb') as file:
        pickle.dump(trans_dict, file)


def main():
    """
    Processing the xmls files and returning datasets and labels.
    Where data set is
    Preprocessing applied:
        - Check for any undesired dot or line and removing it.
        - Seperating sequences of points based on the end of stroke.
        - Determinig new line via distances between end of stoke and beginning
          of the other.
        - storing `data` as tuple of individual linetext from xml and the
          respective array of points.
        - keeping note of all characters encountered under `charset`.
        - forming a dict `translation` which maps chars to index. (encoding)
        - returns:
            - dataset (list): list of array of points. where each array
                              corresponds to respective textline.
            - label (list): list of array of int-encoded textlines.
            - translation (dict): dict mapping characters to integer value.
    """
    data = []
    charset = set()

    file_no = 0
    files_paths = glob.glob('original-xml-part/**/*.xml', recursive=True)

    for file in files_paths:
        file_no += 1
        print('[{:5d}] File {} -- '.format(file_no, file), end='')
        xml = ElementTree.parse(file).getroot()
        transcription = xml.findall('Transcription')
        if not transcription:
            print('skipped')
            continue
        texts = [html.unescape(tl.get('text')) for
                 tl in transcription[0].findall('TextLine')]
        points = [strk.findall('Point') for
                  strk in xml.findall('StrokeSet/Stroke')]
        strokes = []
        mid_points = []

        for ps in points:
            pts = np.array([[int(p.get('x')), int(p.get('y')), 0] for p in ps])
            pts[-1, 2] = 1  # adding 1 to last point stating end of character

            pts = clear_middle(pts)
            if len(pts) == 0:
                continue

            sepped_pts = separate(pts)
            for sep_ps in sepped_pts:
                if len(sepped_pts) > 1 and len(sep_ps) == 1:
                    continue
                sep_ps[-1, 2] = 1
                strokes += [sep_ps]
                mid_points += [get_midpoints(sep_ps)]
        distances = [-(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
                     for p1, p2 in zip(mid_points, mid_points[1:])]
        splits = sorted(np.argsort(distances)[:len(texts) - 1] + 1)
        lines = []
        for b, e in zip([0] + splits, splits + [len(strokes)]):
            lines += [[p for pts in strokes[b:e] for p in pts]]
        print('lines = {:4d}; texts = {:4d}'.format(len(lines), len(texts)))
        charset |= set(''.join(texts))
        data += [(texts, lines)]
    print('data = {}; charset = ({}) {}'.format(len(data), len(charset),
          ''.join(sorted(charset))))

    translation = {'<NULL>': 0}
    for c in ''.join(sorted(charset)):
        translation[c] = len(translation)

    dataset = []
    labels = []
    for texts, lines in data:
        for text, line in zip(texts, lines):
            line = np.array(line, dtype=np.float32)
            line[:, 0] = line[:, 0] - np.min(line[:, 0])
            line[:, 1] = line[:, 1] - np.mean(line[:, 1])

            dataset += [line]
            labels += [list(map(lambda x: translation[x], text))]

    whole_data = np.concatenate(dataset, axis=0)
    std_y = np.std(whole_data[:, 1])

    norm_data = []
    for line in dataset:
        line[:, :2] /= std_y
        norm_data += [line]
    dataset = norm_data

    print('dataset = {}; labels = {}'.format(len(dataset), len(labels)))

    return labels, dataset, translation


if __name__ == "__main__":
    label, data, trans_dict = main()
    save_data(data, label, trans_dict)
