import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.students
collection = db.students


student = {
    'id': '1',
    'name': 'xiaoming',
    'age': 20
}

result = collection.insert(student)
print(result)