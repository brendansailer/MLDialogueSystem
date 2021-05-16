The model is trying to predict the winner (sentence starts with winning's team name):
['<s> UNK UNK UNK UNK UNK UNK UNK UNK UNK']


The activation layer is plotting the context (x-axis) vs the answer (y-axis)

The context:
<s> 2000 bob davie nebraska 23 fbs independents </s>
[ 2 30 15 16 63 55  7  8  3  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

The image shows that the model is looking at the word nebraska here


The activation_1 layer is plotting the question (x-axis) vs the answer (y-axis)

The question:
<s> who won the game  </s>
[ 3  7 17  2  6  4  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

Likewise the model is looking at "who won" which is good