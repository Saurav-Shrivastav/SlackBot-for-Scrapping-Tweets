import GetOldTweets3 as got

username = 'elonmusk'
count = 5
# Creation of query object
tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                        .setMaxTweets(count)
# Creation of list that contains all tweets
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# Creating list of chosen tweet data
user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
text_only = [[tweet.text] for tweet in tweets]

count = 1
if tweets :
    for tweet in text_only :
        if count == 1:
            response = 'Tweet number ' + str(count) + ' : ' + tweet[0]
        else :
            response = response + '\n' + 'Tweet number ' + str(count) + ' : ' + tweet[0]
        count = count + 1

print(response)
