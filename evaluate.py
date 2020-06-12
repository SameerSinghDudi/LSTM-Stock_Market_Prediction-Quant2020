import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import r2_score as r2

def evaluate(df, num_points, test=False):
    print('\n ----------------- MODEL EVALUATION ----------------- \n')
    
    df.fillna(0)

    open_true = df['open_next_day']
    open_pred = df['pred_open_next_day']
    close_true = df['close_next_day']
    close_pred = df['pred_close_next_day']
    
    if test:
        open_true = open_true[:-1]
        open_pred = open_pred[:-1]
        close_true = close_true[:-1]
        close_pred = close_pred[:-1]


    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16,8))
    
    ax[0,0].plot(open_true[-num_points:], open_pred[-num_points:], 'go')
    ax[0,0].set_title('Open')
    
    ax[0,1].plot(close_true[-num_points:], close_pred[-num_points:], 'r^')
    ax[0,1].set_title('Close')
    
    ax[1,0].plot(open_true[-num_points:])
    ax[1,0].plot(open_pred[-num_points:])
    ax[1,0].set_label(['true','prediction'])
    

    ax[1,1].plot(close_true[-num_points:])
    ax[1,1].plot(close_pred[-num_points:])
    ax[1,1].set_label(['true','prediction'])

    fig.suptitle('Model Price Predictions')
    plt.show()
    plt.close()

    
    mae_open = mae(open_true,open_pred)
    mae_close = mae(close_true, close_pred)
    
    mse_open = mse(open_true, open_pred)
    mse_close = mse(close_true, close_pred)
    
    r2_open = r2(open_true, open_pred)
    r2_close = r2(close_true, close_pred)
    
    print('OPEN PRICES')
    print('\t Mean Absolute Error: {}'.format(mae_open))
    print('\t Mean Squared Error: {}'.format(mse_open))
    print('\t R2 Score: {}'.format(r2_open))
    
    print('CLOSE PRICES')
    print('\t Mean Absolute Error: {}'.format(mae_close))
    print('\t Mean Squared Error: {}'.format(mse_close))
    print('\t R2 Score: {}'.format(r2_close))
    print('')