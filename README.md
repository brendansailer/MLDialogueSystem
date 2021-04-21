Virtual Environment Setup:
- Upgrade pip: python3 -m pip install --user --upgrade pip
- Install virtualenv: python3 -m pip install --user virtualenv
- Create the venv: python3 -m venv env
- Activate the venv: source env/bin/activate
- Install requirements: pip install -r requirements.txt
- Exit: deactivate

This is what the output of the teacher force function is (c=context, q=question, n=next work a=answer):
c: <s> the game occurred in 2001 notre dame won the game bob davie was the coach </s>  q: <s> who was the coach </s>  n: ['bob'] a: <s>
c: <s> the game occurred in 2001 notre dame won the game bob davie was the coach </s>  q: <s> who was the coach </s>  n: ['davie'] a: <s> bob
c: <s> the game occurred in 2001 notre dame won the game bob davie was the coach </s>  q: <s> who was the coach </s>  n: ['was'] a: <s> bob davie
c: <s> the game occurred in 2001 notre dame won the game bob davie was the coach </s>  q: <s> who was the coach </s>  n: ['the'] a: <s> bob davie was
c: <s> the game occurred in 2001 notre dame won the game bob davie was the coach </s>  q: <s> who was the coach </s>  n: ['coach'] a: <s> bob davie was the
c: <s> the game occurred in 2001 notre dame won the game bob davie was the coach </s>  q: <s> who was the coach </s>  n: ['</s>'] a: <s> bob davie was the coach

To get this add this code:

for c, a, q, n in zip(train_context, train_answer, train_question, next_word):
    print("c: " + c + " q: " + q + " n: " + n + " a: " + a)
quit()