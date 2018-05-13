import wget
import pandas as pd
import re
from collections import Counter
import statistics
import numpy as np

def download_data(path, output_dir='./data'):
    filename = wget.download(path, output_dir)
    return filename

def load_data(file_path, header=False, sep=None, usecols=None):
    if header:
        header = 0
    else:
        header = None
    return pd.read_csv(file_path, sep=sep, header=header, usecols=usecols, engine='python')

def get_unique_chars(data_list):
    return sorted(list(set(''.join(data_list))))

def get_char_presence(data_list):
    output = {}
    unique_chars = get_unique_chars(data_list)
    print("Number of sentences containing each char is,")
    for c in unique_chars:
        try:
            filtered_data = filter_data(data_list, "(.*)["+c+"](.*)")
        except:
            filtered_data = filter_data(data_list, "(.*)[\\"+c+"](.*)")
        output[c] = len(filtered_data)
    print(output)
    

def filter_data(data_list, regex):
    r = re.compile(regex)
    return list(filter(r.match, data_list))

def clean_data(data_list, regex, pad_chars):
    # filter sentences which match the regex
    data_list = filter_data(data_list, regex)
    
    # more than one dot to 3 dots, special case... human
    data_list = [re.sub('\.(\.)+', " threedots ", item) for item in data_list]
    
    # special rules to deal with full-stop and '
    data_list = [re.sub(r"([a-zA-Z])(')([^a-zA-Z]|$)", r'\1 \2 \3', item) for item in data_list]
    data_list = [re.sub(r"(^|[^a-zA-Z])(')([a-zA-Z])", r'\1 \2 \3', item) for item in data_list]
    data_list = [re.sub(r"([a-zA-Z])(\.)([^a-zA-Z]|$)", r'\1 \2 \3', item) for item in data_list]
    data_list = [re.sub(r"(^|[^a-zA-Z])(\.)([a-zA-Z])", r'\1 \2 \3', item) for item in data_list]
    
    # multiple repetitions to single
    for c in pad_chars:
        data_list = [re.sub("(\\"+c+")+", ' ' + c + ' ', item) for item in data_list]
    data_list = [re.sub('\\\\', ' ', item) for item in data_list]
    
    # multiple whitespaces to single whitespace
    data_list = [re.sub('\s+', ' ', item) for item in data_list]
    data_list = [item.lower().strip() for item in data_list]
    return data_list

def get_len_stats(data_list):
    lens = [len(item) for item in data_list]
    print("min of length: ", min(lens))
    print("max of length: ", max(lens))
    print("average length: ", statistics.mean(lens))
    print("mode of length: ", statistics.mode(lens))

def tokenize(data_list):
    return [item.split(' ') for item in data_list]

def filter_data_on_length(tokenized_dataL, min_length, max_length):
    return [item for item in tokenized_dataL if len(item) >= min_length and len(item) <= max_length]

def get_vocabulary(data_list):
    word_counter = {}
    for item in data_list:
        tokens = item
        for token in tokens:
            if token in word_counter:
                word_counter[token] = word_counter[token] + 1
            else:
                word_counter[token] = 1
    return word_counter

def get_vocabulary_stats(word_freqs):
    print("Total vocabulary: ", len(word_freqs))
    freqs = [v for k, v in word_freqs.items()]
    print("average of frequency: ", statistics.mean(freqs))
    print("mode of frequency: ", statistics.mode(freqs))

def filter_words(word_freqs, min_freq):
    return [k for k, v in word_freqs.items() if v >= min_freq]

def contains_valid_words(sentence_tokens, words):
    for token in sentence_tokens:
        if token not in words:
            return False
    return True

def get_sentences_with_words(tokenized_data, words):
    words = set(words)
    return [item for item in tokenized_data if contains_valid_words(item, words)]
    