import sys
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)

	tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

if __name__ == '__main__':
	main()
