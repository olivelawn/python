#!/bin/bash

sleep 20
/home/parker/python-analyze-stock-market/stock-rsi.py /home/parker/python-analyze-stock-market/symbols | grep -v completed | mail -s "Daily RSI" pjohn07@yahoo.com
