#!/usr/bin/env python

# Importing functional modules
import loos
import loos.pyloos
import numpy as np
import math
import sys
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score


def segs2pyDicts(model1, segmentListFile):
    '''
    Returns a python dictionary consisting of distinct segid, as decribed in
    the segmentListFile, as the keys and corresponding segment Atomic Groups
    as values.

    Returns a python list consisting of all the segment AGs
    given in the segmentListFile.

    Also returns a python list consisting of all the segment IDs
    given in the segmentListFile.

    Inputs:
    model1 = LOOS processed model object. This is what you get as a resut of
            loos.createSystem(PATH/TO/FILE)
    segmentListFile = Path to the file consisting of a list of segments to be
    included in the dictionary
    '''
    # Getting segid details from external file
    lipidList1 = []

    with open(segmentListFile, 'r') as file:
        for line in file:
            temp1 = line.splitlines()
            lipidList1.append(temp1[0])

    # Defining a container dict to store loos lipid AG separately
    container = {}
    # Defining a list to store all lipid AG.
    system = []

    # Store lipid AG with unique lipid segid as keys
    for lipid1 in lipidList1:
        segment1 = loos.selectAtoms(model1, "segid == '{0}''".format(lipid1))
        molecules1 = segment1.splitByMolecule()
        container[lipid1] = molecules1
        system.extend(molecules1)
    return(container, system, lipidList1)


def centroid2npArray(postSplitAG):
    '''
    Returns an np 3N array of centroids - [x,y,z] - of all subunits in the
    post-split atomicGroup list. Advised to create the atomicGroup list by
    splitBy...() method from loos.

    postSplitAG can be molecules, if splitByMolecule() is used.
    postSplitAG can be residues, if splitByResidue() is used.
    '''
    centroids = np.zeros([len(postSplitAG), 3])

    for i in range(len(postSplitAG)):
        centroid = postSplitAG[i].centroid()
        centroids[i, 0] = centroid[0]
        centroids[i, 1] = centroid[1]
        centroids[i, 2] = centroid[2]
    return centroids


def leafletLipidSeparator(lipids):
    '''
    Returns a tuple corresponding to lipids in Up and Lo leaflet.
    '''
    lipidUp = []
    lipidLo = []

    for lipid in lipids:
        if lipid.centroid().z() > 0:
            lipidUp.append(lipid)
        else:
            lipidLo.append(lipid)
    return (lipidUp, lipidLo)


def bin2DRangeFromBox(box):
    '''
    Returns an array with shape(2,2) corresponding to the leftmost and
    rightmost edges of the bins along each dimension :
    [[xmin, xmax], [ymin, ymax]]

    The edges care calculated using the bounding values of the system
    box : box should be calculate for corresponding frame using the LOOS by
    box = frame.periodicBox()
    '''
    boxX = box[0]
    boxY = box[1]
    binMinX = -(boxX/2)
    binMinY = -(boxY/2)
    binMaxX = boxX/2
    binMaxY = boxY/2
    binRange = [[binMinX, binMaxX], [binMinY, binMaxY]]
    return (binRange)


def bin3DRangeFromBox(box):
    '''
    Returns an array with shape(3,2) corresponding to the leftmost and
    rightmost edges of the bins along each dimension :
    [[xmin, xmax], [ymin, ymax], [zmin, zmax]]

    The edges care calculated using the bounding values of the system
    box : box should be calculate for corresponding frame using the LOOS by
    box = frame.periodicBox()
    '''
    boxZ = box[2]
    binMinZ = -(boxZ/2)
    binMaxZ = boxZ/2
    bin3D = bin2DRangeFromBox(box)
    bin3D.append([binMinZ, binMaxZ])
    return (bin3D)


def bin2DRange(frame):
    '''
    Returns an array with shape(2,2) corresponding to the leftmost and
    rightmost edges of the bins along each dimension :
    [[xmin, xmax], [ymin, ymax]]

    The edges care calculated using the bounding values of the system
    box for that particular frame
    '''
    box = frame.periodicBox()
    binRange = bin2DRangeFromBox(box)
    return (binRange)


def bin3DRange(frame):
    '''
    Returns an array with shape(3,2) corresponding to the leftmost and
    rightmost edges of the bins along each dimension :
    [[xmin, xmax], [ymin, ymax], [zmin, zmax]]

    The edges care calculated using the bounding values of the system
    box for that particular frame
    '''
    box = frame.periodicBox()
    bin3D = bin3DRangeFromBox(box)
    return (bin3D)


def edgeCheck(edge, numBin):
    '''
    Returns true if (i) bin edges (array_like) stayed same while
    histogramming each key and (ii) this unique bin edge has the
    same shape as (1, numBin+1).
    '''
    return (np.shape(np.unique(edge, axis=0)) == (1, numBin+1))


