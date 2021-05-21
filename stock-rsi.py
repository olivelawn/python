#!/usr/local/bin/python3

# Program takes file with list of stock symbols.
# Program uses yfinance api to pull open/close data for list of symbols and computes RSI

from datetime import datetime, timedelta
import sys
import math
import yfinance as yf
import pandas as pd
import numpy as np
import config
import mysql.connector

def sort_and_print(symbol_percent_list_of_tuples):
  symbol_percent_list_of_tuples.sort(reverse=True)
  for value, symbol in symbol_percent_list_of_tuples:
    print(symbol, value)

def create_stock_table():
  create_stock_table_query = "CREATE TABLE IF NOT EXISTS stocks (date date NOT NULL, PRIMARY KEY (date))"
  cursor.execute(create_stock_table_query)
  cnx.commit()
   
def does_column_exist(column):
  column_exist_query = "SHOW COLUMNS FROM stocks LIKE '{}'".format(column)
  cursor.execute(column_exist_query)
  cursor.fetchall()
  return(cursor.rowcount)

def add_column(column):
  add_column_query = "ALTER TABLE stocks ADD `{}` FLOAT".format(column)
  cursor.execute(add_column_query)
  cnx.commit()

def insert_rsi(date, stocktuple):
  rsivals = str()
  stocks = str()
  count = 0
  for rsival, stock in stocktuple:
    if count == 0:
      rsivals = str(rsival)
      stocks = "`" + stock + "`"
    else:
      rsivals = rsivals + ", " + str(rsival)
      stocks = stocks + ", " + "`" + stock + "`"
    count = count + 1

  insert_rsi_query = "INSERT into stocks(date, {}) value('{}', {})".format(stocks,date,rsivals)
  try:
    cursor.execute(insert_rsi_query)
    cnx.commit()
  except mysql.connector.Error as err:
    print("Exception caught with mysql.connector, skipping mysql transaction: {}".format(err))

#main
cnx = mysql.connector.connect(user=config.USER, password=config.PASS, host=config.HOST, database=config.MYDB, auth_plugin='mysql_native_password')
cursor = cnx.cursor()

args_list = sys.argv
del args_list[0]
symbol_rsi_list_of_tuples=list()
rsi_period = 14 

#filename="symbols-test"
filename=args_list[0]

today = datetime.today()
today_minus_three_months = today - timedelta(365/4)
today_Y_M_D = datetime.today().strftime('%Y-%m-%d')

with open(filename) as f:
    symbol_list = [line.rstrip() for line in f]
#print(symbol_list)

# create stock table
create_stock_table()

# could be more elegant with try/except. Adding a new column if dne.
# this adds stock tickers as columns in stocks table
for symbol in symbol_list:
  if not does_column_exist(symbol):
    add_column(symbol)

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

insert_rsi(today_Y_M_D, symbol_rsi_list_of_tuples)
sort_and_print(symbol_rsi_list_of_tuples)
