G_IMPORTS = 1
G_DEBUG = 0
import pymongo
import sys
import json

if G_IMPORTS != 0:
	print("importing PrettyTable, Counter, vaderSentiment")
	from prettytable import PrettyTable
	from collections import Counter
	from vaderSentiment.vaderSentiment import sentiment as vaderSentiment


#
def lex(text):
	return	0

#returns the polarity of the text, 
#automatically split because of sentiment function
def sentiment(text):
	if text is not None:
		vs = vaderSentiment(text)
		return vs['compound']
	return 0

def main():
	
	try: #to establish connection with the Mongo database
		conn = pymongo.MongoClient('localhost:27017')
		db = conn.cmsc491
	except pymongo.errors.ConnectionFailure as e:
		#otherwise yell at the user for a bad connection
		print "problem connected to db cmsc491" , e
		sys.exit(1)
	
	
	coke = db.CocaCola
	pepsi = db.pepsi

	cTweet = coke.find({"lang":"en"})
	pTweet = pepsi.find({"lang":"en"})
	
	cTexts = []
	pTexts = []
	
	numTweets = 25
	
	for i in range(0,numTweets):
		cTexts.append(cTweet[i]["text"].encode("utf-8"))
		pTexts.append(pTweet[i]["text"].encode("utf-8"))
		
	if G_IMPORTS != 0:
		width = 45
		cokePT = PrettyTable(field_names=['Coke Tweet','Lexical An.','Sentiment An.'])
		cokePT.max_width['Coke Tweet'] = width
		cokePT.align = 'c'
		
		pepsiPT = PrettyTable(field_names=['Pepsi Tweet', 'Lexical An.','Sentiment An.'])
		pepsiPT.max_width['Pepsi Tweet'] = width
		pepsiPT.align = 'c'
		
	if G_DEBUG == 1:
		for t in cTexts:
			print t
		for z in pTexts:
			print z		
	
	for text in cTexts:
		r = [str(text+"\n"),lex(text),sentiment(text)]
		cokePT.add_row(r)

	for text in pTexts:
		r = [str(text+"\n"),lex(text),sentiment(text)]
		pepsiPT.add_row(r)
		

	print cokePT
	print pepsiPT
	return
	
	
	
main()