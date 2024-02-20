This script splits the cleared twitter data into train and test files. Because Obama had less twitter data compared to Ellen and Trump, we enhanched his dataset with text retrieved from his speeches. The speeches can be downloaded from https://github.com/samim23/obama-rnn/blob/master/input.txt.

To run the script, place each twitter user's data into a file named [user_name].csv and Obama's speeches into a file named Obama_speeches.csv and then run "python preprocess_twitter_data.py"
