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

def sort_and_print(symbol_percent_list_of_tuples):
  symbol_percent_list_of_tuples.sort(reverse=True)
  for value, symbol in symbol_percent_list_of_tuples:
    print(symbol, value)

def print_actual_dates(start_date, end_date):
  print("Actual start date:", start_date.date())
  print("Actual end date:", end_date.date())
  
args_list = sys.argv
del args_list[0]
symbol_percent_list_of_tuples=list()

filename=args_list[0]
str_start_date=args_list[1]
str_end_date=args_list[2]

#filename="symbols-ugh"
#str_start_date="2020-04-14"
#str_end_date="2020-04-14"

with open(filename) as f:
    symbol_list = [line.rstrip() for line in f]

print(symbol_list)

#convert string to a datetime object. not strictly neccesary. could also just pass date as a string to yf.download
start_datetime_object_day = datetime.strptime(str_start_date, '%Y-%m-%d').date()
end_datetime_object_day = datetime.strptime(str_end_date, '%Y-%m-%d').date()

start_datetime_object = datetime.strptime(str_start_date, '%Y-%m-%d')
end_datetime_object = datetime.strptime(str_end_date, '%Y-%m-%d')

today_datetime_object = datetime.today().date()

todayonly=False
range_not_ending_today=False

if start_datetime_object_day == today_datetime_object and end_datetime_object_day == today_datetime_object:  #looking for just 1 day!
  todayonly=True

if start_datetime_object_day != today_datetime_object and end_datetime_object_day != today_datetime_object:   #looking for range, but range does not include today
  range_not_ending_today=True

if todayonly:
  data = yf.download(symbol_list, period="1d")
  for symbol in symbol_list:
    open_price=data.iloc[len(data)-1].Open.loc[symbol]
    close_price=data.iloc[len(data)-1].Close.loc[symbol]
    percent_chg = get_change(close_price, open_price)
    percent_chg_rounded = round(percent_chg, 2)
    symbol_percent_list_of_tuples.append((percent_chg_rounded, symbol))

  print_actual_dates(start_datetime_object, end_datetime_object)
  sort_and_print(symbol_percent_list_of_tuples)


if range_not_ending_today:
  data = yf.download(symbol_list, start=start_datetime_object_day, end=end_datetime_object_day)
  #There is a whole bunch of wonkiness going on I don't totally understand. Some Stocks return nan values.
  #Gonna cycle through each and make sure none of them are doing that.
  screwed_up_data_flag=False

  for symbol in symbol_list:
    open_price=data.iloc[0].Open.loc[symbol]
    close_price=data.iloc[len(data)-1].Close.loc[symbol]

    if math.isnan(open_price) or math.isnan(close_price):
      screwed_up_data_flag=True

  #Fortunately the API is smart enough to grab data either on the dates specified or between the dates specified 
  # (if for instance a weekend date is passed as the end dates, it will grab the preevious friday's close data)

  actual_start_date=data.iloc[0].name                   #grab timestamp of 1st day in panda
  if screwed_up_data_flag:
    actual_end_date=data.iloc[len(data)-2].name           #grab timestamp of last day in panda
    print("Nan Values Detected...look at dates carefully")
  else:
    actual_end_date=data.iloc[len(data)-1].name

  print_actual_dates(actual_start_date, actual_end_date)

  for symbol in symbol_list:
    open_price=data.iloc[0].Open.loc[symbol]
    close_price=data.loc[actual_end_date].Close.loc[symbol]
  
    if math.isnan(open_price) or math.isnan(close_price): 
      print("nan value detected for symbol:", symbol +"...omitting from results. End date too soon? Stock exist on specified dates?")
    else:
      percent_chg = get_change(close_price, open_price)
      percent_chg_rounded = round(percent_chg, 2)
      symbol_percent_list_of_tuples.append((percent_chg_rounded, symbol))

  sort_and_print(symbol_percent_list_of_tuples)
