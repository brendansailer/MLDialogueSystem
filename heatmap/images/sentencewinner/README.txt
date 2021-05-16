The model is trying to predict the winner (sentence starts with winning's team name):
['<s> UNK UNK UNK UNK UNK UNK UNK UNK UNK']


The activation layer is plotting the context (x-axis) vs the answer (y-axis)

The context:
<s> the game was played in 2000 the head coach was bob davie the winner of the game was nebraska notre dame was ranked 23 notre dame was a part of the fbs independents conference </s>
[ 9  2  6  3 10 11 43  2 12 13  3 28 29  2 14  7  2  6  3 76  4  5  3 15 68  4  5  3  8 16  7  2 20 21 17 18  0  0  0  0]

The image shows that the model is looking at the winner not as heavily.  This may be a sign of some overfitting/memorization.
Leaving the periods in the sentence when tokenized or putting team names as numbers (w/ a dictionary lookup) or in brackets would have helped a lot here.


The activation_1 layer is plotting the question (x-axis) vs the answer (y-axis)

The question:
<s> who won the game  </s>
[ 3  7 17  2  6  4  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

When the model is trying to predict the winner it looks heavily at "who won" which is a key indicator of this type of question.