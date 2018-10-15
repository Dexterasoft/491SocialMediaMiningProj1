#Title: Project 1 
#Author: Group 8 
#Date: 10/15/18
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


# File: proj1.py
# Date: 10/15/18
# Group: 8
import re
# Name: tokenizer
# Input: tweet (string)
# Output: a dictionary containing each unique word in the tweet and
# their number of occurrences along with the lexical diversity
#code provided by JayT
def tokenizer (tweet):
	lexicon = {}
	wordCount = 0
	punctuation = re.compile('[\W|_]')
	
	# initial break up
	broken = tweet.split(' ')
	#print(broken)
	
	# clean up by removing punctuation w/ regex
	cleanData = []
	for word in broken:
		clean = re.split(punctuation, word)
		#print(clean)
		
		# Parse cleaned data
		for x in clean:
			if x != '' and x != None:
				if len(x) == 1 and (x != 'a' and x != 'A' and x != 'I'):
					#print (x)
					continue
				cleanData.append(x)
				wordCount += 1
	#print (cleanData)

	for word in cleanData: 
		if word in lexicon:
			lexicon[word] += 1
		else:
			lexicon[word] = 1

	# Calculate lexical diversity
	diversity = 0.0
	diversity = float(len(lexicon))/wordCount
			
	return lexicon, diversity
#print (tokenizer('This is a_test. It\'s going well! Random a a a a a'))	



#returns the lexical analysis 
def lex(text):
	return	tokenizer(text)[1]
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
	
	
	#gather the databases
	coke = db.CocaCola
	pepsi = db.pepsi

	#get the "english" tweets
	cTweet = coke.find({"lang":"en"})
	pTweet = pepsi.find({"lang":"en"})
	
	#setup the texts
	cTexts = []
	pTexts = []
	
	#set number  of tweets for professor's sanity
	numTweets = 25
	
	#add tweets from database, not checking whether or not the tweet exists
	for i in range(0,numTweets):
		cTexts.append(cTweet[i]["text"].encode("utf-8"))
		pTexts.append(pTweet[i]["text"].encode("utf-8"))
		
	#for debug purposes
	if G_IMPORTS != 0:
		width = 45
		
		#create table parameters
		cokePT = PrettyTable(field_names=['Coke Tweet','Lexical An.','Sentiment An.'])
		cokePT.max_width['Coke Tweet'] = width
		cokePT.align = 'c'
		
		pepsiPT = PrettyTable(field_names=['Pepsi Tweet', 'Lexical An.','Sentiment An.'])
		pepsiPT.max_width['Pepsi Tweet'] = width
		pepsiPT.align = 'c'
		#END TABLE SETUP
		
	if G_DEBUG == 1:
		for t in cTexts:
			print t
		for z in pTexts:
			print z		
	
	
	#do the lexical and sentiment analysis for each tweet in the Text List
	print "Adding row to Coke table",
	for text in cTexts:
		print ".",
		r = [str(text+"\n"),lex(text),sentiment(text)]
		cokePT.add_row(r)
	
	print "\n"
	print "Adding row to Pepsi table",
	for text in pTexts:
		print ".",
		r = [str(text+"\n"),lex(text),sentiment(text)]
		pepsiPT.add_row(r)
		
	#print the tables
	print cokePT
	print pepsiPT
	return
main()