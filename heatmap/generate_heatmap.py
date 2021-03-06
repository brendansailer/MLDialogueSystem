import argparse
import re
import random
# Optional to get rid of annoying tf warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

import numpy as np
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from keras.models import load_model
import keras.backend as K

# This is a class which loads the tokenizes and model ONLY once, which speeds up subsequent predictions
class Predictor:
    def __init__(self, test):
        random.seed(1337)
        np.random.seed(1337)
        tf.random.set_seed(1337)

        model_file, context_file, answ_tok, ques_tok, cont_tok, context_size = self.get_paths(test)

        with open(answ_tok) as f:
            self.answer_tokenizer = tokenizer_from_json(f.read())
        with open(cont_tok) as f:
            self.context_tokenizer = tokenizer_from_json(f.read())
        with open(ques_tok) as f:
            self.question_tokenizer = tokenizer_from_json(f.read())

        self.model = load_model(model_file)

        self.context_file = context_file
        self.context_size = context_size

    def get_paths(self, test):
        if test == "simple":
            model = "heatmap/models/qa_g_lstm_context_increased_11_2.2.h5" # Simple context
            context = "data/contexts.txt"
            answ_tok = "heatmap/toks/answer_tok_2.2.json"
            ques_tok = "heatmap/toks/question_tok_2.2.json"
            cont_tok = "heatmap/toks/context_tok_2.2.json"
            context_size = 30

        elif test == "sentence":
            model = "heatmap/models/qa_g_lstm_context_increased_11_sentence2.2.h5" # Sentence context
            context = "data/contexts_sentence.txt"
            answ_tok = "toks/answer_tok.json"
            ques_tok = "toks/question_tok.json"
            cont_tok = "toks/context_tok_sentence.json"
            context_size = 40

        # Open to expansion of other models ...

        return model, context, answ_tok, ques_tok, cont_tok, context_size

    def make_prediction(self, question, name, line_num, stop, debug):
        question = re.sub('[^0-9a-zA-Z</>]+', ' ', question)
        question = question.lower()
        question = "<s> " + question + " </s>"

        answer = "<s>"

        context_line = ''
        with open(self.context_file) as f:
            for i, line in enumerate(f):
                if i == line_num:
                    context_line = line.strip()
                    context_line = re.sub('[^0-9a-zA-Z</>]+', ' ', context_line)
                    context_line = context_line.lower()
                elif i > line_num:
                    break

        tokenized_context  = self.context_tokenizer.texts_to_sequences([context_line])
        tokenized_question = self.question_tokenizer.texts_to_sequences([question])
        tokenized_answer   = self.answer_tokenizer.texts_to_sequences([answer])

        tokenized_context  = pad_sequences(tokenized_context, padding="post", truncating="post", maxlen=self.context_size)
        tokenized_question = pad_sequences(tokenized_question, padding="post", truncating="post", maxlen=20)
        tokenized_answer   = pad_sequences(tokenized_answer, padding="post", truncating="post", maxlen=10)

        if debug:
            print(context_line, tokenized_context)
            print(question, tokenized_question)
            print(answer, tokenized_answer)

        for i in range(1, stop): # <s> notre dame won the game </s> is the sentence so we want it to stop after the first prediction
            results = self.model.predict([tokenized_question, tokenized_answer, tokenized_context])
            tokenized_answer[0][i] = np.argmax(results)

        for layer in ['activation', 'activation_1']:
            activations = get_activations(self.model, [tokenized_question, tokenized_answer, tokenized_context], layer)
            for act in activations: # This loop will run once for activations[0]
                display_activations(act, layer, name, self.context_size, stop)
        
        response = self.answer_tokenizer.sequences_to_texts(tokenized_answer)

        if debug:
            print()
            print(tokenized_answer)
            print(response)

def display_activations(activations, layer, name, context_size, stop):
    print('----- plotting -----')
    import matplotlib.pyplot as plt

    plt.rcParams["figure.figsize"] = (40, 10)
    for i, activation_map in enumerate(activations):
        activation_map = np.expand_dims(activation_map, axis=0)
        batch_size = activation_map.shape[0] # Should be 1
        print(activation_map.shape)

        if layer == "activation_1":
            context_size = 20 # This layer is the question (which is max length 20)
        
        plt.imshow(activation_map[0], interpolation='nearest')
        plt.xticks([i for i in range(0, context_size)])
        plt.title("Acivation Heatmap for" + layer)
        plt.savefig("heatmap/images/" + name + "/" + layer + "_stop=" + str(stop) + ".png")

def get_activations(model, model_inputs, layer_name):
    print('----- activations -----')
    activations = []
    inp = model.input # This is a list

    outputs = [layer.output for layer in model.layers if layer.name == layer_name]  # all layer outputs

    funcs = [K.function(inp + [K.learning_phase()], [out]) for out in outputs]  # evaluation functions

    list_inputs = []
    list_inputs.extend(model_inputs)
    list_inputs.append(0.)

    layer_outputs = [func(list_inputs)[0] for func in funcs]
    for layer_activations in layer_outputs:
        activations.append(layer_activations)
        print(layer_activations.shape)
    
    return activations

if __name__ == "__main__":
    # Uncomment this to make images for the simple model
    '''
    predictor = Predictor("simple")
    predictor.make_prediction('What year was the game ?', "simpleyear", 20, 5, True) # Put the images in the images/simpleyear/ and stop on word 5 (the year 2000)
    predictor.make_prediction('Who was the coach ?', "simplecoach", 20, 1, True)
    predictor.make_prediction('Who won the game ?', "simplewinner", 20, 1, True)
    '''
    predictor = Predictor("sentence")
    predictor.make_prediction('What year was the game ?', "sentenceyear", 20, 5, True) # Put the images in the images/sentenceyear/ and stop on word 5 (the year 2000)
    predictor.make_prediction('Who was the coach ?', "sentencecoach", 20, 1, True)
    predictor.make_prediction('Who won the game ?', "sentencewinner", 20, 1, True)
