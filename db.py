import pymongo

client = pymongo.MongoClient()
db = client.interview_mosaic

def get_collection(collectionname='c1'):
    return db[collectionname]

# useful stuff
# insert
# coll.insert_one({})
# coll.insert_many([{}])
# find
# coll.find_one({})
# find by range and sort
# coll.find({'date': {'$lt': datetime.datetime(year, month, day, hour=0, ..)}}).sort('author', 1(asc)|-1(dsc))
# find subdocument
# coll.find_one({'subdocument.a': 1.0,
#...                      'subdocument.b': 1.0})
# creating indexes
# coll.create_index([('field', pymongo.ASCENDING)], unique=True)
