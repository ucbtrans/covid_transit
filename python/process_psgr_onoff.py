'''
PROCEESS_PSGR_ONOFF - Quick assessment of total passenger counts per bus stop
'''


import sys
import dbconn
import numpy as np
import posixpath
import os
import pickle
from bbox import BB
from ctract import CT
import util as u


#==============================================================================
# Auxiliary functions
#==============================================================================




#==============================================================================
# Processing functions
#==============================================================================
def get_stops(table):
    print("Getting stop info...")

    stops = dict()

    conn, cur = dbconn.get_dbconn()

    sql = "SELECT DISTINCT ON (stop_id) stop_id, stop_name, latitude, longitude FROM {} ORDER BY stop_id, stop_name;".format(table)

    cur.execute(sql)
    records = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    for r in records:
        stops[r[0]] = {'name': r[1], 'lat': float(r[2]), 'lon': float(r[3])}

    return stops



def get_passenger_totals(table, begin_time, end_time):

    stops = get_stops(table)

    print("Getting passenger counts...")
    data = []

    conn, cur  = dbconn.get_dbconn()

    sql = "SELECT stop_id, SUM(psgr_on), SUM(psgr_off), SUM(psgr_load) FROM {} ".format(table)
    sql += "WHERE act_stop_time>='{}' and act_stop_time<='{}' ".format(begin_time, end_time)
    sql += "GROUP BY stop_id ORDER BY SUM(psgr_on);"

    cur.execute(sql)
    records = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    mn, mx = np.inf, 0
    for r in records:
        if r[0] not in stops.keys():
            continue

        s = stops[r[0]]
        entry = {'id': r[0], 'name': s['name'], 'lat': s['lat'], 'lon': s['lon'], 'on': int(r[1]), 'off': int(r[2]), 'load': int(r[3])}
        entry['metric'] = np.max([entry['on'], entry['off']])
        mn, mx = np.min([mn, entry['metric']]), np.max([mx, entry['metric']])
        #print(entry['on'], entry['off'])
        data.append(entry)

    return {'data': data, 'min': mn, 'max': mx}



def make_boxes(bb, stops):
    boxes = dict()

    thres = 0

    for s in stops['data']:
        if (s['on'] < thres) and (s['off'] < thres):
            continue

        lat, lon = float(s['lat']), float(s['lon'])
        if lat < 37 or lon > 121:
            continue

        addr = bb.box_address(lat, lon)
        if addr not in boxes.keys():
            boxes[addr] = {'on': 0, 'off': 0, 'load': 0, 'num_stops': 0, 'metric': 0, 'stops': []}

        boxes[addr]['on'] += s['on']
        boxes[addr]['off'] += s['off']
        boxes[addr]['load'] += s['load']
        boxes[addr]['num_stops'] += 1
        boxes[addr]['stops'].append(s)
        boxes[addr]['metric'] = np.max([boxes[addr]['on'], boxes[addr]['off']])

    return boxes



def make_tracts(ct, stops):
    tracts = dict()

    thres = 0
    count = 1

    for s in stops['data']:
        count += 1
        if (s['on'] < thres) and (s['off'] < thres):
            continue

        lat, lon = float(s['lat']), float(s['lon'])
        if lat < 37 or lon > 121:
            continue

        key = ct.tract_address_by_stop(s['id'])
        if key == None:
            print("Not found")
            continue

        meta = ct.tract_meta(key)
        if key not in tracts.keys():
            tracts[key] = {'on': 0, 'off': 0, 'load': 0, 'num_stops': 0, 'metric': 0, 'stops': [], 'geometry': meta['geometry']}

        tracts[key]['on'] += s['on']
        tracts[key]['off'] += s['off']
        tracts[key]['load'] += s['load']
        tracts[key]['num_stops'] += 1
        tracts[key]['stops'].append(s)
        tracts[key]['metric'] = np.max([tracts[key]['on'], tracts[key]['off']])

    return tracts






#==============================================================================
# Main function
#==============================================================================
def main(argv):
    table = 'actransit'
    #table = 'tridelta'
    year = '2020'
    year = '2019'
    sort_key = 'metric'
    cut_off = 20
    #begin_date = year + '-01-01'
    begin_date = year + '-09-01'
    end_date = year + '-12-31'

    output = "./output"
    prefix = begin_date + "_" + end_date + "_" + table
    data_file = prefix + "_stop_totals.pkl"
    boxes_shp = posixpath.join(output, prefix + "_boxes.shp")
    boxes_kml = posixpath.join(output, prefix + "_boxes.kml")
    tracts_shp = posixpath.join(output, prefix + "_tracts.shp")
    tracts_kml = posixpath.join(output, prefix + "_tracts.kml")
    begin_time = begin_date + ' 00:00:00'
    end_time = end_date + ' 23:59:59'

    
    if not posixpath.isfile(data_file):
        stops = get_passenger_totals(table, begin_time, end_time)
        with open(data_file, 'wb') as f:
            pickle.dump(stops, f)
        f.close
    else:
        with open(data_file, 'rb') as f:
            stops = pickle.load(f)
        f.close

    if not posixpath.isdir(output):
        print("Making directory '{}'...".format(output))
        os.mkdir(output)

    bb = BB()
    boxes = make_boxes(bb, stops)
    print("Made boxes!")

    box_list = u.dict2list(boxes)
    box_list = sorted(box_list, key=lambda i: i[sort_key], reverse=True)[0:cut_off]
    boxes = u.list2dict(box_list)

    bb.make_shapefile(boxes, boxes_shp)
    print("Created shapefile '{}'!".format(boxes_shp))

    bb.make_kml(boxes, boxes_kml, key=sort_key)
    print("Created KML file '{}'!".format(boxes_kml))

    ct = CT()
    tracts = make_tracts(ct, stops)
    print("Made tracts!")

    tract_list = u.dict2list(tracts)
    tract_list = sorted(tract_list, key=lambda i: i[sort_key], reverse=True)[0:cut_off]
    tracts = u.list2dict(tract_list)

    ct.make_shapefile(tracts, tracts_shp)
    print("Created shapefile '{}'!".format(tracts_shp))

    ct.make_kml(tracts, tracts_kml, key=sort_key)
    print("Created KML file '{}'!".format(tracts_kml))





if __name__ == "__main__":
    main(sys.argv)