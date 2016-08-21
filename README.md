# Alignment Measures

This tools loads two sets of time-aligned sequences and outputs several measures of accuracy between them.
 
This project was initially based on the following paper:

Okko Johannes Räsänen, Unto Kalervo Laine, and Toomas Altosaar: _An Improved Speech Segmentation Quality Measure: the R-value_

It can be viewed under this link:

http://legacy.spa.aalto.fi/research/stt/papers/r_value.pdf

### Caveat

There is one minor addition to the paper above. All the segmentation measure papers seem to treat boundaries as
 entities described only by the time they occur in. The segments between the boundaries is not checked by these measures.
 
While this may be fine for most uses, this tool assigns a name to each boundary based on the segments located around them.
Eg: if a boundary exists between segments for silence and the phoneme 'a', the boundary will be named "sil_a". Hits are counted
if and only if the names of the boundaries (reference and hypothesis) match.

## Supported input formats

  * CTM
  
## Computed measures
 
  * Hit rate
  * Over-segmentation rate
  * Precision
  * Recall
  * F-measure
  * r1 (computed as a part of R-value)
  * r2 (computed as a part of R-value)
  * R-value