import sqlite3

# Replace 'your_database.db' with the path to your SQLite database file
conn = sqlite3.connect('BankNH.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Query to get the list of tables
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all table names
# Display the tables
# print("Tables in the database:")
# for table in tables:
#     print(table[0])
# cursor.execute("UPDATE NEWBANK SET BAL = 0 WHERE  USERNAME =?",("sambak",))
# cursor.execute("DELETE FROM NEWBANK WHERE BAL = ?", (10000.0,))

# Commit the changes
# conn.commit()

# cursor.execute("UPDATE NEWBANK SET CONFIRM = ?  WHERE USERNAME =? ",('9908','udayk'))
cursor.execute("select * from NEWBANK")
rows = cursor.fetchall()

# cursor.execute(f"PRAGMA table_info (NEWBANK)")
# structure = cursor.fetchall()
# print(structure)


# Print each row
for row in rows:
    print(row)
# Close the connection
conn.commit()
conn.close()
# sqlite_sequence
# NEWBANK
# NEW
# NEWB
# NEWT
#strcuture of the NEWBANK table 
# (0, 'ID', 'INTEGER', 0, None, 1), 
# (1, 'USERNAME', 'CHAR (20)', 1, None, 0), 
# (2, 'FIRSTNAME', 'STR', 1, None, 0),
# (3, 'LASTNAME', 'STR', 1, None, 0), 
# (4, 'EMAIL', 'STR', 1, None, 0), 
# (5, 'PASSWORD', 'STR', 1, None, 0), 
# (6, 'CONFIRM', 'PASSWORD STR', 1, None, 0), 
# (7, 'PHONE', 'CHAR (11)', 1, None, 0), 
# (8, 'SEX', 'STR', 0, None, 0), 
# (9, 'ADDRESS', 'CHAR (50)', 1, None, 0), 
# (10, 'BAL', 'REAL (200)', 0, None, 0)]