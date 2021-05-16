This directory holds the files for the heatmap generation.  Note that we use Tensorflow version 2.2 here (see new requirements.txt)

Run the script from inside the parent directory like: python heatmap/generate_heatmap.py

The purpose of the script is to look at the activation layer when it needs to look in the context for the next word.
It is also interesting to look at the activation_1 layer to see what is it looking at in the question when predicting the next word.