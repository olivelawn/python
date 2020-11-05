#!/bin/bash

HOUR=$(date +%H)

# /etc/rc.local calls this on boot. 
# Azure runbooks power vm up for about 3 mins/day to execut this and power down
# Only want to run this when my azuer vm boots M-F just before market opens.
# Otherwise need to boot outside of these hours for db maintenance
if (($HOUR >= 9 && $HOUR < 10)); then
  sleep 20
  source config.sh
  /home/$MYHOME/python-analyze-stock-market/stock-rsi.py /home/$MYHOME/python-analyze-stock-market/symbols | grep -v completed | mail -s "Daily RSI" $MYEMAIL
fi
