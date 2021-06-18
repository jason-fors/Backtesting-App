import gzip
import os



def unzipAndAppend(year, date, ticker, thisFile):
    nextFile = "C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\fut_trades_1min\\" + year + "\\" + date + "\\" + ticker + "\\" + thisFile
    with gzip.open(nextFile, 'rb') as unzippedFile:     # Opens a .gz file
        file_content = unzippedFile.read()
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "a") as f:  # Appending records from unzipped file to aggregate file. 
        f.write(file_content)
        file_content.close()  # Close file to prevent memory leak

def getFileLength(file):
    print("Called getFileLenth method, which has not been defined yet.")


if __name__ == "__main__":
    folderPath = "C:\\Users\\Jason Fors\\Documents\\GitHub\\Python-Projects"
    folderDirectory = os.listdir(path=folderPath)
    
    for i in folderDirectory:
        longest = 0
        
        if ".txt" in i:
            fullPath = os.path.join(folderPath, i)
            print(fullPath + "\n Seconds since the Epoch: " + str(os.path.getmtime(fullPath)))




