from numpy import sign
from argparse import Namespace

pc_m = 3.08567758128E+16
pc2ly = 3.26156
FILTER = False

def use_it(row):
    if FILTER is False:
        return True
    if row.Dec < 50.0 and row.spec[0] in ['O', 'B', 'A'] and row.dist_pc * pc2ly > 100.0:
        return True
    return False


class Catalog:
    # stellar_type = ['K', 'M', 'F', 'G', 'A', 'B']
    stellar_type = ['B', 'A', 'F', 'G', 'K', 'M']
    bins = [3, 5, 10, 15, 20, 25, 32]
    bgcolor = 'k'

    def __init__(self, fn='isaacsonetal.dat'):
        self.cat = []
        ctr = 0
        print(f"Opening {fn}")
        with open(fn, 'r') as fp:
            for line in fp:
                if not ctr:
                    self.header = line.strip().split()
                else:
                    rd = self._prow(line.strip().split())
                    if use_it(rd):
                        self.cat.append(rd)
                ctr += 1

    def _prow(self, row):
        rd = Namespace(Name=row[0].strip())
        rd.RA = float(row[1]) + float(row[2]) / 60.0 + float(row[3]) / 3600.0
        rd.Dec = sign(float(row[4])) * (abs(float(row[4])) + float(row[5]) / 60.0 + float(row[6]) / 3600.0)
        rd.mag = float(row[8])
        rd.spec = row[9]
        rd.dist_pc = float(row[10])
        rd.dist = rd.dist_pc * pc_m
        rd.disterr = 0.0
        rd.pmRA = float(row[11])
        rd.pmDec = float(row[12])
        return rd