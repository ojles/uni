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
def portfolio_metrics(w):
    p_ret = np.sum(returns_mean * w_i) * ANNUAL_TRADING_DAYS
    p_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))) * np.sqrt(ANNUAL_TRADING_DAYS)
    sharpe_ratio = (p_ret - RISK_FREE_RATE) / p_vol
    return p_ret, p_vol, sharpe_ratio

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
    p_ret, p_vol, p_sharpe_ratio = portfolio_metrics(w_i)
    portfolio_returns[i] = p_ret
    portfolio_vol[i] = p_vol
    sharpe_ratios[i] = p_sharpe_ratio

# Знаходимо оптимальний портфель (найбільший коефіцієнт Шарпа)
max_sharpe_index = sharpe_ratios.argmax()
optimal_mc_weights = all_w[max_sharpe_index, :]
optimal_mc_return = portfolio_returns[max_sharpe_index]
optimal_mc_volatility = portfolio_vol[max_sharpe_index]
optimal_mc_ratio = sharpe_ratios[max_sharpe_index]


#
# SLSQP
#
def sharpe_ratio_neg(w):
    _, _, sharpe_ratio = portfolio_metrics(w)
    return -sharpe_ratio

w0 = np.array([1/len(tickers)] * len(tickers))
# Сума ваг повинна дорівнювати 1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
# Ваги можуть бути лише додатніми
bounds = tuple((0, 1) for _ in range(len(tickers)))

from scipy.optimize import minimize
optimized_results = minimize(
    sharpe_ratio_neg,
    w0,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

# Отримуємо метрики оптимального портфеля
optimal_slsqp_w = optimized_results.x
optimal_slsqp_return, \
    optimal_slsqp_vol, \
    optimal_slsqp_ratio = portfolio_metrics(optimal_slsqp_w)
