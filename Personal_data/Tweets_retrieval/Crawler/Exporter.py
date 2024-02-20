# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
import got3 as got
from nltk.tokenize import sent_tokenize, word_tokenize
from langdetect import detect

def main(argv):

    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        print (f.read())
        f.close()

        return

    try:
        opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output="))

        tweetCriteria = got.manager.TweetCriteria()
        outputFileName = "output_got_whole_processed_only_utf8_TEST.csv"

        for opt,arg in opts:
            if opt == '--username':
                tweetCriteria.username = arg

            elif opt == '--since':
                tweetCriteria.since = arg

            elif opt == '--until':
                tweetCriteria.until = arg

            elif opt == '--querysearch':
                tweetCriteria.querySearch = arg

            elif opt == '--toptweets':
                tweetCriteria.topTweets = True

            elif opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)
            
            elif opt == '--near':
                tweetCriteria.near = '"' + arg + '"'
            
            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--within':
                tweetCriteria.within = '"' + arg + '"'

            elif opt == '--output':
                outputFileName = arg
                
        outputFile = codecs.open(outputFileName, "w+", encoding='utf-8')
        outputFile.write('username,date,text')

      
        print('Searching...\n')

        def receiveBuffer(tweets):
            for t in tweets:
                outputFile.write(('\n%s,%s,"%s"' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.text))) #, t.initial_text

            outputFile.flush()
            print('More %d saved on file...\n' % len(tweets))

        got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

    # except arg:
    #     print('Arguments parser error, try -h' + arg)
    except Exception as e:
        print(str(e))
    finally:
        outputFile.close()
        print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
    main(sys.argv[1:])
