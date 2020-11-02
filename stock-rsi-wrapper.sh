#!/bin/bash

sleep 20

source ./config.sh

/home/$MYHOME/python-analyze-stock-market/stock-rsi.py /home/$MYHOME/python-analyze-stock-market/symbols | grep -v completed | mail -s "Daily RSI" $MYEMAIL
