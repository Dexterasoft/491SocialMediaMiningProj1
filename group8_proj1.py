import pymongo
import sys
import json

from collections import Counter
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

try:
    conn = pymongo.MongoClient('localhost:27017')
    db = conn.cmsc491
except pymongo.errors.ConnectionFailure as e:
    print "problem connected to db cmsc491" , e
    sys.exit(1)

	
coke = db.CocaCola
pepsi = db.pepsi

cTweet = coke.find()
pTweet = pepsi.find()

cText = []
pText = []

counter = 0

#LEXICAL ANALYSIS
for status in cTweet:
	if(counter > 25):
		counter = 0
		break
	cText.append(status["text"])
	counter += 1
	
for status in pTweet:
	if(counter > 25):
		counter = 0
		break
	pText.append(status["text"])
	counter += 1
#print(pText[:25])
cWords = []
pWords = []

for text in cText:
	for w in text.split():
		cWords.append(w)
		
for text in pText:
	for w in text.split():
		pWords.append(w)
		
#end loops
cCnt = Counter(cWords)
pCnt = Counter(pWords)

cSortCnt = sorted(cCnt.items(), key=lambda pair: pair[1], reverse=True)
pSortCnt = sorted(pCnt.items(), key=lambda pair: pair[1], reverse=True)

#print("END LEXICAL ANALYSIS")
#END OF LEXICAL ANALYSIS
counter=0
#SENTIMENT ANALYSIS

print("Tweet\tLex. Analysis\tSentiment Analysis")
for tweet in cTweet:
	if counter>=25: #counter of professor's sanity
		break
	if(tweet["user"]["description"] is not None):
		counter+=1
		vs = vaderSentiment(tweet["user"]["description"].encode('utf-8'))
		print "\n"+str(counter)+"\t"+str((1.0*len(set(cWords))/len(cWords)))+"\t"+str(vs['compound'])
		print tweet["text"].encode("utf-8")
print("END COKE")
print("START PEPSI")
#SENTIMENT ANALYSIS
counter=0
##print(counter,pTweet)
for tweet in pTweet:
	if counter>=25: #counter of professor's sanity
		break
	if(tweet["user"]["description"] is not None):
		counter+=1
		vs = vaderSentiment(tweet["user"]["description"].encode('utf-8'))
		print "\n"+str(counter)+"\t"+str((1.0*len(set(pWords))/len(pWords)))+"\t"+str(vs['compound'])
		print tweet["text"].encode("utf-8")
		
#print("END PEPSI")
		
