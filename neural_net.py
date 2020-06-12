from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
from keras import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import evaluate
import yfinance as yf
import helper
import math
import pandas as pd
import numpy as np

def construct_model():
    
    model = Sequential()
    model.add(LSTM(75, input_shape = (1,5), activation='tanh', recurrent_activation='sigmoid'))
    model.add(Dense(2))

    model.compile(loss='mse', optimizer = 'adam', metrics = [metrics.mae])

    callback = EarlyStopping(monitor='loss', patience=3)

    model.summary()
    
    model = {'model':model, 'callback': callback}
    
    return model

def train_dataset(data, model, scaler):
    x_train, x_test, y_train, y_test = train_test_split(data['x'],data['y'],test_size = 0.25)
    
    history = model['model'].fit(x_train, y_train, epochs=100, callbacks=[model['callback']])
    
    print('\nTraining finished')

    
    predict = model['model'].predict(x_test)
    
    original_values = scaler['y'].inverse_transform(y_test)
    predicted_values = scaler['y'].inverse_transform(predict)
    
    values = np.concatenate((original_values, predicted_values),axis=1)
    
    values = pd.DataFrame(values, columns = list(('open_next_day', 'close_next_day', 'pred_open_next_day', 'pred_close_next_day')))
    
    values = values.round(2)
    
    func = lambda x: math.log(x)
    val = [func(x) for x in history.history['loss']]
    
    plt.figure()
    plt.plot(val)
    plt.xlabel('epochs')
    plt.ylabel('log(mse)')
    plt.title('Model Loss Function')
    plt.show()
    
    evaluate.evaluate(values,75)

    
    return values

def test(ticker, model):
    
    print('Testing {}'.format(ticker))
   
    df = yf.download(ticker, '2010-01-01', '2020-05-30')

    df, data, scaler = helper.modify_dataset(df, False)
    
    predict = model['model'].predict(data['x'])
    
    predict = scaler['y'].inverse_transform(predict)
    
    predictions = pd.DataFrame(predict, columns = list(('pred_open_next_day', 'pred_close_next_day'))).round(2)
    df['pred_open_next_day'] = predictions['pred_open_next_day'].to_numpy()
    df['pred_close_next_day'] = predictions['pred_close_next_day'].to_numpy()
    
    evaluate.evaluate(df,100,True)
    
    data = {'ticker':ticker, 'data':df}

    
    
    return data
