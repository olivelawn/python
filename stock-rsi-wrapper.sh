#!/bin/bash

sleep 20
/home/***REMOVED***/python-analyze-stock-market/stock-rsi.py /home/***REMOVED***/python-analyze-stock-market/symbols | grep -v completed | mail -s "Daily RSI" ***REMOVED***
