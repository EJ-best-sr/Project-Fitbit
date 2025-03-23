import sqlite3

# Connect to the database
conn = sqlite3.connect("fitbit_database.db")
cursor = conn.cursor()

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Loop through tables and get column names
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print(f"Table: {table_name}")
    for col in columns:
        print(f" - {col[1]}")  # col[1] contains the column name
    print("\n")

# Close the connection
conn.close()
