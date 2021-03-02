from flaskext.mysql import MySQL
conn = ""
cursor = ""
def setupDB():
    mysql = MySQL()

    conn = mysql.connect()
    cursor =conn.cursor()