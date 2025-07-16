import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True) #using yfinance to load in a bunch of data
    
    # ^^ the auto_adjust makes it so that I'm adjusting the graph for whena share splits into 2, and when a company pays dividends and it's stock slightly goes down
    
    df = df[['Close']]
    
    #^^ data fram is a 2D table, i only care about the closing price, not the open, high , or low
    df.dropna(inplace=True) #remove NaN, that result from missing data
    return df

#user input
def get_user_input():
    ticker = input("Enter stock ticker (e.g., AAPL, MSFT): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    short_window = int(input("Enter short window for SMA (e.g., 50): "))
    long_window = int(input("Enter long window for SMA (e.g., 200): "))
    return ticker, start_date, end_date, short_window, long_window



#------------------
#indicators and signals
def add_indicators(df, short_window=50, long_window=200):
    df['SMA50'] = df['Close'].rolling(window=short_window).mean() #moving average of last 50 closing prices
    df['SMA200'] = df['Close'].rolling(window=long_window).mean() #moving average of last 200 closing prices
    
    #SMA = (1/n) * sum(Price(t-i)) from i=0 to n-1
    #^^ helps me see trends

    df['Signal'] = (df['SMA50'] > df['SMA200']).astype(int)
    
    #golden cross strategy
    # if SMA50 > SMA200, bullish
    #if SMA50 < SMA200, bearish
    df['Position'] = df['Signal'].diff()
    # 0 -> 1 = 1-0 = 1 = buy
    #1 -> 0 = 0-1 = -1 = sell
    # 1-1, 0-0, = 0 = hold
    
    return df

#backtest a portfolio
def backtest(df, initial_cash=10000):
    df['Returns'] = df['Close'].pct_change()
    
    # ^^ daily returns = % change yesterday to today
    df['Signal'] = df['Signal'].fillna(0).astype(int) #acting on yesterday's signal

    df['Strategy_Returns'] = df['Signal'].shift(1) * df['Returns'] #if in position (1) earn return, else loss
    df['Strategy_Returns'].fillna(0, inplace=True)

    df['Portfolio_Value'] = initial_cash * (1 + df['Strategy_Returns']).cumprod() #compounding returns AKA reinvisting gains
    
    # ^^^

    df['Buy_Signal'] = df['Position'] == 1 #where I should have bought
    df['Sell_Signal'] = df['Position'] == -1 #where I should have sold

    return df


#plot
def plot_results(df):
    fig, axs = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Price chart with signals
    axs[0].plot(df['Close'], label='Price', alpha=0.5)
    axs[0].plot(df['SMA50'], label='SMA50', linestyle='--', alpha=0.75)
    axs[0].plot(df['SMA200'], label='SMA200', linestyle='--', alpha=0.75)

    axs[0].scatter(df.index[df['Buy_Signal']], df['Close'][df['Buy_Signal']], label='Buy Signal', marker='^', color='g', s=100)
    axs[0].scatter(df.index[df['Sell_Signal']], df['Close'][df['Sell_Signal']], label='Sell Signal', marker='v', color='r', s=100)

    axs[0].legend()
    axs[0].set_title("Price and Moving Averages")

    # Portfolio value chart
    axs[1].plot(df['Portfolio_Value'], label='Portfolio Value', color='blue')
    axs[1].legend()
    axs[1].set_title("Portfolio Performance")

    plt.tight_layout()
    plt.show()

#performance metrics
def calculate_metrics(df):
    returns = df['Strategy_Returns'].dropna()
    sharpe_ratio = returns.mean() / returns.std() * (252 ** 0.5) #risk-adjusted return, 252 days in trading year
    
    # Sharpe ratio: 1 = acceptable, 2 = good, 3 = excelent
    
    annualized_return = (df['Portfolio_Value'].iloc[-1] / df['Portfolio_Value'].iloc[0])**(1/len(df)) - 1
    volatility = returns.std() * (252 ** 0.5)  #annualized volatility
    win_percentage = len(df[df['Strategy_Returns'] > 0]) / len(df) * 100
    loss_percentage = 100 - win_percentage

    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    #^^^ largest peak to trough decline in portfolio
    # Drawdown = (portfolio value - max portfolio value so far)/max portfolio value so far

    return {
        'Sharpe Ratio': round(sharpe_ratio, 2),
        'Max Drawdown': round(max_drawdown, 2),
        'Annualized Volatility': round(volatility, 2),
        'Final Portfolio Value': round(df['Portfolio_Value'].iloc[-1], 2)
    }


def detailed_trade_info(df):
    trades = df[df['Position'].notna()]
    trade_details = []
    for i, row in trades.iterrows():
        trade_type = "Buy" if row['Position'] == 1 else "Sell"
        trade_price = row['Close']
        trade_return = row['Strategy_Returns']
        trade_details.append({
            'Date': row.name,
            'Trade Type': trade_type,
            'Price': trade_price,
            'Return': round(trade_return * 100, 2)
        })
    trade_df = pd.DataFrame(trade_details)
    return trade_df



def interactive_plot(df):
    fig = go.Figure()

    #Price
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Price'))

    #SMA50
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], mode='lines', name='SMA50'))

    #SMA200
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA200'], mode='lines', name='SMA200'))

    #buy Signals
    fig.add_trace(go.Scatter(x=df.index[df['Buy_Signal']], y=df['Close'][df['Buy_Signal']], mode='markers', marker=dict(symbol='triangle-up', color='green', size=10), name='Buy Signal'))

    #seell Signals
    fig.add_trace(go.Scatter(x=df.index[df['Sell_Signal']], y=df['Close'][df['Sell_Signal']], mode='markers', marker=dict(symbol='triangle-down', color='red', size=10), name='Sell Signal'))

    #portfolio Value
    fig.add_trace(go.Scatter(x=df.index, y=df['Portfolio_Value'], mode='lines', name='Portfolio Value', line=dict(color='blue')))

    fig.update_layout(title="Price, Moving Averages, Signals, and Portfolio Value",
                      xaxis_title="Date",
                      yaxis_title="Price / Portfolio Value",
                      template="plotly_dark")
    
    fig.show()



if __name__ == "__main__":
    df = get_data('XOM', '2019-01-01', '2025-05-20')
    df = add_indicators(df)
    df = backtest(df)
    metrics = calculate_metrics(df)

    print("\nPerformance Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")

    plot_results(df)

