import numpy

def load_clucountchol(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clucountchol']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_clucountdppc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clucountdppc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_clucountdxpc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clucountdxpc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_clucounttotal(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clucounttotal']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_clusbychol(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clusbychol']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_clusbydppc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clusbydppc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_clusbydxpc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/clusbydxpc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_corebychol(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/corebychol']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_corebydppc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/corebydppc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_corebydxpc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/corebydxpc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_corebytotal(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/corebytotal']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_outbytotal(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/outbytotal']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_silcoeffchol(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/silcoeffchol']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_silcoeffdppc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/silcoeffdppc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset

def load_silcoeffdxpc(n_iter, iter_group):
    auxgroup1 = iter_group['auxdata/silcoeffdxpc']
    auxgroup2 = iter_group['pcoord']
    dataset = numpy.dstack((auxgroup1, auxgroup2))
    return dataset
