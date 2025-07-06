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

    def __init__(self, fn='recons100.txt'):
        print(f"Opening {fn}")
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
            self.sysnum = int(row[:3])
        except ValueError:
            pass
        name = row[4:13].strip()
        ra = [float(x) for x in row[34:44].split()]
        ra = ra[0] + ra[1] / 60.0 + ra[2] / 3600.0
        dec = [float(x) for x in row[45:54].split()]
        dec = sign(dec[0]) * (abs(dec[0]) + dec[1] / 60.0 + dec[2] / 3600.0)
        try:
            mass = float(row[126:131])
        except ValueError:
            mass = -1.0
        notes = row[132:152].strip()
        spec = row[99:103].strip()
        common_name = row[155:].strip()
        rd = Namespace(sysnum=copy(self.sysnum), name=name, ra=ra, dec=dec, spec=spec, common_name=common_name, mass=mass, notes=notes)
        return rd