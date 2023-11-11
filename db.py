import mysql.connector
import typing as t

# Establish a connection to your MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="TjvJrKbJDEah93C*",
            port=3306,
            database="fuelapp"
        )
        return connection
    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return None

# Create a Users table
def create_users_table(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    id INT PRIMARY KEY,
                    name VARCHAR(255),
                    email VARCHAR(255) UNIQUE,
                    password VARCHAR(255)
                )
                """
            )
            connection.commit()
            cursor.close()
            print("Users table created successfully.")
        except mysql.connector.Error as error:
            print("Error creating Users table:", error)

# Functions for User Operations
def getAllUsers(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
            cursor.close()
            return users
        except mysql.connector.Error as error:
            print("Error fetching all users:", error)
            return None

# Implement other functions similarly

# Example usage:
connection = connect_to_db()
if connection is not None:
    create_users_table(connection)
    # Use the functions here as needed
    all_users = getAllUsers(connection)
    print("All users:", all_users)
    connection.close()
