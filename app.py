import json
from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
cors = CORS(app)
FLASK_APP = "Bob's Online Shop"
FLASK_ENV = "development"
app.config['TESTING'] = True
connection = sqlite3.connect('bob-online-shop.db', check_same_thread=False)
cursor = connection.cursor()

def create_db():
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS "Items" (
    "item_id"	INTEGER NOT NULL UNIQUE,
    "name"	TEXT NOT NULL,
    "image"	TEXT NOT NULL,
    "cost"	REAL NOT NULL,
    "manufacturer"	TEXT NOT NULL,
    PRIMARY KEY("item_id" AUTOINCREMENT)
  );
  """)
  connection.commit()
  print("Database created.")
  return

create_db()

@app.post("/add/item")
def add_item():
  if request.is_json:
    item = request.get_json()
    add_item_query = """
      INSERT INTO Items (name, image, cost, manufacturer)
      VALUES (?, ?, ?, ?);
    """
    values = (item["name"], item["image"], item["cost"], item["manufacturer"])
    cursor.execute(add_item_query, values)
    connection.commit()
    return "Item added successfully"

  return {"error": "Request must be JSON"}, 415

@app.get("/get/items")
def get_all_items():
  get_items_query = """
    SELECT * FROM Items;
  """

  items = cursor.execute(get_items_query).fetchall()
  items_list = []

  for item in items:
    all_items = {}
    all_items["item_id"] = item[0]
    all_items["name"] = item[1]
    all_items["image"] = item[2]
    all_items["cost"] = item[3]
    all_items["manufacturer"] = item[4]
    items_list.append(all_items)

  return items_list

@app.post("/items/search")
def search_items():
  if request.is_json:
    search = request.get_json()
    val = search["search"]
    search_item_query = """
      SELECT * FROM Items
      WHERE name LIKE ('%' || ? || '%')
      OR manufacturer LIKE ('%' || ? || '%')
      OR cost LIKE ('%' || ? || '%');
    """
    search_results = cursor.execute(search_item_query, (val, val, val)).fetchall()
    items_list = []

    for item in search_results:
      all_items = {}
      all_items["item_id"] = item[0]
      all_items["name"] = item[1]
      all_items["image"] = item[2]
      all_items["cost"] = item[3]
      all_items["manufacturer"] = item[4]
      items_list.append(all_items)

    return items_list

  return {"error": "Request must be JSON"}, 415



if __name__ == "__main__":
    create_db()
    app.run(debug=True)