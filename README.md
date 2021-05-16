# Welcome - Project Overview
- This is our final project for Interactive Dialogue Systems
- We created an Question/Answer system using an encoder-decoder model to answer questions about past Notre Dame football games
- The model is heavily based from this paper: https://arxiv.org/abs/2101.03999

## General
- For the best experience, clone the repository and open it in an IDE like VSCode that supports .png's
- Each subdirectory has a README.txt which details what is contained in it
- The root directory contains the files to:
    - Collect the college football data (`dataCollection.py`)
    - Create the context, answer, and question files (`txtCreation.py`)
    - Create the model (`model.py`)
    - Train the model (`train.py`)
    - Make a single prediction (`live_predictor.py`)
    - Test the models (`test.py`)
- The heatmap directory provides insight into where the model is looking to predict the next word
    - Please look there for analysis on the heatmap images when answering 3 questions
    - The images were generated for the simple model and the sentence context model

## TO USE:
- python3 `live_predictor.py` -n 1 -q "who was the coach ?"
- python3 `test.py`

# Setup

## Virtual Environment Setup (or use student machine):
- Upgrade pip: python3 -m pip install --user --upgrade pip
- Install virtualenv: python3 -m pip install --user virtualenv
- Create the venv: python3 -m venv env
- Activate the venv: source env/bin/activate
- Install requirements: pip install -r requirements.txt
- Exit: deactivate

## This is what the output of the teacher force function is (c=context, q=question, n=next work a=answer):  
c: \<s\> the game occurred in 2001 notre dame won the game bob davie was the coach \</s\>  q: \<s\> who was the coach \</s\>  n: ['bob'] a: \<s\>  
c: \<s\> the game occurred in 2001 notre dame won the game bob davie was the coach \</s\>  q: \<s\> who was the coach \</s\>  n: ['davie'] a: \<s\> bob  
c: \<s\> the game occurred in 2001 notre dame won the game bob davie was the coach \</s\>  q: \<s\> who was the coach \</s\>  n: ['was'] a: \<s\> bob davie  
c: \<s\> the game occurred in 2001 notre dame won the game bob davie was the coach \</s\>  q: \<s\> who was the coach \</s\>  n: ['the'] a: \<s\> bob davie was  
c: \<s\> the game occurred in 2001 notre dame won the game bob davie was the coach \</s\>  q: \<s\> who was the coach \</s\>  n: ['coach'] a: \<s\> bob davie was the  
c: \<s\> the game occurred in 2001 notre dame won the game bob davie was the coach \</s\>  q: \<s\> who was the coach \</s\>  n: ['\</s\>'] a: \<s\> bob davie was the coach  

## To get this add this code:
```
for c, a, q, n in zip(train_context, train_answer, train_question, next_word):  
    print("c: " + c + " q: " + q + " n: " + n + " a: " + a)  
quit()  
```

```
To see vectors going into the model:  
for i in range(50):  
    print("c: " + str(train_context[i]))  
    print(" q: " + str(train_question[i]))  
    print(" n: " + str(train_next_word[i]))  
    print(" a: " + str(train_answer[i]))  
    print()  
quit()  
```
# Useful links
https://github.com/aakashba/paqs2021/blob/paper/paqs_dev/models/ast_attendgru_xtra.py
https://github.com/aakashba/paqs2021/blob/paper/model.md
https://github.com/mcmillco/funcom/blob/master/models/attendgru.py