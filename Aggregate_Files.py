import gzip
import os




def unzipAndAppend(year, date, ticker, thisFile):
    nextFile = "C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\fut_trades_1min\\" + year + "\\" + date + "\\" + ticker + "\\" + thisFile
    with gzip.open(nextFile, 'rt') as unzippedFile:     # Opens a .gz file
        file_content = unzippedFile.read()
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "a") as f:  # Appending records from unzipped file to aggregate file. 
        f.write(file_content)
        file_content.close()  # Close file to prevent memory leak


if __name__ == "__main__":
    




