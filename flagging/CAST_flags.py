flags = """CANONICAL_CENTER	0x0000000000000001	Measurements used the center in r*, rather than the locally determined center.
BRIGHT	0x0000000000000002	Object detected in first, bright object-finding; generally r*<17.5
EDGE	0x0000000000000004	Object is too close to edge of frame
BLENDED	0x0000000000000008	Object had multiple peaks detected within it; was thus a candidate to be a deblending parent.
CHILD	0x0000000000000010	Object is the product of an attempt to deblend a BLENDED object.
PEAKCENTER	0x0000000000000020	Given center is position of peak pixel, rather than based on the maximum-likelihood estimator.
NODEBLEND	0x0000000000000040	No deblending was attempted on this object, even though it is BLENDED.
NOPROFILE	0x0000000000000080	Object was too small or too close to the edge to estimate a radial profile.
NOPETRO	0x0000000000000100	No valid Petrosian radius was found for this object.
MANYPETRO	0x0000000000000200	More than one Petrosian radius was found.
NOPETRO_BIG	0x0000000000000400	Petrosian radius is beyond the last point in the radial profile.
DEBLEND_TOO_MANY_PEAKS	0x0000000000000800	There were more than 25 peaks in this object to deblend; deblended brightest 25.
COSMIC_RAY	0x0000000000001000	Contains a pixel interpreted to be part of a cosmic ray.
MANYR50	0x0000000000002000	Object has more than one 50% light radius.
MANYR90	0x0000000000004000	Object has more than one 90% light radius.
BAD_RADIAL	0x0000000000008000	Some of the points in the given radial profile have negative signal-to-noise ratio. Not a significant parameter.
INCOMPLETE_PROFILE	0x0000000000010000	Petrosian radius intersects the edge of the frame.
INTERP	0x0000000000020000	Object contains one or more pixels whose values were determined by interpolation.
SATURATED	0x0000000000040000	Object contains one or more saturated pixels
NOTCHECKED	0x0000000000080000	There are pixels in the object which were not checked to see if they included a local peak, such as cores of saturated stars.
SUBTRACTED	0x0000000000100000	This BRIGHT object had its wings subtracted from the frame
NOSTOKES	0x0000000000200000	Object has no measured Stokes params
BADSKY	0x0000000000400000	The sky level is so bad that the highest pixel in the object is very negative; far more so than a mere non-detection. No further analysis is attempted.
PETROFAINT	0x0000000000800000	At least one possible Petrosian radius was rejected as the surface brightness at r_P was too low. If NOPETRO is not set, a different, acceptable Petrosian radius was found.
TOO_LARGE	0x0000000001000000	The object is too large for us to measure its profile (it extends beyond a radius of approximately 260), or at least one child is larger than half a frame.
DEBLENDED_AS_PSF	0x0000000002000000	Deblender treated obj as PSF
DEBLEND_PRUNED	0x0000000004000000	At least one child was removed because its image was too similar to a supposedly different child.
ELLIPFAINT	0x0000000008000000	Object center is fainter than the isophote whose shape is desired, so the isophote properties are not measured. Also flagged if profile is incomplete.
BINNED1	0x0000000010000000	Object was detected in 1x1 binned image
BINNED2	0x0000000020000000	Object was detected in 2x2 binned image, after unbinned detections are replaced by background.
BINNED4	0x0000000040000000	Object was detected in 4x4 binned image
MOVED	0x0000000080000000	The deblender identified this object as possibly moving.
DEBLENDED_AS_MOVING	0x0000000100000000	A MOVED object that the deblender treated as moving.
NODEBLEND_MOVING	0x0000000200000000	A MOVED object that the deblender did not treat as moving.
TOO_FEW_DETECTIONS	0x0000000400000000	A child of this object was not detected in enough bands to reliably deblend as moving.
BAD_MOVING_FIT	0x0000000800000000	Moving fit too poor to be believable.
STATIONARY	0x0000001000000000	This object was consistent with being stationary.
PEAKS_TOO_CLOSE	0x0000002000000000	At least some peaks within this object were too close to be deblended, thus they were merged into a single peak.
MEDIAN_CENTER	0x0000004000000000	Center given is of median-smoothed image.
LOCAL_EDGE	0x0000008000000000	Center in at least one band is too close to an edge.
BAD_COUNTS_ERROR	0x0000010000000000	An object containing interpolated pixels had too few good pixels to form a reliable estimate of its error; the quoted error may be underestimated.
BAD_MOVING_FIT_CHILD	0x0000020000000000	A possible moving child's velocity fit was too poor, so it was discarded and the parent was not deblended as moving.
DEBLEND_UNASSIGNED_FLUX	0x0000040000000000	After deblending, a significant fraction of flux was not assigned to any children.
SATUR_CENTER	0x0000080000000000	Object center is close to at least one saturated pixel.
INTERP_CENTER	0x0000100000000000	Object center is close to at least one interpolated pixel.
DEBLENDED_AT_EDGE	0x0000200000000000	An object close enough to the edge of the frame normally not deblended, is deblended anyway. Only set for objects large enough to be EDGE in all fields/strips.
DEBLEND_NOPEAK	0x0000400000000000	There was no detected peak within this child in at least one band.
PSF_FLUX_INTERP	0x0000800000000000	Greater than 20% of the PSF flux is from interpolated pixels.
TOO_FEW_GOOD_DETECTIONS	0x0001000000000000	A child of this object had too few good detections to be deblended as moving.
CENTER_OFF_AIMAGE	0x0002000000000000	At least one peak's center lay off of the atlas image. This can happen when the object is deblended as moving, or if the astrometry is bad.
DEBLEND_DEGENERATE	0x0004000000000000	Two or more candidate children were essentially identical; one one was retained.
BRIGHTEST_GALAXY_CHILD	0x0008000000000000	This child is the brightest family member (in this band) that is classified as a galaxy.
CANONICAL_BAND	0x0010000000000000	This is the 'canonical' band; r unless the object is undetected in the r filter.
AMOMENT_FAINT	0x0020000000000000	Object was too faint to measure weighted moments such as mE1_g; unweighted values are reported.
AMOMENT_SHIFT	0x0040000000000000	Centroid shift too large when measuring adaptive moments. Row/Column shifts are reported in mE1, mE2.
AMOMENT_MAXITER	0x0080000000000000	Maximum number of iterations exceeded measuring e.g. mE2_g; unweighted values are reported.
MAYBE_CR	0x0100000000000000	There is reasonable suspicion that this object is actually a cosmic ray.
MAYBE_EGHOST	0x0200000000000000	There is reasonable suspicion that this object is actually a ghost produced by the CCD electronics.
NOTCHECKED_CENTER	0x0400000000000000	The center of this object lies in a region that was not searched for objects.
OBJECT2_HAS_SATUR_DN	0x0800000000000000	The electrons in this saturated object's bleed trails have been included in its estimated flux.
OBJECT2_DEBLEND_PEEPHOLE	0x1000000000000000	Deblend was modified by the deblender's peephole optimiser.
GROWN_MERGED	0x2000000000000000	Growing led to a merger
HAS_CENTER	0x4000000000000000	Object has a canonical center
RESERVED	0x8000000000000000	Not used"""

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)


flags = flags.split('\n')

newflag = [ a.split() for a in flags]

newflag = dict([(a[0], (int(a[1],16), ' '.join(a[2:]))) for a in newflag])

for key in newflag.keys():
    print key, newflag[key]

for key in ['DEBLEND_NOPEAK','BINNED1','NOPROFILE']:
    print key, newflag[key]



