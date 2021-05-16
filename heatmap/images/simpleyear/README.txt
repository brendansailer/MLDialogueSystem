The model is trying to predict the year of the game (2000) in this sentence:
['<s> the game occurred in UNK UNK UNK UNK UNK']


The activation layer is plotting the context (x-axis) vs the answer (y-axis)

The context:
<s> 2000 bob davie nebraska 23 fbs independents </s> 
[ 2 30 15 16 63 55  7  8  3  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

The image shows that the model is looking at the 1st element in the context (the year) which is good because it needs to put that next.


The activation_1 layer is plotting the question (x-axis) vs the answer (y-axis)

The question:
<s> what year was the game  </s>
[ 3  8 11  5  2  6  4  0  0  0  0  0  0  0  0  0  0  0  0  0]

When the model is trying to predict the year it is looking at the word "year" most intensly.