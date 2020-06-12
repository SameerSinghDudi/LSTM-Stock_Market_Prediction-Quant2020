from matplotlib.pyplot import plt
import fundamental_metrics

def algo_vs_market(df, spy):
    annual_returns = fundamental_metrics.calculate_annual_returns(df)
    daily_returns = spy[['Adj Close']].pct_change().fillna(0)
    daily_returns = daily_returns.rename(columns={'Adj Close':'daily return'})
    spy_returns = fundamental_metrics.calculate_annual_returns(daily_returns)
    
    plt.figure(figsize=(16,8))
    plt.plot_date(annual_returns.index, annual_returns['return'], linestyle='solid')
    plt.plot_date(spy_returns.index, spy_returns['return'], linestyle='solid')
    plt.legend(['Algorithm','S&P 500'])
    plt.title('Algorithm Performance vs S&P 500')
    plt.grid(True)
    plt.tight_layout()
    plt.show()   
    
def visualize_dollar_profits(df):    
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(32,16))
    ax[0].plot(df['profit/loss'])
    ax[0].set_title('Daily Profit/Loss')
    ax[0].grid(True)

    ax[1].plot(df['initial capital'][:-1])
    ax[1].set_title('Capital Gains')
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()
    plt.close()