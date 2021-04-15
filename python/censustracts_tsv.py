'''

CENSUSTRACTS_TSV - Extract polyshapes of Census tracts from a shapefile and store them in a TSV file
                   that maps Census tract ID to a simple polygon.

'''


import sys
import shapefile as shp




#==============================================================================
# Auxiliary functions
#==============================================================================

def points2string(points):
    str = ""
    for p in points:
        if str != "":
            str += " "
        str += "{},{}".format(p[0], p[1])

    return str




#==============================================================================
# Processing functions
#==============================================================================

def make_census_tracts_csv(out_tsv, shpfile, p_id, p_name):


    try:
        sf = shp.Reader(shpfile)
    except:
        print("Cannot open shapefile '{}'...".format(shpfile))

    shapes = sf.shapes()
    records = sf.records()
    params = sf.fields
    sz = len(params)
    idx = dict()
    for i in range(sz):
        if (params[i][0] in [p_id, p_name]):
            idx[params[i][0]] = i - 1

    sz = sf.numRecords

    ofp = open(out_tsv, "w+")
    ofp.write("census tract\tfull id\tshape\n")

    for i in range(sz):
        full_id = records[i][idx[p_id]]
        name = records[i][idx[p_name]]
        tract = name.split(" ")[-1]

        points = shapes[i].points
        ofp.write("{}\t{}\t{}\n".format(tract,  full_id, points2string(points)))

    ofp.close()
    return










# ==============================================================================
# Main function - for standalone execution.
# ==============================================================================

def main(argv):
    print(__doc__)

    out_tsv = "ba_census_tracts.tsv"
    shpfile = "ba_tracts_2010/91e59542-cadc-4758-87de-87b60df95dea202044-1-1rj2hcj.veax.shp"
    param_id = "trctid"
    param_name = "trctname"
    #shpfile = "ba_tracts_2020/tl_2020_06_tract.shp"
    #param_id = "GEOID"
    #param_name = "NAME"

    make_census_tracts_csv(out_tsv, shpfile, param_id, param_name)

    return




if __name__ == "__main__":
    main(sys.argv)