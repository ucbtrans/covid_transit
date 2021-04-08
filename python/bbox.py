"""

Bounding Box routines.

"""


import sys
import logging
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import shapefile as shp
from kml_routines import KML


class BB:


    
    def __init__(self, dx=1000, dy=1000, o_lat=37.0, o_lon=-122.54):
        '''
        Constructor...

        :param dx: horizontal (longitudinal) cell size in meters.
        :param dy: vertical (latitudinal) cell size in meters.
        :param ref_lat: origin.
        '''

        self.o_lat = o_lat
        self.o_lon = o_lon

        rlat = self.o_lat * np.pi / 180
        meters_per_londeg = 111412.84 * np.cos(rlat) - 93.5 * np.cos(3 * rlat)
        meters_per_latdeg = 111132.92 - 559.82 * np.cos(2 * rlat) + 1.175 * np.cos(4 * rlat)
        self.dlon = dx / meters_per_londeg
        self.dlat = dy / meters_per_latdeg
        
        return



    def box_address(self, lat, lon):
        '''
        Get row and column of the box containing a given geo location (lat, lon).
        Row and column are computed with respect to origin (o_lat, o_lon), dx and dy.

        :param lat: latitude of the location.
        :param lon: longitude of the location.

        :return: Tuple (row, column).
        '''

        diff_lat, diff_lon = np.max([0, lat - self.o_lat]), np.max([0, lon - self.o_lon])
        row, col = int(np.ceil(diff_lat / self.dlat)), int(np.ceil(diff_lon / self.dlon))
        
        return (row, col)



    def box_bounds(self, address):
        '''
        Compute bounds of a given geo box.

        :param address: (row, column) tuple pointing to the geo box with sizes dx-by-dy.

        :return: Tuple (min_lat, min_lon, max_lat, max_lon).
        '''

        row, column = address[0], address[1]

        min_lat, min_lon = self.o_lat + row * self.dlat, self.o_lon + column * self.dlon
        max_lat, max_lon = min_lat + self.dlat, min_lon + self.dlon

        return (min_lat, min_lon, max_lat, max_lon)



    def make_shapefile(self, boxes, shpfile):
        '''
        Create shapefile with geo boxes with some attributes.
        It is expected that all boxes have the same attributes.

        :param boxes: dictionary of dictionaries, keyed by a tuple (row,column),
                      which represents the address of a geo box.
                      Values of this dictionary are dictionaries with the same set of keys.
        :param shpfile: path to the shapefile to be generated.
        '''

        w = shp.Writer(shp.POLYGON)
        w.field('Box Address', 'C', 32)
        attrs = []

        for k in boxes.keys():
            if len(attrs) < 1:
                for a in boxes[k].keys():
                    attrs.append(a)
                    w.field(a, 'C', 32)

            b = self.box_bounds(k)
            parts = [[[b[1], b[0]], [b[3], b[0]], [b[3], b[2]], [b[1], b[2]]]]
            w.poly(parts=parts)

            rlist = [k]
            for a in attrs:
                rlist.append(boxes[k][a])

            w.record(*tuple(rlist))

        w.save(shpfile)

        return









#==============================================================================
# Main function.
#==============================================================================
def main(argv):
    print(__doc__)
    







if __name__ == "__main__":
    main(sys.argv)


