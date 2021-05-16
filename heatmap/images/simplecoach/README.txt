The model is trying to predict the coach (The sentence starts with the coach's name):
['<s> UNK UNK UNK UNK UNK UNK UNK UNK UNK']


The activation layer is plotting the context (x-axis) vs the answer (y-axis)

The context:
<s> 2000 bob davie nebraska 23 fbs independents </s>
[ 2 30 15 16 63 55  7  8  3  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

The image shows that the model is looking at the proper spot for the coach and is looking for a 2-word coach.


The activation_1 layer is plotting the question (x-axis) vs the answer (y-axis)

The question:
<s> who was the coach  </s>
[ 3  7  5  2 10  4  0  0  0  0  0  0  0  0  0  0  0  0  0  0]

When the model is trying to predict the coach it is looking at the word "coach" most intensly.