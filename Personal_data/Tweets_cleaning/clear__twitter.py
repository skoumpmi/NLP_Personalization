"""
Copyright 2020, Samsung Electronics Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================
"""
# -*- coding: utf-8 -*-
import sys
import string
import re
import numpy as np
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import pandas as pd
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

class TextPreprocessing:
    def __init__(self):
        print("TextPreprocessing")

    def clean_text(self, text):
        text = re.sub('[^.,\.‘’‐‑‑–—―''⁇⁈⁉!?a-zA-Z0-9 \n\.]', '', text)
        text = re.sub(r'\s([’](?:\s|$))', " '", text)
        text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
        text = re.sub(r":", " : ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"e - mail", "email", text)
        text = re.sub(r"j k", "jk", text)
        text = re.sub(r"\s{2,}", " ", text)

        return text

    def keep_punctuation(self, text):
        text = re.sub(r"\\xe2\\x80\\x90", "‐", text)
        text = re.sub(r"\\xe2\\x80\\x91", "‑", text)
        text = re.sub(r"\\xe2\\x80\\x92", "‑", text)
        text = re.sub(r"\\xe2\\x80\\x93", "–", text)
        text = re.sub(r"\\xe2\\x80\\x94", "—", text)
        text = re.sub(r"\\xe2\\x80\\x95", "―", text)
        text = re.sub(r"\\xe2\\x80\\x98", "‘", text)
        text = re.sub(r"\\xe2\\x80\\x99", "’", text)
        text = re.sub(r"\\xe2\\x80\\x9a", "''", text)
        text = re.sub(r"\\xe2\\x80\\x9b", "''", text)
        text = re.sub(r"\\xe2\\x80\\x9c", """ " """, text)
        text = re.sub(r"\\xe2\\x80\\x9d", """ " """, text)
        text = re.sub(r"\\xe2\\x80\\xb2", " , ", text)
        text = re.sub(r"\\xe2\\x80\\xb3", " "" ", text)
        text = re.sub(r"\\xe2\\x80\\xb4", " ''' ", text)
        text = re.sub(r"\\xe2\\x80\\xb5", " '' ", text)
        text = re.sub(r"\\xe2\\x80\\xb6", " ‶ ", text)
        text = re.sub(r"\\xe2\\x80\\xb7", " ‷ ", text)
        text = re.sub(r"\\xe2\\x81\\x87", " ⁇ ", text)
        text = re.sub(r"\\xe2\\x81\\x88", " ⁈ ", text)
        text = re.sub(r"\\xe2\\x81\\x89", " ⁉ ", text)
        return text
    def clear_urls(self, text):
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', " ", text)
        text = re.sub(r'(http(s)?://)?([\w-]+\.)+[\w-]+[.com]+(/[/?%&=]*)?', " ", text)
        return text
    def clean_emojis(self, text):
        text=text.replace('\\',' \\')
        text = word_tokenize(text)
        for j in range (0,len(text)):
            if (text[j][0]=='\\'):
                text[j]=text[j].replace(text[j],' ')

        text=TreebankWordDetokenizer().detokenize(text)
        text=re.sub(' +', ' ', text)
        return text

    #+''.join('.')
    def clean_hashtag_user(self,text):
            start_sent = sent_tokenize(text)[:-1]
            last_sent = (sent_tokenize(text))[-1].split()
            index = len(last_sent) - 1
            for j in range(index, -1, -1):
                if (last_sent[j][0] == '@' or last_sent[j][0] == '#' or last_sent[j][0:4] == 'http'):
                    last_sent.remove(last_sent[j])

                else:
                    break
                text = ' '.join(start_sent + last_sent)
            return text

    def clean_byte_character(self,text):
            text=((word_tokenize(text)[0]).replace(word_tokenize(text)[0][0], ''))+' '+' '.join(word_tokenize(text)[1:])
            return text


    def clean_initial_dot(self, text):
        if (len(word_tokenize(text))> 0 and word_tokenize(text)[0]=='.'):
            text = (word_tokenize(text)[0]).replace(word_tokenize(text)[0],'') + ' ' + ' '.join(word_tokenize(text)[1:])

        return text



#dt = pd.read_csv('samsung_dataset_without_retweets.csv', index_col=0)
FILENAME = sys.argv[1]
dt=  pd.read_csv(FILENAME,  index_col=0, error_bad_lines=False)
dt = pd.DataFrame(data=dt)
dt[sys.argv[4]]=dt.index
dt.index = pd.RangeIndex(len(dt))
obj=TextPreprocessing()
RT_list=[]
for i in range(0,len(dt)):


   for j in range(0,len(word_tokenize(dt[sys.argv[3]].iloc[i]))):
        if(dt[sys.argv[3]].iloc[i][j]=='RT' and dt[sys.argv[3]].iloc[i][j+1]=='@'):#and dt.tweet.iloc[i][j+2]==' 'and dt.tweet.iloc[i][j+3]=='@'):
            dt[sys.argv[3]].iloc[i]=dt[sys.argv[3]].iloc[i].replace("RT @",'')
            k=0
            text=dt[sys.argv[3]].iloc[i][j - 1]
            while(dt[sys.argv[3]].iloc[i][j+k])!=' ':
                text+='{}'.format( dt.sys.argv[3].iloc[i][j + k])
                k+=1
            dt[sys.argv[3]].iloc[i] = dt[sys.argv[3]].iloc[i].replace(text, '')
   dt[sys.argv[3]].iloc[i] = TextPreprocessing.clean_initial_dot (obj,TextPreprocessing.clean_byte_character(obj,TextPreprocessing.clean_text(obj,TextPreprocessing.clean_emojis(obj,TextPreprocessing.clear_urls (obj,TextPreprocessing.keep_punctuation(obj,TextPreprocessing.clean_hashtag_user(obj, dt[sys.argv[3]].iloc[i])))))))

   if(len(word_tokenize(dt[sys.argv[3]].iloc[i]))<=2 or dt[sys.argv[3]].iloc[i]== None):
            RT_list.append(i)
   if (len(sent_tokenize(dt[sys.argv[3]].iloc[i]))) !=0:

       if len(word_tokenize(sent_tokenize(dt[sys.argv[3]].iloc[i])[-1]))==2 and (dt[sys.argv[3]].iloc[i][-1]=='.'or dt[sys.argv[3]].iloc[i][-1]=='!' or dt[sys.argv[3]].iloc[i][-1]=='?'):


            dt[sys.argv[3]].iloc[i]= ' '.join(sent_tokenize(dt[sys.argv[3]].iloc[i])[:-1])
   for k in range(0, len(word_tokenize(dt.tweet.iloc[i]))):
        if (dt[sys.argv[3]].iloc[i][0] == 'RT' ):#and dt.tweet.iloc[i][j + 1] == '@'):
            dt[sys.argv[3]].iloc[i] = ' '.join(dt[sys.argv[3]].iloc[i][2:])

cols = dt.columns.tolist()
cols = cols[-1:] + cols[:-1]
dt = dt[cols]
dt[sys.argv[3]].replace('', np.nan, inplace=True)

for index in RT_list:
    dt = dt.drop(index=index)
dt = dt.reset_index(drop=True)

dt.to_csv(sys.argv[2])
