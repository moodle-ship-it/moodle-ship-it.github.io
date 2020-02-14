from flask import Flask, request, jsonify
import json
from uuid import uuid4
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

def load_db():
	# open DB and write to it (database.JSON)
	with open("database.JSON", "r") as db1:
		database = json.load(db1)
	# Save it as something or return it
	return database

def save_db(database):
	# look up and find the database file and write to it (database.JSON)
	with open("database.JSON", "w") as db1:
		database = json.dump(database, db1, indent=4)

@app.route("/diaryentry", methods=["GET"])
@cross_origin()
def get_all_entries():
	#I need a function to load my DB
	#Then need to make my DB be JSON 
	db = load_db()
	n_entries = len(db)
	#Then I need to return the JSON to the user
	response = {
		"message": "Successfully got all diary entries!",
		"entries": db,
		"count": n_entries
	}
	return jsonify(response), 200
	#Do I need to do anything else?

@app.route("/diaryentry/<entryid>", methods=["GET"])
@cross_origin()
def get_one_entry(entryid):
	#We want to load our database
	db = load_db()
	returned_entry = ""
	#We need to search the database for our entryid
	if entryid in db:
		returned_entry = db.get(entryid)
	#We need to return the entry associated with the entryid
	#If that entry doesn't exist, let the user know their entryid wasn't available
		response = {
		"success_message": "We've found your diary entry!",
		"returned_entry": returned_entry,
		"entry_id": entryid
		}
		return jsonify(response), 200
	else:
		return jsonify({"message":f"Sorry! We can't find your entry {entryid}"}), 404
	#If the user entry does exist
	#We want to return that entry to the user with a success message

@app.route("/diaryentry", methods=["POST"])
@cross_origin()
	#This route is a post route
def create_diary_entry():
	#defines function we want to run
	#Get the data from the post request
	#Save the data into a variable
	diary_entry = json.loads(request.data)
	#Load the DB
	db = load_db()
	#We create an entry ID for the new entry
	unique_id = str(uuid4())
	#We add a new entry to the end of the DB
	db[unique_id] = diary_entry
	#Give new entry a timestamp
	db[unique_id]["createdat"] = str(datetime.now())
	#save to database
	save_db(db)
	#response message
	response = {
		"message": "New entry created",
		"data": diary_entry,
		"id": unique_id
	}
	#return the new entry 
	return jsonify(response), 201
	




