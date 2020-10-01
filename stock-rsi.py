#!/usr/local/bin/python3

# Program takes file with list of stock symbols.
# Program uses yfinance api to pull open/close data for list of symbols and computes RSI

from datetime import datetime, timedelta
import sys
import math
import yfinance as yf
import pandas as pd
import numpy as np

def sort_and_print(symbol_percent_list_of_tuples):
  symbol_percent_list_of_tuples.sort(reverse=True)
  for value, symbol in symbol_percent_list_of_tuples:
    print(symbol, value)

args_list = sys.argv
del args_list[0]
symbol_rsi_list_of_tuples=list()
rsi_period = 14 

#filename="symbols-test"
filename=args_list[0]

today = datetime.today()
today_minus_three_months = today - timedelta(365/4)

with open(filename) as f:
    symbol_list = [line.rstrip() for line in f]

#print(symbol_list)

data = yf.download(symbol_list, start=today_minus_three_months, end=today)

for symbol in symbol_list:
  chg = data['Close'][symbol].diff(1)
  gain = chg.mask(chg<0,0)
  loss = chg.mask(chg>0,0)
  avg_gain = gain.ewm(com = rsi_period - 1, min_periods = rsi_period).mean()
  avg_loss = loss.ewm(com = rsi_period - 1, min_periods = rsi_period).mean()
  rs = abs(avg_gain/avg_loss)
  rsi = 100-(100/(1+rs))
  rsi_rounded = round(rsi[len(rsi)-1], 2)
  symbol_rsi_list_of_tuples.append((rsi_rounded, symbol))

sort_and_print(symbol_rsi_list_of_tuples)
