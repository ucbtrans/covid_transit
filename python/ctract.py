"""

Bounding Box routines.

"""


import sys
import logging
import numpy as np
import posixpath
import matplotlib.pyplot as plt
import shapefile as shp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from kml_routines import KML


class CT:

    tracts = None
    stop2tract = None

    
    def __init__(self, ctfile="ba_census_tracts.tsv", stfile="stop2tract.csv"):
        '''
        Constructor...

        :param ctfile: name of a TSV file with Census tract geometry.
        '''

        self.tracts = dict()

        with open(ctfile, "r") as tsv:
            line = tsv.readline().strip()
            line = tsv.readline().strip()
            count = 1

            while line:
                subs = line.split("\t")
                key = subs[0]
                full_id = subs[1]
                coord_str = subs[2]

                ptsubs = coord_str.split(" ")
                points = []
                for pts in ptsubs:
                    lonlat = pts.split(",")
                    points.append([float(lonlat[0]), float(lonlat[1])])

                entry = {'full_id': full_id, 'geometry_str': coord_str, 'geometry': points}
                entry = {'full_id': full_id, 'geometry': points}
                self.tracts[key] = entry
                line = tsv.readline().strip()
                count += 1

            tsv.close()

        if posixpath.isfile(stfile):
            self.stop2tract = dict()
            with open(stfile, "r") as csv:
                line = csv.readline().strip()
                line = csv.readline().strip()

                while line:
                    subs = line.split(",")
                    self.stop2tract[int(subs[0])] = subs[1]
                    line = csv.readline().strip()

                csv.close()

        return



    def tract_address(self, lat, lon):
        '''
        Get tract name for a given (lat, lon) if applicable.

        :param lat: latitude of the location.
        :param lon: longitude of the location.

        :return: Tract key.
        '''

        for k in self.tracts.keys():
            t = self.tracts[k]
            polygon = Polygon(np.array(t['geometry']))
            point = Point(lon, lat)
            if polygon.contains(point): # or point.within(polygon):
                return k

        return None



    def tract_address_by_stop(self, stop_id):
        '''
        Get tract name for a given stop ID if applicable.

        :param stop_id:

        :return: Tract key.
        '''

        if self.stop2tract == None:
            return None

        if stop_id in self.stop2tract.keys():
            return self.stop2tract[stop_id]

        return None



    def tract_meta(self, key):
        '''
        Compute bounds of a given geo box.

        :param key: Tract name.

        :return: Dictionary with the tract meta and geometry.
        '''

        if key in self.tracts.keys():
            return self.tracts[key]

        return None



    def make_shapefile(self, tracts, shpfile):
        '''
        Create shapefile with geo boxes with some attributes.
        It is expected that all boxes have the same attributes.

        :param tracts: dictionary of dictionaries, keyed by a tract name,
                       which represents the address of a tract.
        :param shpfile: path to the shapefile to be generated.
        '''

        w = shp.Writer(shp.POLYGON)
        w.field('Tract', 'C', 32)
        attrs = []

        for k in tracts.keys():
            if len(attrs) < 1:
                for a in tracts[k].keys():
                    if isinstance(tracts[k][a], dict) or isinstance(tracts[k][a], list):
                        continue
                    attrs.append(a)
                    w.field(a, 'C', 32)

            parts = []
            coords = tracts[k]['geometry']
            sz = len(coords)
            for i in range(sz):
                row = coords[i]
                parts.append([row[0], row[1]])

            w.poly(parts=[parts])

            rlist = [k]
            for a in attrs:
                rlist.append(tracts[k][a])

            w.record(*tuple(rlist))

        w.save(shpfile)

        return



    def make_kml(self, tracts, kmlfile, key='metric', num_colors=10):
        '''

        :param tracts:
        :param kmlfile:
        :param key:
        :param num_colors:
        :return:
        '''

        min, max = float(sys.maxsize), 0
        for k in tracts.keys():
            t = tracts[k]
            min, max = np.min([min, t[key]]), np.max([max, t[key]])
        #max = 0.5 * max


        cmap = plt.cm.get_cmap('jet')
        c = 255
        e = 1

        try:
            K = KML(kmlfile)
        except IOError as err:
            logging.error("make_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, err.strerror))
            return
        except:
            logging.error("make_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, sys.exc_info()[0]))
            return

        for i in range(int(num_colors) + 1):
            style_id = "clr{}".format(i)
            clr = cmap(float(i) / num_colors)
            color = "7F{:02X}{:02X}{:02X}".format(int(c * clr[2]), int(c * clr[1]), int(c * clr[0]))
            K.style(style_id, poly_color=color)

        for k in tracts.keys():
            t = tracts[k]
            if float(t[key]) < 2000:
                continue
            style_id = "#clr{}".format(np.min([num_colors, int(np.round((float(t[key])-min) * num_colors / float(max-min)))]))
            name = "{}".format(k)

            desc = ""
            for a in t.keys():
                if isinstance(t[a], dict) or isinstance(t[a], list):
                    continue
                desc += "{}: {}\n".format(a, t[a])

            coords = tracts[k]['geometry']
            poly = []
            for row in coords:
                poly.append([row[0], row[1], e])

            K.polygon(poly, name=name, description=desc, style=style_id)

        K.close()

        return









#==============================================================================
# Main function.
#==============================================================================
def main(argv):
    print(__doc__)
    







if __name__ == "__main__":
    main(sys.argv)


