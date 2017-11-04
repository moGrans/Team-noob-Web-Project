import pymongo, datetime

CONNECTION_STR = \
    "mongodb://Gransy:dfvGhUj068c9YqiA\
@cluster0-shard-00-00-chyjq.mongodb.net:27017,\
cluster0-shard-00-01-chyjq.mongodb.net:27017,\
cluster0-shard-00-02-chyjq.mongodb.net:27017/\
test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

client  = pymongo.MongoClient(CONNECTION_STR)

db = client.test_database

collection = db.test_collection

post = {"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()}

posts = db.posts
post_id = posts.insert_one(post).inserted_id

urls = db.urls

url = {""}

print db.collection_names(include_system_collections=False)

