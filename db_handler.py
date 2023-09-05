
import mysql.connector as connector
import socketserver
import http.server as server


# DEFINE A HANDLER FOR THE HTTP REQUESTS:
class DataHandler(server.SimpleHTTPRequestHandler):

    def do_POST(self):
        data = self.parseHTTP()
        db_cursor = self.connectToDatabase()
        
        try:
            query = f"""INSERT INTO responses (age, gender, isReady, fieldOfInterest, 
                    companyOfInterest, mentorOpinion, scale, netPromoterScore) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            # values = (int(data['age']), data['gender'], data['isReady'], data['fieldOfInterest'],
            #         data['companyOfInterest'], data['mentorOpinion'], 
            #         int(data['scale']), int(data['netPromoterScore']))

            db_cursor.execute(query, data.values())

            # save the changes to the database
            db_cursor.connection.commit()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data inserted successfully!')
        except Exception as e:
            self.send_error(500, 'Internal Server Error', str(e))


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
        data = {}
        for kv_pair in form_data.split('&'):
            key, val = kv_pair.split('=')
            data[key] = val

        return data



# START THE SERVER TO LISTEN FOR REQUESTS FROM THE FORM:
with socketserver.TCPServer(('localhost', 8000), DataHandler) as s:
    print('Server running and listening on port 8000...\n')
    s.serve_forever()



# HOW THE DATABASE WAS CREATED:
# cursor.execute("CREATE DATABASE survey")

# HOW THE TABLE SCHEMA WAS CREATED:
# cursor.execute('''CREATE TABLE IF NOT EXISTS responses(
#             id SMALLINT PRIMARY KEY AUTO_INCREMENT,
#             age TINYINT,
#             gender VARCHAR(10),
#             isReady VARCHAR(3),
#             fieldOfInterest VARCHAR(25),
#             companyOfInterest VARCHAR(15),
#             mentorOpinion VARCHAR(3),
#             scale TINYINT,
#             netPromoterScore TINYINT);''')