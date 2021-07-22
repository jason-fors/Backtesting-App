""" Create Backtesting tool
Use GUI window 
Test initial algorithm
Make testing adaptable for testing different algorithms.

Consider developing approach for optimizing along certain parameters.

Looking at a deviation where:
YM (Dow) - Tick Size = $5
ES (S&P) - tick size = $0.25
Net change from previous close, $0.25 increments.

(delta ES * 50) - (delta YM * 5) = Deviation

Dow is roughly 8 times S&P.  Why only 

Different Regimes: Sunday, Monday-Wednesday, Friday

Rules:
1. 6pm - 9pm - Mean Reversion
After 10pm - Deviation trend - Following
$100 gain or loss
Change in deviation

Opens: 6pm EST
Closes: 5pm EST
Week is 6pm Sun to 5pm Fri


previousDayDeviationES = finalPreviousES - currentES
previousDayDeviationYM = finalPreviousYM - currentYM

Shape of previous day: maxDev, minDev, zeroCrossings, rangeYM, rangeES



So, we're going to cycle through each day, and starting with day 2, check against the previous day for:
1. 




"""


from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import shutil
import os
import time





source = ""
destination = ""

class ParentWindow(Frame):
    def __init__(self, window):
        Frame.__init__(self)

        # Main window features
        self.window = window 
        self.window.resizable(width=True, height=True) 
        self.window.title("File Archiver")
        self.window.config(bg='#EEE')  

        # Declare string variable within tkinter
        #self.source = StringVar()  

        # For assigning value to variable in tkinter
        #self.source.set('Source Directory: ')     

        # Labels with font, font size, foreground and background colors, placement and padding
        self.lblFName = Label(self.window,text="Source Directory: ", font = ("Helvetica", 14), fg = "black", bg = "#EEE")
        self.lblFName.grid(row=0, column=2, padx=(30,0), pady=(30,0), sticky=SW)  # Padding on left and right, top and bottom

        self.lblLName = Label(self.window,text="Destination Directory: ", font = ("Helvetica", 14), fg = "black", bg = "#EEE")
        self.lblLName.grid(row=2, column=2, padx=(30,0), pady=(30,0), sticky=SW)  # Typically place with grid or pack

        # Text boxes with font, font size, foreground and background colors, placement and padding
        self.sourcedir = Text(self.window, width = 80, height = 1, font = ("Helvetica", 10), fg='black', bg="#FFF")
        self.sourcedir.grid(row=1, column=2, rowspan=1, columnspan=2, padx=(20,10), pady=(0,0), sticky = W)
        self.sourcedir.insert(1.0, '')

        self.destdir = Text(self.window, width = 80, height = 1, font = ("Helvetica", 10), fg='black', bg="#FFF")
        self.destdir.grid(row=3, column=2, rowspan=1, columnspan=2, padx=(20,10), pady=(0,0), sticky = W)
        self.destdir.insert(1.0, '')

        # Buttons with size, command, placement and padding
        self.btnsource = Button(self.master, text="Browse...", width=12, height=1, command=self.set_source)
        self.btnsource.grid(row=1, column=1, padx=(20,0), pady=(0,0), sticky = NE)  # Sticky northeast
        
        self.btndestination = Button(self.master, text="Browse...", width=12, height=1, command=self.set_dest)
        self.btndestination.grid(row=3, column=1, padx=(20,0), pady=(0,0), sticky = NE)  

        self.btnArchive = Button(self.master, text="Archive", width=12, height=2, command=self.archive)
        self.btnArchive.grid(row=4, column=3, padx=(0,10), pady=(10,10), sticky = NE)          
        
        self.btnClose = Button(self.master, text="Cancel", width=12, height=2, command=self.cancel)
        self.btnClose.grid(row=4, column=3, padx=(0,0), pady=(10,10), sticky = NW)  

    def set_source(self):
        """ invoke a dialog modal which will allow users the ability to select a source directory from their system """
        self.directory = fd.askdirectory()
        self.sourcedir.delete(1.0,END)                        # Emptying text box before inserting new content.
        self.sourcedir.insert(1.0, "{}".format(self.directory))  # To show the source path in the text box        
        
        #self.lblDisplay.config(text="Directory: {}".format(self.directory))  # To change something in window while it's running, use config        

    def set_dest(self):
        """ invoke a dialog modal which will allow users the ability to select a source directory from their system """
        self.directory = fd.askdirectory()
        self.destdir.delete(1.0,END)                            # Emptying text box before inserting new content.
        self.destdir.insert(1.0, "{}".format(self.directory))   # To show the source path in the text box
       
    def archive(self):
        " converts source and destination dircectories to usable paths, and archives files that have been modified more than one day ago "
        # Get path from text boxes
        source = self.sourcedir.get(1.0,END)            
        destination = self.destdir.get(1.0,END)
        source = source.rstrip() + "/"                  # Remove new lines from end of path
        destination = destination.rstrip() + "/"        # Remove new lines from end of path

        if source == destination:
            messagebox.showinfo("Update Aborted","Your source and destination dirctories are the same. \nCheck and try again.")
        else:
            try:
                files = os.listdir(source)
                files_moved = 0                 # To count number of files archived
                for i in files:
                    fullPath = os.path.join(source, i)
                    secondsSinceModified = time.time() - os.path.getmtime(fullPath) # Calculating seconds since modified.
                    print(secondsSinceModified)
                    if (secondsSinceModified < 86400):  # If less than one day
                        shutil.move(source+i, destination) # move the selected files to a new destination
                        files_moved += 1
                        
                messagebox.showinfo("Update Complete","Update Successful. You archived {} files.".format(files_moved))
            except:
                messagebox.showinfo("Update Failed","Please use browse buttons to select directories. \nCancelling the archive.")        

    def cancel(self):
        self.master.destroy()  # Closes window
    

