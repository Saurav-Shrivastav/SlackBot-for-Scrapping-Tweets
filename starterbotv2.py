from bs4 import BeautifulSoup
import requests
import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "what can you do?"
com1 = "tweets"
greetings = ['hi', 'hello', 'hello there', 'hey']
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
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
        if len(arr) == 1:
            arr = command.split('=')
            return fetchTweets(int(arr[1]))
        else:
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

    username = "elonmusk"

    source = requests.get(f"https://twitter.com/{username}").text

    soup = BeautifulSoup(source, 'lxml')

    count=1
    for tweet in soup.findAll('li', class_ = 'js-stream-item stream-item stream-item'):
        if count > num:
            break
        else:
            tweet_text = tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
            tweet_text = tweet_text.text
            tweet_link_small = tweet.find('a', class_='tweet-timestamp js-permalink js-nav js-tooltip')['href']
            tweet_link = f'https://twitter.com/{tweet_link_small}'
            tweet_date = tweet.find('a', class_='tweet-timestamp js-permalink js-nav js-tooltip')['title']
            slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=f'Tweet number {str(count)}: {tweet_text} \nYou can see this tweet at: {tweet_link} \nDate and time of the above tweet: {tweet_date}\n'
            )
        count = count + 1

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
