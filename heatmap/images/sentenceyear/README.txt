The model is trying to predict the year of the game (2000) in this sentence:
['<s> the game occurred in UNK UNK UNK UNK UNK']


The activation layer is plotting the context (x-axis) vs the answer (y-axis)

The context:
<s> the game was played in 2000 the head coach was bob davie the winner of the game was nebraska notre dame was ranked 23 notre dame was a part of the fbs independents conference </s> [
[ 9  2  6  3 10 11 43  2 12 13  3 28 29  2 14  7  2  6  3 76  4  5  3 15 68  4  5  3  8 16  7  2 20 21 17 18  0  0  0  0]

The image shows that the model is looking at the year a little, but not as much as other fields.  This may be a sign of some overfitting/memorization.


The activation_1 layer is plotting the question (x-axis) vs the answer (y-axis)

The question:
<s> what year was the game  </s>
[ 3  8 11  5  2  6  4  0  0  0  0  0  0  0  0  0  0  0  0  0]

When the model is trying to predict the year, it does look at the right spot in the question.