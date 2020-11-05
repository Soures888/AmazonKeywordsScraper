from peewee import SqliteDatabase


# Create connect to database
db = SqliteDatabase('database.db')
db.connect()