def maxTheoreticalShannonEntropy(numLipidTypes):
    '''
    Returns the maximum theoretical Shannon Entropy possible for a system
    consisting of n lipid types.

    S = -sum(p(i)ln(p(i))), where i = 1,2..n
    Max S ==> p(i) = 1/n
    Smax = -n*(1/n)*ln(1/n) = ln(n)

    Input in an int_like = no .of lipid types
    '''
    return (np.log(numLipidTypes))


def shannonMFEntropyGlobal(lipidCountArray):
    '''
    Returns Mean Field Shannon entropy of entire system.

    This is intended as a check to see a if the global entropy of the system
    changes dramatically. For example, if there's too many cholesterol or small
    molecules in the system that can flipflop across the leaflets and change
    the number of total particles in the leaflet and thereby the entropy.

    Not to be confused with the average of local entropies which give more info
    on local fluctuations.

    Input is an array_like with dimension ((numLipidTypes,)). Each row
    corresponds to number of lipids of a particular type.
    '''
    totalLipids = np.add.reduce(lipidCountArray, axis=0)
    moleFraction = lipidCountArray[:]/totalLipids
    entropyContribution = moleFraction*(np.log(moleFraction))
    shannonMFEntropyGlobal = -1*(np.add.reduce(entropyContribution, axis=0))
    return (shannonMFEntropyGlobal)


def shannonMFEntropyLocal(hist2D):
    '''
    Returns local Mean Field of Shannon entropy for each bin in the
    given histogram data.

    Input is an array_like with dimension ((numLipidTypes,numBin,numBin))
    This is nothing but the 2D histogram data indexed corresponding to
    respective lipid species.
    '''
    # Calculating total population per bin
    hist2DBinPop = np.add.reduce(hist2D, axis=0)

    # Calculating probabilities for each bin
    hist2DBinPop = np.ma.masked_invalid(hist2DBinPop)
    prob = hist2D[:]/hist2DBinPop
    probMasked = np.ma.masked_equal(prob, value=0)

    # Estimating local entropy
    entropyContribution = probMasked*(np.log(probMasked))
    shannonMFEntropyLocal = -1*(np.add.reduce(entropyContribution, axis=0))
    return (shannonMFEntropyLocal)


def shannonMFEntropyLocalAveraged(hist2D):
    '''
    Returns averaged local Mean Field of Shannon entropy over all the bins
    of the given histogram data.

    Basically a wraper over the shannonMFEntropyLocal(hist2D) that take the
    average over all the bins.

    Input is an array_like with dimension ((numLipidTypes,numBin,numBin))
    This is nothing but the 2D histogram data indexed corresponding to
    respective lipid species.
    '''
    gridData = shannonMFEntropyLocal(hist2D)
    sumOverAllBins = np.add.reduce(np.concatenate(gridData))
    bins = (np.unique(np.shape(hist2D[0])))[0]
    average = sumOverAllBins/(bins*bins)
    return (average)


def shannonMFEntropyLocalNormalized(hist2D):
    '''
    Returns normalized local Mean Field of Shannon entropy over all the bins
    of the given histogram data.

    Basically a wraper over the shannonMFEntropyLocalAveraged(hist2D) that
    normalize the averaged value by dividing it by ln(n). The output lies
    inside the interval [0,1]

    Input is an array_like with dimension ((numLipidTypes,numBin,numBin))
    This is nothing but the 2D histogram data indexed corresponding to
    respective lipid species.
    '''
    gridAveragedData = shannonMFEntropyLocalAveraged(hist2D)
    lipidTypes = np.shape(hist2D)[0]
    average = gridAveragedData/np.log(lipidTypes)
    return (average)


def shannonDiversity(entropyMF):
    '''
    Returns the shannon diversity D for a given input S, where S = ln(D).

    Theoretial max value for D = numLipidTypes (please take a look at
    maxTheoreticalShannonEntropy() for why this is the case) and theoretical
    minimum value for D = 1, correpsonding to S = ln(1) = 0.
    '''
    return (np.exp(entropyMF))


def binning2D(atomicGroup, numBins, binRange):
    '''
    Returns (i) a 2D histogram of centroids of loos Atomic Group
    (example: lipids), (ii) an array containing x axis bin edges, and (iii) an
    array containing y axis bin edges for a given value of bins and binRange

    Input arguments are following:
    atomicGroup = loos AG list. Advised to create the atomicGroup list by
    splitBy...() method from loos.

    numBins = No. of bins in one dimension. Same number of bins will be applied
    in second dimension to make square 2D bins. (int)

    binRange = an array with shape(2,2) corresponding to the leftmost and
    rightmost edges of the bins along each dimension :
    [[xmin, xmax], [ymin, ymax]]
    '''
    # Storing centroid of lipids into a np array
    centroid = centroid2npArray(atomicGroup)

    # 2D binning
    hist2D, xEdge, yEdge = np.histogram2d(centroid[:, 0],
                                          centroid[:, 1],
                                          bins=numBins,
                                          range=binRange)
    return (hist2D, xEdge, yEdge)


