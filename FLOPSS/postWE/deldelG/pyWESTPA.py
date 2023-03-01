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
