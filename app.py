import backtest
import evaluate
import fundamental_metrics
import helper
import neural_net
import visualization

import yfinance as yf

def run_algo(ticker,spy):
    df = neural_net.test(ticker, model)
    df, beta, risk, sharpe, ret, profit = backtest.trade(df)
    visualization.algo_vs_market(df,spy)
    visualization.visualize_dollar_profits(df)

df,data,scalar = helper.set_up() 
model = neural_net.construct_model()
values = neural_net.train_dataset(data, model, scalar)

spy = yf.download('SPY','2010-01-01','2020-05-30')

## INTEL CORPORATION ##
run_algo('INTC',spy)

## HOME DEPOT ##
run_algo('HD',spy)

##Testing 100 companies
backtest.test_100()

