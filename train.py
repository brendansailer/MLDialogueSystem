import csv
import re
import random
import numpy as np
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
import tensorflow as tf

from model import MLModel

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

# Teacher Force
def teacher_force(context, answer, question):
    context_new, answer_new, question_new, next_word = [], [], [], []
    for cont, answ, ques in zip(context, answer, question):
        answ = answ.rstrip().split(' ') # Split the answer into words so we can index them.  Remove any trailing spaces as well
        for i in range(1, len(answ)-1):
            context_new.append(cont)
            question_new.append(ques)
            answer_new.append(' '.join(answ[:i])) # This is the first part of the answer.  Join the individual words back to form a sentence
            next_word.append(answ[i:i+1][0])  # This is the next predicted word

    return context_new, answer_new, question_new, next_word

# Tokenize the data
def tokenize(tokenizer, train, val, test):
    train = tokenizer.texts_to_sequences(train)
    val   = tokenizer.texts_to_sequences(val)
    test  = tokenizer.texts_to_sequences(test)

    return [train, val, test]

# Pad the data
def pad_data(text_maxlen, train, val, test):
    train = pad_sequences(train, padding="post", truncating="post", maxlen=text_maxlen)
    val   = pad_sequences(val, padding="post", truncating="post", maxlen=text_maxlen)
    test  = pad_sequences(test, padding="post", truncating="post", maxlen=text_maxlen)

    return [train, val, test]

# Create the tokenizer and save it as a file in the /toks directory
def create_tokenizer(training_data, vocab_size, filename):
    tokenizer = Tokenizer(lower=False, num_words=vocab_size, oov_token="UNK", split=' ', filters="") # Don't split the start token <s>
    tokenizer.fit_on_texts(training_data)

    tokenizer_json = tokenizer.to_json()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(tokenizer_json)

    return tokenizer

def pad_next_word(tokenizer, next_words, vocab_size):
    train_next_word = answer_tok.texts_to_sequences(next_words) # Tokenize the words so that we have the word index for the next line below
    padded_next_words = to_categorical(train_next_word, num_classes=vocab_size) # num_classes tells to_categorical to make the vector 1000 long
    return padded_next_words

if __name__ == "__main__":
    ques_vocabsize = 500
    cont_vocabsize = 500
    answ_vocabsize = 500

    context  = read_data('data/contexts.txt')
    answer   = read_data('data/answers.txt')
    question = read_data('data/questions.txt')
    
    line_count = len(question)
    print("The training data has " + str(line_count) + " rows.")

    train_context, val_context, test_context    = data_split(context, line_count)
    train_answer, val_answer, test_answer       = data_split(answer, line_count)
    train_question, val_question, test_question = data_split(question, line_count)

    # Use the tokenizer fit_on_texts before we teacher force (manipulate the data)
    context_tok  = create_tokenizer(train_context, cont_vocabsize, 'toks/context_tok.json')
    answer_tok   = create_tokenizer(train_answer, answ_vocabsize, 'toks/answer_tok.json') # TODO - use smaller vocab size on the answers b/c it'll work better to have less 0's
    question_tok = create_tokenizer(train_question, ques_vocabsize, 'toks/question_tok.json')

    # Use teacher forcing on the data.  We need to teacher force the train, val, and test separately after the data_split above
    train_context, train_answer, train_question, train_next_word = teacher_force(train_context, train_answer, train_question)
    val_context, val_answer, val_question, val_next_word         = teacher_force(val_context, val_answer, val_question)
    test_context, test_answer, test_question, test_next_word     = teacher_force(test_context, test_answer, test_question)
    
    # Always use the answer_tok to tokenize the next_word list. This will take next_words of size 1 and turn them into size answ_vocabsize (500) which have a single 1 and 999 0's
    train_next_word = pad_next_word(answer_tok, train_next_word, answ_vocabsize)
    val_next_word   = pad_next_word(answer_tok, val_next_word, answ_vocabsize)
    test_next_word  = pad_next_word(answer_tok, test_next_word, answ_vocabsize)

    # Tokenize and pad in the same line for cleaner code
    train_context, val_context, test_context    = pad_data(30, *tokenize(context_tok, train_context, val_context, test_context))
    train_answer, val_answer, test_answer       = pad_data(10, *tokenize(answer_tok, train_answer, val_answer, test_answer))
    train_question, val_question, test_question = pad_data(20, *tokenize(question_tok, train_question, val_question, test_question))

    model = MLModel(ques_vocabsize, cont_vocabsize, answ_vocabsize).get_model()

    K.set_value(model.optimizer.learning_rate, 0.001)

    batch_size  = 70 # May update for more data # TODO - check if the order of arguments is wrong
    history = model.fit(x=[train_question, train_answer, train_context], y=np.asarray(train_next_word), batch_size=batch_size, epochs=5, verbose=1, validation_data=([val_question, val_answer, val_context], val_next_word))
    model.save('qa_g_lstm.h5') # Save the model after training
