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
import pandas as pd
from nltk import word_tokenize,sent_tokenize
import string
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import pickle
import nltk
from itertools import groupby
import sys
import io
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

word_token_text = ''
words = pd.read_csv(config['data_paths']['data_paths_vocabulary'])
nb_words=0
sent_text=[]
g= open("All_datasets_results.txt","w+")
pct_id_words = []
pct_ood_words = []
pct_id_unique_words = []
pct_ood_unique_words = []
nb_id_words = []
nb_ood_words = []
nb_uniq_id_words = []
nb_uniq_ood_words = []
def make_word_dist(input_data,headline,output_data):
    word_token_text = ''
    nb_words = 0
    sent_text = []
    with open(config['data_paths'][input_data],encoding= 'utf-8') as infile:
        g.write(headline)
        word_token_text = infile.read()
        nb_words += len(word_token_text.split())
        unique = (len(Counter(word_token_text.split())))
        k2 = [k for k, v in dict(Counter(word_token_text.split())).items()]
        cnt_unq = 0
        cnt_words = 0
        # Count how much words of text belongs to dictionary and how much unique words belongs to dictionary
        for i in range(0, len(words)):
            if words.word[i] in k2:
                cnt_unq += Counter(word_token_text.split())[words.word[i]]
                cnt_words += 1
        g.write('The length of text in words is: {} \n'.format(nb_words))
        g.write('The number of words which belong to dictionary are: {} \n'.format(cnt_unq))
        nb_id_words.append(cnt_unq)
        pct_id_words.append(round(cnt_unq / nb_words, 2))
        g.write('The number of words which do not belong to dictionary are: {} \n'.format(nb_words - cnt_unq))
        nb_ood_words.append(nb_words - cnt_unq)
        pct_ood_words.append(round(((nb_words - cnt_unq) / nb_words), 2))
        g.write('The number of unique words  are: {} \n'.format(unique))
        g.write('The number of unique words which belong to dictionary are: {} \n'.format(cnt_words))
        nb_uniq_id_words.append(cnt_words)
        pct_id_unique_words.append(round(cnt_words / unique, 2))
        g.write('The number of unique words which do not belong to dictionary are: {} \n'.format(unique - cnt_words))
        nb_uniq_ood_words.append(unique - cnt_words)
        pct_ood_unique_words.append(round(((unique - cnt_words) / unique), 2))
        sent_text += (sent_tokenize(word_token_text))
        cnt_sent = 0
        sent_text_new = []
        for i in range(0, len(sent_text)):
            if ((sent_text[i].translate(str.maketrans(' ', ' ', string.punctuation)))) != '':
                sent_text_new.append((sent_text[i].translate(str.maketrans(' ', ' ', string.punctuation))))
        g.write('The number of sentences is: {} \n'.format(len(sent_text_new)))
        for i in range(0, len(sent_text_new)):
            cnt_sent += len(sent_text_new[i].split())

        g.write('The average length of sentence in words is: {} \n'.format(round(cnt_sent / len(sent_text_new), 3)))
        str_results = ''
        word_list = words.word.tolist()

        cnt_sent = 0
        for i in range(0, len(sent_text_new)):
            for j in range(0, len(sent_text_new[i].split())):
                if sent_text_new[i].split()[j] in word_list:
                    cnt_sent += 1
            if (len(sent_text_new[i].split()) != 0):
                known_avg = round(cnt_sent / len(sent_text_new[i].split()), 2)
            else:
                known_avg = 0
            str_results += ' ' + str(known_avg)
            cnt_sent = 0
        counter = Counter(str_results.split())
        list = (sorted(counter.items()))
        list_keys = [x[0] for x in list]
        list_values = [x[1] for x in list]
        cumulative = np.cumsum(list_values)
        list_keys_num = [float(i) for i in list_keys]
        dist_db = pd.DataFrame({'keys': list_keys_num, 'values': list_values})
        df = pd.DataFrame(columns=["Interval", "Sentences"])
        z = dist_db.loc[(dist_db['keys'] == 0.0), 'values'].sum()
        df = df.append({
            "Interval": 0.0,
            "Sentences": round(z / len(sent_text_new), 3) if len(sent_text_new) != 0 else 0
        }, ignore_index=True)
        intervals = [0.0, 0.1, 0.2, 0.3,0.4, 0.5, 0.6, 0.7,0.8, 0.9,1.0]
        for i in range (0, len(intervals)-1):
            if i == 0:
                z = dist_db.loc[
                    (dist_db['keys'] >= intervals[i]) & (dist_db['keys'] <= intervals[i + 1]), 'values'].sum()
                df = df.append({
                    "Interval": intervals [i+1],
                    "Sentences": round(z / len(sent_text_new), 3)
                }, ignore_index=True)
            else :
                z = dist_db.loc[(dist_db['keys'] <= intervals[i + 1]), 'values'].sum()
                df = df.append({
                    "Interval": intervals[i + 1],
                    "Sentences": round(z / len(sent_text_new), 3)
                }, ignore_index=True)
        df.to_csv(output_data)
