


import matplotlib.pyplot as plt
import logging
import i2c_gui
import i2c_gui.chips
from i2c_gui.usb_iss_helper import USB_ISS_Helper
from i2c_gui.fpga_eth_helper import FPGA_ETH_Helper
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tqdm import tqdm
import os, sys
import multiprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
daq_path = os.path.join(BASE_DIR, "ETROC_DAQ")

if daq_path not in sys.path:
    sys.path.append(daq_path)

import run_script
import parser_arguments
import datetime
import pandas
from pathlib import Path
import subprocess
import sqlite3
from notebooks.notebook_helpers import *
from fnmatch import fnmatch
import scipy.stats as stats
from math import ceil
from numpy import savetxt
import argparse



def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--parent-directory", required=True)
    parser.add_argument("--hybrid-name", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--vhold", type=float, required=True)
    parser.add_argument("--chip-address", default="0x60")


    return parser.parse_args()

def main():

    args = parse_args()

    # turn command-line arguments into the variables
    # your old script expects

    parent_directory = args.parent_directory
    hybrid_name = args.hybrid_name
    tag = args.tag

    chip_address = [int(args.chip_address, 0)]
    ws_address = [None]
    port = 'dev/ttyACM0'


# !!!!!!!!!!!!
# It is very important to correctly set the chip name, this value is stored with the data
    chip_names = ["ET2p01_PolyamidedRemoved_D01"]
    chip_fignames = ["ET2.01 Polyamide Removed 01"]
    chip_figtitles = chip_names

    i2c_conn = i2c_connection(port,chip_address,ws_address,chip_names,[("1","1"),("1","1"),("1","1"), ("1","1")])

    #perform auto calibration
    i2c_conn.config_chips('00100101')

    # ## Set power mode to high if currents are too low
    highPowerMode = False
    if highPowerMode:
        full_col_list, full_row_list = np.meshgrid(np.arange(16),np.arange(16))
        full_scan_list = list(zip(full_row_list.flatten(),full_col_list.flatten()))
        i2c_conn.set_power_mode_scan_list(address, full_scan_list, 'high')




    plt.figure()
    plt.show()

# %%
    print(i2c_conn.NW_map_THCal)
##new stuff i added for testing multiple BL/NW to compare results per pixel (over N tests)
    print(i2c_conn.BL_map_THCal)
#also print the BL map then save these to a text file for later analysis
    chipInfo = "W04F2-84"
    TestNumber = "TESTSCRIPT"
    #TestNumber = "1BV"
    #TestNumber = "1NOPIN"
    #TestNumber = "1"
    targetpath = './'
    np.savetxt(targetpath+"NW"+chipInfo+TestNumber+".csv", i2c_conn.NW_map_THCal[96], delimiter=' ')
    np.savetxt(targetpath+"BL"+chipInfo+TestNumber+".csv", i2c_conn.BL_map_THCal[96], delimiter=' ')
    print("savedtxt")


# %%
#histdir = Path('../hybrid_testing/')
    histdir = Path(targetpath)
    histdir.mkdir(exist_ok=True)
    histfile = histdir / 'BaselineHistory.sqlite'
    #i2c_conn.save_baselines(chip_fignames,fig_path,histdir,histfile)
    i2c_conn.save_baselines(chip_fignames,histdir,histdir,histfile)

if __name__ == "__main__":
    main()






