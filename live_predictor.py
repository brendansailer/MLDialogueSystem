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

def get_paths(test):
    if test == "simple":
        model = "models/qa_g_lstm_context_increased_11.h5" # Simple context
        context = "data/contexts.txt"
        answ_tok = "toks/answer_tok.json"
        ques_tok = "toks/question_tok.json"
        cont_tok = "toks/context_tok.json"

    elif test == "sentence":
        model = "models/qa_g_lstm_context_increased_11_sentence.h5" # Sentence context
        context = "data/contexts_sentence.txt"
        answ_tok = "toks/answer_tok.json"
        ques_tok = "toks/question_tok.json"
        cont_tok = "toks/context_tok_sentence.json"

    elif test == "jumbled":
        model = "models/qa_g_lstm_context_increased_11_jumbled.h5" # Jumbled context
        context = "data/contexts_jumbled.txt"
        answ_tok = "toks/answer_tok.json"
        ques_tok = "toks/question_tok.json"
        cont_tok = "toks/context_tok_jumbled.json"

    elif test == "deduction":
        model = "models/qa_g_lstm_context_increased_11_deduction.h5" # Deduction question added
        context = "data/contexts_deduction.txt"
        answ_tok = "toks/answer_tok_deduction.json"
        ques_tok = "toks/question_tok_deduction.json"
        cont_tok = "toks/context_tok_deduction.json"

    return model, context, answ_tok, ques_tok, cont_tok

def make_prediction(question, line_num, test):
    random.seed(1337)
    np.random.seed(1337)
    tf.random.set_seed(1337)
    
    model_file, context_file, answ_tok, ques_tok, cont_tok = get_paths(test)

    with open(answ_tok) as f:
        answer_tokenizer = tokenizer_from_json(f.read())
    with open(cont_tok) as f:
        context_tokenizer = tokenizer_from_json(f.read())
    with open(ques_tok) as f:
        question_tokenizer = tokenizer_from_json(f.read())

    # Sanitize the question input
    question = re.sub('[^0-9a-zA-Z</>]+', ' ', question)
    question = question.lower()
    question = "<s> " + question + " </s>"

    # Prepare the answer that starts with <s>
    answer = "<s>"

    # Load in the context
    context_line = ''
    with open(context_file) as f:
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

    print(context_line, tokenized_context)
    print(question, tokenized_question)
    print(answer, tokenized_answer)

    tokenized_context = pad_sequences(tokenized_context, padding="post", truncating="post", maxlen=30)
    tokenized_question = pad_sequences(tokenized_question, padding="post", truncating="post", maxlen=20)
    tokenized_answer = pad_sequences(tokenized_answer, padding="post", truncating="post", maxlen=10)

    model = load_model(model_file)

    # Predict one word at a time
    for i in range(1, 10):
        results = model.predict([tokenized_question, tokenized_answer, tokenized_context])
        tokenized_answer[0][i] = np.argmax(results)

    print()
    print(tokenized_answer)
    response = answer_tokenizer.sequences_to_texts(tokenized_answer)
    print(response)
    final_answer = response[0][response[0].index("<s>")+4:response[0].index("</s>")]
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

    make_prediction(' '.join(args.q), args.n, "deduction")
