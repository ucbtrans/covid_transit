"""

Utilities...

"""

import sys
import urllib
import posixpath
import re
import numpy as np
import matplotlib.pyplot as plt
import datetime









# ==============================================================================
# Utilities API
# ==============================================================================

def dict2list(d):
    '''
    Convert dictionary of dictionaries to a list of dictionaries, where keys are added to the dictionaries.

    :param d: dictionary of dictionaries to be converted.

    :return: resulting list.
    '''

    l = []

    for k in d.keys():
        entry = d[k]
        entry['_key'] = k
        l.append(entry)

    return l


def list2dict(l):
    '''
    Convert list of dictionaries to a dictionary of dictionaries, where values of '_key" entries will be used as keys.

    :param l: list of dictionaries to be converted.

    :return: resulting dictionary.
    '''

    d = dict()
    sz = len(l)

    for i in range(sz):
        entry = l[i]
        key = entry['_key']
        del entry['_key']
        entry['_rank'] = i+1
        d[key] = entry

    return d




def make_wkt_projection(shpfile, epsg_code=4326):
    '''
    Make projection file.

    :param epsg_code: EPSG:4326 (WGS84)
           The World Geodetic System of 1984 is the geographic coordinate system (the three-dimensional one)
           used by GPS to express locations on the earth. WGS84 is the defined coordinate system for GeoJSON,
           as longitude and latitude in decimal degrees.
    :return:
    '''

    # access projection information
    wkt = urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    # remove spaces between charachters
    remove_spaces = wkt.read().decode('utf-8').replace(" ", "")
    # place all the text on one line
    output = remove_spaces.replace("\n", "")

    prjfile = posixpath.splitext(shpfile)[0] + ".prj"
    with open(prjfile, 'w+') as prj:
        prj.write(output)
        prj.close()

    return




# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)



    return


if __name__ == "__main__":
    main(sys.argv)