def binaryShannonEntropy(frame, system, radius):
    '''
    Returns the Binary Mixing Entropy of the system.
    NOT TO BE CONFUSED WITH THE ENTROPY OF MIXING OF A TWO COMPONENT SYSTEM.
    HERE BINARY MEANS BETWEEN LIKE AND UNLIKE PARTICLES.

    Will update soon..
    '''
    box = frame.periodicBox()
    likeContribution = 0
    unlikeContribution = 0
    for lipid1 in system:
        like = 0
        unlike = 0
        totalNeighbors = 0
        for lipid2 in system:
            if lipid1 != lipid2:
                if lipid1.hardContact2D(lipid2, radius, box):
                    if lipid1[0].segid() == lipid2[0].segid():
                        like += 1
                    else:
                        unlike += 1

        totalNeighbors = like + unlike
        if totalNeighbors != 0:
            likeProb = like/totalNeighbors
            unlikeProb = unlike/totalNeighbors
            if likeProb != 0:
                likeContribution += (-likeProb*(math.log(likeProb)))
            if unlikeProb != 0:
                unlikeContribution += (-unlikeProb*(math.log(unlikeProb)))

    binaryShannonEntropy = (likeContribution+unlikeContribution)
    return(binaryShannonEntropy, likeContribution, unlikeContribution)


def enrichmentHard(system, radius, systemArea, box):
    '''
    Return the enrichment of entites in a single species system.

    Input :
        system = A single species sytem. This system can be a subset of
                 multispecies system. Example: all DPPC lipids in a
                 DPPC-DIPC-CHOL system.
        radius = Radius of the local region over which enrichment is
                 estimated
        systemArea = Lateral area of the system.
        box = loos periodicBox

    '''

    # Calculating local area
    localArea = math.pi*(radius)*(radius)

    # Initializing
    hardContacts = 0

    # Calculating number of lipids
    num = len(system)

    # Calculating number density
    numDen = num/(systemArea)

    for lipid1 in system:
        # Initializing and including central lipid contribution
        like = 1
        for lipid2 in system:
            if lipid1 != lipid2:
                like += lipid1.hardContact2D(lipid2, radius, box)

        hardContacts += like

    # Hard contacts per lipid
    hardContacts /= num
    # (Hard contacts per lipid) per local area
    hardContacts /= localArea
    # Enrichment w.r.t to uniformaly mixed system
    enrichmentHard = hardContacts/numDen
    return(enrichmentHard)


def rFileReader(rFile):
    '''
    Read input rFile with follwing format and returns three lists:
        1. List of lipids (First coulmn)
        2. List of avg. radius (Second coulmn)
        3. List of var. of radius (Third coulmn)

    Input rFile format:
        lipid1  avg1    var1
        lipid2  avg2    var2
        ....    ....    ....

    '''
    # Initializing output lists
    rlipidList = []
    radiusList = []
    rVarList = []

    with open(rFile, 'r') as file:
        for line in file:
            # Spliting columns
            split = line.split()
            # Make sure that no empty lines are parsed as empty lists
            if split:
                rlipidList.append(split[0])
                radiusList.append(split[1])
                rVarList.append(split[2])
    return(rlipidList, radiusList, rVarList)


def pDist(lipidAG, box, planar=False):

    numLipid = len(lipidAG)

    # Initializing
    pDistMatrix = np.zeros((numLipid, numLipid))
    centroidList = []

    for m in lipidAG:
        centroid = m.centroid()
        if planar:
            # We are only interested in planar distance
            centroid.set(centroid[0],
                         centroid[1],
                         0)
        centroidList.append(centroid)

    for i in range(numLipid-1):
        for j in range(i+1, numLipid):
            pdist = centroidList[i].distance(centroidList[j],
                                             box)
            pDistMatrix[i][j] = pdist
            pDistMatrix[j][i] = pdist
    return(pDistMatrix)


