#!/usr/local/bin/python3

# Program takes 3 arguments. File with list of stock symbols, 1 per line and 2 dates in format 2020-02-20.
# Program uses yfinance api to pull open/close data for list of symbols for specified time and computes % chg.

from datetime import datetime, timedelta
import sys
import yfinance as yf

def get_change(current, previous):
  if current == previous:
      return 0
  try:
      return (current - previous) / previous * 100.0
  except ZeroDivisionError:
      return float('inf')

args_list = sys.argv
del args_list[0]
symbol_percent_list_of_tuples=list()
filename=args_list[0]
str_start_date=args_list[1]
str_end_date=args_list[2]

with open(filename) as f:
    symbol_list = [line.rstrip() for line in f]

print(symbol_list)

start_datetime_object = datetime.strptime(str_start_date, '%Y-%m-%d')
end_datetime_object = datetime.strptime(str_end_date, '%Y-%m-%d')
dd = timedelta(days=-1)
end_datetime_object = end_datetime_object + dd

data = yf.download(symbol_list, start=str_start_date, end=str_end_date)

for symbol in symbol_list:
  open_price=data.loc[str_start_date].Open.loc[symbol]
  close_price=data.loc[end_datetime_object.date()].Close.loc[symbol]
  
  percent_chg = get_change(close_price, open_price)
  percent_chg_rounded = round(percent_chg, 2)
  symbol_percent_list_of_tuples.append((percent_chg_rounded, symbol))

symbol_percent_list_of_tuples.sort(reverse=True)
for value, symbol in symbol_percent_list_of_tuples:
  print(symbol, value)
