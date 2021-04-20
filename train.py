import csv
import re
import random
import numpy as np
from keras.preprocessing.text import Tokenizer

#from keras.preprocessing.sequence import pad_sequences
#from keras.utils import to_categorical
import tensorflow as tf
#from keras.models import Sequential
#from keras.layers import Activation, Dense, Dropout, LSTM, Embedding, Conv1D, Masking, Flatten

random.seed(1337)
np.random.seed(1337)
tf.random.set_seed(1337)

# Takes a file, preprocesses it, and returns every line in order
def read_data(file_path):
    dat = []
    with open(file_path, 'r') as file_handle:
        for row in file_handle:
            
            row = row.replace('\n', ' ')
            row = re.sub('[^0-9a-zA-Z</>]+', ' ', row)
            row = row.lower()
    
            dat.append(row)
    
    return dat

# Split the data into train, validation, and test
def data_split(data, line_count):
    trainlen = int(line_count * 0.80)
    vallen = int(line_count * 0.10)
    testlen = int(line_count * 0.10)

    traindat = data[:trainlen]
    valdat = data[trainlen:trainlen+vallen]
    testdat = data[trainlen+vallen:]

    return traindat, valdat, testdat

# Create the tokenizer and save it as a file in the /toks directory
def create_tokenizer(training_data, vocab_size, filename):
    tokenizer = Tokenizer(lower=False, num_words=vocab_size, oov_token="UNK")
    tokenizer.fit_on_texts(training_data)

    tokenizer_json = tokenizer.to_json()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(tokenizer_json)

    return tokenizer

if __name__ == "__main__":
    context  = read_data('data/contexts.txt')
    answer   = read_data('data/answers.txt')
    question = read_data('data/questions.txt')
    
    line_count = len(question)
    print("The training data has " + str(line_count) + " rows ")

    train_context, val_context, test_context    = data_split(context, line_count)
    train_answer, val_answer, test_answer       = data_split(answer, line_count)
    train_question, val_question, test_question = data_split(question, line_count)

    context_tok  = create_tokenizer(train_context, 1000, 'toks/context_tok.json')
    answer_tok   = create_tokenizer(train_answer, 1000, 'toks/answer_tok.json')
    question_tok = create_tokenizer(train_question, 1000, 'toks/question_tok.json')