def runTest():
    # Establishing global variables here due to all the conditional logic
    global netReturns
    global sellStatus
    global buyStatus
    global holding
    global winBuyValue
    global loseBuyValue
    global winSellValue
    global loseSellValue
    global deviation
    global dayCount
    global buyValue
    global winThreshold
    global loseThreshold
    global day
    global buyReturns
    global sellReturns

    # For iterative testing
    global deltaES
    global deltaYM
    global priceYM
    global priceES
    global previousDayES
    global previousDayYM
    global previousHour
    global minute
    global tradeCount    

    dayComplete = True  # Need a previous day status to start test, so start first day as True and cycle through to next day.
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "rt") as allRecords:  
        file_content = allRecords.readlines()
        testBuySellValue = 50.0
        testWinThreshold = 400.0
        testLoseThreshold = 390.0
        for testWinThreshold in range(400,411,10):
            netReturns = 0
            winThreshold = testWinThreshold
            loseThreshold = testLoseThreshold
            buyValue = testBuySellValue
            sellValue = -testBuySellValue
            deviation = 0.00                
            deltaES = 0                     
            deltaYM = 0                     
            priceYM = 28548.00              
            priceES = 3236.25                
            buyStatus = False               
            sellStatus = False              
            previousDayES = 0.00            
            previousDayYM = 0.00            
            winBuyValue = 100.00            
            loseBuyValue = -20.00           
            winSellValue = -100.00          
            loseSellValue = 20.00           
            previousHour = 0                
            holding = 0.00                  
            minute = "0:00"
            day = "20200101"                 
            dayCount = 0                    
            netReturns = 0.00
            buyReturns = 0.00
            sellReturns = 0.00     
            tradeCount = 0          
            i = 0  
            k = 0                                                                             # For testing
            for line in file_content:
                #print("Next Line.")
                if dayComplete == True:
                    k += 1
                    #print(k)
                    dayComplete = checkNewDay(line)
                    #print("Day complete status: {0}".format(dayComplete))                                   # For testing
                    if dayComplete == True:
                        continue
                    #else:
                        #dayCount += 1
                        #print("That was Date: {0}".format(day))
                        #print("Processing first line of new day.")
                i += 1                                                                               # For testing
                #if i > 2000:                                                                               # For testing
                #       break
                #if tradeCount > 30:
                #     break                                                                               # For testing
                if (processLine(line)):
                    #print("Doing continue. Next thing should be 'Price of...is'.")
                    continue
                deviation = (deltaES * esMult) - (deltaYM * ymMult)
                #print("Deviation: {0}".format(deviation))
                if buyStatus == True:
                    if (deviation >= winBuyValue or deviation <= loseBuyValue):
                        result = closeBuy()
                        #print("Closing buy. Return is {0}".format(result))
                        if (result > 2000 or result < -2000):
                            print("Something went wrong. Change of {0}".format(result))
                        buyReturns += result
                        netReturns += result
                        #print("Total returns = {0}".format(netReturns))
                        buyStatus = False
                        dayComplete = True
                    else:
                        checkNewDay(line)
                        continue
                elif sellStatus == True:
                    if (deviation <= winSellValue or deviation >= loseSellValue):
                        result = closeSell()
                        #print("Closing sell. Return is {0}".format(result))
                        if (result > 2000 or result < -2000):
                            print("Something went wrong. Change of {0}".format(result))
                        sellReturns += result                        
                        netReturns += result
                        #print("Total returns = {0}".format(netReturns))
                        sellStatus = False
                        dayComplete = True
                    else:
                        checkNewDay(line)
                        continue
                else:
                    if deviation >= buyValue:
                        buyStatus = True
                        tradeCount += 1
                        #print("Changing buy status to true.")
                        #print("Price of ES is {0}.  Price of YM is {1}".format(priceES, priceYM))
                        #print("Change in ES is {0}.  Change in YM is {1}".format(deltaES, deltaYM))
                        winBuyValue = deviation + winThreshold
                        loseBuyValue = deviation - loseThreshold
                        holding = 50 * priceES - 5 * priceYM
                        #print("Holding value is: {0}".format(holding))
                    elif deviation <= sellValue:
                        sellStatus = True
                        tradeCount += 1
                        #print("Changing sell status to true.")
                        #print("Price of ES is {0}.  Price of YM is {1}".format(priceES, priceYM))
                        #print("Change in ES is {0}.  Change in YM is {1}".format(deltaES, deltaYM))
                        winSellValue = deviation - winThreshold
                        loseSellValue = deviation + loseThreshold
                        holding = -50 * priceES + 5 * priceYM
                        #print("Holding value is: {0}".format(holding))
                    #else:
                        #print("No buy/sell status.")
                checkNewDay(line)
            #print (k)
            #print (i)
            print ("For Open Threshold={0} and Win Threshold={1}, Lose Threshold={2} Total returns={3}. Buy returns={4}.  Sell returns={5}".format(buyValue, winThreshold, loseThreshold, netReturns, buyReturns, sellReturns))
            print ("Trade count = {0}".format(tradeCount))
        allRecords.close()
        print("Day count = {0}".format(dayCount))


