#!/usr/bin/env python
# coding: utf-8
# train: python DeepEdit.py --mode=train --train_csv=train.csv --test_csv=test.csv --output_fold=train --model_name=model
# predict: python DeepEdit.py --mode=predict --predict_csv=predict.csv --output_fold=predict_result --model_name=model.h5

import keras
import argparse
import os
import sys
import pandas as pd
import joblib
import numpy as np
from keras.layers import Dense,Dropout
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn import metrics


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--mode', type=str, required=True)
parser.add_argument('--train_csv', type=str, default=None)
parser.add_argument('--test_csv', type=str, default=None)
parser.add_argument('--predict_csv', type=str, default=None)
parser.add_argument('--predict_results', type=str, default=None)
parser.add_argument('--output_fold', type=str, required=True)
parser.add_argument('--model_name', type=str, required=True)
args = parser.parse_args()

if args.mode not in ['train','predict']:
    print('Please choose a mode: train/test')
    sys.exit(0)

def define_model(shape):
    model = Sequential()
    model.add(Dense(1024, activation = "relu",input_shape = (shape,)))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation = "relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation = "relu"))
    model.add(Dense(2,activation = 'softmax'))
    return model

def train(train_csv,test_csv,output_fold,model_name):
    try:
        train_data = pd.read_csv(train_csv, header=None, encoding='utf_8_sig')
        x_train, y_train = train_data.iloc[:,3:-1].values, train_data.iloc[:,-1].values
        train_shape = np.shape(x_train)[1]
        y_train = to_categorical(y_train)
        test_data = pd.read_csv(test_csv, header=None, encoding='utf_8_sig')
        x_test, y_test = test_data.iloc[:,3:-1].values, test_data.iloc[:,-1].values
        y_test = to_categorical(y_test)
    except IOError:
        raise IOError('Error opening csv files.')

    model = define_model(train_shape)
    model.summary()
    early_stopping = EarlyStopping(monitor='val_loss', patience=100,restore_best_weights=True)
    model.compile(optimizer=Adam(lr=0.0001,decay=0.00001),loss='categorical_crossentropy',metrics=['accuracy'])
    history = model.fit(x=x_train,y=y_train,batch_size=16, epochs=10000, validation_data=(x_test,y_test),callbacks=[early_stopping])
    model.save(output_fold+'/'+model_name+'.h5')

def predict(predict_csv,output_fold,model_name):
    try:
        data = pd.read_csv(predict_csv, header=None, encoding='utf_8_sig')
        x = data.iloc[:,3:].values
    except IOError:
        raise IOError('Error opening predict_csv.')

    try:
        model = keras.models.load_model(model_name)
    except IOError:
        raise IOError('Erros opening model files')

    print('Predicting...')
    y_prob = model.predict(x)
    y_pred = []
    for i in range(0, len(y_prob)):
        y_pred.append(y_prob[i][1])
    data[-1] = y_pred
    data.to_csv(output_fold+'/result',index=False,encoding='utf_8_sig')

output_fold = args.output_fold
model_name = args.model_name

if not os.path.exists(output_fold):
    os.makedirs(output_fold)

if args.mode == 'train':
    train_csv = args.train_csv
    test_csv = args.test_csv
    train(train_csv,test_csv,output_fold,model_name)

if args.mode == 'predict':
    predict_csv = args.predict_csv
    predict(predict_csv,output_fold,model_name)
