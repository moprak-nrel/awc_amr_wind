import pathlib
import netCDF4 as nc
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from cycler import cycler
from functools import reduce

plt.style.use(pathlib.Path(__file__).parent.resolve() / "project.mplstyle")

def read_ncfile(fname):
    res = {}
    with nc.Dataset(fname) as dset:
        res['time'] = dset['T0']['time'][:]
        res['power'] = dset['T0']['power'][:]/1e6
        res['f_x'] = -dset['T0']['total_disk_force'][:,0]
        res['f_y'] = -dset['T0']['total_disk_force'][:,1]
        res['f_z'] = -dset['T0']['total_disk_force'][:,2]
    return res

def main():
    pfile = 'joukowsky_awc_plots.pdf'
    cases = ['baseline', 'pulse']
    fields = ['power', 'f_x', 'f_y', 'f_z']
    case_data = {}
    for case in cases:
        fname = f'./{case}/post_processing/actuator00000/T0.nc'
        case_data[case] = read_ncfile(fname)
    for field in fields:
        plt.figure(f'{field}')
        for case in cases:
            plt.plot(case_data[case]['time'], case_data[case][field], label = case)
    with PdfPages(pfile) as pdf:
        for field in fields:
            plt.figure('power')
            plt.xlabel(r'Time $[s]$')
            plt.ylabel(r'GenPwr $[MW]$')
            plt.legend()
            pdf.savefig()
            for dim in ['x', 'y','z']:
                plt.figure(f'f_{dim}')
                plt.xlabel(r'Time $[s]$')
                plt.ylabel(f'Disk Force ${dim}$')
                plt.legend()
                pdf.savefig()

if __name__ == "__main__":
    main()
