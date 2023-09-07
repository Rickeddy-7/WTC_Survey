
import http.server as server
import socketserver
import sqlite3


# DEFINE A HANDLER FOR THE HTTP REQUESTS:
class DataHandler(server.SimpleHTTPRequestHandler):

    def do_POST(self):
        '''connects to the database and adds new records to the table'''

        data = self.parseHTTP()
        connection = self.connectToDatabase()
        db_cursor = connection.cursor()
        # self.create_table(db_cursor)

        query = """INSERT INTO responses (age, gender, isReady, feildOfInterest, 
                    companyOfInterest, mentorOpinion, scale, netPromoterScore) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

        fieldOfInterest = self.formatDataString(data['career'])
        companyOfInterest = self.formatDataString(data['company'])
        values = (int(data['age']), data['gender'], data['ready'], fieldOfInterest,
                companyOfInterest, data['mentors'], int(data['curriculum']), int(data['nps']))

        try:
            db_cursor.execute(query, values)
            connection.commit()# save the changes to the database
            # for x in db_cursor: print(x)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data inserted successfully!')

        except Exception as e:
            self.send_error(500, 'Internal Server Error', str(e))
        
        finally:
            db_cursor.close()
            connection.close()


    def connectToDatabase(self) -> sqlite3.Connection:
        '''returns a connection object to be used to curse the database'''
        # create or connect to a database
        return sqlite3.connect("survey.db")


    def parseHTTP(self) -> dict:
        '''takes the request string, decodes it, and then seperates it into key-value pairs'''

        # get the length of the request body:
        content_length = int(self.headers["Content-Length"])
        # then use it to determine how much data to read from the incoming request:
        form_data: str = self.rfile.read(content_length).decode("utf-8")
        data = {}
        for kv_pair in form_data.split('&'):
            key, val = kv_pair.split('=')
            data[key] = val

        return data
    

    def formatDataString(self, string: str) -> str:
        '''takes in a string and replaces the + sign with an empty space'''

        if "+" not in string: return string

        words = string.split("+")
        return " ".join(words)
    

    def createTable(self, cursor: sqlite3.Cursor):
        
        query = """CREATE TABLE IF NOT EXISTS responses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    age INTEGER,
                    gender TEXT(10),
                    isReady TEXT(3),
                    fieldOfInterest TEXT(25),
                    companyOfInterest TEXT(15),
                    mentorOpinion TEXT(3),
                    scale INTEGER,
                    netPromoterScore INTEGER
                );"""
        cursor.execute(query)



def start_server():
    '''start the server and accept requests from the form'''

    PORT = 8000
    with socketserver.TCPServer(('127.0.0.1', PORT), DataHandler) as s:
        print(f'Server running and listening on port {PORT}...\n')
        s.serve_forever() # this method will call do_POST upon invocation



if __name__ == "__main__":
    start_server()