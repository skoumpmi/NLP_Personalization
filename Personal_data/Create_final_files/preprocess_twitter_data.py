from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re


num_words={}

for file_name in ['TheEllenshow', "Obama", "Trump"]:
    num_words[file_name] = 0
    with open(os.path.join(os.getcwd(), 'data', file_name + '.csv'), encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            words = re.findall(r"['’]*[\w]+|[.,!?;]", line.lstrip('\".').rstrip('\"'))
            if len(words) > 2:
                num_words[file_name]+= len(words)
max_words = max([num_words[file_name] for file_name in ['TheEllenshow', "Obama", "Trump"]])
min_words = min([num_words[file_name] for file_name in ['TheEllenshow', "Obama", "Trump"]])
lines_added = []
if min_words == num_words["Obama"]:
    min_words_excl_Obama = min([num_words[file_name] for file_name in ['TheEllenshow', "Trump"]])
    extra_Obama_words = 0
    with open(os.path.join(os.getcwd(), 'data', 'Obama_speeches.csv'), encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            words = re.findall(r"['’]*[\w]+|[.,!?;]", line.lstrip('\".').rstrip('\"'))
            if len(words) > 2:
                extra_Obama_words+= len(words)
                lines_added.append(line)
                if num_words["Obama"] + extra_Obama_words >= min_words_excl_Obama:
                    break
    min_words = min([num_words[file_name] for file_name in ['TheEllenshow', "Trump"]]+[num_words["Obama"]+extra_Obama_words])
num_train_words = int(min_words*0.9)
num_test_words = int(min_words*0.1)
for file_name in ['TheEllenshow', "Obama", "Trump"]:
    test_lines = []
    num_words = 0
    with open(os.path.join(os.getcwd(), 'data', file_name + '.csv'), encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            words = re.findall(r"['’]*[\w]+|[.,!?;]", line.lstrip('\".').rstrip('\"'))
            if len(words) > 2:
                test_lines.append(line)
                num_words+= len(words)
                if num_words >= num_test_words:
                    with open(os.path.join(os.getcwd(), 'data', file_name + '_test.txt'), "w", encoding="utf8") as file:
                        file.writelines(test_lines)
                    break
    train_lines = []
    num_words = 0
    with open(os.path.join(os.getcwd(), 'data', file_name + '.csv'), encoding="utf8") as file:
        lines = file.readlines()
        for line in lines:
            words = re.findall(r"['’]*[\w]+|[.,!?;]", line.lstrip('\".').rstrip('\"'))
            if len(words) > 2:
                train_lines.append(line)
                num_words += len(words)
                if num_words >= num_train_words:
                    with open(os.path.join(os.getcwd(), 'data', file_name + '_train.txt'), "w", encoding="utf8") as file:
                        file.writelines(train_lines)
                    break
    if file_name == "Obama":
        train_lines = train_lines + lines_added
        with open(os.path.join(os.getcwd(), 'data', file_name + '_train.txt'), "w", encoding="utf8") as file:
            file.writelines(train_lines)
