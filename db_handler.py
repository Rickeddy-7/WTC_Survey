
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
        self.create_table(db_cursor)

        query = f"""INSERT INTO responses (age, gender, isReady, feildOfInterest, 
                    companyOfInterest, mentorOpinion, scale, netPromoterScore) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

        values = (int(data['age']), data['gender'], data['ready'], data['career'],
                data['company'], data['mentors'], int(data['curriculum']), int(data['nps']))

        try:
            db_cursor.execute(query, values)
            # print('[REACHED]')
            connection.commit()# save the changes to the database
            for x in db_cursor: print(x)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data inserted successfully!')

        except Exception as e:
            self.send_error(500, 'Internal Server Error', str(e))
        
        finally:
            db_cursor.close()
            connection.close()


    def connectToDatabase(self):
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
    

    def create_table(self, cursor: sqlite3.Cursor):
        
        query = '''CREATE TABLE IF NOT EXISTS responses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    age INTEGER,
                    gender TEXT(10),
                    isReady TEXT(3),
                    feildOfInterest TEXT(25),
                    companyOfInterest TEXT(15),
                    mentorOpinion TEXT(3),
                    scale INTEGER,
                    netPromoterScore INTEGER
                );'''
        cursor.execute(query)



def start_server():
    '''start the server and accept requests from the form'''

    PORT = 8000
    with socketserver.TCPServer(('127.0.0.1', PORT), DataHandler) as s:
        print(f'Server running and listening on port {PORT}...\n')
        s.serve_forever()



if __name__ == "__main__":
    start_server()