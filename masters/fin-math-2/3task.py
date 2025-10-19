#!/usr/bin/python3

"""
Завдання 3 (20 балів).
Коефіцієнт beta для акцій певної компанії зазвичай обчислюється
на базі помісячної дохідності протягом останніх 5 років.
Наприклад, https://finance.yahoo.com/quote/AAPL?p=AAPL містить коментар як саме це beta
було обчислено для акцій Apple.

'^GSPC' - ринок Standard & Poor`s 500
Обчислити beta за допомогою коваріацій для певної акції, наприклад 'IBM`.
Обчислити beta використовуючи регресійну модель і метод найменших квадратів
(наприклад функцію polyfit в бібліотеці NumPy)
Порівняти отримані beta з зазначеною beta на сайті Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


ticker = 'TSLA'
market_ticker = '^GSPC' # S&P500
start_date = '2020-01-01'
end_date = '2025-10-01'

#
# Завантаження та кешування даних
#
stock_prices_csv = f'3task_stock_prices_{ticker}.csv'
if not os.path.exists(stock_prices_csv):
    data = yf.download([ticker, market_ticker], start=start_date, end=end_date, interval='1mo')['Close']
    data.to_csv(stock_prices_csv)
else:
    data = pd.read_csv(stock_prices_csv, index_col=0, parse_dates=True)

# Обчислення помісячної дохідності (Percent Change)
returns = data.pct_change().dropna()
asset_returns = returns[ticker]
market_returns = returns[market_ticker]


# Бета за допомогою коваріацій
covariance = returns.cov().loc[ticker, market_ticker]
market_variance = market_returns.var()
beta_covariance = covariance / market_variance

# Обчислення Бета за допомогою МНК
from scipy.stats import linregress
slope, intercept, r_value, p_value, std_err = linregress(market_returns, asset_returns)
beta_regression = slope

print("Бета-коефіцієнт:")
print(f"  - за допомогою Коваріації: {beta_covariance:.4f}")
print(f"  - за допомогою Регресії МНК: {beta_regression:.5f}")

#
# Візуалізація МНК
#
x_range = np.linspace(market_returns.min(), market_returns.max(), 100)
y_line = beta_regression * x_range + intercept

plt.figure(figsize=(10, 6))
plt.scatter(market_returns, asset_returns, alpha=0.6, label='Помісячна дохідність')
plt.plot(x_range, y_line, color='red',
         label=f'Лінія регресії (Бета = {beta_regression:.4f})')
plt.title(f'Лінійна регресія для обчислення Бета {ticker} vs {market_ticker}')
plt.xlabel(f'Дохідність ринку ({market_ticker})')
plt.ylabel(f'Дохідність акції ({ticker})')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
