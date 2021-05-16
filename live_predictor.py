import argparse
import re
import random
# Optional to get rid of annoying tf warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from keras.models import load_model

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
            model = "models/qa_g_lstm_context_increased_11.h5" # Simple context
            context = "data/contexts.txt"
            answ_tok = "toks/answer_tok.json"
            ques_tok = "toks/question_tok.json"
            cont_tok = "toks/context_tok.json"
            context_size = 30

        elif test == "sentence":
            model = "models/qa_g_lstm_context_increased_11_sentence.h5" # Sentence context
            context = "data/contexts_sentence.txt"
            answ_tok = "toks/answer_tok.json"
            ques_tok = "toks/question_tok.json"
            cont_tok = "toks/context_tok_sentence.json"
            context_size = 40

        elif test == "jumbled":
            model = "models/qa_g_lstm_context_increased_11_jumbled.h5" # Jumbled context
            context = "data/contexts_jumbled.txt"
            answ_tok = "toks/answer_tok.json"
            ques_tok = "toks/question_tok.json"
            cont_tok = "toks/context_tok_jumbled.json"
            context_size = 40

        elif test == "deduction":
            model = "models/qa_g_lstm_context_increased_11_deduction.h5" # Deduction question added
            context = "data/contexts_deduction.txt"
            answ_tok = "toks/answer_tok_deduction.json"
            ques_tok = "toks/question_tok_deduction.json"
            cont_tok = "toks/context_tok_deduction.json"
            context_size = 30

        return model, context, answ_tok, ques_tok, cont_tok, context_size

    def make_prediction(self, question, line_num, debug):
        # Sanitize the question input
        question = re.sub('[^0-9a-zA-Z</>]+', ' ', question)
        question = question.lower()
        question = "<s> " + question + " </s>"

        # Prepare the answer that starts with <s>
        answer = "<s>"

        # Load in the context
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

        if debug:
            print(context_line, tokenized_context)
            print(question, tokenized_question)
            print(answer, tokenized_answer)

        tokenized_context  = pad_sequences(tokenized_context, padding="post", truncating="post", maxlen=self.context_size)
        tokenized_question = pad_sequences(tokenized_question, padding="post", truncating="post", maxlen=20)
        tokenized_answer   = pad_sequences(tokenized_answer, padding="post", truncating="post", maxlen=10)

        # Predict one word at a time
        for i in range(1, 10):
            results = self.model.predict([tokenized_question, tokenized_answer, tokenized_context])
            tokenized_answer[0][i] = np.argmax(results)
        
        response = self.answer_tokenizer.sequences_to_texts(tokenized_answer)
        final_answer = response[0][response[0].index("<s>")+4:response[0].index("</s>")-1]

        if debug:
            print()
            print(tokenized_answer)
            print(response)
            print("FINAL ANSWER: " + final_answer)

        return final_answer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', metavar='line', type=int, help='Enter a number to pick the context line')
    parser.add_argument('-q',  metavar='question', type=str, nargs='+', help='Enter a question to ask')
    args = parser.parse_args()

    if not args.n or not args.q:
        print("Please use the -n and -q flags")
        quit()

    predictor = Predictor("simple")
    predictor.make_prediction(' '.join(args.q), args.n, True)
