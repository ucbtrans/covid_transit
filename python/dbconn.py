import sys
import psycopg2


def get_dbconn():

    conn = psycopg2.connect(host="localhost", database="transit", user="postgres", password="postgres")
        
    return conn, conn.cursor()




#==============================================================================
# Main function
#==============================================================================
def main(argv):


    return






if __name__ == "__main__":
    main(sys.argv)