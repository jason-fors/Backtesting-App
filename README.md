# Backtesting-App


### Aggregate_Files
Goes through all the files purchased from vendor and aggregates the desired case data into one file. 
This required:
1. Trarversing the (2,273) files in the folder structure (3 layers deep, 1,193 folders) and:
    a. Cycling through for each ticker (ES or YM) within each day,
    b. Identifying which contract makes the most sense for that day (the file with the most records should work)
    c. Add those records into an aggregate file.
2. Repeat this process for each ticker, putting them all in one file. 

The data files were compressed with .gz.  Needed to use gzip library in Python.

### Backtesting Tool
Will allow for testing pairs trading algorithms on the year of by-minute ticker data.

