import os
import time
import re
from slackclient import SlackClient
import GetOldTweets3 as got

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "what can you do?"
com1 = "tweets "
greetings = ['hi', 'hello', 'hello there', 'hey']
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}* to know about my capabilities.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None

    command = command.lower()

    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Well I was designed to scrape tweets by Elon Musk for you. For example tell me the number of tweets that you'd like to see.\n You can do that by sending the command as 'tweets = <number of tweets that you wish to see>'."
    elif command.startswith(com1):
        arr = command.split()
        return fetchTweets(int(arr[2]))
    else:
        for greeting in greetings:
            if greeting == command:
                response = "Hello there! Try *{}*".format(EXAMPLE_COMMAND)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

def fetchTweets(num):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text='Fetching tweets....'
    )

    username = 'elonmusk'
    count = num
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                            .setMaxTweets(count)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating list of chosen tweet data
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
    text_only = [[tweet.text] for tweet in tweets]

    default_response = 'Could not fetch the tweets.'
    response = None

    count = 1
    if tweets :
        for tweet in tweets :
            if count == 1:
                response = 'Tweet number ' + str(count) + ' : ' + tweet.text + '\n' + 'You can see this tweet at: ' + tweet.permalink + '\n' + 'Date and time of the above tweet: ' + str(tweet.date) + '\n'
            else :
                response = response + '\n' + 'Tweet number ' + str(count) + ' : ' + tweet.text + '\n' + 'You can see this tweet at: ' + tweet.permalink + '\n' + 'Date and time of the above tweet: ' + str(tweet.date) + '\n'
            count = count + 1

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