input = ['data_paths_Trump_Test','data_paths_Trump_Train','data_paths_Obama_Test','data_paths_Obama_Train','data_paths_TheEllenShow_Test','data_paths_TheEllenShow_Train',
         'data_paths_Wiki_Valid','data_paths_Wiki_Test','data_paths_Wiki_Train']
output = ['Trump Test.csv','Trump Train.csv','Obama Test.csv','Obama Train.csv','TheEllenShow Test.csv','TheEllenShow Train.csv','Wiki Valid.csv','Wiki Test.csv','Wiki Train.csv']
headline = ['\n Trump Test Results are: \n','\n Trump Train Results are: \n','\n Obama Test Results are: \n','\n Obama Train Results are: \n','\n TheEllenShow Test Results are: \n',
            '\n TheEllenShow Train Results are: \n','\n Wiki Valid Results are: \n','\n Wiki Test Results are: \n','\n Wiki Train Results are: \n']
for i in range (0, len(input)):
    make_word_dist(input [i], headline[i], output[i])
dict = {'pct_id_words': pct_id_words, 'pct_ood_words': pct_ood_words, 'pct_id_unique_words': pct_id_unique_words,
            'pct_ood_unique_words': pct_ood_unique_words, 'nb_id_words': nb_id_words, 'nb_ood_words': nb_ood_words,
            'nb_uniq_id_words': nb_uniq_id_words, 'nb_uniq_ood_words': nb_uniq_ood_words}
df = pd.DataFrame(dict)
df.to_csv('all_dataset_pcntgs.csv')
data_trump_test = pd.read_csv('Trump Test.csv',index_col=0)
data_trump_test = pd.DataFrame(data = data_trump_test).rename(columns={"Sentences": "Trump_Test","Interval":"Interval1"}).round(3)
data_trump_train= pd.read_csv('Trump Train.csv',index_col=0)
data_trump_train = pd.DataFrame(data = data_trump_train).rename(columns={"Sentences": "Trump_Train","Interval":"Interval1"}).round(3)
data_the_ellen_Train = pd.read_csv('TheEllenShow Train.csv',index_col=0)
data_the_ellen_Train = pd.DataFrame(data = data_the_ellen_Train).rename(columns={"Sentences": "Ellen_Train"}).round(3)
data_the_ellen_Test = pd.read_csv('TheEllenShow Test.csv',index_col=0)
data_the_ellen_Test = pd.DataFrame(data = data_the_ellen_Test).rename(columns={"Sentences": "Ellen_Test"}).round(3)
data_Obama_train= pd.read_csv('Obama Train.csv',index_col=0)
data_Obama_train = pd.DataFrame(data = data_Obama_train).rename(columns={"Sentences": "Obama_Train","Interval":"Interval1"}).round(3)
data_Obama_test = pd.read_csv('Obama Test.csv',index_col=0)
data_Obama_test = pd.DataFrame(data = data_Obama_test).rename(columns={"Sentences": "Obama_Test"}).round(3)
data_wiki_valid = pd.read_csv('Wiki Valid.csv',index_col=0)
data_wiki_valid = pd.DataFrame(data = data_wiki_valid).rename(columns={"Sentences": "Wiki_Valid"}).round(3)
data_wiki_test = pd.read_csv('Wiki Test.csv',index_col= 0)
data_wiki_test = pd.DataFrame(data = data_wiki_test).rename(columns={"Sentences": "Wiki_Test"}).round(3)
data_wiki_train = pd.read_csv('Wiki Train.csv',index_col= 0)
data_wiki_train = pd.DataFrame(data = data_wiki_train).rename(columns={"Sentences": "Wiki_Train"}).round(3)
frames=[data_trump_test.transpose(),data_trump_train.transpose(),data_Obama_train.transpose(),data_Obama_test.transpose(),data_the_ellen_Train.transpose(),
        data_the_ellen_Test.transpose(),data_Obama_train.transpose(),data_Obama_test.transpose(),data_wiki_valid.transpose(),data_wiki_test.transpose(),data_wiki_train.transpose()]
