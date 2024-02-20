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
from nltk import word_tokenize, sent_tokenize
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
words = pd.read_csv(config['data_paths']['data_paths_vocabulary'])

#plt.title('Trump Test word frequency 200-300', fontsize=20)
#input_numb = '{}-{}'.format(start,end)
#The word frequency plots for Trump Test Dataset
def word_distribution(input,input_head,start,end):
    with open(config['data_paths'][input], encoding='utf-8') as infile:
        word_token_text = ''
        #This plots the 1st  to 100th most common words
        word_token_text = infile.read()
        counter1 = (Counter(word_token_text.split()).most_common()[start:end])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.rcParams.update({'font.size': 8})
        ax.tick_params(axis='x', labelsize=8)
        plt.xticks(rotation='vertical')
        plt.title('{} word frequency {}-{}'.format(input_head,start,end), fontsize=20)
        plt.xlabel('Words', fontsize=12)
        plt.ylabel('frequency', fontsize=12)
        list_keys1 = [x[0] for x in counter1]
        for k in range(0, len(list_keys1)):
            if list_keys1[k] not in words.word.tolist():
                list_keys1[k] = '{} <unk>'.format(list_keys1[k])
        list_values1 = [x[1] for x in counter1]

        values = set(map(lambda x: x[1], counter1))
        plt.bar(list_keys1, list_values1)
        for a, b in zip(list_keys1, list_values1):
                plt.text(a, b, str(b))
        plt.show()
input = ['data_paths_Trump_Test','data_paths_Trump_Train','data_paths_Obama_Test','data_paths_Obama_Train','data_paths_TheEllenShow_Test','data_paths_TheEllenShow_Train',
         'data_paths_Wiki_Valid','data_paths_Wiki_Test','data_paths_Wiki_Train']
input_head = ['Trump Test','Trump_Train','Obama_Test','Obama_Train','TheEllenShow_Test','TheEllenShow_Train','Wiki_Valid','Wiki_Test','Wiki_Train']
start = [0,100,200,300,400,500]
index = 0
for input in input:
    for i in range(0,len(start)-1):
        mystart = start[i]
        myend = start [i+1]
        word_distribution(input, input_head[index], mystart, myend)
    index += 1
