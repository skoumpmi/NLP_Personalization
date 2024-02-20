Tweets_cleaning functionality 
---------------------------------------------
Scope: clean tweets retrieved using Twitter API. The data used as input should be on csv format.


Main script: clear__twitter.py  
Execution: 
    `python clear__twitter.py "<path_to_folder>\initial_tweets_dataset_without_retweets.csv" "<path_to_folder>\final_dataset_twitter.csv" "tweet" "user_id"`
	
	
Explanation of system parameters:

   1. sys.argv[0]: path where stored the python script

   2. sys.argv[1]: path of the input csv file with Twitter Texts

   3. sys.argv[2]: path of the output csv file with clear Twitter Text

   4. sys.argv[3]: is the column in the retrieved tweet's csv file including the tweet's text (i.e. tweet)

   5. sys.argv[4]: is the column in the retrieved tweet's csv file including the user's twitter id (i.e. user_id)
   
	
Cleaning process: 

	1. Cleaning of text tokens that have # or @ prefixes in tweet's texts. The algorithm clears reletive text entity  e.g. @Peter or #GoodMorning if they are in the end of the text. 

    2. Cleaning of the emojis. Emojis are encoded as UTF-8 format e.g. \xF0\x9F\x98\x83. Those characters are removed from within text.

    3. Unicode characters are replaced with UTF-8 characters.   

    4. Cleaning of the urls included in tweet's text.

    5. Cleaning of the byte character 'b' in the beggining of a tweet.

    6. Cleaning of all special characters and punctuation except for (.) dot, (,) comma, (!) Exclamation Mark and (?) Question mark. This type of punctuation are important for capturing the meaning of text. In addition, formalise some specific phrases such as haven't became have not.

    7. Cleaning of an unexponential dot in the beggining of each tweet.

    8. Drop the tweet's that do not include any words after processing.
	
	
