"""
Generate AC Transit CSV files for import into the DB.
"""

import sys
import posixpath
import pickle
import re
import numpy as np
import matplotlib.pyplot as plt
import datetime


# ==============================================================================
# Aux functions.
# ==============================================================================

def map_columns(header, cols):
    colmap = dict()
    cnames = header.split(",")
    sz = len(cnames)

    for i in range(sz):
        nm = cnames[i].lower()
        if nm in cols:
            colmap[nm] = i

    return colmap


def make_header(cols):
    header = ""
    for c in cols:
        if header != "":
            header += ","
        header += c

    return header


def make_data_line(line, cols, colmap):
    entries = line.split(",")
    buf = ""

    for c in cols:
        if buf != "":
            buf += ","

        idx = colmap[c]
        buf += entries[idx]

    return buf







# ==============================================================================
# Processing functions.
# ==============================================================================

def process_csv(in_file, out_file, cols):
    ofp = open(out_file, "w+")
    #ofp.write(make_header(cols) + "\n")

    with open(in_file, "r") as ifp:
        line = ifp.readline().strip()
        colmap = map_columns(line, cols)
        line = ifp.readline().strip()
        cnt = 0

        while line:
            ofp.write(make_data_line(line, cols, colmap) + "\n")
            line = ifp.readline().strip()
            cnt += 1

        ifp.close()
        print("Created \"{}\": {} lines.".format(out_file, cnt), flush=True)

    ofp.close()
    return






# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)

    in_dir = "../../../../Downloads/"
    out_dir =  "../ACTransit/"

    src_files = ['Stop_Actual_By_Booking_1812WR', 'Stop_Actual_By_Booking_1903SP', 'Stop_Actual_By_Booking_1906SU',
                 'Stop_Actual_By_Booking_1908FA', 'Stop_Actual_By_Booking_1912WR', 'Stop_Actual_2020']

    src_files = ['Stop_Actual_By_Booking_1908FA', 'Stop_Actual_By_Booking_1912WR', 'Stop_Actual_2020']

    cols = ['stop_id', 'stop_name', 'route', 'trip', 'stop_seq_id', 'bus', 'act_stop_time', 'direction',
            'latitude', 'longitude', 'psgr_on', 'psgr_off', 'psgr_load', 'val_full', 'val_overcrowd',
            'num_wc_recs', 'num_sp1_recs', 'num_sp2_recs', 'dwell_tot_mins', 'cars']


    for s in src_files:
        src = posixpath.join(in_dir, s + ".csv")
        dest = posixpath.join(out_dir, s + ".csv")
        process_csv(src, dest, cols)


    return


if __name__ == "__main__":
    main(sys.argv)