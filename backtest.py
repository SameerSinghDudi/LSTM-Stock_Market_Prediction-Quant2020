import pandas as pd
import math
import fundamental_metrics
import model
import random

def trade(data):
    
    df = data['data']
    
    initial_capital = 100000
    total_profit = 0
    long_days = 0
    short_days = 0
    num_loss_days = 0
    df['profit/loss'] = 0
    df['total profit'] = 0
    df['initial capital'] = initial_capital
    df['daily return'] = 0.0
    

    
    for i in range(0,(len(df)-2)):
        pred_open_next_day = df['pred_open_next_day'][i]
        pred_close_next_day = df['pred_close_next_day'][i]
        tomorrow = pd.to_datetime(df.index.values[i+1]).date()
        print('Day {} \n[ {} ]'.format(i+1, tomorrow))
        df.at[df.index.values[i+1],'initial capital'] = df.at[df.index.values[i],'initial capital']
        
        
        if pred_open_next_day < pred_close_next_day:
            buy_price = df['Open'][i+1]
            sell_price = df['Close'][i+1]
            
            if math.isnan(buy_price) or math.isnan(sell_price):
                continue
            
            if initial_capital > 0:
                num_shares = initial_capital/buy_price
                long_days+=1
                
                print('\t Buying {} shares at {}'.format(num_shares, buy_price))
                print('\t Selling {} shares at {}'.format(num_shares, sell_price))

                profit = (num_shares*sell_price) - (num_shares*buy_price)
                ret = profit/initial_capital
            
                
                df.at[df.index.values[i+1],'profit/loss'] = profit
                df.at[df.index.values[i+1],'daily return'] = ret
                    
                    
                initial_capital += profit
                total_profit += profit
                
                df.at[df.index.values[i+1],'total profit'] = total_profit
                df.at[df.index.values[i+1],'initial capital'] = initial_capital
                
                
                    
                if profit < 0:
                    num_loss_days+=1

                print('\tDay profit/loss: {}\n'.format(round(profit,2)))
            else:
                print('Not enough money')



        elif pred_open_next_day > pred_close_next_day:

            sell_price = df['Open'][i+1]
            buy_back_price = df['Close'][i+1]
            
            if math.isnan(buy_back_price) or math.isnan(sell_price):
                continue
            
            if initial_capital !=0:
                num_shares = 100
                short_days+=1

                print('\t Shorting {} shares at {}'.format(num_shares, buy_back_price))
                print('\t Buying Back {} shares at {}'.format(num_shares, sell_price))

                profit = (num_shares*sell_price) - (num_shares*buy_back_price)
                ret = profit/initial_capital
                
                df.at[df.index.values[i+1],'profit/loss'] = profit
                df.at[df.index.values[i+1],'daily return'] = ret
                    
                initial_capital += profit
                total_profit += profit
                df.at[df.index.values[i+1],'total profit'] = total_profit
                df.at[df.index.values[i+1],'initial capital'] = initial_capital
                    
                if profit < 0:
                    num_loss_days+=1
                    
                print('Day profit/loss: {}\n'.format(round(profit,2)))

            else:
                print('Not enough money')
                    
                    

    total_return = (total_profit/100000)*100
    annual_return = fundamental_metrics.annualized_return(total_return/100)*100
    
    beta = fundamental_metrics.get_beta(data['ticker'])
    risk = fundamental_metrics.calculate_risk(df)*100
    sharpe = (((annual_return/100) - 0.00942)/(risk/100))
    
    
     
    print('Beta: {}'.format(beta))
    print('\n------------------- EVALUATION METRICS -------------------\n')
    print('Total Return: {}%'.format(round(total_return,2)))
    print('Annualized Return: {}%'.format(round(annual_return,2)))
    print('Std. Deviation: {}%'.format(round(risk,2)))
    print('Sharpe Ratio: {}%'.format(round(sharpe,2)))
    print('Total Profit: {}'.format(round(total_profit,2)))
    print('Final Value of Capital: {}'.format(round(initial_capital,2)))
    
    print('\n------------------- TRADING STATISTICS -------------------\n')
    print('Total days long: {}'.format(long_days))
    print('Total days short: {}'.format(short_days))
    print('Number of days with loss: {}'.format(num_loss_days))
    print('')
    
    return df,beta,risk,sharpe,round(annual_return,2),round(total_profit,2)

def testing_program(tickers, model):
    x = []
    for ticker in tickers:
        data = model.test(ticker, model)
        print('Trading on: {}'.format(ticker))
        data,beta, risk, sharpe, ret, profit = trade(data)
        temp = {
            'ticker':ticker,
            'beta':beta,
            'risk':risk,
            'sharpe': sharpe,
            'return':ret,
            'profit':profit
        }
        x.append(temp)
        
    df = pd.DataFrame(x, columns=['ticker','beta','risk','sharpe','return','profit'])
        
    return df

def select_random(tickers, num):
    test_companies = []
    already_used = []
    for i in range(0,num):
        pos = random.randint(0,len(tickers)-1)
        
        while True:
            if pos in already_used:
                pos = random.randint(0,len(tickers))
            else:
                already_used.append(pos)
                break
            
        test_companies.append(tickers[pos])
    
    return test_companies

def test_100():
    companies = pd.read_csv('constituents.csv')
    tickers = companies['Symbol'].tolist()
    for n, i in enumerate(tickers):
        if i == 'BRK.B':
            tickers[n] = 'BRK'
        if i == 'BF.B':
            tickers[n] = 'BF'

    companies = select_random(tickers, 100)
    df = testing_program(companies, model)
    df.to_csv('Backtest_100_Stocks.csv')
