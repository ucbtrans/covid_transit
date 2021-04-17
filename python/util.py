"""

Utilities...

"""
import sys
import pickle
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









# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)



    return


if __name__ == "__main__":
    main(sys.argv)