import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Dense, Embedding, Reshape, GRU, merge, LSTM, Dropout, BatchNormalization, Activation, concatenate, multiply, MaxPooling1D, Conv1D, Flatten, Bidirectional, RepeatVector, Permute, TimeDistributed, dot
from keras.optimizers import RMSprop, Adamax
import keras
import keras.utils

class MLModel:
    def __init__(self):
        self.ques_vocabsize = 1000
        self.cont_vocabsize = 1000
        self.answ_vocabsize = 1000
        
        self.ques_len = 20
        self.cont_len = 30
        self.answ_len = 10

        self.embdims = 100
        self.recdims = 256

    def create_model(self):
        ques_input = Input(shape=(self.ques_len,))
        cont_input = Input(shape=(self.cont_len,))
        answ_input = Input(shape=(self.answ_len,))

        # Question
        ques_embed = Embedding(output_dim=self.embdims, input_dim=self.ques_vocabsize, mask_zero=False)(ques_input)
        enc = GRU(self.recdims, return_state=True, return_sequences=True, activation='tanh', unroll=True)
        encout, state_ques = enc(ques_embed)
        
        # Context
        cont_embed = Embedding(output_dim=self.embdims, input_dim=self.cont_vocabsize, mask_zero=False)(cont_input)
        dec = GRU(self.recdims, return_state=True, return_sequences=True, activation='tanh', unroll=True)
        decout, state_cont = dec(cont_embed, initial_state=state_ques)

        # Answer
        answ_embed = Embedding(output_dim=self.embdims, input_dim=self.answ_vocabsize, mask_zero=False)(answ_input)
        ans = GRU(self.recdims, return_sequences=True, activation='tanh', unroll=True)
        ansout = ans(cont_embed, initial_state=state_cont)
        
        # Attn for Answer - Context
        attn = dot([ansout, encout], axes=[2, 2])
        attn = Activation('softmax')(attn)

        # Attn for Answer - Question
        ast_attn = dot([ansout, decout], axes=[2, 2])
        ast_attn = Activation('softmax')(ast_attn)

        # Combine results
        context = dot([attn, encout], axes=[2, 1])
        ast_context = dot([ast_attn, decout], axes=[2, 1])

        context = concatenate([context, ansout, ast_context])
            
        out = TimeDistributed(Dense(self.recdims, activation="tanh"))(context)

        out = Flatten()(out)
        out = Dense(self.answ_vocabsize, activation="softmax")(out)
            
        model = Model(inputs=[ques_input, answ_input, cont_input], outputs=out)

        model.summary()

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.save('qa_g_lstm.h5')

        return model

    def get_model(self):
        return self.create_model()