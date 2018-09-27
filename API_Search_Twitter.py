import os
import twitter
from pymongo import MongoClient
from authentication import *
from flask import Flask
from API_collect_data import *

#create connection MongoDB
#MONGO_HOST= 'mongodb://localhost:27017/'

#Create session using python-twitter module
session = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

#uri = "q=%23{0}&result_type=recent&count=2"

#app = Flask(__name__)

@app.route("/")
def home():
    return "<title>Chris API</title><br>Hello, <p>Welcome to Chris API, a fun interactive way to get some data from tweets using hashtag.</p> <br>To collect tweets hit this URI below, the user name can be a name of your choice, this is just for tracking your tags on database. <br>i.e '/gettweets/chris/challenge' <p>The tags are stored on every hit to the URI mentioned above. To start a fresh sample tag search you can run the clean URI. <br>i.e '/clean/chris'</p> <p>To display who are the 5 users that has most followers hit: <br>i.e '/most_followers/chris'</p> <p>To check total of tweets per hour for all tags hit: <br>i.e '/tag_hour/chris'</p> <p>To check total of tweets per language for each tags hit: <br>i.e '/tweet_language/chris'</p>"

@app.route('/gettweets/<username>/<hashtag>')
def collect_tweets(username, hashtag):
    #uri = uri.format(tag)
    #call twitter api to fletch results per tag
    #results = session.GetSearch(raw_query=uri,return_json=True)
    tag = "#" + hashtag
    results = session.GetSearch(term=tag, count=100, result_type='recent', return_json=True)
    
    #remove hashtag character
    #tag = hashtag[1:].strip()

    #return response
    response = "<title>Chris API - Get Tweets</title>Collected twiits for the hashtag: " + tag

    try:
        client = MongoClient(MONGO_HOST)

        # Use twitterdb database. If it doesn't exist, it will be created.
        db = client[username]

        #named collection to be the tag name
        collection = db[hashtag]

        # delete tag collection, it might have previous data.
        collection.drop()

        #insert the data into the mongoDB into a collection for the specified tag
        #tag collection doesn't exist, it will be created.
        collection.insert(results)
  	  
    except Exception as e:
        return e
    return response

@app.route('/clean/<username>')
def delete_db(username):
    response = "<title>Chris API - Delete Sample</title>Deleted db " + username + " you may now start new sample"
    try:
        client = MongoClient(MONGO_HOST)
        #delete db
        client.drop_database(username)

    except Exception as e:
        return e
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2880, debug=True)

