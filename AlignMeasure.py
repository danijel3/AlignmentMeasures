#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import math

from textgrid import TextGrid


# based on the paper: An Improved Speech Segmentation Quality Measure: the R-value
#   by Okko Johannes Räsänen, Unto Kalervo Laine, and Toomas Altosaar
# link: http://legacy.spa.aalto.fi/research/stt/papers/r_value.pdf

class Segment:
    def __init__(self, text, start, dur):
        self.text = text
        self.start = start
        self.dur = dur

    def __str__(self):
        return '["{}": {} - {}]'.format(self.text, self.start, self.start + self.dur)


def read_ctm(file):
    ret = {}
    with open(file, 'r') as f:
        for line in f:
            tok = line.strip().split(' ')
            file = tok[0] + '_' + tok[1]
            if file not in ret:
                ret[file] = []
            start = float(tok[2])
            len = float(tok[3])
            text = tok[4]
            ret[file].append(Segment(text, start, len))
    return ret


def read_textgrid(file, tier):
    tg = TextGrid()
    tg.read(file)

    if len(tg.tiers) <= tier:
        raise IOError('Texgrid file ' + file + ' doesn\'t have enough tiers to get tier: ' + str(tier))

    if not hasattr(tg.tiers[tier], 'intervals'):
        raise IOError('The selected tier: ' + str(tier) + ' is not and IntervalTier in file: ' + file)

    ret = []
    for seg in tg.tiers[tier].intervals:
        ret.append(Segment(seg.mark, seg.minTime, seg.duration()))
    return {'textgid': ret}


class Boundary:
    def __init__(self, time, name, search_reg=0.02):
        self.time = time
        self.name = name
        self.reg_beg = time - search_reg
        self.reg_end = time - search_reg

    def __str__(self):
        return '<"{}": {}>'.format(self.name, self.time)


def count_hits(ref_bound, hyp_bound, search_reg=0.02):
    hit = 0
    # update search regions:
    for i, b in enumerate(ref_bound):
        b.reg_beg = b.time - search_reg
        b.reg_end = b.time + search_reg
        ref_bound[i] = b

    # search regions of a typical fixed size,
    # e.g., ±20 ms, are placed around each reference boundary. If
    # overlapping search regions exist, that is, adjacent regions with
    # their reference boundaries exist closer than 40 ms to each other,
    # then the regions are asymmetrically shrunk to divide the space
    # between two reference boundaries into two equal-width halves
    for i in range(len(ref_bound) - 1):
        if ref_bound[i].reg_end > ref_bound[i + 1].reg_beg:
            t = ref_bound[i].time + ref_bound[i + 1].time / 2
            ref_bound[i].reg_end = t
            ref_bound[i + 1].reg_beg = t

    # "a boundary is considered to be correctly detected if the hypothesis and
    # the manual transcription are within 20 ms of each other"
    for b in ref_bound:
        for b2 in hyp_bound:
            if b.reg_beg <= b2.time <= b.reg_end and b.name == b2.name:
                hit += 1

    return hit


def seg2boundary(segments):
    ret = []
    for i in range(len(segments) + 1):
        name_p = '#'
        name_n = '#'
        if i > 0:
            name_p = segments[i - 1].text
            time = segments[i - 1].start + segments[i - 1].dur
        else:
            time = segments[i].start

        if i < len(segments):
            name_n = segments[i].text
            if i > 0:
                assert abs(time - segments[i].start) <= 0.01, '{} - {}'.format(time, segments[i].start)

        ret.append(Boundary(time, name_p + "_" + name_n))
    return ret


def debug(lst):
    for el in lst:
        print(el)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calcualte various alignemnt accuracy measures.')
    parser.add_argument('ref', help='reference segmentation (CTM or TextGrid)')
    parser.add_argument('hyp', help='studied segmentation (CTM or TextGrid)')
    parser.add_argument('--ref-tier', '-rt', dest='reftier', type=int, default=0,
                        help='for TextGrid, use which tier for reference (default:0)')
    parser.add_argument('--hyp-tier', '-ht', dest='hyptier', type=int, default=0,
                        help='for TextGrid, use which tier for hypothesis (default:0)')

    args = parser.parse_args()

    if args.ref.endswith('.ctm'):
        refs = read_ctm(args.ref)
    elif args.ref.endswith('.TextGrid'):
        refs = read_textgrid(args.ref, args.reftier)
    else:
        raise IOError('Unknown extension for ref file: ' + args.ref)

    if args.ref.endswith('.ctm'):
        hyps = read_ctm(args.hyp)
    elif args.ref.endswith('.TextGrid'):
        hyps = read_textgrid(args.hyp, args.hyptier)
    else:
        raise IOError('Unknown extension for hyp file: ' + args.hyp)

    hit_count = 0
    hyp_count = 0
    ref_count = 0
    for file, hyp_seg in hyps.items():
        assert file in refs, 'Missing hyp file in ref: ' + file

        ref_seg = refs[file]

        # debug(ref_seg)
        # debug(hyp_seg)

        ref_bound = seg2boundary(ref_seg)
        hyp_bound = seg2boundary(hyp_seg)

        # debug(ref_bound)
        # debug(hyp_bound)

        hit_count += count_hits(ref_bound, hyp_bound)
        hyp_count += len(hyp_bound)
        ref_count += len(ref_bound)

    hr = (hit_count / float(ref_count)) * 100.0
    os = ((hyp_count / float(ref_count)) - 1) * 100.0
    prc = (hit_count / float(hyp_count))
    rcl = (hit_count / float(ref_count))
    f_meas = ((2 * prc * rcl) / (prc + rcl))
    r1 = math.sqrt((100.0 - hr) ** 2 + os ** 2)
    r2 = (-os + hr - 100.0) / math.sqrt(2.0)
    R = 1 - ((math.fabs(r1) + math.fabs(r2)) / 200.0)

    print('Number of boundaries in reference segmentation: {}'.format(ref_count))
    print('Number of boundaries in studied segmentation: {}'.format(hyp_count))
    print('Number of hits: {}'.format(hit_count))
    print('Hit rate (higher=>better_: {:%}'.format(hr / 100.0))
    print('Over-segmentation rate (closer-zero=>better): {}'.format(os))
    print('Precision (higher=>better): {:%}'.format(prc))
    print('Recall (higher=>better): {:%}'.format(rcl))
    print('F-measure (higher=>better): {:%}'.format(f_meas))
    print('r1 (closer-zero=>better): {}'.format(r1))
    print('r2 (closer-zero=>better): {}'.format(r2))
    print('R-value (higher=>better): {:%}'.format(R))