def checkNewDay(line):
    #print("Checking new day.")
    checkNewDayFields = line.split(",")
    #print(fields[2])
    timeString = str(checkNewDayFields[4])
    endIndex = timeString.find(":")
    hour = int(timeString[0:endIndex])
    #print("Hour: {0}".format(hour))
    global previousHour
    global previousDayYM
    global previousDayES
    global priceYM
    global priceES
    global dayCount
    if (previousHour <= 16 and hour >=17):
        closeOpenPositions()
        #print("Date: {0}".format(day))
        previousHour = hour
        #print("Previous hour: {0}".format(previousHour))
        previousDayYM = priceYM
        #print("Previous day Dow price: {0}".format(previousDayYM))
        previousDayES = priceES
        #print("Previous day S&P price: {0}".format(previousDayES))
        dayCount += 1
        return False
    else:
        #print("In checkNewDay else statement.")
        previousHour = hour
        #print("Previous hour: {0}".format(previousHour))
        updatePrices(line)
        return True


def processLine(line):
    global priceES
    global priceYM
    global previousDayES
    global previousDayYM
    global deltaES
    global deltaYM
    global minute
    global day
    fields = line.split(",")
    ticker = fields[0][0:2]
    price = float(fields[8])
    day = fields[1]
    #print("Price of {0} is: {1}".format(ticker,price))
    if ticker == "ES":
        priceES = price
        deltaES = priceES - previousDayES
    if ticker == "YM":
        priceYM = price
        deltaYM = priceYM - previousDayYM
    # We need to update both tickers each minute before calculating deviations and doing trades.
    #print("Previous minute is {0}, this minute is {1}".format(minute, fields[4]))
    if fields[4] == minute:                         
        #print("Same minute.")
        return False
    else:
        #print("Different minute.")
        minute = fields[4]
        return True


