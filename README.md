# Futures Backtester

Python-based backtesting of a Simple Moving Average (SMA) crossover trading strategy. Utilizes `yfinance` for data, `pandas` for manipulation, and `matplotlib`/`plotly` for visualization.

## Abstract

This project backtests a quantitative trading strategy based on "Golden Cross" and "Death Cross" SMA signals. It assesses performance, risk, and profitability, calculating Sharpe Ratio, Maximum Drawdown, Annualized Volatility, and Final Portfolio Value.

## Methodology


Indicator and Signal Generation:

   * **Simple Moving Averages (SMAs):** `SMA50` and `SMA200` computed.

   * **Trading Signal:** `Signal = 1` (Buy) if `SMA50 > SMA200`, `0` (Sell) otherwise.

   * **Position Tracking:** `Position` column identifies buy (`1`) and sell (`-1`) points from `Signal` changes (`.diff()`).

Initializations:

   * `initial_cash` (default $10,000) simulates portfolio.

   * `Daily Returns` calculated from `Close` price percentage change.

   * `Strategy_Returns` derived from lagged `Signal` multiplied by `Daily Returns`.

   * `Portfolio_Value` compounds `Strategy_Returns`.

   * `Buy_Signal` and `Sell_Signal` flags for visualization.

Performance Metrics Calculation:

   * **Sharpe Ratio:** Risk-adjusted return.

   * **Max Drawdown:** Largest peak-to-trough portfolio decline.

   * **Annualized Volatility:** Annualized standard deviation of daily returns.

   * **Final Portfolio Value:** Portfolio value at backtest end.


## Mathematical Concepts

### Simple Moving Average (SMA)

The Simple Moving Average (SMA) for a given period $n$ is calculated as the sum of the closing prices over that period, divided by $n$:

$$
\mathrm{SMA}_n(t) = \frac{1}{n} \sum_{i=0}^{n-1} \mathrm{Price}(t - i)$$

Where:

* $\text{Price}(t-i)$ is the closing price at time $t-i$.

* $n$ is the number of periods (e.g., 50 for SMA50, 200 for SMA200).

### Daily Returns

Daily returns are calculated as the percentage change in the closing price from one day to the next:

$$
\text{Returns}_t = \frac{\text{Close}_t - \text{Close}_{t-1}}{\text{Close}_{t-1}}
$$

### Strategy Returns

The strategy returns are calculated by multiplying the lagged signal (position) by the daily returns. If the signal is 1 (long position), the strategy earns the daily return; otherwise, it earns 0 (no position).

$$
\text{Strategy\_Returns}_t = \text{Signal}_{t-1} \times \text{Returns}_t
$$

### Portfolio Value

The portfolio value is calculated by compounding the strategy returns over time, starting with an initial cash amount:

$$
\text{Portfolio\_Value}_t = \text{Initial\_Cash} \times \prod_{i=1}^{t} (1 + \text{Strategy\_Returns}_i)
$$

### Sharpe Ratio

The Sharpe Ratio measures the risk-adjusted return of the strategy. It is calculated as the mean of the strategy returns divided by the standard deviation of the strategy returns, annualized. A higher Sharpe Ratio indicates a better risk-adjusted performance.

$$
\text{Sharpe Ratio} = \frac{\text{Mean}(\text{Strategy\_Returns})}{\text{StdDev}(\text{Strategy\_Returns})} \times \sqrt{252}
$$

Where $\sqrt{252}$ is used for annualization based on 252 trading days in a year.

### Max Drawdown

Max Drawdown (MDD) represents the largest percentage decline from a peak in portfolio value to a subsequent trough. It is a measure of downside risk.

$$
\text{Drawdown}_t = \frac{\text{Cumulative Returns}_t - \text{Rolling Max Cumulative Returns}_t}{\text{Rolling Max Cumulative Returns}_t}
$$

$$
\text{Max Drawdown} = \min(\text{Drawdown})
$$

## Outcome and Conclusions

Backtesting results for AAPL (2019-01-01 to 2025-05-20, SMA50/SMA200):

### Performance Metrics:

### Performance Metrics:

Sharpe Ratio: 0.6
Max Drawdown: -0.31
Annualized Volatility: 0.26
Final Portfolio Value: 22037.22

Portfolio growth: 120.37%

## Visualizations:

Plots show stock price, SMAs, buy/sell signals, and portfolio performance.

<img width="1458" height="870" alt="Screenshot 2025-07-16 at 11 36 51 AM" src="https://github.com/user-attachments/assets/ecd8f69f-5029-4a24-bdc7-af01cc774463" />


### Analysis:

* **Sharpe Ratio (0.6):** Suboptimal risk-adjusted returns; insufficient compensation for risk. This is mostly due to the simplicity of the strategy. Golden Cross is strong but not as the only layer of confluence being utilized

* **Max Drawdown (-0.31):** Significant 31% peak-to-trough decline.

* **Final Portfolio Value ($22,037.22):** Initial $10,000 capital more than doubled, but this return must be weighed against risk and a buy-and-hold benchmark.

### Future Improvements:

To enhance Sharpe Ratio and reduce drawdown I can do:

   * **Parameter Optimization:** Test SMA window combinations for optimal Sharpe Ratios.

   * **Additional Indicators:** Integrate other technical indicators (such as RSI, MACD, Volume, Bollinger Bands) for signal confirmation and false positive reduction.

   * **Stop-Loss/Take-Profit:** Implement dynamic mechanisms for risk management and profit locking.

   * **Market Regime Filtering:** Adapt strategy based on market trends.

