from argparse import Namespace


from numpy import sign
from argparse import Namespace

kpc_m = 3.08567758128E+19
FILTER = True

def use_it(row):
    if FILTER is False:
        return True
    if row.DE_ICRS < 50.0:
        return True
    return False


class Catalog:
    colstr = ['GaiaEDR3']
    colfloat = ['RA_ICRS', 'DE_ICRS',
            'Plx', 'pmRA', 'pmDE', 'Gmag', 'BPmag', 'RPmag', 'RV',
            'Dist50', 'xcoord50', 'ycoord50', 'zcoord50', 'Uvel50', 'Vvel50', 'Wvel50',
            'gmag', 'rmag', 'imag', 'zmag', 'Jmag', 'Hmag', 'Ksmag', 'W1mag', 'W2mag', 'W3mag', 'W4mag',]
    stellar_type = None
    bins = [3, 5, 10, 15, 20, 25, 32]
    bgcolor = '0.8'

    def __init__(self, fn='vizier_votable.tsv', numlines=1E9):
        self.cat = []
        self.header = []
        self.dist = []
        ctr = 0
        with open(fn, 'r') as fp:
            print(f"Reading {fn}")
            for line in fp:
                if ctr > numlines:
                    break
                if ctr < 2:
                    self.header.append(line.strip().split(';'))
                else:
                    row = self._prow(line.strip().split(';'))
                    if use_it(row):
                        self.cat.append(row)
                ctr += 1

    def _prow(self, row):
        rd = Namespace()
        for key, val in zip(self.header[0], row):
            if not len(val.strip()):
                setattr(rd, key, ' ')
            elif key in self.colfloat:
                setattr(rd, key, float(val))
            elif key in self.colstr:
                setattr(rd, key, val)
        try:
            rd.dist = rd.Dist50 * kpc_m
            self.dist.append(rd.Dist50 * 1000.0)
        except AttributeError:
            pass
        try:
            Dec = rd.DE_ICRS
        except AttributeError:
            print(row)
        return rd