def updatePrices(line):
    global priceES
    global priceYM
    fields = line.split(",")
    ticker = fields[0][0:2]
    price = float(fields[8])
    #print("Price of {0} is: {1}".format(ticker,price))
    if ticker == "ES":
        priceES = price
    if ticker == "YM":
        priceYM = price


def closeOpenPositions():
    global netReturns
    global buyReturns
    global sellReturns
    global buyStatus
    global sellStatus
    if buyStatus == True:
        result = closeBuy()
        #print("End of day closing open buy position. Result is: {0}".format(result))
        buyReturns += result
        netReturns += result
        #print("Total returns = {0}".format(netReturns))
        buyStatus = False
    elif sellStatus == True:
        result = closeSell()
        #print("End of day closing open sell position. Result is: {0}".format(result))
        sellReturns += result
        netReturns += result
        #print("Total returns = {0}".format(netReturns))
        sellStatus = False
    #else:
        #print("End of day. No open positions.")


def closeBuy():
    global holding
    global priceES
    global priceYM
    #print("Closing buy. Price ES is {0}, price YM is {1}.".format(priceES, priceYM))
    closePosition = 50 * priceES - 5 * priceYM
    #print("...holding value is {0}, and close value is {1}".format(holding, closePosition))
    result = closePosition - holding
    return result


def closeSell():
    global holding
    global priceES
    global priceYM
    #print("Closing sell. Price ES is {0}, price YM is {1}.".format(priceES, priceYM))
    closePosition = -50 * priceES + 5 * priceYM
    #print("...holding value is {0}, and close value is {1}".format(holding, closePosition))
    result = closePosition - holding
    return result


        
if __name__ == "__main__":    
    esMult = 50                     # Global variable: Multiplier for Dow for deviation calculation. Constant for now.
    ymMult = 5                      # Global variable: Multiplier for S&P for deviation calculation.  Constant for now.
    winThreshold = 170             # Global variable: Threshold for taking gains.
    loseThreshold = 170             # Global variable: Threshold for taking losses.   
    deviation = 0.00                # Global variable: Net pair deviation from previous day
    deltaES = 0.00                  # Global variable: Change in S&P
    deltaYM = 0.00                  # Global variable: Change in Dow
    priceYM = 28868.00              # Global variable: Latest price of Dow -- establish a starting price, same as end of first day
    priceES = 3261.5                # Global variable: Latest price of S&P -- establish a starting price, same as end of first day
    buyStatus = False               # Global variable: Do we have on open 'sell' position?
    sellStatus = False              # Global variable: Do we have on open 'buy' position? 
    previousDayES = 0.00            # Global variable: ES value at previous day's close.
    previousDayYM = 0.00            # Global variable: YM value at previous day's close.
    buyValue = 60.00                # Global variable: Value to trigger "buy". Constant for now.
    winBuyValue = 100.00            # Global variable: Value to take profit on buy
    loseBuyValue = -20.00           # Global variable: Value to take loss on buy
    sellValue = -60.00              # Global variable: Value to trigger "sell". Constant for now.
    winSellValue = -100.00          # Global variable: Value to take profit on buy
    loseSellValue = 20.00           # Global variable: Value to take loss on buy
    previousHour = 0                # Global variable: Hour of previous recorded trade
    holding = 0.00                  # Global variable: Value of contracts at purchase
    minute = "0:00"                 # Global variable: Minute of transaction. (Need to remember through iterations of processing lines.)
    dayCount = 0                    # Global variable: Running count of trading days
    netReturns = 0.00               # Global variable: Total profit/loss
    buyReturns = 0.00               # Global variable: Total profit/loss on buy positions
    sellReturns = 0.00              # Global variable: Total profit/loss on sell positions
    tradeCount = 0                  # For tracking how many contracts are bought/sold



    runTest()    

    # Launching GUI Window and keeping it open
    # root = Tk()
    # mainWindow = ParentWindow(root)
    # root.mainloop()

