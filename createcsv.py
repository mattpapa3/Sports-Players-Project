import sqlite3
import csv

# Connect to your SQLite database
connection = sqlite3.connect('subscribers.db')  # Replace 'your_database_name.db' with your database file

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# SQL command to select all data from a table
select_command = "SELECT * FROM traindataNBA2;"

# Execute the select command
cursor.execute(select_command)

# Fetch all rows from the cursor
rows = cursor.fetchall()

# CSV file path to which you want to export the data
csv_file_path = 'NBAdata.csv'

# Write fetched data to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header if needed
    csv_writer.writerow([description[0] for description in cursor.description])
    # Write data rows
    csv_writer.writerows(rows)

# SQL command to select all data from a table
select_command = "SELECT * FROM traindataNBA;"

# Execute the select command
cursor.execute(select_command)

# Fetch all rows from the cursor
rows = cursor.fetchall()

# CSV file path to which you want to export the data
csv_file_path = 'NBA/oddsdata.csv'

# Write fetched data to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header if needed
    csv_writer.writerow([description[0] for description in cursor.description])
    # Write data rows
    csv_writer.writerows(rows)

# Close the connection
connection.close()

connection = sqlite3.connect('/root/propscode/propscode/MLB/mlb.db')  # Replace 'your_database_name.db' with your database file

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# SQL command to select all data from a table
select_command = "SELECT * FROM traindataPitcherStrikeouts;"

# Execute the select command
cursor.execute(select_command)

# Fetch all rows from the cursor
rows = cursor.fetchall()

# CSV file path to which you want to export the data
csv_file_path = '/root/propscode/propscode/MLB/pitcherstrikeoutdata.csv'

# Write fetched data to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header if needed
    csv_writer.writerow([description[0] for description in cursor.description])
    # Write data rows
    csv_writer.writerows(rows)

select_command = "SELECT * FROM traindataPitcherOther;"  # Replace 'your_table_name' with your table name

# Execute the select command
cursor.execute(select_command)

# Fetch all rows from the cursor
rows = cursor.fetchall()

# CSV file path to which you want to export the data
csv_file_path = '/root/propscode/propscode/MLB/pitcherotherdata.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header if needed
    csv_writer.writerow([description[0] for description in cursor.description])
    # Write data rows
    csv_writer.writerows(rows)


select_command = "SELECT * FROM traindataHitters;"

# Execute the select command
cursor.execute(select_command)

# Fetch all rows from the cursor
rows = cursor.fetchall()

# CSV file path to which you want to export the data
csv_file_path = '/root/propscode/propscode/MLB/Hitterdata.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header if needed
    csv_writer.writerow([description[0] for description in cursor.description])
    # Write data rows
    csv_writer.writerows(rows)

# Close the connection
connection.close()