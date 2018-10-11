import pymongo
import sys
import json

try:
    conn = pymongo.MongoClient('localhost:27017')
    db = conn.cmsc491
except pymongo.errors.ConnectionFailure as e:
    print "problem connected to db cmsc491" , e
    sys.exit(1)

#Coke 

hlc = db.CocaCola
in_str = open("CocaCola.txt").read()
in_lst = eval(in_str)
for tweet in in_lst:
    if "text" in tweet:
        print tweet["text"].encode('utf-8')
        hlc.insert(tweet)
print "Length is", len(in_lst)