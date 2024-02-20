import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,json,re,datetime,sys,http.cookiejar
from .. import models
from pyquery import PyQuery
from nltk.tokenize import sent_tokenize, word_tokenize
from langdetect import detect

class TweetManager:
    
    def __init__(self):
        pass
        
    @staticmethod
    def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):
        refreshCursor = ''
    
        results = []
        resultsAux = []
        cookieJar = http.cookiejar.CookieJar()

        active = True

        while active:
            json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
            if len(json['items_html'].strip()) == 0:
                break

            refreshCursor = json['min_position']
            scrapedTweets = PyQuery(json['items_html'])
            #Remove incomplete tweets withheld by Twitter Guidelines
            scrapedTweets.remove('div.withheld-tweet')
            tweets = scrapedTweets('div.js-stream-tweet')
            
            if len(tweets) == 0:
                break
            
            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet = models.Tweet()
                
                usernameTweet = tweetPQ("span.username.js-action-profile-name b").text()
                txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text())
                txt = txt.replace('!', ' ! ').replace('…', '').replace('?', ' ? ').replace('@', ' @').replace(' @ ', ' @').replace('#', ' #').replace(' # ', ' #')
                #print(txt)
                print("detect")
                print(detect(txt))
                txt = re.sub(r"[^.,\.!?a-zA-Z0-9 \n\.]", "", txt)
                if(len(txt) == 0):
                    break
                elif (txt == "....") or (txt.startswith("...")):
                    break
                elif (txt == "3-0") or (txt == "$5"):
                    break
                elif (txt == "6.5") or (txt == "30%"):
                    break
                elif (txt == "7") or (txt == "35,000"):
                    break
                elif (txt == " !  ! ") or (txt == " ! "):
                    break
                if(txt[0:4] == "http"):
                    break
                elif (txt.startswith('pic.twitter')):
                    break
                elif (detect(txt) == 'en'):
                    txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
                    txt = txt.replace('!', ' ! ').replace('…', '').replace('?', ' ? ').replace('@', ' @').replace(' @ ', ' @').replace('#', ' #').replace(' # ', ' #')
                else:
                    break

                if (len(sent_tokenize(txt))>1):
                    start_sent = sent_tokenize(txt)[:-1]
                last_sent = (sent_tokenize(txt))[-1].split()
                for j in range(0,len(last_sent)):
                    # last_sent[j] = last_sent[j].replace('!', ' ! ').replace('?', ' ? ')
                    if (last_sent[j][0] == "@" or last_sent[j][0] == "#" ): #or last_sent[j][0:4] == "http"):
                        last_sent[j] = "<unk>"
                    if ("http" in last_sent[j]):
                        head, sep, tail = last_sent[j].partition('http')
                        last_sent[j] = head
                    if (last_sent[j].startswith('http')):
                        last_sent[j] = "<unk>"
                    if (last_sent[j].startswith('https')):
                        last_sent[j] = "<unk>"
                    if (last_sent[j].startswith('pic.twitter.com')):
                        last_sent[j] = "<unk>"
                    if ("pic.twitter.com" in last_sent[j]):
                        head, sep, tail = last_sent[j].partition('pic.twitter')
                        last_sent[j] = head

                        
                stopwords = ['<unk>', '@', '#', 'http', 'pic.twitter']
                last_sent = [word for word in last_sent if word not in stopwords[0]]
                if (len(sent_tokenize(txt))>1):
                    start_sent = [item.replace("!", " ! ") for item in start_sent]
                    # start_sent = start_sent.split()
                    start_sent = [s.replace('@', '') for s in start_sent] #[word for word in start_sent if word not in stopwords]
                    start_sent = [s.replace('#', '') for s in start_sent]
                    txt = " ".join(start_sent + last_sent)
                else:
                    txt = " ".join(last_sent)
                if(len(txt) == 0):
                    break
                txt = txt.encode('utf-8').decode('latin-1')
                txt = txt.encode('latin1').decode('utf8')
                if txt.find("\\") != -1:
                    txt = (re.sub(r"\\.+\\", " ", txt).replace(re.sub(r"\\.+\\", " ",\
                                 re.sub(r"\\.+\\", " ", txt.rsplit("\\", 1)[-1]).\
                                 rsplit("\\", 1)[-1]), " ")\
                                 + " ".join(re.sub(r"\\.+\\", " ",\
                                 txt.rsplit("\\", 1)[-1]).split()[1:]))
                txt = re.sub(r"(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b", " ", txt)
                txt = re.sub(r"(http(s)?://)?([\w-]+\.)+[\w-]+[.com]+(/[/?%&=]*)?", " ", txt)
                #Clean the special characters in  Twitter Text.
                # txt = re.sub(r"[^.,\.!?a-zA-Z0-9 \n\.]", "", txt)
                txt = re.sub(r"what's", "what is ", txt)
                # txt = re.sub(r"\"s", " ", txt)
                txt = re.sub(r"\'s", " 's ", txt)
                txt = re.sub(r"\’s", " ’s ", txt)
                txt = re.sub(r"\"ve", " have ", txt)
                txt = re.sub(r"n't", " not ", txt)
                txt = re.sub(r"i'm", "i am ", txt)
                txt = re.sub(r"I'm", "I am ", txt)
                txt = re.sub(r"\"'re", " are ", txt)
                txt = re.sub(r"’re", " are ", txt)
                txt = re.sub(r"\"d", " would ", txt)
                txt = re.sub(r"\"ll", " will ", txt)
                txt = re.sub(r",", " , ", txt)
                txt = re.sub(r"\. ", " . ", txt)
                txt = re.sub(r"\/", " ", txt)
                txt = re.sub(r"\&", "and", txt)
                txt = re.sub(r"\“", " “ ", txt)
                txt = re.sub(r"\”", " ” ", txt)
                txt = re.sub(r"\^", " ^ ", txt)
                txt = re.sub(r"\+", " + ", txt)
                txt = re.sub(r"\-", " - ", txt)
                txt = re.sub(r"\=", " = ", txt)
                txt = re.sub(r"\-", " - ", txt)
                # txt = re.sub(r"'", " ", txt)
                txt = re.sub(r"(\d+)(k)", r"\g<1>000", txt)
                txt = re.sub(r":", " : ", txt)
                # txt = re.sub(r" e g ", " eg ", txt)
                txt = re.sub(r" b g ", " bg ", txt)
                # txt = re.sub(r" u s ", " american ", txt)
                txt = re.sub(r"\0s", "0", txt)
                txt = re.sub(r" 9 11 ", "911", txt)
                txt = re.sub(r"\ … ", "", txt)
                txt = re.sub(r"\.", " . ", txt)
                txt = re.sub(r"e - mail", "email", txt)
                # txt = re.sub(r"j k", "jk", txt)
                txt = re.sub(r"\s{2,}", " ", txt)
                """Clean an unexpected dot in the beggining of Twitter Text."""
                if (len(word_tokenize(txt)) > 0
                        and word_tokenize(txt)[0] == "."):
                    txt = (word_tokenize(txt)[0]).replace(word_tokenize(txt)[0], "")\
                           + " " + " ".join(word_tokenize(txt)[1:])

                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
 
                tweet.username = usernameTweet
                #txt = txt.encode('utf-8').decode('latin-1')
                tweet.text = txt#.encode('latin1').decode('utf8')
                print(txt)
                print("\n")
                tweet.date = datetime.datetime.fromtimestamp(dateSec)
                tweet.formatted_date = datetime.datetime.fromtimestamp(dateSec).strftime("%a %b %d %X +0000 %Y")
                
                results.append(tweet)
                resultsAux.append(tweet)
                
                if receiveBuffer and len(resultsAux) >= bufferLength:
                    receiveBuffer(resultsAux)
                    resultsAux = []
                
                if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
                    active = False
                    break
                    
        
        if receiveBuffer and len(resultsAux) > 0:
            receiveBuffer(resultsAux)
        
        return results
    
    @staticmethod
    def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s"
        
        urlGetData = ''
        if hasattr(tweetCriteria, 'username'):
            urlGetData += ' from:' + tweetCriteria.username
            
        if hasattr(tweetCriteria, 'since'):
            urlGetData += ' since:' + tweetCriteria.since
            
        if hasattr(tweetCriteria, 'until'):
            urlGetData += ' until:' + tweetCriteria.until
            
        if hasattr(tweetCriteria, 'querySearch'):
            urlGetData += ' ' + tweetCriteria.querySearch
            
        if hasattr(tweetCriteria, 'lang'):
            urlLang = 'lang=' + tweetCriteria.lang + '&'
        else:
            urlLang = ''
        url = url % (urllib.parse.quote(urlGetData), urlLang, refreshCursor)
        #print(url)

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        if proxy:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}), urllib.request.HTTPCookieProcessor(cookieJar))
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookieJar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except:
            #print("Twitter weird response. Try to see on browser: ", url)
            print("Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" % urllib.parse.quote(urlGetData))
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit()
            return
        
        dataJson = json.loads(jsonResponse.decode())
        
        return dataJson        
