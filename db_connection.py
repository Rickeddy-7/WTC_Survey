import mysql.connector as connector

# connect to the mysql database: 
db_connection = connector.connect(
    host="localhost", user="root", database="survey"
)

# create a cursor object to query the database using the connection established above:
cursor = db_connection.cursor()

# create a new database:
# cursor.execute("CREATE DATABASE survey")