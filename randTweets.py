__author__ = "Amil Mahida"
__email__ = "amil.mahida@gmail.com"
__status__ = "Prototype"

import tweepy
import random

# THESE MUST BE FILLED OUT BEFORE THE PROGRAM CAN WORK
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
CONSUMER_KEY = "..."
CONSUMER_KEY_SECRET = "..."
ACCESS_TOKEN = "..."
ACCESS_TOKEN_SECRET = "..."
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

USERNAME = "djkhaled"  # Replace with whoever you want

COUNT = 10  # Number of tweets to process at a time; see https://dev.twitter.com/rest/public/timelines
MAX_TWEETS = 100  # Max number of tweets to collect, not including retweets

tweet_count = 0
timeline = []  # A list to store all the status objects, as returned by tweepy's methods
tweet_text_list = []  # A list of strings containing the text from the tweets, excluding retweets

timeline += api.user_timeline(screen_name=USERNAME, count=COUNT)
for tweet in timeline:
    if not tweet.text.startswith("RT @"):  # Save the text only from original tweets, not retweets
        tweet_count += 1
        tweet_text_list.append(tweet.text)

lowest_id = timeline[-1].id

while tweet_count < MAX_TWEETS:
    # Not likely to happen, but stop looping in case we've gone through all tweets
    if not api.user_timeline(screen_name=USERNAME, max_id=lowest_id - 1, count=COUNT):
        break

    # Retrieve the next set of tweets
    timeline += api.user_timeline(screen_name=USERNAME, max_id=lowest_id - 1, count=COUNT)

    for i in range(len(timeline) - COUNT, len(timeline)):
        if not timeline[i].text.startswith("RT @"):
            tweet_count += 1
            tweet_text_list.append(timeline[i].text)

            if tweet_count >= MAX_TWEETS:
                break

    lowest_id = timeline[-1].id


# Above, we retrieved the raw text data from a number of tweets.
# Now we will process the data and generate our own.
# ---------------------------------------------------------------------------------------------------------------------

# Storing words as objects allows us to also keep track of what they were preceded and followed by.
class Word:
    word = ""
    prefix = ""
    suffix = ""

    def __init__(self, w, p, s):
        self.word = w
        self.prefix = p
        self.suffix = s

# This will store all of the Words used in the tweets we gathered earlier.
master_word_list = []


# Reads through the text of a tweet and stores each word as a Word object in a list of Words.
# tweet_text - A string corresponding to the text of a tweet.
# wlist - List of Word objects.
def process_tweet(tweet_text, wlist):
    # Split up the tweet into a list of individual words
    simple_words = tweet_text.split()

    if not simple_words:
        return

    # Start by storing the first word of the tweet, which is preceded by
    # nothing and followed by the word in the next index
    if len(simple_words) == 1:
        current_word = Word(simple_words[0], "", "")
    else:
        current_word = Word(simple_words[0], "", simple_words[1])

    wlist.append(current_word)

    # Go through the rest of the tweet's words and store them in wlist
    for i in range(1, len(simple_words) - 1):
        current_word = Word(simple_words[i], simple_words[i - 1], simple_words[i + 1])
        wlist.append(current_word)

    if len(simple_words) > 1:
        current_word = Word(simple_words[-1], simple_words[-2], "")
        wlist.append(current_word)

# Go through all of the tweets and store their word data in the master Word list
for tweet in tweet_text_list:
    process_tweet(tweet, master_word_list)


# Starts creating a tweet by randomly selecting its first word.
# wlist - A list of Words used by the user in their tweets.
# gen_tweet - The tweet to be generated (must be empty).
def start_chain(wlist, gen_tweet):
    # List of Words that can be used to start a tweet.
    # This draws from all the words the given user used to start their tweets.
    valid_starters = []

    # If a word appeared at the beginning of a tweet (preceded by nothing),
    # add it to the list of possible starter words.
    for w in wlist:
        if w.prefix == "":
            valid_starters.append(w)

    # Randomly choose a starter word to begin the tweet.
    gen_tweet.append(random.choice(valid_starters))


# Adds another word to a tweet that's being made
# wlist - A list of Words used by the used in their tweets.
# gen_tweet - The tweet that's being generated (must contain at least one word).
def continue_chain(wlist, gen_tweet):
    prev_word = gen_tweet[len(gen_tweet) - 1]  # The last word in the current tweet
    valid_words = []  # List of all the words that can be used to follow the last word

    # A word is considered valid for appending if it was ever used in any of the
    # tweets to follow the last word of gen_tweet.
    for w in wlist:
        if w.prefix == prev_word.word:
            valid_words.append(w)

    if not valid_words:
        return 0

    # Randomly choose one of the valid words to be appended to the tweet
    selected_word = random.choice(valid_words)
    gen_tweet.append(selected_word)

    # If the chosen word is a tweet ender (not followed by anything), return 0 to indicate it.
    if selected_word.suffix == "":
        return 0
    else:
        return 1


# Uses a master Word list, start_chain, and continue_chain to generate a tweet
# wlist- The list of all words used in the tweets
def create_tweet(wlist):
    generated_tweet = []
    cont = 1

    start_chain(wlist, generated_tweet)
    while cont:
        cont = continue_chain(wlist, generated_tweet)

    return generated_tweet

test_tweet = create_tweet(master_word_list)

# Open a text file to write the generated tweet to. Unicode is used because of emojis.
# Disclaimer: emojis will probably appear in the text file as squares or junk characters
# due to lack of emojis in most text editor fonts.
fileout = open("tweet.txt", "w", encoding="utf8")

for w in test_tweet:
    string = w.word
    fileout.write(w.word + " ")

fileout.close()
