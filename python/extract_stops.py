'''
EXTRACT_STOPS - Retrieve stop location information from the transit DB.
'''

import sys
import dbconn
import numpy as np
import posixpath
import os
import pickle
from bbox import BB
import geodata_export as geo


# ==============================================================================
# Auxiliary functions
# ==============================================================================


# ==============================================================================
# Processing functions
# ==============================================================================
def get_stops(table, csv_file):
    print("Getting stop info...")
    ofp = open(csv_file, "w+")
    ofp.write("stop_id,stop_name,latitude,longitude\n")

    stops = dict()

    conn, cur = dbconn.get_dbconn()

    sql = "SELECT DISTINCT ON (stop_id) stop_id, stop_name, latitude, longitude FROM {} ORDER BY stop_id, stop_name;".format(
        table)

    cur.execute(sql)
    records = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    for r in records:
        stops[r[0]] = {'name': r[1], 'lat': float(r[2]), 'lon': float(r[3])}
        ofp.write("{},{},{},{}\n".format(r[0], r[1], r[2], r[3]))

    ofp.close()

    return stops




# ==============================================================================
# Main function
# ==============================================================================
def main(argv):
    table = 'actransit'
    stops_csv = table + "_stops.csv"

    stops = get_stops(table, stops_csv)


if __name__ == "__main__":
    main(sys.argv)