dataset=(pd.concat(frames)).transpose()
prctgs = df.copy()
#pcntgs = pd.read_csv('all_dataset_pcntgs.csv',index_col=0)
#Plot the percentage of total number of words
fig = plt.figure()
ax = fig.add_subplot(111)
N = 9
known_words = pcntgs.pct_id_words.values.tolist()
unknown_words = pcntgs.pct_ood_words.values.tolist()
df = pd.DataFrame({'known_words':known_words,'unknown_words':unknown_words})
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence
p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)
for colNum,col in df.iterrows():
    xpos = 0
    for val in col:
        xpos += val
        plt.text(x= colNum , y=xpos, s=str(val), color='black', size=18)
    xpos = 0
plt.rcParams.update({'font.size': 12})
ax.tick_params(axis='x', labelsize=12)
plt.ylabel('Percentage of total number of  Words')
plt.title('Percentage of total number of words by dataset and by categories known-unknown words')
plt.xticks (ind,('Trump Train', 'Trump Test', 'Obama Train', 'Obama Test', 'Ellen Train', 'Ellen Test', 'Wiki Valid' , 'Wiki test','Wiki train'))
plt.yticks(np.arange(0, 1.2, 0.1),rotation='horizontal')
plt.legend((p1[0], p2[0]), ('Percentage of Total known words', 'Percentage of Total unknown words'))
plt.show()
#Plot the percentage of unique words
N = 9
known_words = pcntgs.pct_id_unique_words.values.tolist()
unknown_words = pcntgs.pct_ood_unique_words.values.tolist()
df = pd.DataFrame({'known_words':known_words,'unknown_words':unknown_words})
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)
for colNum,col in df.iterrows():
    xpos = 0
    for val in col:
        xpos += val
        plt.text(x= colNum , y=xpos, s=str(val), color='black', size=18)
    xpos = 0
plt.rcParams.update({'font.size': 12})
ax.tick_params(axis='x', labelsize=12)
plt.ylabel('Percentage of unique number of  Words')
plt.title('Percentage of unique words by dataset and by categories known-unknown words')
plt.xticks (ind, ('Trump Train', 'Trump Test', 'Obama Train', 'Obama Test', 'Ellen Train', 'Ellen Test', 'Wiki Valid' , 'Wiki test','Wiki train'))
plt.yticks(np.arange(0, 1.2, 0.1),rotation='horizontal')
plt.legend((p1[0], p2[0]), (' Percentage of known unique words', ' Percentage of unknown unique words'))
plt.show()
#Plot the frequency values of total number of  words
fig = plt.figure()
ax = fig.add_subplot(111)
N = 9
known_words = pcntgs.nb_id_words.values.tolist()
unknown_words = pcntgs.nb_ood_words.values.tolist()
df = pd.DataFrame({'known_words':known_words,'unknown_words':unknown_words})
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)
for colNum,col in df.iterrows():
    xpos = 0
    for val in col:
        xpos += val
        plt.text(x= colNum , y=xpos, s=str(val), color='black', size=18)
    xpos = 0

plt.rcParams.update({'font.size': 12})
ax.tick_params(axis='x', labelsize=12)
plt.ylabel('Nb of  Words')
plt.title('Frequency of total number of words by dataset and by categories known-unknown words')
plt.xticks (ind, ('Trump Train', 'Trump Test', 'Obama Train', 'Obama Test', 'Ellen Train', 'Ellen Test', 'Wiki Valid' , 'Wiki test','Wiki train'))
plt.yticks(np.arange(0, 500000, 10000),rotation='horizontal')
plt.legend((p1[0], p2[0]), (' Total known  words', ' Total unknown words'))
plt.show()
#Plot the frequency values of total number of unique words
N = 9
known_words = pcntgs.nb_uniq_id_words.values.tolist()
unknown_words = pcntgs.nb_uniq_ood_words.values.tolist()
df = pd.DataFrame({'known_words':known_words,'unknown_words':unknown_words})
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, df.known_words, width)
p2 = plt.bar(ind, df.unknown_words, width,
             bottom=known_words)
