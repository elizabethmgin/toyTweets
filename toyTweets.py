from flask import Flask
from flask import request, url_for, render_template
import shelve
import collections
from config import api

app = Flask(__name__)


newTweet = []
listTweets = []
length = 0

tweetsDB = shelve.open('tweets.db')
try: 
    if 'local_dict' in tweetsDB:
        local_dict = tweetsDB['local_dict']
    else:
        tweetsDB['local_dict'] = {}
finally:
    tweetsDB.close()

@app.route('/gather')
def gather():
        #screen_name = dictTweets['user']['screen_name']
        #image = dictTweets['user']['profile_image_url']
        #tweet = dictTweets['text']
        #date = dictTweets['created_at']
        #tweetID = dictTweets['id']
        #source = dictTweets['source']
        #location = dictTweets['geo']['coordinates']
        #newTweet = {'screen_name':dictTweets['user']['screen_name'],'image':dictTweets['user']['profile_image_url'],'tweet':dictTweets['text'],'date':dictTweets['created_at'],'tweetID':dictTweets['id'],'source':dictTweets['source']}
        #print str(dictTweets['id'])
        #print newTweet['tweetID']
        #listTweets.append(newTweet)
    tweetsDB = shelve.open('tweets.db')
    try:
        result = api.GetSearch('dtla',show_user='true', per_page=15, page=10)
        global newTweet
        #global listTweets
        for i in range(len(result)):
            dictTweets = result[i].AsDict()
            key = str(dictTweets['id'])
            if not key in local_dict:
                new_tweet = {'screen_name':dictTweets['user']['screen_name'],'image':dictTweets['user']['profile_image_url'],'tweet':dictTweets['text'],'date':dictTweets['created_at'],'tweetID':dictTweets['id']}
                print new_tweet
                if dictTweets.has_key('geo'):
                    new_tweet['location'] = dictTweets['geo']['coordinates']
                local_dict[key] = new_tweet
        tweetsDB['local_dict'] = local_dict
            #tweetsDB[str(new_length)] = {'screen_name':dictTweets['user']['screen_name'],'image':dictTweets['user']['profile_image_url'],'tweet':dictTweets['text'],'date':dictTweets['created_at'],'tweetID':dictTweets['id'],'source':dictTweets['source']}
        print str(len(tweetsDB['local_dict']))
        return render_template('display.html', tweetsDB = tweetsDB['local_dict'])
    finally:
        tweetsDB.close()

dictTweets = {}

@app.route('/display')
def display():
    tweetsDB = shelve.open('tweets.db')
    try: 
        return render_template('display.html', tweetsDB = tweetsDB['local_dict'])
    finally:
        tweetsDB.close()
        
@app.route('/detail/<user>')
def tweet_detail(user):
    tweetDB = shelve.open('tweets.db')
    search_dict = {}
    try:
        for tweet in local_dict:
            if local_dict[tweet]['screen_name'] == user:
                search_dict[tweet] = local_dict[tweet]
        return render_template('display.html', tweetsDB = search_dict)
    finally:
        tweetsDB.close()
        
@app.route('/map')
def map():
    tweetDB = shelve.open('tweets.db')
    location_list = []
    #location_list = "["
    longlat = []
    
    mini_list = []
    try:
        for tweet in local_dict:
            if local_dict[tweet].has_key('location'):
                longlat = local_dict[tweet]['location']
                print longlat
                lat = longlat[0] 
                #lat = str(lat)
                #print 'lat:' + lat
                longitude = longlat[1]
                #longitude = str(longitude)
                #print 'lat:' + longitude
                name = local_dict[tweet]['screen_name']
                name = str(name) 
                print name
                message = local_dict[tweet]['tweet']
                #message = str(message)
                #message = message[:1]
                #message = message[0:-1]
                print message
                #location_list = location_list + '[hello, %s, %s], ' % (lat, longitude)
                #location_list = location_list + "['" + name + "', " + lat + ', ' + longitude + '],'
                #location_list.append(locate_tweet)
                locate_tweet = []
                locate_tweet.append(name)
                #locate_tweet.append(message)
                locate_tweet.append(lat)
                locate_tweet.append(longitude)
                #location_list.append(local_dict[tweet]['location'])
                location_list.append(locate_tweet)
                print location_list
        #location_list = location_list + "]"
        return render_template('map.html', location_list=location_list)
    finally:
        tweetsDB.close()
sorted_template = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>Toy Tweets</title>
    
    <style type="text/css">
    body
        {
                margin: 45px;
                font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                font-size: 12px;
        }
    
    h1
        {
                padding: 10px 8px;
                color: #FF8000;
        }
                
    #hor-zebra
        {
                width: 900px;
                text-align: left;
                border-collapse: collapse;
        }
    #hor-zebra th
        {
                font-size: 14px;
                font-weight: normal;
                padding: 10px 8px;
                color: #039;
        }
    #hor-zebra td
        {
                padding: 8px;
                color: #669;
        }
    #hor-zebra tr:nth-child(even)
        {
                background: #e8edff; 
        }
    #hor-zebra tbody tr:hover td, a:hover
        {
                color: #FF8000;
                cursor: pointer;
        }
    a
        {
                text-decoration: none;
                color: #669;
        }
        
    </style>
<script type=text/javascript src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.js"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            $("tr").click(function() {
                url = $(this).attr("url");
                window.open(url,'new window');
                });
            });
    </script>
</head>
<body>

<h1>DTLA Sorted</h1>


<table id="hor-zebra">
    <thead>
    	<tr>
            <th scope="col">Tweet ID</th>
            <th scope="col">Name</th>
            <th scope="col">Image</th>
            <th scope="col">Tweet</th>
            <th scope="col">Date</th>
        </tr>
    </thead>
    <tbody>
    %s
    </tbody>
</table>
"""

@app.route('/sort')
def sort():
    tweetDB = shelve.open('tweets.db')
    try:
        sorted_tweets = ""
        for key in sorted(local_dict.iterkeys()):
            sorted_tweets = sorted_tweets + "<tr><td>" + str(key) + "</td><td>" + str(local_dict[key]['screen_name']) + "</td><td><img src='" + local_dict[key]['image'] + "'/></td><td>" + local_dict[key]['tweet'] + "</td><td>" + local_dict[key]['date'] + "</td></tr>"
        sorted_tweets = sorted_tweets + "</table>"
        #sorted_dict = collection.OrderedDict(sorted(local_dict.items(), key=lambda item: item[0]))
        return sorted_template % sorted_tweets
    finally:
        tweetsDB.close()
    
if __name__ == '__main__':
    app.run(debug=True)