## What is this?

A silly Python script that reads and processes the text data from a given user's tweets and uses it to create its own randomized tweet, which can optionally be posted to Twitter.
Not very original, but I wanted to make it regardless.

I'm in the process of getting it on Heroku so it can actually run automatically as a bot.

## Usage

This isn't meant to be run as-is. Rather, you could use my code in your own program, or as a guide.
If you really do just want to try it, do the following (no guarantees it will work, though):

1.	Make sure you have Python 3+ installed, as well as Tweepy (http://www.tweepy.org/)
2.	Download the script file and fill in the authentication keys at the top with your own (https://apps.twitter.com/)
3.	Set the USERNAME variable to whoever you want (it's djkhaled by default, bless up), don't include the '@'
4.	Run the script. When it's done, it will prompt you to post the tweet to Twitter using the account that the authentication keys belong to.
	Regardless of your choice, the text of the tweet will be saved to a file called "tweet.txt"
	If you get an error, or if the program exits without prompting you, try running it again.