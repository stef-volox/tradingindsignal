import os
import datetime as dt
import pytz
import matplotlib.pyplot as plt
import pandas_datareader as web
from tradingview_ta import TA_Handler, Interval, Exchange

plt.style.use('dark_background')

sma_20 = 20
sma_50 = 50
sma_200 = 100

invalid_tkr = True
def start():

    print("                    TYPE IN STOCK / CRYPTO:")
    print('\n')
    print("               |Type in only capital letters.")
    print("               |Yahoo! Finance free-license API")
    print("               |For cryptocurrencies add -USD at the end.")
    print("               |E.x. BTC-USD")
    print('\n')

    tkr = input("               TICKER: ")

    btc_data = web.DataReader(tkr, 'yahoo',
                              start = dt.datetime.now() - dt.timedelta(days=365),
                              end = dt.datetime.now())
    btc_data[f'SMA_{sma_20}'] = btc_data['Adj Close'].rolling(window=sma_20).mean()
    btc_data[f'SMA_{sma_50}'] = btc_data['Adj Close'].rolling(window=sma_50).mean()
    btc_data[f'SMA_{sma_200}'] = btc_data['Adj Close'].rolling(window=sma_200).mean()

    print("                    ----------", tkr, "----------")
    print(btc_data)


    pinbar_bear = btc_data['High']-btc_data['Adj Close']
    pinbar_bull = btc_data['Adj Close']-btc_data['Low']
    btc_data['Bullish Pin Bar'] = pinbar_bull*3
    btc_data['Bearish Pin Bar'] = pinbar_bear*3

    for x in range(len(btc_data)):
        btc_data['Close Difference'] = btc_data['Adj Close'].iloc[x-1]-btc_data['Adj Close'].iloc[x]

    bull_signal = []
    bear_signal = []
    trigger1 = 0

    for x in range(len(btc_data)):
        if btc_data['Bullish Pin Bar'].iloc[x] > btc_data['Close Difference'].iloc[x] and trigger1 != 1:
            bull_signal.append(btc_data['Adj Close'].iloc[x])
            bear_signal.append(float('nan'))
            trigger1 = 1
            invalid_tkr = False
        elif btc_data['Bearish Pin Bar'].iloc[x] > btc_data['Close Difference'].iloc[x] and trigger1 != 1:
            bull_signal.append(float('nan'))
            bear_signal.append(btc_data['Adj Close'].iloc[x])
            trigger1 = 1
            invalid_tkr = False
        elif btc_data['Bullish Pin Bar'].iloc[x] < btc_data['Close Difference'].iloc[x] and trigger1 != -1:
            bull_signal.append(float('nan'))
            bear_signal.append(float('nan'))
            trigger1 = -1
            invalid_tkr = False
        elif btc_data['Bearish Pin Bar'].iloc[x] < btc_data['Close Difference'].iloc[x] and trigger1 != -1:
            bull_signal.append(float('nan'))
            bear_signal.append(float('nan'))
            trigger1 = -1
            invalid_tkr = False
        else:
            bull_signal.append(float('nan'))
            bear_signal.append(float('nan'))
            invalid_tkr = False

    btc_data['Bull Signal'] = bull_signal
    btc_data['Bear Signal'] = bear_signal


    buy_signals = []
    sell_signals = []
    trigger = 0

    for x in range(len(btc_data)):
        if btc_data[f'SMA_{sma_20}'].iloc[x] < btc_data[f'SMA_{sma_200}'].iloc[x] and trigger != 1:
            buy_signals.append(btc_data['Adj Close'].iloc[x])
            sell_signals.append(float('nan'))
            trigger = 1
            invalid_tkr = False
        elif btc_data[f'SMA_{sma_20}'].iloc[x] > btc_data[f'SMA_{sma_200}'].iloc[x] and trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(btc_data['Adj Close'].iloc[x])
            trigger = -1
            invalid_tkr = False
        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))
            invalid_tkr = False

    btc_data['Buy Signals'] = buy_signals
    btc_data['Sell Signals'] = sell_signals

    print(btc_data)

    plt.plot(btc_data['Adj Close'], label="Stock Price", color="lightgray")
    plt.plot(btc_data[f'SMA_{sma_20}'], label=f"SMA_{sma_20}", color="orange", linestyle="--")
    plt.plot(btc_data[f'SMA_{sma_50}'], label=f"SMA_{sma_50}", color="blue", linestyle="--")
    plt.plot(btc_data[f'SMA_{sma_200}'], label=f"SMA_{sma_200}", color="red")
    plt.scatter(btc_data.index, btc_data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
    plt.scatter(btc_data.index, btc_data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=3)
    plt.legend(loc="upper left")
    plt.show()

###### STILL IN PROGRESS ######
    btc_tradingview = TA_Handler(
        symbol = "BTCUSDT",
        screener = "crypto",
        exchange = "Binance",
        interval = Interval.INTERVAL_1_DAY)

    analysis = btc_tradingview.get_analysis()

###### STILL IN PROGRESS ######
    #plt.style.use('classic')

    #plt.figure()
    #width = 1
    #width2 = 0.1
    #price_up = btc_data[btc_data.Close>=btc_data.Open]
    #price_down = btc_data[btc_data.Close<btc_data.Open]

    #plt.bar(price_up.index, price_up.Close-price_up.Open, width, bottom=price_up.Open, color="green")
    #plt.bar(price_up.index, price_up.High-price_up.Close, width2, bottom=price_up.Close, color="green")
    #plt.bar(price_up.index, price_up.Low-price_up.Open, width2, bottom=price_up.Open, color="green")

    #plt.bar(price_down.index, price_down.Close-price_down.Open, width, bottom=price_down.Open, color="red")
    #plt.bar(price_down.index, price_down.High-price_down.Open, width2, bottom=price_down.Open, color="red")
    #plt.bar(price_down.index, price_down.Low-price_down.Close, width2, bottom=price_down.Close, color="red")
    #plt.plot(btc_data[f'SMA_{sma_20}'], label=f"SMA_{sma_20}", color="orange")
    #plt.plot(btc_data[f'SMA_{sma_50}'], label=f"SMA_{sma_50}", color="blue")
    #plt.plot(btc_data[f'SMA_{sma_200}'], label=f"SMA_{sma_200}", color="purple")
    #plt.scatter(btc_data.index, btc_data['Bull Signal'], label="Buy Signal", marker="^", color="#6fff00", lw=5)
    #plt.scatter(btc_data.index, btc_data['Bear Signal'], label="Sell Signal", marker="v", color="#ff7100", lw=5)
    #plt.legend(loc="upper left")
    #plt.grid()

    print('\n')
    print("             Would you like to view another stock/crypto?")
    print("             --------------------------------------------")
    print('\n')
    print("             |Y|   or   |N|")
    print('\n')
    select_option = input("             Type answer: ")

    if select_option == "Y":
        print("...Redirecting now...")
        print('\n')
        invalid_tkr = True

    elif select_option == "N":
        invalid_tkr = False
        quit()

    else:
        print("ANSWER INVALID. PLEASE CLICK ON |X| IN THE TOP-RIGHT CORNER OF THE WINDOW TO EXIT.")
        print("...Redirecting now...")
        print('\n')
        invalid_tkr = False

while invalid_tkr == True:
    start()
