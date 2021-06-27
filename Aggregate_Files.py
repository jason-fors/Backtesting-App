""" Go through all the files purchased from vendor and aggregate the desired case data into one file. 
This will require:
1. Moving through all the (2,273) files in the folder structure (3 layers deep, 1,193 folders) and:
    a. Identifying the correct folders for each ticker (ES or YM) within each day,
    b. Identifying which contract makes the most sense for that day (the file with the most records should work)
    c. Add those records into an aggregate file.
2. Repeat this process for each ticker, putting them all in one file. 

.gz files are compressed.  Need to unzip as well.

"""

import gzip
import os



def unzipAndAppend(year, date, ticker, thisFile):
    nextFile = "C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\fut_trades_1min\\" + year + "\\" + date + "\\" + ticker + "\\" + thisFile
    with gzip.open(nextFile, 'rb') as unzippedFile:     # Opens a .gz file
        file_content = unzippedFile.read()
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "a") as f:  # Appending records from unzipped file to aggregate file. 
        f.write(file_content)
        file_content.close()  # Close file to prevent memory leak


# Function for finding longest file in a folder
def findActiveContract(tickerPath):        #  Pass in the current directory
    tickerDirectory = os.listdir(path=tickerPath)
    for i in tickerDirectory:
        fileLength = 0     # Set initial value to 0. Need to find the file with the most records in each folder -- this will be the most-traded contract.
        if "gz" in i:       # Don't want to include unzipped or any other file types.
            iFilePath = tickerPath + i
            with gzip.open(iFilePath, 'rt') as nextFile:
                file_content = nextFile.read()
                if len(file_content) > fileLength:
                    fileLength = len(file_content)
                    longestFilePath = iFilePath
                    print(longestFilePath) 
                    print(iFilePath)
                nextFile.close()
    return longestFilePath


# Function for appending content from a selected file to the aggregate file
def appendData(iFilePath):
    with gzip.open(iFilePath, 'rt') as unzippedFile:
        file_content = unzippedFile.read()
        print(len(file_content))
        unzippedFile.close()
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "w") as f:  # Writing records from unzipped file to aggregate file. 
        f.write(file_content[1:])       # Need to skip the first line so we don't get a new header line for every file.
        f.close()  




if __name__ == "__main__":
    # Using nested for loops to cycle through the folder tree structure provided by data vendor
    tradesPath = r'C:\Users\jason\OneDrive\Documents\Old PC\Model_Test\fut_trades_1min'
    tradesDirectory = os.listdir(path=tradesPath)
    for year in tradesDirectory: 
        yearPath = tradesPath + "\\" + year
        yearDirectory = os.listdir(path=yearPath)
        print(yearDirectory)
        for day in yearDirectory:
            dayPath = yearDirectory + "\\" + day
            dayDirectory = os.listdir(path=dayPath)
            print(dayDirectory)
            for ticker in dayDirectory:
                tickerPath = dayPath + "\\" + ticker
                tickerDirectory = os.listdir(path=tickerPath)
                print(tickerDirectory)
   
