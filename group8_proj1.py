import pymongo
import sys
import json
from collections import Counter 

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
tweets = hlc.find()

for tweet in in_lst:
    if "text" in tweet:
        print tweet["text"].encode('utf-8')
        hlc.insert(tweet)
print "Length is", len(in_lst)



if tweets[1]["user"]:
    print tweets[1]["user"].keys()
    print tweets[1]["user"]["screen_name"].encode('utf-8')
    print tweets[1]["user"]["description"].encode('utf-8')
    print tweets[1]["user"]["location"].encode('utf-8')
    print "======================================="
else:
    print "No user data found during this iteration."

texts = []
for status in tweets:
    texts.append(status["text"])
print texts

print "======================="

