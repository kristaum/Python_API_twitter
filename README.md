# Python_API_twitter

Project to collect tweets from user for determined hastags using python, flask and mongodb.
<br>You need to install mongodb locally.
<br>Also there is a file called authentication.py which you must store your twitter authentication.
<br>The file has the following variables, which you populate with your own:
<br>  CONSUMER_KEY = ""
<br>  CONSUMER_SECRET = ""
<br>  ACCESS_TOKEN = ""
<br>  ACCESS_TOKEN_SECRET = ""
<br>

<br>Code has the following operations/URIs:

- Collect tweets for a hashtag, the user name can be a name of your choice, this is just for tracking your tags on database.
<br>http://0.0.0.0:2880/gettweets/dbname/hashtag
  <br>i.e '/gettweets/twitterdb/github'

- The tags are stored on every hit to the URI mentioned above. To start a fresh sample tag search you can run the clean URI, it's kind a DELETE Rest operation.
<br>http://0.0.0.0:2880/clean/dbname
<br>i.e '/clean/twitterdb'

- To display who are the 5 users that has most followers:
<br>http://0.0.0.0:2880/most_followers/dbname
<br>i.e '/most_followers/chris'

- To check total of tweets per hour for all tags hit:
<br>http://0.0.0.0:2880/tag_hour/dbname
<br>i.e '/tag_hour/chris'

- To check total of tweets per language for each tags hit:
<br>http://0.0.0.0:2880/tweet_language/dbname
<br>i.e '/tweet_language/chris'

