'''
PROCEESS_PSGR_ONOFF - Quick assessment of total passenger counts per bus stop
'''


import sys
import dbconn
import numpy as np
import posixpath
import pickle
import geodata_export as geo


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
        print(entry['on'], entry['off'])
        data.append(entry)

    return {'data': data, 'min': mn, 'max': mx}







#==============================================================================
# Main function
#==============================================================================
def main(argv):
    data_file = "stop_summary.pkl"
    kml = "stop_summary.kml"
    table = 'actransit'
    begin_time = '2020-01-01 00:00:00'
    end_time = '2021-03-31 23:59:59'

    
    if not posixpath.isfile(data_file):
        stops = get_passenger_totals(table, begin_time, end_time)
        with open(data_file, 'wb') as f:
            pickle.dump(stops, f)
        f.close
    else:
        with open(data_file, 'rb') as f:
            stops = pickle.load(f)
        f.close

    geo.stop_passengers_kml(kml, stops, key='off')






if __name__ == "__main__":
    main(sys.argv)