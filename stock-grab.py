#!/usr/local/bin/python3

# Program takes 3 arguments. File with list of stock symbols, 1 per line and 2 dates in format 2020-02-20.
# Program uses yfinance api to pull open/close data for list of symbols for specified time and computes % chg.

from datetime import datetime, timedelta
import sys
import math
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

#convert string to a datetime object. not strictly neccesary. could also just pass date as a string to yf.download
start_datetime_object = datetime.strptime(str_start_date, '%Y-%m-%d')
end_datetime_object = datetime.strptime(str_end_date, '%Y-%m-%d')

data = yf.download(symbol_list, start=start_datetime_object, end=end_datetime_object)

#Fortunately the API is smart enough to grab data either on the dates specified or between the dates specified 
# (if for instance a weekend date is passed as the end dates, it will grab the preevious friday's close data)

actual_start_date=data.iloc[0].name                   #grab timestamp of 1st day in panda
actual_end_date=data.iloc[len(data)-1].name           #grab timestamp of last day in panda
print("Actual start date:", actual_start_date)
print("Actual end date:", actual_end_date)

for symbol in symbol_list:
  open_price=data.iloc[0].Open.loc[symbol]
  close_price=data.iloc[len(data)-1].Close.loc[symbol]
  
  if math.isnan(open_price) or math.isnan(close_price): 
    print("nan value detected for symbol:", symbol +"...omitting from results. End date too soon? Stock exist on specified dates?")
  else:
    percent_chg = get_change(close_price, open_price)
    percent_chg_rounded = round(percent_chg, 2)
    symbol_percent_list_of_tuples.append((percent_chg_rounded, symbol))

symbol_percent_list_of_tuples.sort(reverse=True)
for value, symbol in symbol_percent_list_of_tuples:
  print(symbol, value)
