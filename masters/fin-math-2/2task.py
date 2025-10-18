#!/usr/bin/python3

import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#
# Завантаження даних
#
stock_prices_csv = 'stock_prices.csv'
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM']
if not os.path.exists(stock_prices_csv):
    start_date = '2018-01-01'
    end_date = '2025-10-10'
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
    data.to_csv(stock_prices_csv)
else:
    data = pd.read_csv(stock_prices_csv, index_col=0, parse_dates=True)


#
# Вивід графіка цін
#
plt.figure(figsize=(14, 8))
data.plot(ax=plt.gca(), linewidth=2)
plt.title('Історичні ціни закриття акцій (2018-2025)', fontsize=16)
plt.xlabel('Дата', fontsize=12)
plt.ylabel('Ціна закриття (USD)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Тікер')
plt.tight_layout()
plt.show()


#
# Середнє, волатильність та матриця коваріацій
#
returns = data.pct_change().dropna()
returns_mean = returns.mean() 
cov_matrix = returns.cov()



#
# Метод Монте-Карло
#
PORTFOLIOS_N = 5000
ANNUAL_TRADING_DAYS = 252 
RISK_FREE_RATE = 0.0 # Ставка дохідності безризикового активу

portfolio_returns = np.zeros(PORTFOLIOS_N)
portfolio_vol = np.zeros(PORTFOLIOS_N)
sharpe_ratios = np.zeros(PORTFOLIOS_N)
all_w = np.zeros((PORTFOLIOS_N, len(tickers)))

for i in range(PORTFOLIOS_N):
    w_i = np.random.random(len(tickers))
    w_i /= np.sum(w_i)
    all_w[i, :] = w_i

    # Метрики портфоліо
    portfolio_returns[i] = np.sum(returns_mean * w_i) * ANNUAL_TRADING_DAYS
    portfolio_vol[i] = np.sqrt(np.dot(w_i.T, np.dot(cov_matrix, w_i))) * np.sqrt(ANNUAL_TRADING_DAYS)
    sharpe_ratios[i] = (portfolio_returns[i] - RISK_FREE_RATE) / portfolio_vol[i]

# 4. Знаходимо оптимальний портфель (найбільший коефіцієнт Шарпа)
max_sharpe_index = sharpe_ratios.argmax()
optimal_sharpe_weights = all_w[max_sharpe_index, :]
optimal_sharpe_return = portfolio_returns[max_sharpe_index]
optimal_sharpe_volatility = portfolio_vol[max_sharpe_index]
optimal_sharpe_ratio = sharpe_ratios[max_sharpe_index]
