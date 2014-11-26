# Import/Export data from a database using SQL
import graphlab as gl

# The user guide contains details on how to setup the connection to the database.
db = gl.connect_odbc("DSN=test_db")

# Import data from your database to SFrames.
sf = gl.SFrame.from_odbc(db, "SELECT * FROM customers WHERE age >= 10")

# Perform your operations
sf = sf.dropna()

# Export data back into your dataase.
sf.to_odbc(db, 'test_db_without_null')

