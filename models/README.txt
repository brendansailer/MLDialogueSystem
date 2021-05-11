Data about current models:

qa_g_lstm_context_increased_11.h5
- 11 Epochs on the 3 starter questions
- Use txtCreation.py to create contexts with 5 fields

qa_g_lstm_context_increased_11_sentence.h5
- 11 Epochs on the 3 starter questions with contexts as sentences, rather than a CSV
- Use txtCreation.py to create contexts with 5 fields

qa_g_lstm_context_increased_11_jumbled.h5
- 11 Epochs on the 3 starter questions with contexts as sentences, BUT jumbled (context sentences are not in the same order each time)
- Use txtCreation.py to create contexts with 5 fields

qa_g_lstm_context_increased_11_deduction.h5
- 11 Epochs on 3 starter questions and a deduction question
- Use txtCreation.py to create contexts with 7 fields (the addition of home and away score so the model can subtract the two and pick the higher one)