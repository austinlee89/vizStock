import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates


# Download the stock data for a given ticker
ticker1 = input("Enter the first stock ticker symbol: ")
ticker2 = input("Enter the second stock ticker symbol: ")
start_date = input("Enter the start date (yyyy-mm-dd): ")
end_date = input("Enter the end date (yyyy-mm-dd): ")
data1 = yf.download(ticker1, start=start_date, end=end_date, actions=True)
data2 = yf.download(ticker2, start=start_date, end=end_date, actions=True)

# Normalize the stock chart by dividing the closing prices with the closing price of the start date
norm_Data1 = data1["Close"] / data1.iloc[0]["Close"]
norm_Data2 = data2["Close"] / data2.iloc[0]["Close"]
# -------end-------

# -------start-------

# Calculate the cumulative sum of dividends starting a start date
cumDiv1 = data1["Dividends"].cumsum()
cumDiv2 = data2["Dividends"].cumsum()

# Add the stock price with cumulative sum of dividends
plusDiv1 = data1["Close"] + cumDiv1
plusDiv2 = data2["Close"] + cumDiv2

# Normalize the stock price that includes the cumulative sum of dividends
normPlusDiv1 = plusDiv1 / plusDiv1[0]
normPlusDiv2 = plusDiv2 / plusDiv2[0]

# -------end-------

# -------start-------

# Normalize the stock chart by dividing the closing prices with the closing price of the start date
norm_Data1 = data1["Close"] / data1.iloc[0]["Close"]
norm_Data2 = data2["Close"] / data2.iloc[0]["Close"]

# Calculate the cumulative return from reinvesting dividends
totalStockPurchased1 = 0
adjDiv1 = np.zeros(len(data1))
numStockTotal1 = np.ones(len(data1))

totalStockPurchased2 = 0
adjDiv2 = np.zeros(len(data2))
numStockTotal2 = np.ones(len(data2))

for i in range(1, len(data1)):
    totalStockPurchased1 = totalStockPurchased1 + adjDiv1[i-1] / data1["Close"][i-1]
    numStockTotal1[i] = numStockTotal1[i] + totalStockPurchased1
    adjDiv1[i] = data1.iloc[i, data1.columns.get_loc("Dividends")] * numStockTotal1[i]
    # print(totalStockPurchased1, numStockTotal1[i], adjDiv1[i])
for i in range(1, len(data2)):
    totalStockPurchased2 = totalStockPurchased2 + adjDiv2[i - 1] / data2["Close"][i - 1]
    numStockTotal2[i] = numStockTotal2[i] + totalStockPurchased2
    adjDiv2[i] = data2.iloc[i, data2.columns.get_loc("Dividends")] * numStockTotal2[i]

# Calculate the normalized cumulative return with dividend reinvested
normDivReinv1 = norm_Data1 * numStockTotal1
normDivReinv2 = norm_Data2 * numStockTotal2

# -------end-------

# Plot the total return of the two tickers
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(12, 8))

ax1.plot(normDivReinv1, label=ticker1)
ax1.plot(normDivReinv2, label=ticker2)
ax1.grid(True)
ax1.legend()
ax1.set_title("Cumulative return with dividends reinvested")

ax2.plot(normPlusDiv1, label=ticker1)
ax2.plot(normPlusDiv2, label=ticker2)
ax2.grid(True)
ax2.legend()
ax2.set_title("Cumulative return with dividends (no reinvestment)")

ax3.plot(norm_Data1, label=ticker1)
ax3.plot(norm_Data2, label=ticker2)
ax3.grid(True)
ax3.legend()
ax3.set_title("Normalized Stock Price only")

plt.tight_layout()
plt.show()
