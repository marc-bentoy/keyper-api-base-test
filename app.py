import os
import psycopg2
from datetime import datetime, timezone
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
database_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(database_url)

# DATABASE QUERIES
CREATE_BUILDINGS_TABLE = """
CREATE TABLE IF NOT EXISTS buildings (
    id SERIAL PRIMARY KEY, 
    name TEXT
);"""

CREATE_STORIES_TABLE = """
CREATE TABLE IF NOT EXISTS stories (
    id SERIAL PRIMARY KEY,
    building_id INTEGER REFERENCES buildings(id), 
    storey INTEGER 
);"""

CREATE_ROOMS_TABLE = """
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    building_id INTEGER REFERENCES buildings(id), 
    storey_id INTEGER REFERENCES stories(id), 
    name TEXT, 
    number TEXT 
);"""

CREATE_KEYS_TABLE = """
CREATE TABLE IF NOT EXISTS keys (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id), 
    rfid TEXT, 
    borrowed BOOLEAN 
);"""

CREATE_BORROW_LIST_TABLE = """
CREATE TABLE IF NOT EXISTS borrow_list (
    id SERIAL PRIMARY KEY,
    key_id INTEGER REFERENCES keys(id), 
    date TIMESTAMP 
);"""

CREATE_RETURN_LIST_TABLE = """
CREATE TABLE IF NOT EXISTS return_list (
    id SERIAL PRIMARY KEY,
    key_id INTEGER REFERENCES keys(id), 
    date TIMESTAMP 
);"""

INSERT_BUILDING_RETURN_ID = "INSERT INTO buildings (name) VALUES (%s) RETURNING id;"
INSERT_STOREY = "INSERT INTO stories (building_id, storey) VALUES (%s, %s);"
INSERT_ROOM = "INSERT INTO rooms (building_id, storey_id, name, number) VALUES (%s, %s, %s, %s);"
INSERT_KEY = "INSERT INTO keys (room_id, rfid, borrowed) VALUES (%s, %s, %s);"
INSERT_BORROW = "INSERT INTO borrow_list (key_id, date) VALUES (%s, %s);"
INSERT_RETURN = "INSERT INTO return_list (key_id, date) VALUES (%s, %s);"

UPDATE_KEY_BORROWED = """UPDATE keys SET borrowed=true WHERE id=%s;"""
UPDATE_KEY_RETURNED = """UPDATE keys SET borrowed=false WHERE id=%s;"""

@app.get("/")
def home():
    return "keyper base api (test)"


@app.post("/api/building")
def create_building():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BUILDINGS_TABLE)
            cursor.execute(INSERT_BUILDING_RETURN_ID, (name,))
            building_id = cursor.fetchone()[0]
    
    return {"id": building_id, "message": f"{name} building was created."}, 201


@app.post("/api/storey")
def insert_storey():
    data = request.get_json()
    storey = data["storey"]
    building_id = data["building"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_STORIES_TABLE)
            cursor.execute(INSERT_STOREY, (building_id, storey))
    
    return {"message": f"Storey {storey} added on building {building_id}"}, 201


@app.post("/api/room")
def insert_room():
    data = request.get_json()
    name = data["name"]
    number = data["number"]
    building_id = data["building"]
    storey_id = data["storey"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM, (building_id, storey_id, name, number))
    
    return {"message": f"Room {name} - {number} was added on -> {storey_id} - {building_id}."}, 201


@app.post("/api/key")
def insert_key():
    data = request.get_json()
    room_id = data["room"]
    rfid = data["rfid"]
    borrowed = data["borrowed"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_KEYS_TABLE)
            cursor.execute(INSERT_KEY, (room_id, rfid, borrowed))
    
    return {"message": f"Key with RFID: {rfid} was added on room {room_id}."}, 201


@app.post("/api/borrow")
def borrow_key():
    data = request.get_json()
    key_id = data["key"]

    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_BORROW_LIST_TABLE)
            cursor.execute(INSERT_BORROW, (key_id, date))
            cursor.execute(UPDATE_KEY_BORROWED, (key_id, ))
    
    return {"message": f"Key {key_id} was borrowed."}, 201


@app.post("/api/return")
def return_key():
    data = request.get_json()
    key_id = data["key"]

    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_RETURN_LIST_TABLE)
            cursor.execute(INSERT_RETURN, (key_id, date))
            cursor.execute(UPDATE_KEY_RETURNED, (key_id, ))
    
    return {"message": f"Key {key_id} was returned."}, 201