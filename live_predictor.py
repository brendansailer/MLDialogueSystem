import json
import argparse
import re
import random
import pickle

import numpy as np
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from keras.models import load_model

random.seed(1337)
np.random.seed(1337)
tf.random.set_seed(1337)

parser = argparse.ArgumentParser()
parser.add_argument('-n', metavar='line', type=int, help='Enter a number to pick the context line')
parser.add_argument('-q',  metavar='question', type=str, nargs='+', help='Enter a question to ask')
args = parser.parse_args()

if not args.n or not args.q:
    print("Please use the -n and -q flags")
    quit()
    
#with open("toks/answer_tok.json") as f:
with open("toks/answer_tok_deduction.json") as f:
    answer_tokenizer = tokenizer_from_json(f.read())
#with open("toks/context_tok.json") as f: # Simple context
#with open("toks/context_tok_sentence.json") as f: # Sentence context
#with open("toks/context_tok_jumbled.json") as f: # Jumbled context
with open("toks/context_tok_deduction.json") as f:
    context_tokenizer = tokenizer_from_json(f.read())
#with open("toks/question_tok.json") as f:
with open("toks/question_tok_deduction.json") as f:
    question_tokenizer = tokenizer_from_json(f.read())

# Sanitize the question input
question = ' '.join(args.q)
question = re.sub('[^0-9a-zA-Z</>]+', ' ', question)
question = question.lower()
question = "<s> " + question + " </s>"

# Prepare the answer that starts with <s>
answer = "<s>"

# Load in the context
context_line = ''
line_num = args.n
#with open("data/contexts.txt") as f: # Simple context
#with open("data/contexts_sentence.txt") as f: # Sentence context
#with open("data/contexts_jumbled.txt") as f: # Jumbled context
with open("data/contexts_deduction.txt") as f: # Deduction question added
    for i, line in enumerate(f):
        if i == line_num:
            context_line = line.strip()
            context_line = re.sub('[^0-9a-zA-Z</>]+', ' ', context_line)
            context_line = context_line.lower()
        elif i > line_num:
            break

tokenized_context = context_tokenizer.texts_to_sequences([context_line])
tokenized_question = question_tokenizer.texts_to_sequences([question])
tokenized_answer = answer_tokenizer.texts_to_sequences([answer])

print(context_line)
print(tokenized_context)
print()
print(question)
print(tokenized_question)
print()
print(answer)
print(tokenized_answer)

tokenized_context = pad_sequences(tokenized_context, padding="post", truncating="post", maxlen=30)
tokenized_question = pad_sequences(tokenized_question, padding="post", truncating="post", maxlen=20)
tokenized_answer = pad_sequences(tokenized_answer, padding="post", truncating="post", maxlen=10)

#model = load_model("models/qa_g_lstm_context_increased_11.h5") # Simple context
#model = load_model("models/qa_g_lstm_context_increased_11_sentence.h5") # Sentence context
#model = load_model("models/qa_g_lstm_context_increased_11_jumbled.h5") # Jumbled context
model = load_model("models/qa_g_lstm_context_increased_11_deduction.h5") # Deduction question added

# Predict one word at a time
for i in range(1, 10):
   results = model.predict([tokenized_question, tokenized_answer, tokenized_context])
   tokenized_answer[0][i] = np.argmax(results)

print()
print(tokenized_answer)
response = answer_tokenizer.sequences_to_texts(tokenized_answer)
print(response)
print("FINAL ANSWER: " + response[0][response[0].index("<s>")+4:response[0].index("</s>")])

