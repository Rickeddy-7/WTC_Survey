import mysql.connector as connector
import json


# connect to the mysql database: 
db_connection = connector.connect(
    host="localhost", user="root", database="survey"
)

# create a cursor object to query the database using the connection established above:
cursor = db_connection.cursor()

# create a new database:
# cursor.execute("CREATE DATABASE survey")

# TODO create the table schema:
cursor.execute('''CREATE TABLE IF NOT EXIST responses(
               id tiny-int primary-key auto_increment,
               age tiny-int,
               gender varchar(10),
               isReady boolean,
               feildOfInterest varchar(25),
               companyOfInterest varchar(15),
               mentorOpinion varchar(3),
               scale tinyint
               netPromoterScore tinyint
               )'''
            )

#TODO: LOAD THE DATA FROM THE JSON FILE AND STORE IN THE DATABASE
