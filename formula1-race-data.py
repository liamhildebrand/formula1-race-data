import requests
import json
import mysql.connector

# Define the API endpoint for the latest race weekend data
url = "https://ergast.com/api/f1/current/last/results.json"

# Send a GET request to the API endpoint and convert the response to JSON format
response = requests.get(url)
data = json.loads(response.text)

# Extract the name of the latest race weekend
race_name = data['MRData']['RaceTable']['Races'][0]['raceName']

# Extract the data for all drivers in the latest race weekend
driver_data = []
for result in data['MRData']['RaceTable']['Races'][0]['Results']:
    driver_data.append((result['Driver']['givenName'], result['Driver']['familyName'], result['Constructor']['name'], result['position'], result['points']))

# Define the MySQL connection and cursor
db = mysql.connector.connect(
    host="hostname",
    user="username",
    password="password",
    database="databasename"
)
cursor = db.cursor()

# Define the MySQL query to create a table with the race weekend name
create_table_query = f"CREATE TABLE {race_name.replace(' ', '_').lower()} (id INT AUTO_INCREMENT PRIMARY KEY, driver_first_name VARCHAR(255), driver_last_name VARCHAR(255), constructor VARCHAR(255), position INT, points FLOAT)"

# Execute the MySQL query to create the table
cursor.execute(create_table_query)

# Define the MySQL query to insert the driver data into the table
insert_data_query = f"INSERT INTO {race_name.replace(' ', '_').lower()} (driver_first_name, driver_last_name, constructor, position, points) VALUES (%s, %s, %s, %s, %s)"

# Execute the MySQL query to insert the driver data into the table
cursor.executemany(insert_data_query, driver_data)

# Commit the changes to the database
db.commit()

# Close the MySQL connection and cursor
cursor.close()
db.close()
