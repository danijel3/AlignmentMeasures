# Alignment Measures

This tools loads two sets of time-aligned sequences and outputs several measures of accuracy between them.
 
This project was initially based on the following paper:

> Okko Johannes Räsänen, Unto Kalervo Laine, and Toomas Altosaar: _An Improved Speech Segmentation Quality Measure: the R-value_

It can be viewed under this link: http://legacy.spa.aalto.fi/research/stt/papers/r_value.pdf

### Caveat

There is one minor addition to the paper above. All the segmentation measure papers seem to treat boundaries as entities described only by the time they occur in. The contents of the segments between the boundaries are not checked.
 
While this may be fine for most uses, this tool assigns a name to each boundary based on the segments located around them. Eg: if a boundary exists between segments titled 'a' and 'b', the boundary will be named "a_b". Hits are counted if and only if the time AND the names of the boundaries (reference and hypothesis) match.

## Supported input formats

  * CTM
  * TextGrid
  
## Computed measures
 
  * Hit rate
  * Over-segmentation rate
  * Precision
  * Recall
  * F-measure
  * r1 (computed as a part of R-value)
  * r2 (computed as a part of R-value)
  * R-value
  
## Requirements

TextGrid input requires the installation of the TextGrid package, as described in the followin repo: https://github.com/kylebgorman/textgrid

It can easily be installed using pip:

```
pip install TextGrid
```

## Usage

```
usage: AlignMeasure.py [-h] [--ref-tier REFTIER] [--hyp-tier HYPTIER] ref hyp

Calcualte various alignemnt accuracy measures.

positional arguments:
  ref                   reference segmentation (CTM or TextGrid)
  hyp                   studied segmentation (CTM or TextGrid)

optional arguments:
  -h, --help            show this help message and exit
  --ref-tier REFTIER, -rt REFTIER
                        for TextGrid, use which tier for reference (default:0)
  --hyp-tier HYPTIER, -ht HYPTIER
                        for TextGrid, use which tier for hypothesis
                        (default:0)
```

### Note

The input file type is determined based on the extension only!

## Example output

```
Number of boundaries in reference segmentation: 6
Number of boundaries in studied segmentation: 7
Number of hits: 4
Hit rate (higher=>better_: 66.666667%
Over-segmentation rate (closer-zero=>better): 16.6666666667
Precision (higher=>better): 57.142857%
Recall (higher=>better): 66.666667%
F-measure (higher=>better): 61.538462%
r1 (closer-zero=>better): 37.267799625
r2 (closer-zero=>better): -35.3553390593
R-value (higher=>better): 63.688431%
```