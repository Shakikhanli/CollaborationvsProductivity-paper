"""
This file is for creating word2vec model according to the created file structures.
"""

import gensim
import logging
import glob, os
import platform

os.chdir("File Structures")  # You should add new location for files.
count = 0
sentences = []
last = []


def sentence_formatter(line):
    line = line.replace("/", " ")
    line = line.replace(".", "")
    line = line.replace("_", "")
    line = line.replace("-", "")
    # print(line.split())
    return line.split()


#This function is for parsing sentences of file and collect them in a list
def sentence_parser(text):
    sentence_list = []
    for each_sentence in text:
        sentence_list = sentence_list + sentence_formatter(each_sentence)
    return sentence_list


for file in glob.glob("*.txt"):
    count += 1
    f = open(file, "r", encoding="utf-8")
    contents = f.read().splitlines()
    sentences.append(sentence_parser(contents))
    print('Files left: ' + str(len(glob.glob("*.txt")) - count))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print('Sentences count' + str(len(sentences)))

print('Count: ' + str(count))

model = gensim.models.Word2Vec(sentences, min_count=2, size=300)
model.save("ModelMatched2.word2vec")