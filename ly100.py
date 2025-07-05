from numpy import sign
from argparse import Namespace
from copy import copy

pc2m = 3.08567758128E+16
pc2ly = 3.26156
FILTER = True

def use_it(row):
    return True
    if FILTER is False:
        return True
    return False


class Catalog:
    colstr = ['GaiaEDR3']
    colfloat = ['RA_ICRS', 'DE_ICRS',
            'Plx', 'pmRA', 'pmDE', 'Gmag', 'BPmag', 'RPmag', 'RV',
            'Dist50', 'xcoord50', 'ycoord50', 'zcoord50', 'Uvel50', 'Vvel50', 'Wvel50',
            'gmag', 'rmag', 'imag', 'zmag', 'Jmag', 'Hmag', 'Ksmag', 'W1mag', 'W2mag', 'W3mag', 'W4mag',]
    stellar_type = ['B', 'A', 'F', 'G', 'K', 'M']
    bins = [3, 5, 10, 15, 20, 25, 32]
    bgcolor = 'k'

    def __init__(self, fn='stars100ly.txt', numlines=1E9):
        self.cat = []
        self.header = []
        self.dist = []
        for stype in self.stellar_type:
            gfn = f"{stype}{fn}"
            print(f"Opening {gfn}")
            with open(gfn, 'r') as fp:
                for line in fp:
                    row = self._prow(line.strip().split('\t'))
                    if row is not None:
                        self.cat.append(row)

    def _prow(self, row):
        if len(row) < 3:
            return None
        rd = Namespace()
        dist = row[0].split()
        if len(dist) == 1:
            dist = row[0].split('-')
        if len(dist) != 2:
            dist.append('0.0')
        try:
            rd.dist_ly = float(dist[0])
        except ValueError:
            rd.dist_ly = float(dist[0][:3])
        rd.dist_pc = rd.dist_ly / pc2ly
        rd.dist = rd.dist_pc * pc2m
        rd.disterr = dist[1]
        rd.name = row[1].strip()
        rd.spec = copy(row[2])
        try:
            rd.mag = copy(row[3])
        except IndexError:
            rd.mag = ''
        try:
            rd.constellation = row[4].strip()
        except IndexError:
            rd.constellation = ''
        try:
            rd.notes = row[5].strip()
        except IndexError:
            rd.notes = ''
        try:
            rd.other = row[6].strip()
        except IndexError:
            rd.other = ''
        return rd