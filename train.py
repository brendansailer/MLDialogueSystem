import csv
import re
import random
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
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

    # Tokenize and pad in the same line for cleaner code
    train_context, val_context, test_context    = pad_data(50, *tokenize(context_tok, train_context, val_context, test_context))
    train_answer, val_answer, test_answer       = pad_data(50, *tokenize(answer_tok, train_answer, val_answer, test_answer))
    train_question, val_question, test_question = pad_data(50, *tokenize(question_tok, train_question, val_question, test_question))

    model = MLModel().get_model()
'''
K.set_value(model.optimizer.learning_rate, 0.001)

batch_size  = 70 # May update for more data
history = model.fit(Xtrain, Ytrain, batch_size=batch_size, epochs=19, verbose=1, validation_data=(Xval, Yval))

Ypred = model.predict(Xtest)

Ypred = np.argmax(Ypred, axis=1)
Ytest = np.argmax(Ytest, axis=1)

print(Ypred.shape)
print(Ypred)
print(Ytest)

from sklearn import metrics
#print(metrics.classification_report(Ytest, Ypred, target_names=categories)) # Use in deployment where there is an example of every cat in the test set
print(metrics.classification_report(Ytest, Ypred)) # Use in test when there aren't example for every cat in the test set

print(metrics.confusion_matrix(Ytest, Ypred).transpose())
'''