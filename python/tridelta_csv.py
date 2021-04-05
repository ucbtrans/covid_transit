"""
Generate Tri-Delta CSV files for import into the DB.
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


def make_header(cols):
    header = ""
    for c in cols:
        if header != "":
            header += ","
        header += c

    return header


def make_data_line(line, cols, stops):
    entries = line.split(",")
    buf = ""

    row = {'direction': 0, 'num_wc_recs': 0, 'num_sp1_recs': 0, 'num_sp2_recs': 0, 'dwell_tot_mins': 1, 'cars': 1}
    stop_id = entries[3]
    row['stop_id'] = stop_id

    if stop_id not in stops.keys():
        return None, int(stop_id)

    hours = int(entries[5].split(':')[0])
    if hours > 23:
        return None, int(stop_id)

    row['stop_name'] = stops[stop_id]['stop_name']
    row['latitude'] = stops[stop_id]['latitude']
    row['longitude'] = stops[stop_id]['longitude']
    row['route'] = entries[2]
    row['trip'] = entries[1]
    row['stop_seq_id'] = entries[4]
    row['bus'] = entries[11]
    row['act_stop_time'] = entries[0] + " " + entries[5]
    row['psgr_on'] = entries[7]
    row['psgr_off'] = entries[8]
    row['psgr_load'] = entries[6]
    row['val_full'] = entries[9]
    row['val_overcrowd'] = entries[9]

    for c in cols:
        if buf != "":
            buf += ","

        buf += "{}".format(row[c])

    return buf, None







# ==============================================================================
# Processing functions.
# ==============================================================================
def get_stops(stop_file):
    stops = dict()

    with open(stop_file, "r") as fp:
        line = fp.readline().strip()
        line = fp.readline().strip()
        while line:
            entries = line.split(",")
            stop_id = entries[1]
            attr = {'stop_name': entries[2], 'latitude': entries[3], 'longitude': entries[4]}
            stops[stop_id] = attr
            line = fp.readline().strip()

        fp.close()
    return stops





def process_csv(in_file, out_file, cols, stops):
    ofp = open(out_file, "w+")
    #ofp.write(make_header(cols) + "\n")  # FIXME: comment out
    missing = set()

    with open(in_file, "r") as ifp:
        line = ifp.readline().strip()
        line = ifp.readline().strip()
        cnt = 0

        while line:
            buf, stop_id = make_data_line(line, cols, stops)
            line = ifp.readline().strip()
            if buf == None:
                missing.add(stop_id)
                continue

            ofp.write(buf + "\n")
            cnt += 1

        ifp.close()
        print("Created \"{}\": {} lines.".format(out_file, cnt), flush=True)
        print("There are {} stops missing: {}".format(len(missing), missing))

    ofp.close()
    return






# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)

    in_dir = "../Tri-Delta/Data/"
    out_dir = in_dir

    stops_file = "stops.csv"

    src_files = ['180930_Tri_Delta_Transit_App_Export', '190210_Tri_Delta_Transit_App_Export',
                 '190701_Tri_Delta_Transit_App_Export', '200419_Tri_Delta_Transit_App_Export',
                 '201108_Tri_Delta_Transit_App_Export']

    #src_files = ['180930_Tri_Delta_Transit_App_Export']

    cols = ['stop_id', 'stop_name', 'route', 'trip', 'stop_seq_id', 'bus', 'act_stop_time', 'direction',
            'latitude', 'longitude', 'psgr_on', 'psgr_off', 'psgr_load', 'val_full', 'val_overcrowd',
            'num_wc_recs', 'num_sp1_recs', 'num_sp2_recs', 'dwell_tot_mins', 'cars']

    stops = get_stops(posixpath.join(in_dir, stops_file))

    for s in src_files:
        src = posixpath.join(in_dir, s + ".csv")
        dest = posixpath.join(out_dir, "_" + s + ".csv")
        process_csv(src, dest, cols, stops)


    return


if __name__ == "__main__":
    main(sys.argv)