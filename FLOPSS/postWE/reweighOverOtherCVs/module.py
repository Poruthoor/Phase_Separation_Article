import numpy

def load_CHE(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/CHE']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_CHE_CHOL(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/CHE_CHOL']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_CHE_DPPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/CHE_DPPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_CHE_DXPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/CHE_DXPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI_CHOL(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI_CHOL']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI_DPPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI_DPPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI_DXPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI_DXPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI_WithoutCHOL(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI_WithoutCHOL']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI_WithoutCHOL_DPPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI_WithoutCHOL_DPPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_SI_WithoutCHOL_DXPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/SI_WithoutCHOL_DXPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_pcoord(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/pcoord']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_weightedCluster_CHOL(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/weightedCluster_CHOL']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_weightedCluster_DPPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/weightedCluster_DPPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_weightedCluster_DXPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/weightedCluster_DXPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops_DPPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops_DPPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops_DIPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops_DIPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops_DAPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops_DAPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops_POPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops_POPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops_CHOL(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops_CHOL']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops2D_DPPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops2D_DPPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops2D_DIPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops2D_DIPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops2D_DAPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops2D_DAPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops2D_POPC(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops2D_POPC']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_mops2D_CHOL(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/mops2D_CHOL']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_DBSCAN_fixed_min(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/DBSCAN_fixed_min']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_DBSCAN_fixed_max(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/DBSCAN_fixed_max']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset
