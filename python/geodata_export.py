"""

Routines for zoning data export.

Supported data formats:
    + KML
    + ESRI shapefile

API:
    + export_measurement_sequences_kml()
    + export_bounding_boxes_kml()
    + export_kml()
    + export_areas_to_kml()
    + export_shapefile()
    
@author: Alex Kurzhanskiy <akurzhan@gmail.com>

"""

import sys
import logging
import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import shapefile as shp
from kml_routines import KML



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    stream=sys.stdout,
                    #filename='mylog.log',
                    filemode='w+')



#==============================================================================
# Auxiliary functions
#==============================================================================

def make_zone_binary_matrix(cluster, dims):
    '''
    Make a binary matrix with a zone indicated by 1s.

    :param cluster:
        A set of (i, j) tuples indicating matrix elements belonging to the zone.
    :param dims:
        A tuple (M, N) specifying matrix dimensions.

    :returns:
        M-by-N numpy array of zeros and ones.
    '''

    matrix = np.zeros(dims)

    for e in cluster:
        matrix[e[0], e[1]] = 1

    return matrix



def make_geo_boxes(args):
    '''
    Generate a list of geo boxes defining the zone.

    :param args:
        Dictionary with function arguments:
            args['bounding_box'] = List [min_lon, min_lat, max_lon, max_lat], representing
                                   geo bounding box for field data.
            args['dims'] = Tuple with data matrix dimensions (<Number of Rows>, <Number of Columns>).
            args['londeg_per_dx'] = Number of longitude degrees in the segment of length dx.
            args['latdeg_per_dy'] = Number of latitude degrees in the segment of length dy.
            args['cluster'] = Set of (i, j) tuples.

    :returns geo_boxes:
        List of [min_lon, min_lat, max_lon, max_lat]-type lists, each defining a geo box.
    '''

    bb = args['bounding_box']
    dims = args['dims']
    min_lon, min_lat = bb[0], bb[1]
    londeg_per_dx = args['londeg_per_dx']
    latdeg_per_dy = args['latdeg_per_dy']
    cluster = args['cluster']
    matrix = make_zone_binary_matrix(cluster, dims)
    m, n = dims[0], dims[1]
    non_zero = True

    geo_boxes = []

    while non_zero:
        idx = np.where(matrix > 0)
        non_zero = len(idx[0]) > 0
        if not non_zero:
            continue

        i0, j0 = idx[0][0], idx[1][0]
        i, j = i0, j0
        while (i < m) and (matrix[i, j0] > 0):
            i += 1
        while (j < n) and (matrix[i0, j] > 0):
            j += 1
        i1, j1 = i-1, j-1

        i_a, j_a = i1, j1
        i_b, j_b = i1, j1

        submatrix = matrix[i0:i1+1, j0:j1+1]
        idx_a = np.where(submatrix < 1)
        if len(idx_a[0]) > 0:
            i_a, j_a = i0 + idx_a[0][0], j0 + idx_a[1][0]
        idx_b = np.where(np.transpose(submatrix) < 1)
        if len(idx_b[0]) > 0:
            i_b, j_b = i0 + idx_b[1][0], j0 + idx_b[0][0]

        if (i_a - i0 + 1) * (j_a - j0 + 1) >= (i_b - i0 + 1) * (j_b - j0 + 1):
            i1, j1 = i_a, j_a
        else:
            i1, j1 = i_b, j_b

        for i in range(i0, i1+1):
            for j in range(j0, j1+1):
                matrix[i, j] = 0

        mn_lon = min_lon + j0 * londeg_per_dx
        mn_lat = min_lat + i0 * latdeg_per_dy
        mx_lon = min_lon + (j1 + 1) * londeg_per_dx
        mx_lat = min_lat + (i1 + 1) * latdeg_per_dy

        geo_boxes.append([mn_lon, mn_lat, mx_lon, mx_lat])

    return geo_boxes





#==============================================================================
# API
#==============================================================================

def stop_passengers_kml(kmlfile, stops, key='metric'):
    '''
    Export stop passenger counts data to a KML file.



    :returns res:
        True if operation was successful, False - otherwise.

    :execution time:
        ~10 sec
    '''

    data = stops['data']
    max = 0
    for r in data:
        max = np.max([max, r[key]])
    max = 20000
    print(max)
    dist = 150.0

    num_colors = 10
    cmap = plt.cm.get_cmap('jet')
    c = 255
    e = 1

    rlat = 37.88 * np.pi / 180
    meters_per_londeg = 111412.84 * np.cos(rlat) - 93.5 * np.cos(3 * rlat)
    meters_per_latdeg = 111132.92 - 559.82 * np.cos(2 * rlat) + 1.175 * np.cos(4 * rlat)
    dlon = dist / meters_per_londeg
    dlat = dist / meters_per_latdeg

    try:
        K = KML(kmlfile)
    except IOError as err:
        logging.error("geodata_export.stop_passengers_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, err.strerror))
        return False
    except:
        logging.error("geodata_export.stop_passengers_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, sys.exc_info()[0]))
        return False


    for i in range(int(num_colors) + 1):
        style_id = "clr{}".format(i)
        clr = cmap(float(i) / num_colors)
        color = "FF{:02X}{:02X}{:02X}".format(int(c * clr[2]), int(c * clr[1]), int(c * clr[0]))
        K.style(style_id, poly_color=color)

    for r in data:
        if r[key] < 2000:
            continue
        style_id = "#clr{}".format(np.min([num_colors, int(np.round(float(r[key]) * num_colors / float(max)))]))
        mn_lat, mn_lon = r['lat'] - dlat, r['lon'] - dlon
        mx_lat, mx_lon = r['lat'] + dlat, r['lon'] + dlon

        name = "{}: {}".format(r['id'], r['name'].replace("&", "and"))
        desc = "Passengers On: {}\nPassengers Off: {}\nPassengers Load: {}".format(r['on'], r['off'], r['load'])
        poly = [(mn_lon, mn_lat, e), (mn_lon, mx_lat, e), (mx_lon, mx_lat, e), (mx_lon, mn_lat, e)]
        K.polygon(poly, name=name, description=desc, style=style_id)

    K.close()

    return True





def export_measurement_sequences_kml(args):
    '''
    Export measurement data sequences to a KML file.

    :param args:
        Dictionary with function arguments:
            args['kmlfile'] = Path to KML file that needs to be generated.
            args['data'] = List of lists of dictionaries, indexed by i.
                          Data are broken down to separate lists when the sequence of timestamps
                          is broken - when the time interval between two consecutive data points exceeds threshold.
                          Each sub-list is indexed by j:
                            args['data'][i][j]['heading'] = Heading, where 0 or 360 is north, 180 is south, 90 is east, 270 is west.
                            args['data'][i][j]['width'] = Swath width.
                            args['data'][i][j]['distance'] = Distance from the previous data point.
                            args['data'][i][j]['<param 1>'] = Value of the first parameter in args['params'] list.
                            ...
                            args['data'][i][j]['<param n>'] = Value of the n-th parameter in args['params'] list.
                            args['data'][i][j]['geo'] = List of (lon, lat) tuples.
            args['num_colors'] = (Optional) Number of colors to use in map display. Default = 10.

    :returns res:
        True if operation was successful, False - otherwise.

    :execution time:
        ~10 sec
    '''

    if args == None:
        return False

    kmlfile = args['kmlfile']

    data = args['data']

    num_colors = 10
    if 'num_colors' in args.keys():
        num_colors = args['num_colors']

    cmap = plt.cm.get_cmap('jet')
    c = 255
    e = 1

    try:
        K = KML(kmlfile)
    except IOError as err:
        logging.error("geodata_export.export_measurement_sequences_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, err.strerror))
        return False
    except:
        logging.error("geodata_export.export_measurement_sequences_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, sys.exc_info()[0]))
        return False

    for i in range(int(num_colors) + 1):
        style_id = "clr{}".format(i)
        clr = cmap(float(i) / num_colors)
        color = "FF{:02X}{:02X}{:02X}".format(int(c * clr[2]), int(c * clr[1]), int(c * clr[0]))
        K.style(style_id, poly_color=color)


    sz = len(data)

    for i in range(sz):
        s_sz = len(data[i])
        for j in range(s_sz):
            style_id = "#clr{}".format(int(np.round(float(j) * num_colors / float(s_sz))))
            geo = data[i][j]['geo']
            p_sz = len(geo)
            mn_lon, mx_lon = geo[0][0], geo[0][0]
            mn_lat, mx_lat = geo[0][1], geo[0][1]
            for k in range(p_sz):
                lon, lat = geo[k][0], geo[k][1]
                mn_lon, mx_lon = np.min([lon, mn_lon]), np.max([lon, mx_lon])
                mn_lat, mx_lat = np.min([lat, mn_lat]), np.max([lat, mx_lat])
            name = "Datum {}/{}: {}".format(i, j, data[i][j]['time'])
            desc = "Time: {}\nDistance: {}\n".format(data[i][j]['time'], data[i][j]['distance'])
            poly = [(mn_lon, mn_lat, e), (mn_lon, mx_lat, e), (mx_lon, mx_lat, e), (mx_lon, mn_lat, e)]
            K.polygon(poly, name=name, description=desc, style=style_id)

    K.close()

    return True



def export_bounding_boxes_kml(args):
    '''
    Export measurement data sequences to a KML file.

    :param args:
        Dictionary with function arguments:
            args['kmlfile'] = Path to KML file that needs to be generated.
            args['bboxes'] = List of bounding boxes:
                args['bboxes'][i]['bbox'] = [min_lon, min_lat, max_lon, max_lat].
                args['bboxes'][i]['volume'] = area of the bounding box in meters.
                args['bboxes'][i]['contributors'] = set of indices pointing to original bounding boxes

    :returns res:
        True if operation was successful, False - otherwise.

    :execution time:
        ~10 sec
    '''

    if args == None:
        return False

    kmlfile = args['kmlfile']
    data = args['bboxes']
    num_colors = len(data)

    cmap = plt.cm.get_cmap('jet')
    c = 255
    e = 1

    try:
        K = KML(kmlfile)
    except IOError as err:
        logging.error("geodata_export.export_bounding_boxes_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, err.strerror))
        return False
    except:
        logging.error("geodata_export.export_bounding_boxes_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, sys.exc_info()[0]))
        return False

    for i in range(int(num_colors) + 1):
        style_id = "clr{}".format(i)
        clr = cmap(float(i) / num_colors)
        color = "FF{:02X}{:02X}{:02X}".format(int(c * clr[2]), int(c * clr[1]), int(c * clr[0]))
        K.style(style_id, poly_color=color)


    sz = len(data)

    for i in range(num_colors):
        style_id = "#clr{}".format(i)
        mn_lon, mx_lon = data[i]['bbox'][0], data[i]['bbox'][2]
        mn_lat, mx_lat = data[i]['bbox'][1], data[i]['bbox'][3]
        name = "BBox {} ({})".format(i, data[i]['volume'])
        desc = "Contributors: {}".format(data[i]['contributors'])
        poly = [(mn_lon, mn_lat, e), (mn_lon, mx_lat, e), (mx_lon, mx_lat, e), (mx_lon, mn_lat, e)]
        K.polygon(poly, name=name, description=desc, style=style_id)

    K.close()

    return True





def export_kml(args):
    '''
    Export zoning data to a KML file.
    
    :param args:
        Dictionary with function arguments:
            args['kmlfile'] = Path to KML file that needs to be generated.
            args['zoning'] = Dictionary with zoning info:
                             args['zoning']['bounding_box'] = List [min_lon, min_lat, max_lon, max_lat], representing
                                                              geo bounding box for field data.
                             args['zoning']['dims'] = Tuple with data matrix dimensions (<Number of Rows>, <Number of Columns>).
                             args['zoning']['londeg_per_dx'] = Number of longitude degrees in the segment of length dx.
                             args['zoning']['latdeg_per_dy'] = Number of latitude degrees in the segment of length dy.
                             args['zoning']['clusters'] = List of (i, j)-tuple sets, each set describing cells
                                                          that belong to the same class.
            
    :returns res:
        True if operation was successful, False - otherwise.
            
    :execution time:
        ~10 sec
    '''
    
    if args == None:
        return False
    
    kmlfile = args['kmlfile']
    zoning = args['zoning']
    bb = zoning['bounding_box']
    min_lon, min_lat = bb[0], bb[1]
    dims = zoning['dims']
    clusters = zoning['clusters']
    d_lon, d_lat = bb[2] - bb[0], bb[3] - bb[1]
    londeg_per_dx, latdeg_per_dy = d_lon / float(dims[1]), d_lat / float(dims[0])
    
    cmap = plt.cm.get_cmap('jet')
    c = 255
    e = 20
    
    num_zones = len(clusters)
    
    try:
        K = KML(kmlfile)
    except IOError as err:
        logging.error("geodata_export.export_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, err.strerror))
        return False
    except:
        logging.error("geodata_export.export_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, sys.exc_info()[0]))
        return False
    
    for i in range(int(num_zones)+1):
        style_id = "clr{}".format(i)
        clr = cmap(float(i)/num_zones)
        color = "FF{:02X}{:02X}{:02X}".format(int(c*clr[2]), int(c*clr[1]), int(c*clr[0]))
        K.style(style_id, poly_color=color)

    args2 = {'bounding_box': bb, 'dims': dims, 'londeg_per_dx': londeg_per_dx, 'latdeg_per_dy': latdeg_per_dy}

    meta = None
    if 'meta' in args['zoning']:
        meta = args['zoning']['meta']

    sz = len(clusters)
    for k in range(sz):
        cl = clusters[k]

        p_stats = dict()
        if meta != None:
            p_stats = meta['zone-{}'.format(k)]['param_stats']

        logging.debug("geodata_export.export_kml(): Exporting zone {} to KML file \"{}\"...".format(k, kmlfile))

        args2['cluster'] = cl
        polys = make_geo_boxes(args2)

        for p in polys:
            name = "Zone {}".format(k)
            style_id = "#clr{}".format(k)

            desc = "<![CDATA["
            for ps in p_stats.keys():
                s = p_stats[ps]
                desc += "<b>{}:</b><br>".format(ps)
                desc += "min = {:.4f}<br>".format(s['min'])
                desc += "max = {:.4f}<br>".format(s['max'])
                desc += "mean = {:.4f}<br>".format(s['mean'])
                desc += "<p>"
            desc += "]]>"
                               
            poly = [(p[0], p[1], e), (p[0], p[3], e), (p[2], p[3], e), (p[2], p[1], e)]
            K.polygon(poly, name=name, description=desc, style=style_id)
            
    K.close()
    
    return True



def export_areas_to_kml(args):
    '''
    Export area data to a KML file.

    :param args:
        Dictionary with function arguments:
            args['kmlfile'] = Path to KML file that needs to be generated.
            args['zoning'] = Dictionary with zoning info:
                             args['zoning']['bounding_box'] = List [min_lon, min_lat, max_lon, max_lat], representing
                                                              geo bounding box for field data.
                             args['zoning']['dims'] = Tuple with data matrix dimensions (<Number of Rows>, <Number of Columns>).
                             args['zoning']['londeg_per_dx'] = Number of longitude degrees in the segment of length dx.
                             args['zoning']['latdeg_per_dy'] = Number of latitude degrees in the segment of length dy.
                             args['zoning']['clusters'] = Updated list of (i, j)-tuple sets, each set describing cells
                                                          that belong to the same class.
                             args['zoning']['areas'] = List of dictionaries with area descriptions sorted by area volume:
                                                        args['zoning']['areas'][i]['id'] = Area ID.
                                                        args['zoning']['areas'][i]['zone'] = Zone ID.
                                                        args['zoning']['areas'][i]['area_set'] = Set of (i, j)-tuples addressing matrix cells.
                                                        args['zoning']['areas'][i]['border_areas'] = Set of area IDs surrounding our area.

    :returns res:
        True if operation was successful, False - otherwise.

    :execution time:
        ~10 sec
    '''

    if args == None:
        return False

    kmlfile = args['kmlfile']
    zoning = args['zoning']
    bb = zoning['bounding_box']
    min_lon, min_lat = bb[0], bb[1]
    dims = zoning['dims']
    clusters = zoning['clusters']
    areas = zoning['areas']
    d_lon, d_lat = bb[2] - bb[0], bb[3] - bb[1]
    londeg_per_dx, latdeg_per_dy = d_lon / float(dims[1]), d_lat / float(dims[0])

    cmap = plt.cm.get_cmap('jet')
    c = 255
    e = 20

    num_zones = len(clusters)

    try:
        K = KML(kmlfile)
    except IOError as err:
        logging.error("geodata_export.export_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, err.strerror))
        return False
    except:
        logging.error(
            "geodata_export.export_kml(): Cannot open KML file \"{}\": {}.".format(kmlfile, sys.exc_info()[0]))
        return False

    for i in range(int(num_zones) + 1):
        style_id = "clr{}".format(i)
        clr = cmap(float(i) / num_zones)
        color = "FF{:02X}{:02X}{:02X}".format(int(c * clr[2]), int(c * clr[1]), int(c * clr[0]))
        K.style(style_id, poly_color=color)

    args2 = {'bounding_box': bb, 'dims': dims, 'londeg_per_dx': londeg_per_dx, 'latdeg_per_dy': latdeg_per_dy}

    for a in areas:
        logging.debug("geodata_export.export_kml(): Exporting area {} to KML file \"{}\"...".format(a['id'], kmlfile))

        args2['cluster'] = a['area_set']
        #if a['id'] != 647 and a['id'] != 97:
         #   continue
        polys = make_geo_boxes(args2)

        for p in polys:
            name = "Area {}".format(a['id'])
            style_id = "#clr{}".format(int(a['zone']))
            desc = "Area: {}\nZone: {}\nVolume: {}\nBorder Areas: {}\nBorder Cell Counts by Zone: {}".format(a['id'], a['zone'], len(a['area_set']), a['border_areas'], a['border_zone_counts'])

            poly = [(p[0], p[1], e), (p[0], p[3], e), (p[2], p[3], e), (p[2], p[1], e)]
            K.polygon(poly, name=name, description=desc, style=style_id)

    K.close()

    return True



def export_shapefile(args):
    '''
    Export zoning data to a shapefile.
    
    :param args:
        Dictionary with function arguments:
            args['shapefile'] = Path to shapefile that needs to be generated.
            args['zoning'] = Dictionary with zoning info:
                             args['zoning']['bounding_box'] = List [min_lon, min_lat, max_lon, max_lat], representing
                                                              geo bounding box for field data.
                             args['zoning']['dims'] = Tuple with data matrix dimensions (<Number of Rows>, <Number of Columns>).
                             args['zoning']['londeg_per_dx'] = Number of longitude degrees in the segment of length dx.
                             args['zoning']['latdeg_per_dy'] = Number of latitude degrees in the segment of length dy.
                             args['zoning']['clusters'] = Updated list of (i, j)-tuple sets, each set describing cells
                                                          that belong to the same class.
            
    :returns res:
        True if operation was successful, False - otherwise.
            
    :execution time:
        ~10 sec
    '''
    
    if args == None:
        return False
    
    shpfile = args['shapefile']
    zoning = args['zoning']
    bb = zoning['bounding_box']
    min_lon, min_lat = bb[0], bb[1]
    dims = zoning['dims']
    clusters = zoning['clusters']
    meta = None
    if 'meta' in zoning.keys():
        meta = zoning['meta']
    d_lon, d_lat = bb[2] - bb[0], bb[3] - bb[1]
    londeg_per_dx, latdeg_per_dy = d_lon / float(dims[1]), d_lat / float(dims[0])
    
    w = shp.Writer(shp.POLYGON)
    w.field('Zone', 'C', 16)
    z0 = dict()
    if meta != None:
        z0 = meta['zone-0']['param_stats']
    for k in z0.keys():
        w.field("min{}".format(k), 'C', 64)
        w.field("max{}".format(k), 'C', 64)
        w.field("mean{}".format(k), 'C', 64)


    args2 = {'bounding_box': bb, 'dims': dims, 'londeg_per_dx': londeg_per_dx, 'latdeg_per_dy': latdeg_per_dy}

    sz = len(clusters)
    for k in range(sz):
        cl = clusters[k]

        p_stats = dict()
        if meta != None:
            p_stats = meta['zone-{}'.format(k)]['param_stats']

        logging.debug("geodata_export.export_shapefile(): Exporting zone {} to shapefile \"{}\"...".format(k, shpfile))

        args2['cluster'] = cl
        polys = make_geo_boxes(args2)

        parts = []
        for p in polys:
            name = "Zone {} ({})".format(k, p)
            poly = [[p[0], p[1]], [p[0], p[3]], [p[2], p[3]], [p[2], p[1]]]
            parts.append(poly)

        if len(parts) > 0:
            w.poly(parts=parts)
            rlist = [k]
            for ps in p_stats.keys():
                s = p_stats[ps]
                rlist.append(s['min'])
                rlist.append(s['max'])
                rlist.append(s['mean'])

            w.record(*tuple(rlist))

    w.save(shpfile)
    
    return






#==============================================================================
# Main function - for standalone execution.
#==============================================================================

def main(argv):
    print(__doc__)
    
    args = dict()
    args['kmlfile'] = "data/zoning.kml"
    args['shapefile'] = "data/zoning.shp"
    args['debug'] = True
    
    import pickle

    f = open("data/zoning.pickle", 'rb')
    args['zoning'] = pickle.load(f)
    f.close()
    
    export_kml(args)
    export_shapefile(args)
    
    return



if __name__ == "__main__":
    main(sys.argv)