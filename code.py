# Import Module
import os
import re
from nltk import word_tokenize
import pandas as pd

# Read text file
def create_text(file_path):
    file_object = open(file_path, 'r')
    
    return file_object.read()

# Create word token of text
def create_word_token(file_text):
    word = re.sub('[^a-z]',' ', file_text.lower())
    tokenize_word = word_tokenize(word)

    return tokenize_word

# Remove exclude word by using exclude word dictionary
def remove_exclude_word_by_file(tokenize_word, exclude_word):
    clean_word = list()
    
    for word in tokenize_word:
        if word not in exclude_word:
            clean_word.append(word)
    
    return clean_word

# Read file path
file_path = "Raw_Data/"

# Read files from the path
file_list = os.listdir(file_path)

# Read exclude word
exclude_word = pd.read_csv("exclude-words.txt")

# Create dictionary
word_dict = dict()

for index, file_name in enumerate(file_list):
    # Check file is text
    if file_name.endswith(".txt"):
        file_text = create_text(os.getcwd()+"/"+file_path+file_name)
        tokenize_word = create_word_token(file_text)
        clean_word = remove_exclude_word_by_file(tokenize_word, exclude_word)
        
        for word in clean_word:
            if word in word_dict.keys():
                if word_dict[word][-1] != index+1:
                    word_dict[word].append(index+1)
            else:
                word_dict[word] = [index+1]

# Sort dictionary
word_dict = dict(sorted(word_dict.items()))

#Create file
with open("index.txt", "w") as output_file:
    output_file.write("Word : Page Numbers"+"\n")
    output_file.write("-------------------"+"\n")
    for word in word_dict:
        output_file.write(word+" : "+','.join(map(str,word_dict[word]))+"\n")
output_file.close()