"""
KML routines.
"""


import sys


class KML:
    
    def __init__(self, kml_file):
        '''
        Constructor...
        '''
        
        self.kml_file = kml_file
        self.kml = open(self.kml_file, 'w')
        
        self.kml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        self.kml.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n  <Document>\n")
        
        return



    def style(self, style_id, line_width=1, line_color="00000000", poly_color="00000000"):
        '''
        
        '''
        
        self.kml.write("    <Style id=\"{}\">\n".format(style_id))
        self.kml.write("     <LineStyle>\n")
        self.kml.write("      <width>{}</width>\n".format(line_width))
        self.kml.write("      <color>{}</color>\n".format(line_color))
        self.kml.write("     </LineStyle>\n")
        self.kml.write("     <PolyStyle>\n")
        self.kml.write("      <color>{}</color>\n".format(poly_color))
        self.kml.write("     </PolyStyle>\n")
        self.kml.write("    </Style>\n")
        
        return
        
    
    
    def polygon(self, outer_boundary, inner_boundaries=None, name="Poly", description=None, style="clr1"):
        '''
        
        '''
        
        self.kml.write("    <Placemark>\n")
        self.kml.write("      <name>{}</name>\n".format(name))
        
        if description != None:
            self.kml.write("      <description>{}</description>\n".format(description))
            
        self.kml.write("      <styleUrl>{}</styleUrl>\n".format(style))
        self.kml.write("      <Polygon>\n")
        self.kml.write("        <extrude>1</extrude>\n")
        self.kml.write("        <altitudeMode>relativeToGround</altitudeMode>\n")
        self.kml.write("        <outerBoundaryIs>\n")
        self.kml.write("          <LinearRing>\n")
        self.kml.write("            <coordinates>\n")
        
        sz = len(outer_boundary)
        for i in range(sz):
            self.kml.write("              {},{},{}\n".format(outer_boundary[i][0], outer_boundary[i][1], outer_boundary[i][2]))
            
        self.kml.write("            </coordinates>\n")
        self.kml.write("          </LinearRing>\n")
        self.kml.write("        </outerBoundaryIs>\n")
        self.kml.write("      </Polygon>\n")
        self.kml.write("    </Placemark>\n")
        
        return



    def close(self):
        '''
        Finish and close KML file.
        '''
        
        self.kml.write("  </Document>\n</kml>\n")
        self.kml.close()
        
        return








#==============================================================================
# Main function.
#==============================================================================
def main(argv):
    print(__doc__)
    
    
    my_kml = "test.kml"
    
    K = KML(my_kml)
    K.close()








if __name__ == "__main__":
    main(sys.argv)


