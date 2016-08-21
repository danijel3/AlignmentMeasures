# Alignment Measures

This tools loads two sets of time-aligned sequences and outputs several measures
 of accuracy between them.
 
This project was initially based on the following paper:

Okko Johannes Räsänen, Unto Kalervo Laine, and Toomas Altosaar: _An Improved Speech Segmentation Quality Measure: the R-value_

It can be viewed under this link:

http://legacy.spa.aalto.fi/research/stt/papers/r_value.pdf

## Supported input formats

  * CTM
  
## Computed measured:
 
  * Hit rate (higher=>better_: {:%}'.format(hr / 100.0)
  * Over-segmentation rate
  * Precision
  * Recall
  * F-measure
  * r1 (computed as a part of R-value)
  * r2 (computed as a part of R-value)
  * R-value