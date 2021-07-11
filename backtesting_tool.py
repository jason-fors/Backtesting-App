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
    with open('C:\\Users\\jason\\OneDrive\\Documents\\Old PC\\Model_Test\\AllRecords.csv', "rt") as allRecords:  
            file_content = allRecords.readlines()
            while dayComplete == True:
                if checkNewDay() == False:
                    continue
                else:
                    dayComplete == False
                for line in file_content:
                    processLine(line)
                    deviation = (deltaES * esMult) + (deltaYM * ymMult)
                    if buyStatus == True:
                        if (deviation >= winBuyValue or deviation <= loseBuyValue):
                            global netReturns
                            netReturns += deviation
                            global buyStatus
                            buyStatus = False
                            dayComplete = True
                        else:
                            continue
                    elif sellStatus == True:
                        if (deviation <= winSellValue or deviation >= loseSellValue):
                            global netReturns
                            netReturns -= deviation
                            global sellStatus
                            sellStatus = False
                            dayComplete = True
                        else:
                            continue
                    else:               
                        if deviation >= buyValue:
                            global buyStatus
                            buyStatus = True
                        elif deviation <= sellValue:
                            global sellStatus
                            sellStatus = True
                        else:
                            continue

            allRecords.close()
            return netReturns


def checkNewDay(line):
    fields = line.split(",")
    hour = fields[2[0:2]]
    global previousHour
    if (previousHour <= 22 and hour >=23):
        previousHour = hour
        global previousDayYM
        previousDayYM = priceYM
        global previousDayES
        previousDayES = priceES
        return True
    else:
        previousHour = hour
        return False


def processLine(line):
    fields = line.split(",")
    ticker = fields[1[0:2]]
    print(ticker)
    global price
    price = fields[8]
    print(price)
    if ticker == "ES":
        global priceES
        priceES = price
        global deltaES
        deltaES = priceES - previousDayES
    if ticker == "YM":
        global priceYM
        priceYM = price
        global deltaYM
        deltaYM = priceYM - previousDayYM


        
if __name__ == "__main__":    
    netReturns = 0                  # Global variable: Total profit/loss
    esMult = 50                     # Global variable: Multiplier for Dow for deviation calculation
    ymMult = 5                      # Global variable: Multiplier for S&P for deviation calculation
    deltaES = -9999                 # Global variable: Change in S&P
    deltaYM = -9999                 # Global variable: Change in Dow
    priceYM = 0
    priceES = 0
    buyStatus = False               # Global variable: Do we have on open 'sell' position?
    sellStatus = False              # Global variable: Do we have on open 'buy' position? 
    previousDayES = 0               # Global variable: ES value at previous day's close.
    previousDayYM = 0               # Global variable: YM value at previous day's close.
    buyValue = 40                   # Global variable: Value to trigger "buy"
    winBuyValue = 100               # Global variable: Value to take profit on buy
    loseBuyValue = -20              # Global variable: Value to take loss on buy
    sellValue = -40                 # Global variable: Value to trigger "sell"
    winSellValue = -100             # Global variable: Value to take profit on buy
    loseSellValue = 20              # Global variable: Value to take loss on buy
    previousHour = 0                # Global variable: Hour of previous recorded trade

    total = runTest()    
    print("Total returns = {0}", total)

    # Launching GUI Window and keeping it open
    # root = Tk()
    # mainWindow = ParentWindow(root)
    # root.mainloop()

