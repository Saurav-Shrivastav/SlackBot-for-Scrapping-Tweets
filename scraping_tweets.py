import GetOldTweets3 as got

username = 'elonmusk'
count = 1
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
    for tweet in tweets :
        if count == 1:
            response = 'Tweet number ' + str(count) + ' : ' + tweet.text
        else :
            response = response + '\n' + 'Tweet number ' + str(count) + ' : ' + tweet.text
        count = count + 1

for tweet in tweets:
    print(tweet.text)
