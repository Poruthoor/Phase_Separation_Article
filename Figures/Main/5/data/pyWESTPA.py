import numpy
import h5py
from scipy import constants

def pdist2numpy(file,pcoord_dim):

    '''
    Convert info in pdist.h5 file corresponding to pcoord_dim to numpy format.

    Returns three numpy arrays corresponding to histograms, midpoints,
    niter and binbounds root groups in pdist.h5 file. This function ONLY
    extracts info corresponding to the mentioned single pcoord_dim (say 0 or 1
    but not both).

    Note : In order to generate  pdist.h5 file, you have to first run w_pdist in
    Command Line Interface.

    Example usage :

        import pyWESTPA as pw
        hist, pcoord, niter, binbounds = pw.pdist2numpy("pdist.h5",0)

    '''

    pdisth5         = h5py.File(file,'r')

    histogram       = numpy.array(pdisth5['/histograms'])
    midpoints       = numpy.array(pdisth5['/midpoints_{}'.format(str(pcoord_dim))])
    n_iter          = numpy.array(pdisth5['/n_iter'])
    binbounds       = numpy.array(pdisth5['/binbounds_{}'.format(str(pcoord_dim))])

    return(histogram,midpoints,n_iter,binbounds)


def sum_except_along(array, axes):

    '''
    Reduce the given array by addition over all axes except those listed in the scalar or 
    iterable ``axes``

    Shamelessly copied from official westpa tool : plothist.py

    '''

    try:
        iter(axes)
    except TypeError:
        axes = [axes]

    kept = set(axes)
    summed = list(set(range(array.ndim)) - kept)

    # Reorder axes so that the kept axes are first, and in the order they 
    # were given
    array = numpy.transpose(array, list(axes) + summed).copy()

    # Now, the last len(summed) axes are summed over
    for _ in range(len(summed)):
        array = numpy.add.reduce(array, axis=-1)

    return array

def _ener_zero(hist,enerzero):
    hist = -numpy.log(hist)
    if enerzero == 'min':
        numpy.subtract(hist, hist.min(), out=hist, casting="unsafe")
    elif enerzero == 'max':
        numpy.subtract(hist, hist.max(), out=hist, casting="unsafe")
    else:
        numpy.subtract(hist, self.enerzero, out=hist, casting="unsafe")
    return hist

def pdist2evolution(file,pcoord_dim,iter_start,iter_stop,zero_energy=None):

    '''
    Compute averages histogram for iterations iter_start to iter_stop

    Adapted from official westpa tool : plothist.py

    '''
    iter_step = 1


    histogram, midpoints, n_iter, binbounds = pdist2numpy(file,pcoord_dim)

    iiter_start = numpy.searchsorted(n_iter, iter_start)
    iiter_stop  = numpy.searchsorted(n_iter, iter_stop)

    itercount = iter_stop - iter_start

    # We always round down, so that we don't have a dangling partial block at the end
    nblocks = itercount // iter_step

    block_iters = numpy.empty((nblocks,2), dtype=n_iter.dtype)
    blocked_hists = numpy.zeros((nblocks,histogram.shape[1+pcoord_dim]), dtype=histogram.dtype) 

    for iblock, istart in enumerate(range(iiter_start, iiter_start+nblocks*iter_step, iter_step)):
        istop = min(istart+iter_step, iiter_stop)
        histslice = histogram[istart:istop]


        # Sum over time
        histslice = numpy.add.reduce(histslice, axis=0)

        # Sum over other dimensions
        blocked_hists[iblock] = sum_except_along(histslice, pcoord_dim)

        # Normalize
        normhistnd(blocked_hists[iblock], [binbounds])

        block_iters[iblock,0] = n_iter[istart]
        block_iters[iblock,1] = n_iter[istop-1]+1


    #enehists = -numpy.log(blocked_hists)
    if zero_energy != None :
        enerzero = zero_energy
    else :
        enerzero = False

    if enerzero:
        lenerzero = enerzero.lower()
        if lenerzero not in ('min', 'max'):
            try:
                enerzero = float(enerzero)
            except ValueError:
                raise ValueError('invalid energy zero point {!r}'.format(enerzero))
        else:
            enerzero = lenerzero
    else:
        enerzero = 'min'


    enehists = _ener_zero(blocked_hists,enerzero)
    log10hists = numpy.log10(blocked_hists)
    return (enehists, log10hists, blocked_hists,block_iters)


def kBT_to_kcal_per_mol(Temperature):

    '''
    Output kBT value in corresponding kcal/mol units for given temperaturein Kelvin.
    '''

    kB  = constants.value('Boltzmann constant')
    Na  = constants.value('Avogadro constant')
    T   = Temperature
    E_Jules = kB*T
    E_Kcal  = E_Jules/(1000*(constants.calorie))
    E_Kcal_per_mol  = E_Kcal*Na
    return (E_Kcal_per_mol)
    #  E_Jules_per_mol  = E_Jules*Na
    #  return (E_Jules_per_mol)

def normhistnd(hist, binbounds):
    '''
    Normalize the N-dimensional histogram ``hist`` with corresponding
    bin boundaries ``binbounds``.  Modifies ``hist`` in place and returns
    the normalization factor used.

    Shamelessly copied from official westpa tool : plothist.py

    '''

    ndim = hist.ndim

    if ndim != len(binbounds):
        raise ValueError(
            'shape of histogram [{!r}] does not match bin boundary sets (there are {})'.format(hist.shape, len(binbounds))
        )

    diffs = [numpy.diff(bb) for bb in binbounds]

    if ndim == 1:
        assert diffs[0].shape == hist.shape
        normfac = (hist * diffs[0]).sum()
    else:
        outers = numpy.multiply.outer(diffs[0], diffs[1])
        for delta in diffs[2:]:
            outers = numpy.multiply.outer(outers, delta)
        assert outers.shape == hist.shape, 'hist shape {} != outers shape {}'.format(hist.shape, outers.shape)
        # Divide by bin volumes
        hist /= outers
        normfac = hist.sum()
        # normfac = (hist * outers).sum()

    hist /= normfac
    return normfac
