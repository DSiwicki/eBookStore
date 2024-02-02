import sqlite3
import datetime

db = 'uAiYPtSRGHGzIrWe.db'
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")

conn = sqlite3.connect(db)
c = conn.cursor()

logs_query = "CREATE TABLE 'logs' ('login' TEXT NOT NULL, 'dt' TEXT NOT NULL, 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE)"
storage_query = "CREATE TABLE 'ebooks_storage' ( 'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'title' TEXT NOT NULL, 'author' TEXT, 'year' INTEGER, 'price' NUMERIC NOT NULL, 'isbn' TEXT NOT NULL, 'publisher' TEXT, 'details' TEXT)"
sales_query = "CREATE TABLE 'sales' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'user_id' INTEGER NOT NULL, 'book_id' INTEGER NOT NULL, 'dt' TEXT NOT NULL, 'cost' INTEGER NOT NULL)"
users_query = "CREATE TABLE 'users' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'name' TEXT NOT NULL, 'login' TEXT NOT NULL UNIQUE, 'mail' TEXT NOT NULL UNIQUE, 'password' TEXT NOT NULL, 'rank' TEXT NOT NULL, 'reg_time' TEXT NOT NULL)"
wishlist_query = "CREATE TABLE 'wishlist' ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 'user_id' INTEGER NOT NULL, 'book_id' INTEGER NOT NULL, 'dt' INTEGER NOT NULL)"

c.execute(logs_query)
c.execute(storage_query)
c.execute(sales_query)
c.execute(users_query)
c.execute(wishlist_query)

c.execute("INSERT INTO users (name, login, mail, password, rank, reg_time) VALUES (?,?,?,?,?,?)", ('admin', 'admin', 'admin@admin.com', 'admin', 'admin', now))

conn.commit()

c.close()


#CREATE TABLE IF NOT EXISTS logs 
# (
#     login TEXT NOT NULL, 
#     dt TEXT NOT NULL, 
#     id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT
# );

#  CREATE TABLE IF NOT EXISTS ebooks_storage
#  ( 
#      id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, 
#      title TEXT NOT NULL, 
#      author TEXT, 
#      year INTEGER, 
#      price NUMERIC NOT NULL, 
#      isbn TEXT NOT NULL, 
#      publisher TEXT, 
#      details TEXT
# );

# CREATE TABLE sales
# (
#     id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, 
#     user_id INTEGER NOT NULL, 
#     book_id INTEGER NOT NULL, 
#     dt TEXT NOT NULL, 
#     cost INTEGER NOT NULL
# );

# CREATE TABLE IF NOT EXISTS users
# (
#     id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, 
#     name TEXT NOT NULL, 
#     login TEXT NOT NULL UNIQUE, 
#     mail TEXT NOT NULL UNIQUE, 
#     password TEXT NOT NULL, 
#     rank TEXT NOT NULL, 
#     reg_time TEXT NOT NULL
# );

# CREATE TABLE IF NOT EXISTS wishlist 
# (
#     id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, 
#     user_id INTEGER NOT NULL, 
#     book_id INTEGER NOT NULL, 
#     dt INTEGER NOT NULL
# );
