The model is trying to predict the coach (The sentence starts with the coach's name):
['<s> UNK UNK UNK UNK UNK UNK UNK UNK UNK']


The activation layer is plotting the context (x-axis) vs the answer (y-axis)

The context:
<s> the game was played in 2000 the head coach was bob davie the winner of the game was nebraska notre dame was ranked 23 notre dame was a part of the fbs independents conference </s>
[ 9  2  6  3 10 11 43  2 12 13  3 28 29  2 14  7  2  6  3 76  4  5  3 15 68  4  5  3  8 16  7  2 20 21 17 18  0  0  0  0]

The image shows that the model is looking at the 12th index (the coach's name).  
Interestingly, it is also looking at "notre dame" later in the sentence.  The model likely has made a connection between coach and team name.


The activation_1 layer is plotting the question (x-axis) vs the answer (y-axis)

The question:
<s> who was the coach  </s>
[ 3  7  5  2 10  4  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

When the model is trying to predict the coach it's looking heavily at the coach and the end token.
I think the model has identified that a lot of the coach questions all end with the word coach and has picked up on that.