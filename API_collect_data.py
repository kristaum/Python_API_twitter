import os
import json
import socket
from pymongo import MongoClient
from flask import Flask
from bson.json_util import dumps
from operator import itemgetter
from collections import Counter

#create connection MongoDB
MONGO_HOST= 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOST)

app = Flask(__name__)

@app.route('/most_followers/<username>')
def most_followers(username):
	message = "<title>Chris API - Most Followers</title>The 5 users with most followers from all your hastags "
	#Get all dbs from mongodb
	dbnames = client.database_names()
	
	#check if database requested exists on mongodb
	if username in dbnames:
		# Use database provided on uri
		db = client[username]
	
		#create list to store the 5 users with most followers
		MF_list = []
	
		#get collections which are the tags previously searched by the user
		collections = db.list_collection_names()
		if collections:
			for collection in collections:
				#stored collection from db 
				coll = db[collection]
				
				#get data from collection
				db_data = dumps(coll.find())
	
				#load data from db into a variable so we can manipulate it
				data = json.loads(db_data)
							
				#following are variables initialized
				n = 0
				user_name = ""
				followers_max = 0
							
				#This while will go through all tweets collected it could be 100 or less
				while n < len(data[0]["statuses"]):
					#store screen_name and followers count for each tweet collected in order to find user with most followers
					user_name = data[0]["statuses"][n]["user"]["screen_name"]
					followers_count = data[0]["statuses"][n]["user"]["followers_count"]
					
					#If will check if it was already provided 5 users if not will populate the list with the user
					if len(MF_list) < 6:
						MF_list.append((user_name, followers_count))
						#This If will sort the list
						if len(MF_list) == 5:
							MF_list.sort(key=itemgetter(1,1))
					else:
						key_count = 0
						temp_x = 0
						temp_list = []
						while temp_x < 6:
							temp_list.append(MF_list[temp_x][0])
							temp_x += 1
						#while will get a new user and check if it's followers are higher then the existent ones on the list
						if user_name not in temp_list: 
							while key_count < 5:
								if followers_count > MF_list[key_count][1]:
									if key_count == 0:
										MF_list[key_count] = (user_name, followers_count)
									else:
										MF_list[key_count-1] = (MF_list[key_count][0], MF_list[key_count][1])
										MF_list[key_count] = (user_name, followers_count)
									key_count += 1
								else:
									key_count = 5
					n += 1
			message = "<p>" + message + str(map(str,collections)).strip('[]') + " lookup are: </p>" + "1 - " + MF_list[4][0] + "<br>2 - " + MF_list[3][0] + "<br>3 - " + MF_list[2][0] + "<br>4 - " + MF_list[1][0] + "<br>5 - " + MF_list[0][0]
		else:
			message = "<title>Chris API - ERROR</title>there are no collections, you have done no tag search for the sample"
	else:
		message = "<title>Chris API - ERROR</title>no db for username: " + username
	return message

@app.route('/tag_hour/<username>')
def tag_per_hour(username):
	message = ""
	#Get all dbs from mongodb
	dbnames = client.database_names()
	
	#check if database requested exists on mongodb
	if username in dbnames:
		# Use database provided on uri
		db = client[username]
	
		#create list to store the count of hashtags per hour
		count_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	
		#get collections which are the tags previously searched by the user
		collections = db.list_collection_names()
		if collections:
			for collection in collections:
				#stored collection from db 
				coll = db[collection]
				
				#get data from collection
				db_data = dumps(coll.find())
	
				#load data from db into a variable so we can manipulate it
				data = json.loads(db_data)
							
				#following is var initialized for the while count
				n = 0
							
				#This while will go through all tweets collected it could be 100 or less
				while n < len(data[0]["statuses"]):
					#the while will go through the data and get the tweet hour from created_dt field
					created_dt = data[0]["statuses"][n]["created_at"]
                                	hour_day = created_dt[11:13]
                                	hour_day = int(hour_day)
                                	count_list[hour_day] += 1	
					n += 1

			message = "<title>Chris API - Tags per Hour</title>Here is the count of tweets per hour: <br> 12am: " + str(count_list[0]) + "<br> 1am: " + str(count_list[1]) + "<br> 2am: " + str(count_list[2]) + "<br> 3am: " + str(count_list[3]) + "<br> 4am: " + str(count_list[4]) + "<br> 5am: " + str(count_list[5]) + "<br> 6am: " + str(count_list[6]) + "<br> 7am: " + str(count_list[7]) + "<br> 8am: " + str(count_list[8]) + "<br> 9am: " + str(count_list[9]) + "<br> 10am: " + str(count_list[10]) + "<br> 11am: " + str(count_list[11]) + "<br> 12pm: " + str(count_list[12]) + "<br> 13pm: " + str(count_list[13]) + "<br> 14pm: " + str(count_list[14]) + "<br> 15pm: " + str(count_list[15]) + "<br> 16pm: " + str(count_list[16]) + "<br> 17pm: " + str(count_list[17]) + "<br> 18pm: " + str(count_list[18]) + "<br> 19pm: " + str(count_list[19]) + "<br> 20pm: " + str(count_list[20]) + "<br> 21pm: " + str(count_list[21]) + "<br> 22pm: " + str(count_list[22]) + "<br> 23pm: " + str(count_list[23])
		else:
			message = "<title>Chris API - ERROR</title>there are no collections, you have done no tag search for the sample"
	else:
		message = "<title>Chris API - ERROR</title>no db for username: " + username
	return message

@app.route('/tweet_language/<username>')
def tweet_per_language(username):
        message = "<title>Chris API - Tweets Lang</title>"
        #Get all dbs from mongodb
        dbnames = client.database_names()
        
        #check if database requested exists on mongodb
        if username in dbnames:
                # Use database provided on uri
                db = client[username]
        
                #create list to store the count of tweet per language of hashtags
                TL_list = []

		#string to store results
		count_lang = ""
        
                #get collections which are the tags previously searched by the user
                collections = db.list_collection_names()
		if collections:
                        for collection in collections:
                                #stored collection from db 
                                coll = db[collection]
                                
                                #get data from collection
                                db_data = dumps(coll.find())
        
                                #load data from db into a variable so we can manipulate it
                                data = json.loads(db_data)
				
				#get languages dict from twitter json file
				with open('json/languages.json', 'r') as langFile:
                                	lang_data = json.load(langFile)
                                                        
                                #following is var initialized for the while count
                                n = 0

				#This while will go through all tweets collected it could 100 or less
				while n < len(data[0]["statuses"]):
					l = 0
					lang = data[0]["statuses"][n]["user"]["lang"]
					#This while will change language abbreviation for the name of it
					while l < len(lang_data):
						if str(lang_data[l]["code"]) == str(lang):
							TL_list.append(str(lang_data[l]["name"]))
						l += 1
					n += 1
				#This string will get the counter of occurences on the TL_list which has the count of tweets per language
				count_lang = (str(Counter(TL_list)).strip('Counter\({')).strip('}\)')
				short_message = "The tweet count for the #" + str(collection) + " per language is: " + count_lang + "<br>"
				message = message + short_message
		else:
			message = "<title>Chris API - ERROR</title>there are no collections, you have done no tag search for the sample"
	else:
		message = "no db for username: " + username
        
	return message
