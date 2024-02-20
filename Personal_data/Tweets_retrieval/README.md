# Tweets retrieval
 
two methods for tweets retrieval were implemented:
1. using a profile crawler
2. via the Twitter API (provided for historical purposes)

The method selected for the NLP project for downloading tweets was the crawler, because it could provide a greater amount of tweets without restrictions.   
Twitter API has certain retrictions and can provide a certain amount of tweets for a specific period of time and thus it was not used for the collection of the final Twitter Dataset.  


## Method 1: Profile crawler*

The scripts implemented for the crawler are available in the "Crawler" folder.

For downloading tweets for a specific user by crawling on his/her profile, follow the steps below:
1. Enter into the "Crawler" folder.
2. Install the requirements by executing the following command
   ``` 
   pip install -r requirements.txt
   ```
3. For downloading tweet's for a specific user, by using his/her twitter username, and for a specific period of time, run the following command:
   ``` 
   python Exporter.py --username "BarackObama" --since 2015-09-10 --until 2020-04-27
   ```
   
   Parameter's explanation:
   
   * username : user's twitter username can be used in this parameter, defining the user from whom the crawler will receive data
   * since: since when you want to download tweets
   * until: till which date you want to download tweets
   
   
   
4. The tweets downloaded are already cleaned and in English. 

*The main core of the crawler has been retrieved from https://github.com/Jefferson-Henrique/GetOldTweets-python



## Method 2: Twitter API
Using this method, tweets will be downloaded using the Twitter API. 

Steps for downloading:
1. enter in the "Twitter API" folder
2. Receive consumer key and other parameters needed for the Twitter API **
3. Insert the parameters retrieved from step 2 in the "Twitter_api\configuration.ini" file
4. execute 
```
python getTweetsByUserId.py
```

Information about the users from whom tweets will be downloaded are available in the "Tweets_retrieval\Twitter_api\SampleData\twitterIds_dataset_famous.csv" file.
In this file, the first column corresponds to user's TwitterID and the second column to user's Twitter name. These columns can be modified in order to download tweets from other users also. 

If this method is selected, the tweets downloaded via Twitter API need to be cleaned using the "clear__twitter.py" file, available at "Personal-data\Tweets_cleaning" folder.  

**information are available in https://developer.twitter.com/en/docs/labs/sampled-stream/quick-start


