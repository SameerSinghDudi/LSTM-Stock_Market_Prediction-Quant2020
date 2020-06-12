from sklearn.preprocessing import MinMaxScaler
import numpy as np
import yfinance as yf

def modify_dataset(df, remove_last=True):
    
    df['open_next_day'] = df['Open'].shift(-1, axis=0)
    df['close_next_day'] = df['Close'].shift(-1, axis=0)
    if remove_last:
        df.drop(df.tail(1).index,inplace=True)
    op = df['Open'].to_numpy()
    close = df['Close'].to_numpy()
    high = df['High'].to_numpy()
    low = df['Low'].to_numpy()
    vol = df['Volume'].to_numpy()
    
    y1 = df['open_next_day'].to_numpy()
    y2 = df['close_next_day'].to_numpy()
    
    x = np.vstack((op,close,high,low,vol)).T
    y = np.vstack((y1,y2)).T
    
    scaler = MinMaxScaler()
    scaler.fit(x)
    x = scaler.transform(x)
    
    scaler1 = MinMaxScaler()
    scaler1.fit(y)
    y = scaler1.transform(y)
    
    x = x.reshape(x.shape[0],1,x.shape[1])
    
    data = {'x':x, 'y':y}
    scaler = {'x':scaler, 'y':scaler1}
    
    return df,data,scaler

def set_up():
    spy = yf.download('SPY', '1995-01-01','2015-01-01')
    
    df, data, scaler = modify_dataset(spy)
    
    
    return df, data, scaler