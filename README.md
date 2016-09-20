## What is this?

A silly Python script I made when I was bored. It reads, stores, and processes the text data from a given user's tweets and uses it to create its own randomized tweet.

## How to use

I haven't yet made this user-friendly, but if you really want to try it:

1. Make sure you have Python 3+ installed, as well as the Tweepy library (get it here: http://www.tweepy.org/)
2. Download the script file and fill in the four authentication keys at the top with your own (get them here: https://apps.twitter.com/)
3. Set the USERNAME variable to whoever you want, making sure to leave off the @ sign (it's djkhaled by default)
4. Run the script and view the resulting text file

## Possible improvements

This wasn't meant to be a serious project, but if I ever do decide to work on it in the future, these are some of the things I might do:

* Reoragnize the code, split it into multiple files
* Make it possible to change options without modifying the code i.e. command line arguments for username, number of tweets to read, etc.
* Tweak the time delays to get more data in a run while staying under Twitter's rate limits
* Be more efficient with data usage
* Make a bot that posts the tweets directly to Twitter