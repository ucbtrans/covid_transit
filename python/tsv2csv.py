"""
Convert TSV file to CSV.
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








# ==============================================================================
# Processing functions.
# ==============================================================================

def process_tsv(in_file, out_file):
    cnt = 0
    with open(in_file, 'r') as myfile:
        with open(out_file, 'w') as csv_file:
            for line in myfile:
                fileContent = re.sub("\t", ",", line)
                csv_file.write(fileContent)
                cnt += 1
            csv_file.close()
        myfile.close()
    print("Created \"{}\": {} lines.".format(out_file, cnt))
    return






# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)

    in_dir = "../../../../Downloads/"
    out_dir = "../../../../Downloads/"

    src_files = ['Stop_Actual_By_Booking_1908FA']



    for s in src_files:
        src = posixpath.join(in_dir, s + ".tsv")
        dest = posixpath.join(out_dir, s + ".csv")
        process_tsv(src, dest)


    return


if __name__ == "__main__":
    main(sys.argv)