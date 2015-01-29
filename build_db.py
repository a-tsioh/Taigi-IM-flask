import pandas as P
import sqlite3 as DBM

db = DBM.connect("data.sqlite3")
df = P.read_json("im_data.json")
df.to_sql("ime", db)
db.close()

