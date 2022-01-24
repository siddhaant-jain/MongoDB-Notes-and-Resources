from pymongo import MongoClient 

mongo_database = MongoClient(host='localhost', port=27017)

#if Mongodb has username and password
# mongo_database = MongoClient("mongodb://username:password@localhost:27017/")

db = mongo_database["siddhantdb"]
current_collection = db["student_marks"]

# record_to_insert = {"regNo": 5346,"name": "student13", "section":"F4", "marks":100, \
#     "course": {"courseName": "B.Tech", "duration": "4 years"},\
#         "address": { "city": "delhi", "state": "NCR", "country": "India"}}
# current_collection.insert_one(record_to_insert)

# first_record_to_insert = {"regNo": 5800,"name": "student14", "section":"F2", "marks":100, \
#     "course": {"courseName": "B.Tech", "duration": "4 years"},\
#         "address": { "city": "delhi", "state": "NCR", "country": "India"}}
# second_record_to_insert = {"regNo": 5900,"name": "student15", "section":"F4", "marks":100, \
#     "course": {"courseName": "B.Tech", "duration": "4 years"},\
#         "address": { "city": "delhi", "state": "NCR", "country": "India"}}
# current_collection.insert_many([first_record_to_insert, second_record_to_insert])

# record_to_find = {"name": "student14"}
# for result in current_collection.find(record_to_find):
#     print(result)
#     print(result["course"]["courseName"])
#     print()

# record_to_find = {"address.city": "delhi"}
# for result in current_collection.find(record_to_find):
#     print(result)
#     print(result["address"]["city"])
#     print()

# record_to_find = {"address.city": "jhansi"}
# result = current_collection.find_one(record_to_find)
# print(result)
# print(result["address"]["city"])
# print()

# results = current_collection.delete_many({}) # this will delete everything in collection
# results = current_collection.delete_many({"address.city": "delhi"})

# re ran the insert command for running next commands
# current_collection.update_one({"name":"student14"},{"$set":{"address.state":"Haryana"}})


