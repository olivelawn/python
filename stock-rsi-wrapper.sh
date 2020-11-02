#!/bin/bash

HOUR=$(date +%H)

#I only want to run this when my azuer vm boots M-F just before market opens.
#Othrwise I want my VM to not run this when I want to do DB maintenance.
if (($HOUR >= 9 && $HOUR < 10)); then
  sleep 20
  source ./config.sh
  /home/$MYHOME/python-analyze-stock-market/stock-rsi.py /home/$MYHOME/python-analyze-stock-market/symbols | grep -v completed | mail -s "Daily RSI" $MYEMAIL

fi
