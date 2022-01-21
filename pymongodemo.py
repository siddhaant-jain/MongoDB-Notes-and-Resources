from pymongo import MongoClient

mongo_database = MongoClient(host='localhost', port=27017)

#if Mongodb has username and password
# mongo_database = MongoClient("mongodb://username:password@localhost:27017/")

db = mongo_database["siddhantdb"]
db.authenticate()
current_collection = db["student_marks"]

record_to_insert = {"regNo": 5346,"name": "student13", "section":"F4", "marks":100, \
    "course": {"courseName": "B.Tech", "duration": "4 years"},\
        "address": { "city": "delhi", "state": "NCR", "country": "India"}}

current_collection.insert_one(record_to_insert)
