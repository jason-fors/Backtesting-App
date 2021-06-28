""" Goes through all the files purchased from vendor and aggregates the desired case data into one file. 
This required:
1. Trarversing the (2,273) files in the folder structure (3 layers deep, 1,193 folders) and:
    a. Cycling through for each ticker (ES or YM) within each day,
    b. Identifying which contract makes the most sense for that day (the file with the most records should work)
    c. Add those records into an aggregate file.
2. Repeat this process for each ticker, putting them all in one file. 

The data files were compressed with .gz.  Needed to use gzip library in Python.

"""

import gzip
import os


# Function for appending content from a selected file to the aggregate file
def appendData(iFilePath):
    with gzip.open(iFilePath, 'rt') as unzippedFile:
        file_content = unzippedFile.readlines()
        print(len(file_content))
        unzippedFile.close()
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "a+") as f:  # Writing records from unzipped file to aggregate file. a+ means append and create if it doesn't exist.
        count = 0
        for line in file_content:
            print(line)
            if count != 0:          # Need to skip the first line so we don't get the header row for every file.
                f.write(line)
            count += 1
        f.close()


# Function for finding longest file in a folder.  This will be treated as the active contract for trading on that day.
def findActiveContract(tickerPath):        #  Pass in the current directory
    tickerDirectory = os.listdir(path=tickerPath)
    fileLength = 0
    for i in tickerDirectory:
        if "gz" in i:       # Don't want to include unzipped or any other file types.
            iFilePath = tickerPath + "//" + i
            with gzip.open(iFilePath, 'rt') as nextFile:
                file_content = nextFile.readlines()
                print(iFilePath)
                print("Length of next file: ")
                print(len(file_content))
                if len(file_content) > fileLength:
                    fileLength = len(file_content)
                    longestFilePath = iFilePath
                    print(fileLength)
                    print(longestFilePath) 
                nextFile.close()
    return longestFilePath


if __name__ == "__main__":
    # Using nested for loops to cycle through the folder tree structure provided by data vendor
    tradesPath = r'C:\Users\jason\OneDrive\Documents\Old PC\Model_Test\fut_trades_1min'
    tradesDirectory = os.listdir(path=tradesPath)
    for year in tradesDirectory: 
        yearPath = tradesPath + "\\" + year
        yearDirectory = os.listdir(path=yearPath)
        print(yearDirectory)
        for day in yearDirectory:
            dayPath = yearPath + "\\" + day
            dayDirectory = os.listdir(path=dayPath)
            print(dayDirectory)
            for ticker in dayDirectory:
                tickerPath = dayPath + "\\" + ticker
                tickerDirectory = os.listdir(path=tickerPath)
                print(tickerDirectory)
                fileToAppend = findActiveContract(tickerPath)
                print(fileToAppend + " ------ File to append")
                appendData(fileToAppend)
                