def translate2Center(listOfArrays, box, inPlane=False):
    '''
    Returns translated points corrected with respect to PBC.

    Rationale: Points given out by Clustering can be from a cluster that is
    near the boundary and while calculating the convex hull, since the points
    are on the boundaries of the box, this can lead to overestimation of area
    as Qhull calculates the larger area exterior to the points rather than
    interior area. This function takes the first point from the cluster and
    translates the entire cluster such that the first point is in the center.
    During this process, points can fall outside the box and the reimaging
    brings them inside the box. The idea is that, cluster near the boundaries
    are translated to center and area is calculated after translation. This
    make sure that almost all the time we estimate interior area. However this
    function does not save us if the cluster size is beyond the half size of
    the box.

    Input:
        listOfArrays = A list of coordinate arrays.
        [arr(x1, y1), arr(x2, y2)..] or [arr(x1, y1, z1), arr(x2, y2, z2)...]

        box = A loos.GCoord type object consisting of dim of simulation box.
              You can obtain this using loos function periodicBox() for each
              frame:
                  box = frame.periodicBox()

        inPlane : False(default) : Bool
                  Explicilty state True, if you have 2D cartesian coordiantes.
                  Else, by default, inPlane=False and expects a 3D coord data.
    '''
    newListOfArrays = []
    reference = listOfArrays[0]
    for array in listOfArrays:
        arrayTranslated = array-reference
        coord = tuple(arrayTranslated)
        if inPlane:
            # You need to add z = 0.0, else loos.GCoord()
            # doesnot work
            coord += (0.0, )
        loosGCoord = loos.GCoord(*coord)
        loosGCoord.reimage(box)
        if inPlane:
            # You need to revert the (x, y, 0) to (x, y)
            # if considering area in a plane, else Qhull
            # calculates the volume.
            listCoord = [loosGCoord.x(), loosGCoord.y()]
        else:
            listCoord = list(loosGCoord)
        newListOfArrays.append(listCoord)
    return(newListOfArrays)


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
    cent = centroid2npArray(system)

    # Calculating distance matrix based on dimensionality of system and the
    # dimensionality of cartesian coordinates
    if inPlane:
        centCoord = np.c_[cent[:, 0], cent[:, 1]]
    else:
        centCoord = np.c_[cent[:, 0], cent[:, 1], cent[:, 2]]
    distanceMatrix = pDist(system, box, planar=inPlane)

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

        ######################################################################

        # Assessing the clustering done using Silhouette Coefficent (SC)
        # SC breaks when there is only one cluster. So treating them as
        # separate case
        if nClusters > 1:
            # Getting Distance matrix without outlires as SC also take outlier
            # -1 as one of the cluster which is not what we want.
            outlierIndex = np.argwhere(labels == -1)
            nonOutlierDistMatrix = np.delete(distanceMatrix,
                                             outlierIndex,
                                             axis=0)
            nonOutlierDistMatrix = np.delete(nonOutlierDistMatrix,
                                             outlierIndex,
                                             axis=1)
            nonOutlierlabels = np.delete(labels, outlierIndex)
            silhouette = silhouette_score(nonOutlierDistMatrix,
                                          nonOutlierlabels,
                                          metric="precomputed")
        else:
            # Incase there is only one cluster, SC meets a singleton case but
            # this is crucial for our case. But the problem is we don't whether
            # this one of the case where CHOL forms a single cluster amidst of
            # numerous outliers OR DPPC forming one giant cluster with a few
            # outliers. Regardless, we are reporting the singleton case
            # occured. The reason why we chose 2 is because, a) it is positive
            # and b) if other lipid has more than one cluster, when min is
            # taken, that value will be carried over instead of this and 2 is
            # only reported if both leaflet has single cluster. If we want to
            # mask this singleton event later, we can since the range of SC is
            # [-1, 1]
            silhouette = 2

        ######################################################################

        # Computing cluster lipid info

        clusterCount = 0
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

                clusterCount += 1
    else:
        # This prevents generating np.zeros((0, )) which is absurd and taking
        # its mean produce NaN which throws a lot of RunTimeWarning and output
        # file ugly.
        coreLipids = np.zeros((1, ), dtype=int)
        boundayLipids = np.zeros((1, ), dtype=int)

        ######################################################################

        # Incase there is no cluseter. Silhouette analysis is pointless. So
        # return a pointless number -2. Why -2? If the other leaflet has even
        # one cluster, then min would pass this number and report this event
        # value. If both leaflet doesn't have cluster, min returns -2, which
        # can be masked later as the range of coefficent is [-1, 1]
        silhouette = -2

        ######################################################################

    # Sanity Check
    nCores = np.sum(coreLipids)
    nBounds = np.sum(boundayLipids)
    totalLipids = nCores + nBounds + nOutliers
    if num != totalLipids:
        sys.exit("DBSCAN estimated a total number of lipids different \
                 from sytem lipids")

    return(nClusters, coreLipids, boundayLipids, nOutliers, silhouette)


def weightedMeanAndStd(values, weights):
    mean = np.average(values, weights=weights)
    var = np.average(((values-mean)*(values-mean)), weights=weights)
    return (mean, math.sqrt(var))
