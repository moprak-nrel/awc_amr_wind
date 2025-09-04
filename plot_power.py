import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt

cases = ['baseline', 'pulse']

plt.figure()
for case in cases:
    fname = f'./{case}/post_processing/actuator00000/T0.nc'
    with nc.Dataset(fname) as dset:
        plt.plot(dset['T0']['time'][:], dset['T0']['power'][:]/1e6, label = case)
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('GenPower (MW)')
plt.savefig('GenPower.pdf')
