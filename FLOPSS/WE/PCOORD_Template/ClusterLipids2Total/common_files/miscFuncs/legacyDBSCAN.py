#!/usr/bin/env python

# Importing functional modules
import numpy as np
import sys
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
import loosFuncs as lf


def lsDBSCAN(system, rCutoff, minNeighbors, box, inPlane=False):
    '''
    Return
        1. An numpy array consisting of area corresponding to each cluster.
        2. Number of total cluster (int)
        3. An numpy array consisting of no. of core lipids in each cluster.
        4. An numpy array consisting of no. of boundary lipids in each cluster.
        5. Number of total outlier lipids (int)
    '''

    num = len(system)
    cent = lf.centroid2npArray(system)

    # Calculating distance matrix based on dimensionality of system and the
    # dimensionality of cartesian coordinates
    if inPlane:
        centCoord = np.c_[cent[:, 0], cent[:, 1]]
        dim = 2
    else:
        centCoord = np.c_[cent[:, 0], cent[:, 1], cent[:, 2]]
        dim = 3
    distanceMatrix = lf.pDist(system, box, planar=inPlane)

    # DBSCAN
    db = DBSCAN(eps=rCutoff,
                min_samples=minNeighbors,
                metric="precomputed").fit(distanceMatrix)

    labels = db.labels_
    coreIndex = db.core_sample_indices_
    uniqueLabels = set(labels)

    # Work around to address the known bug in DBSCAN:
    # https://github.com/scikit-learn/scikit-learn/issues/16360
    bugLabelIndex = []
    bugCoreIndex = []
    for label in uniqueLabels:
        labelIndex = np.argwhere(labels == label)
        if len(labelIndex) < minNeighbors:
            labels[labelIndex] = -1
            bugLabelIndex.extend(labelIndex)
    for bugIndex in bugLabelIndex:
        index = np.argwhere(coreIndex == bugIndex[0])
        if index.size > 0:
            bugCoreIndex.extend(index[0])
    mask = np.ones(len(coreIndex), dtype=bool)
    mask[bugCoreIndex] = False
    newCoreIndex = coreIndex[mask]
    coreSamplesMask = np.zeros_like(labels, dtype=bool)
    coreSamplesMask[newCoreIndex] = True

    # Number of clusters in labels, ignoring noise if present.
    nClusters = len(set(labels)) - (1 if -1 in labels else 0)
    nOutliers = list(labels).count(-1)

    if nClusters != 0:
        clusterCount = 0
        clusterArea = np.zeros((nClusters, ))
        coreLipids = np.zeros((nClusters, ), dtype=int)
        boundayLipids = np.zeros((nClusters, ), dtype=int)
        correctedLabels = set(labels)
        for cluster in correctedLabels:
            # Considering only clusters and NO outliers
            if cluster != -1:
                classMemberMask = (labels == cluster)
                coreLipidsCoord = centCoord[classMemberMask
                                            & coreSamplesMask]
                boundaryLipidsCoord = centCoord[classMemberMask
                                                & ~coreSamplesMask]

                coreLipids[clusterCount] = len(coreLipidsCoord)
                boundayLipids[clusterCount] = len(boundaryLipidsCoord)

                # According to Caratheodory's theorm, you need at least d+1
                # points to create a convex hull, where d is the dimenionality
                # of the carteasian corrdinate. Here we concatenate corelipids
                # with boundarylipids to create the hull, if there are fewer
                # boundary lipids than d+1
                if len(boundaryLipidsCoord) < (dim + 1):
                    boundaryLipidsCoord = np.concatenate((boundaryLipidsCoord,
                                                          coreLipidsCoord))

                # Coordiate transormation to avoid overestimation of
                # area/Volume by considering only interior area/volume rather
                # than exterior. This is done by translating entire cluster to
                # origin of the box and therefore preventing the area
                # estimation close to boundaries. NOT A FOOL_PROOF APPROACH :
                # THIS DOES NOT HELP IF YOU HAVE CLUSTER THAT SPANS ACROSS
                # BOUNDARY AND HAVE AREA > 0.5 BOX AREA.
                correctedBLipidCoord = lf.translate2Center(boundaryLipidsCoord,
                                                           box,
                                                           inPlane=inPlane)
                hull = ConvexHull(correctedBLipidCoord)
                # Just for 2D attribute volume gives area of convex hull
                clusterArea[clusterCount] = hull.volume
                clusterCount += 1
    else:
        # This prevents generating np.zeros((0, )) which is absurd and taking
        # its mean produce NaN which throws a lot of RunTimeWarning and output
        # file ugly.
        clusterArea = np.zeros((1, ))
        coreLipids = np.zeros((1, ), dtype=int)
        boundayLipids = np.zeros((1, ), dtype=int)

    # Sanity Check
    nCores = np.sum(coreLipids)
    nBounds = np.sum(boundayLipids)
    totalLipids = nCores + nBounds + nOutliers
    if num != totalLipids:
        sys.exit("DBSCAN estimated a total number of lipids different \
                 from sytem lipids")

    return(clusterArea, nClusters, coreLipids, boundayLipids, nOutliers)
