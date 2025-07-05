import isaacsonetal, gaia, ly100
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.colors import TABLEAU_COLORS

color_order = list(TABLEAU_COLORS.keys())
color_order = ['b', '#1E90FF', '#4EEE94', 'yellow', 'orange', 'r']

catalogs = [isaacsonetal.Catalog(), gaia.Catalog(), ly100.Catalog()]

arecibo = 20
TW = 1E12

plt.rcParams['font.size'] = 14

pc2m = 3.08567758128E+16
pc2ly = 3.26156
FPI = 4.0 * np.pi
p = 2.0  # using both pols

kB = 1.380649E-23
Tsys = 100.0
B = 10
tau = 300
SNRmin = 5
A = np.pi * 1.5 * 1.5

N = 2.0 * kB * Tsys * B / np.sqrt(p * B * tau)
eirps = [arecibo, 1000 * arecibo]
fig, ax = plt.subplots(len(eirps), 1, figsize=(8, 6), constrained_layout=True)

fignames = {}
ddata = []
for eirp in eirps:
    Dmax = np.sqrt(eirp * A / (FPI * SNRmin * N)) / pc2m
    ddata.append([eirp, pc2ly * Dmax])
    fignames[eirp] = f"{eirp} TW"

print(tabulate(ddata, headers=['EIRP [TW]', f'Distance [ly] @ SNR={SNRmin}']))

for catalog in catalogs:
    for i, eirp in enumerate(eirps):
        snr = []
        for row in catalog.cat:
            if not hasattr(row, 'dist'):
                continue
            P = (eirp * TW) * A / (FPI * row.dist**2)
            SNR = P / N
            if SNR > catalog.bins[-1]:
                SNR = catalog.bins[-1] - 1
            if SNR >= catalog.bins[0]:
                snr.append( SNR )
        print(f"{eirp}  TW  -  N={len(snr)}")
        ax[i].hist(snr, bins=catalog.bins, color=catalog.bgcolor)

if catalog.stellar_type is not None:
    for i, eirp in enumerate(eirps):
        snr = []
        for s, stype in enumerate(catalog.stellar_type):
            snrow = []
            dly = []
            for row in catalog.cat:
                if not hasattr(row, 'spec') or not hasattr(row, 'dist'):
                    continue
                if stype is None or row.spec[0] == stype:
                    try:
                        D = row.dist
                    except AttributeError:
                        continue
                    P = (eirp * TW) * A / (FPI * row.dist**2)
                    SNR = P / N
                    if SNR > catalog.bins[-1]:
                        SNR = catalog.bins[-1] - 1
                    if SNR >= catalog.bins[0]:
                        snrow.append( SNR )
            snr.append(snrow)
            print(f"{stype}  {eirp / 1E12}  TW  -  N={len(snrow)}")
        ax[i].hist(snr, bins=catalog.bins, label=catalog.stellar_type, color=color_order[:len(catalog.stellar_type)])


for i, eirp in enumerate(eirps):
    if eirp > 2.0 * arecibo:
        ax[i].set_yscale('log')
    #else:
    #    ax[i].set_yticks([1, 3, 5, 10, 15])
    ax[i].set_xticks([0, 5, 10, 15, 20, 25], ['0', '5', '10', '15', '20', '>25'])
    ax[i].legend()
    ax[i].set_xlabel('SNR')
    ax[i].set_title(f"EIRP = {fignames[eirp]}")
    ax[i].axis(xmin=0, xmax=32)
    ax[i].grid()
    # ax[i].tight_layout()