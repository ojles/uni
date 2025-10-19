#!/usr/bin/python3

import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#
# Завантаження даних
#
stock_prices_csv = '2task_stock_prices.csv'
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
    # Річна дохідність
    p_ret = np.sum(returns_mean * w) * ANNUAL_TRADING_DAYS
    # Річна волатильність
    p_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))) * np.sqrt(ANNUAL_TRADING_DAYS)
    # Коефіцієнт Шарпа
    sharpe_ratio = (p_ret - RISK_FREE_RATE) / p_vol
    return p_ret, p_vol, sharpe_ratio

PORTFOLIOS_N = 5000
ANNUAL_TRADING_DAYS = 252
RISK_FREE_RATE = 0.0 # Ставка дохідності безризикового активу
NUM_ASSETS = len(tickers)

portfolio_returns = np.zeros(PORTFOLIOS_N)
portfolio_vol = np.zeros(PORTFOLIOS_N)
sharpe_ratios = np.zeros(PORTFOLIOS_N)
all_w = np.zeros((PORTFOLIOS_N, NUM_ASSETS))

for i in range(PORTFOLIOS_N):
    w_i = np.random.random(NUM_ASSETS)
    w_i /= np.sum(w_i)
    all_w[i, :] = w_i

    # Метрики портфоліо
    p_ret, p_vol, p_sharpe_ratio = portfolio_metrics(w_i)
    portfolio_returns[i] = p_ret
    portfolio_vol[i] = p_vol
    sharpe_ratios[i] = p_sharpe_ratio

# Знаходимо оптимальний портфель Монте-Карло
max_sharpe_index = sharpe_ratios.argmax()
optimal_mc_weights = all_w[max_sharpe_index, :]
optimal_mc_return = portfolio_returns[max_sharpe_index]
optimal_mc_volatility = portfolio_vol[max_sharpe_index]
optimal_mc_ratio = sharpe_ratios[max_sharpe_index]


#
# SLSQP Оптимізація
#
def sharpe_ratio_neg(w):
    _, _, sharpe_ratio = portfolio_metrics(w)
    return -sharpe_ratio

w0 = np.array([1/NUM_ASSETS] * NUM_ASSETS)
# Сума ваг повинна дорівнювати 1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
# Ваги можуть бути лише додатніми
bounds = tuple((0, 1) for _ in range(NUM_ASSETS))

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


#
# Візуалізація волатильності vs дохідності
#
plt.figure(figsize=(16, 9))
# Діаграма розсіювання, де колір відображає коефіцієнт Шарпа
scatter = plt.scatter(
    portfolio_vol,
    portfolio_returns,
    c=sharpe_ratios,
    cmap='viridis',
    marker='o',
    alpha=0.7,
    s=20
)
plt.colorbar(scatter, label='Коефіцієнт Шарпа', orientation='vertical')

# Оптимальний портфель Монте-Карло
plt.scatter(
    optimal_mc_volatility,
    optimal_mc_return,
    color='red',
    marker='*',
    s=500,
    label='Оптимальний портфель (Монте-Карло)'
)

# Оптимальний портфель SLSQP
plt.scatter(
    optimal_slsqp_vol,
    optimal_slsqp_return,
    color='blue',
    marker='*',
    s=500,
    label='Оптимальний портфель (SLSQP Оптимізація)'
)

plt.title('Volatility vs. Return', fontsize=18)
plt.xlabel('Волатильність (Стандартне відхилення, Річне)', fontsize=14)
plt.ylabel('Очікувана дохідність (Річна)', fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Виведення результатів
print("\n--- Характеристики Оптимального Портфеля (Монте-Карло) ---")
print(f"Дохідність: {optimal_mc_return:.2%}")
print(f"Волатильність: {optimal_mc_volatility:.2%}")
print(f"Коефіцієнт Шарпа: {optimal_mc_ratio:.4f}")
print("Ваги портфеля:")
for ticker, weight in zip(tickers, optimal_mc_weights):
    print(f"  {ticker}: {weight:.2%}")

print("\n--- Характеристики Оптимального Портфеля (SLSQP Оптимізація) ---")
print(f"Дохідність: {optimal_slsqp_return:.2%}")
print(f"Волатильність: {optimal_slsqp_vol:.2%}")
print(f"Коефіцієнт Шарпа: {optimal_slsqp_ratio:.4f}")
print("Ваги портфеля:")
for ticker, weight in zip(tickers, optimal_slsqp_w):
    print(f"  {ticker}: {weight:.2%}")
