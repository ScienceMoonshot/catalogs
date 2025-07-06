from numpy import sign
from argparse import Namespace
from copy import copy

pc2m = 3.08567758128E+16
pc2ly = 3.26156


class Catalog:
    colstr = ['RECONS100']
    colfloat = ['CNS NAME', '# obj', 'LHS', 'RA', 'DEC', 'proper motion', 'trigonometric parallax', 'Spectral Type', 'V', 'Mv', 'mass estimate', 'notes', 'Common Name']
    stellar_type = ['B', 'A', 'F', 'G', 'K', 'M']
    bins = [3, 5, 10, 15, 20, 25, 32]
    bgcolor = 'k'

    def __init__(self, fn='recons49.txt'):
        self.cat = []
        self.catclump = {}
        self.spec_types = {}
        indata = False
        for line in open(fn, 'r'):
            if line[:3] == '$$$':
                indata = True
                continue
            elif line.startswith('$'):
                continue
            elif line[:3] == '!!!':
                indata = False
                break
            elif not indata:
                continue
            if len(line.strip()) < 120:
                continue
            row = self._prow(line)
            self.cat.append(row)
            self.catclump.setdefault(row.sysnum, [])
            self.catclump[row.sysnum].append(row)
            self.spec_types.setdefault(row.spec[0], [])
            self.spec_types[row.spec[0]].append(row)

    def _prow(self, row):
        try:
            self.sysnum = int(row[:2])
        except ValueError:
            pass
        name = row[3:36].strip()
        radec = [float(x) for x in row[43:82].strip().split()]
        ra = radec[0] + radec[1] / 60.0 + radec[2] / 3600.0
        dec = sign(radec[3]) * (abs(radec[3]) + radec[4] / 60.0 + radec[5] / 3600.0)
        spec = row[133:155].strip()
        rd = Namespace(sysnum=copy(self.sysnum), name=name, ra=ra, dec=dec, spec=spec)
        return rd