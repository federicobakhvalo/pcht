from peewee import MySQLDatabase, Model, IntegerField, CharField, TextField
from dotenv import load_dotenv
import os
from playhouse.mysql_ext import JSONField
import pymysql
import time

# Load environment variables
# load_dotenv()
#
# # Get database credentials
# db_name = os.getenv("DB_NAME")
# db_username = os.getenv("DB_USERNAME")
# db_password = os.getenv("DB_PASSWORD")
# db_host = os.getenv("DB_HOST")
#
# connection = None
# cursor = None
# try:
#     connection = pymysql.connect(
#         host=db_host,
#         user=db_username,
#         password=db_password,
#         port=3306,
#     )
#
#     # Create a cursor object
#     cursor = connection.cursor()
#
#     # Create the database if it doesn't exist
#     cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
#     connection.commit()  # Commit the transaction
# except Exception as e:
#     print(f"Error creating database: {e}")
# finally:
#     if cursor:
#         cursor.close()
#     if connection:
#         connection.close()
#
# my_database = MySQLDatabase(
#     db_name,
#     user=db_username,
#     password=db_password,
#     host=db_host,
#     port=3306,
# )
#
#
# # Model
# class TicketModel(Model):
#     number_of_ticket = IntegerField(null=True)
#     title = CharField(null=True, max_length=1000)
#     text = TextField(null=True)
#     files = JSONField(null=True)  # Array for storing files
#
#     class Meta:
#         database = my_database
#
#
# # Connect to the database and create tables
# try:
#     my_database.connect()
#     my_database.create_tables([TicketModel], safe=True)  # Use safe=True to avoid errors if tables exist
# except Exception as e:
#     print(f"Error creating tables: {e}")
# finally:
#     my_database.close()


load_dotenv()

# Get database credentials
db_name = os.getenv("DB_NAME")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = int(os.getenv("DB_PORT", 3306))  # Allow customizable port with a default of 3306


# Function to initialize the database
def initialize_database():
    max_retries = 10  # Retry limit for database connection
    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to MySQL ({attempt + 1}/{max_retries})...")
            connection = pymysql.connect(
                host=db_host,
                user=db_username,
                password=db_password,
                port=db_port,
            )

            cursor = connection.cursor()
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
            connection.commit()
            print(f"Database '{db_name}' initialized successfully.")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    raise Exception("Failed to initialize database after multiple attempts.")


# Initialize the database
initialize_database()

# Configure the Peewee database connection
my_database = MySQLDatabase(
    db_name,
    user=db_username,
    password=db_password,
    host=db_host,
    port=db_port,
)


# Define the TicketModel
class TicketModel(Model):
    number_of_ticket = IntegerField(null=True)
    title = CharField(null=True, max_length=1000)
    text = TextField(null=True)
    files = JSONField(null=True)  # Array for storing files

    class Meta:
        database = my_database


# Connect to the database and create tables
def create_tables():
    try:
        print("Connecting to the database and creating tables...")
        my_database.connect()
        my_database.create_tables([TicketModel], safe=True)  # Use safe=True to avoid errors if tables exist
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if not my_database.is_closed():
            my_database.close()


# Create tables
create_tables()
