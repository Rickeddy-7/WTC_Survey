
import mysql.connector as connector
import socketserver
import http


# DEFINE A HANDLER FOR THE HTTP REQUESTS:
class DataHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        data = self.parseHTTP()
        db_cursor = self.connectToDatabase()
        db_cursor.execute("""INSERT INTO responses VALUES(
                            ?, ?, ?, ?, ?, ?, ?, ?)""")

    def connectToDatabase(self):
        # connect to the mysql database: 
        db_connection = connector.connect(host="localhost", user="root", database="survey")
        # create a cursor object to query the database using the connection established above:
        return db_connection.cursor()

    def parseHTTP(self):
        content_length = int(self.headers["Content-Length"])
        print(f'[{content_length}]')
        form_data = self.rfile.read(content_length).decode("utf-8")
        print(f'[{form_data}]')
        data = dict
        for kv_pair in form_data.split('&'):
            key, val = kv_pair.split('=')
            data[key] = val

        return data

    def createDatabaseStructure(self, cursor: connector):
        # create a new database:
        # cursor.execute("CREATE DATABASE survey")

        # TODO create the table schema:
        cursor.execute('''CREATE TABLE IF NOT EXIST responses(
                    id tiny-int primary_key auto_increment,
                    age tiny-int,
                    gender varchar(10),
                    isReady boolean,
                    feildOfInterest varchar(25),
                    companyOfInterest varchar(15),
                    mentorOpinion varchar(3),
                    scale tinyint
                    netPromoterScore tinyint)''')
        
        print('Success creating database')



# START THE SERVER:
with socketserver.TCPServer(('localhost', 8000), DataHandler) as server:
    print('Server running and listening on port 8000...\n')
    server.serve_forever()