for colNum,col in df.iterrows():
    xpos = 0
    for val in col:
        xpos += val
        plt.text(x= colNum , y=xpos, s=str(val), color='black', size=18)
    xpos = 0

plt.rcParams.update({'font.size': 12})
ax.tick_params(axis='x', labelsize=12)
plt.ylabel('Nb of unique  Words')
plt.title('Frequency of total number of words by dataset and by categories known-unknown words')
plt.xticks (ind, ('Trump Train', 'Trump Test', 'Obama Train', 'Obama Test', 'Ellen Train', 'Ellen Test', 'Wiki Valid' , 'Wiki test','Wiki train'))
plt.yticks(np.arange(0, 100000, 10000),rotation='horizontal')
plt.legend((p1[0], p2[0]), (' Total Unique known  words', ' Total Unique unknown words'))
plt.show()
#Plot the cumulative distribution of unknown words per test dataset
dataset= pd.read_csv('all_dataset.csv',index_col=0)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.rcParams.update({'font.size': 20})
plt.xticks(np.arange(0.0, 1.0+0.1, 0.1), fontsize=16)
plt.yticks( fontsize=16)
plt.title('All Test Comparisons', fontsize=20)
plt.xlabel('cumulative Known word percentage in relation with all sentences', fontsize=18)
plt.ylabel('Sentence percentage in words of each known-unknown words ratio', fontsize=18)
x=dataset["Interval1"].values.tolist()
y=dataset["Trump_Test"].round(3).values.tolist()
z=dataset["Obama_Test"].round(3).values.tolist()
d=dataset["Ellen_Test"].round(3).values.tolist()
e=dataset["Wiki_Valid"].round(3).values.tolist()
f=dataset["Wiki_Test"].round(3).values.tolist()

plt.plot(x,y,label="Trump Test",c='blue')
plt.plot(x,z,label="Obama Test",c='orange')
plt.plot(x,d,label="TheEllen Show Test",c='red')
plt.plot(x,e,label="Wiki Valid",c='green')
plt.plot(x,f,label="Wiki Test",c='grey')

plt.legend(bbox_to_anchor=(0, 1), loc='upper left',fontsize=12, borderaxespad=0., prop={'size': 20})
plot_test_list = [y,z,d,e,f]
for item in plot_test_list:
    for a,b in zip(x, item):
        if a > 0.7:
            plt.text(a, b, str(b))
plt.show()
#Plot the cumulative distribution of unknown words per train dataset
fig = plt.figure()
ax = fig.add_subplot(111)
plt.rcParams.update({'font.size': 20})
plt.xticks(np.arange(0.0, 1.0+0.1, 0.1), fontsize=16)
plt.yticks( fontsize=16)
plt.title('All Train Comparisons', fontsize=20)
plt.xlabel('cumulative Known word percentage in relation with all sentences', fontsize=18)
plt.ylabel('Sentence percentage in words of each known-unknown words ratio', fontsize=18)
x=dataset["Interval1"].values.tolist()
g=dataset["Trump_Train"].round(3).values.tolist()
h=dataset["Obama_Train"].round(3).values.tolist()
m=dataset["Ellen_Train"].round(3).values.tolist()
n=dataset["Wiki_Train"].round(3).values.tolist()
plt.plot(x,g,label="TrumpTrain",c='pink')
plt.plot(x,h,label="ObamaTrain",c='brown')
plt.plot(x,m,label="TheEllenShowTrain",c='cyan')
plt.plot(x,n,label="WikiTrain",c='black')
plt.legend(bbox_to_anchor=(0, 1), loc='upper left',fontsize=12, borderaxespad=0., prop={'size': 20})
plot_train_list = [g,h,m,n]
for item in plot_train_list:
    for a,b in zip(x, item):
        if a > 0.7:
            plt.text(a, b, str(b))
plt.show()
