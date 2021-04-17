"""

Generate map: stop to Census tract.

"""
import sys
from ctract import CT
import pickle
import re
import numpy as np
import matplotlib.pyplot as plt
import datetime


# ==============================================================================
# Processing functions
# ==============================================================================

def load_stops(stop_file):
    stops = dict()

    with open(stop_file, "r") as fp:
        line = fp.readline().strip()
        line = fp.readline().strip()
        while line:
            entries = line.split(",")
            #print(entries, flush=True)
            stop_id = entries[0]
            attr = {'stop_name': entries[1], 'latitude': entries[2], 'longitude': entries[3]}
            stops[stop_id] = attr
            line = fp.readline().strip()

        fp.close()
    return stops



def make_stop2tract(stop_files, tract_file, map_file):
    ct = CT(ctfile=tract_file)

    with open(map_file, "w+") as mfp:
        mfp.write("stop_id,tract\n")

        for stop_file in stop_files:
            print("Processing '{}'...".format(stop_file))
            stops = load_stops(stop_file)

            for k in stops:
                s = stops[k]
                tract = ct.tract_address(float(s['latitude']), float(s['longitude']))
                if tract == None:
                    print("{} - {}: no tract.".format(k, s['stop_name']))
                    continue

                mfp.write("{},{}\n".format(k, tract))

        mfp.close()

    return






# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)

    stop_files = ["actransit_stops.csv", "tridelta_stops.csv"]
    tract_file = "ba_census_tracts.tsv"
    map_file = "stop2tract.csv"

    make_stop2tract(stop_files, tract_file, map_file)

    return


if __name__ == "__main__":
    main(sys.argv)