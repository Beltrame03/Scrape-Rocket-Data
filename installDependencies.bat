@echo off
title script
echo Installing python dependencies: Beautiful Soup, String, Requests and xlsxwriter.

echo This script will take a while to run as it is searching through ~720 links. 

echo This requires python 3 to run. 

pip3 install Bs4
pip3 install string
pip3 install requests
pip3 install xlsxwriter

python getRocketData.py

echo Look in the directory that this file is in and you will find an Excel Spreadsheet containing all of the data scraped.
pause