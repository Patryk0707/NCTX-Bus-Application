import sqlite3,os.path
import customtkinter as ctk # type: ignore
from datetime import datetime,timedelta
import CSVParser
import passwordManager
from CTkScrollableDropdown import CTkScrollableDropdown
import re

baseDir=os.path.dirname(os.path.abspath(__file__)) #gets the directionary of the python file
dbPath=os.path.join(baseDir,"NCTX Database.db") #uses the directionary of the python file to find the dataabase file
database=sqlite3.connect(dbPath) #python file connects to the database
cursor=database.cursor() #executes commands(the link from the database to the python file)
hashedPassword = passwordManager.hashPassword("admin")



database.commit()
def getTicketUses(title):

    match = re.search(r"\bx\s*(\d+)\b|\b(\d+)\s+trips?\b", title, re.IGNORECASE)

    if match:
        return int(match.group(1) or match.group(2))

    return 1


class adminView(ctk.CTkFrame): #this is the page the admin sees when logging in
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1) #these two configure columns so widgets expand evenly
        self.grid_columnconfigure(1, weight=1)
        try:    #tries loading the csv file containing the ticket data
            self.rows,self.fieldnames=CSVParser.loadCSVRows()
        except FileNotFoundError:   #if the csv file is missing it will alert the user
            dialogBox(self.root,"CSV Error","mobile_products.csv file not found, please ensure it is stored in the same folder as the python file")
            self.rows=[]
            self.fieldnames=[]
        except Exception: #any other error it will also alert the user
            dialogBox(self.root,"CSV Error","The CSV file could not be read")
            self.rows=[] 
            self.fieldnames=[] #prepares drop down options for ticket data
        self.ticketOptions=[]
        self.indexByOption={}
        for i,r in enumerate(self.rows):
            title=r.get("topup_title","unknown")#reads the title
            option=title
            if option in self.indexByOption:
                option=f"{option}" #if duplicate titles exist it wont overwite the dictonary keys
            self.ticketOptions.append(option)
            self.indexByOption[option]=i    #stores the index
        self.ticketSelect = ctk.CTkComboBox(self,width=420,state="readonly")
        self.ticketSelect.set("Select Ticket")
        self.ticketSelect.grid(row=1, column=0, columnspan=2,padx=20, pady=10, sticky="ew")
        self.ticketDropdown = CTkScrollableDropdown(self.ticketSelect,values=["Select Ticket"] + self.ticketOptions,height=250,resize=False,scrollbar=True,justify="left",command=self.ticketChange)
        self.currentPriceText=ctk.CTkLabel(self,text="Current Price: -")#shows current price of ticket
        self.currentPriceText.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        self.newPrice=ctk.CTkEntry(self,placeholder_text="Set New price in £")#shows new price of ticket
        self.newPrice.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.saveButton=ctk.CTkButton(self,text="Save Price",command=self.saveNewPrice)#saves new price into csv
        self.saveButton.grid(row=3, column=1, padx=20, pady=(5, 10), sticky="ew")
        self.selectedRowIndex=None #stores which csv row is currently selected(none until row is selected)
        self.logoutButton=ctk.CTkButton(self,text="Logout",command=self.root.homeViewVisible)#returns the user back to the home screeen
        self.logoutButton.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="ew")

    def ticketChange(self,choice):
        if choice=="Select Ticket":#if the user goes back to select ticket in dropdown
            self.selectedRowIndex=None
            self.currentPriceText.configure(text="Current Price: -")
            return
        self.selectedRowIndex=self.indexByOption.get(choice)#looks up the corresponding CSV row matching the choice
        if self.selectedRowIndex is None:   #if theres no match it will display a current price of -
            self.currentPriceText.configure(text="Current Price: -")
            return
        row = self.rows[self.selectedRowIndex]#retrieves the selected row from the csv ticket data
        busTicketInPence = row.get("topup_price_in_pence", "0")
        try:#converts pence into pounds
            BusTicketInPounds=int(busTicketInPence)/100
            self.currentPriceText.configure(text=f"Current Price: £{BusTicketInPounds:.2f}")
        except Exception:
            dialogBox(self.root,"Error In Changing Price","Invalid Input Please Try Again")

    def saveNewPrice(self):#user must select a ticket before saving price
        if self.selectedRowIndex is None:
            dialogBox(self,"Select Ticket","Please select a ticket first.")
            return
        newPriceInPounds=self.newPrice.get().strip().replace("£","")#removes pound symbol if typed
        try:
            newPriceInPoundsFloat=float(newPriceInPounds)
        except:
            dialogBox(self,"Invalid Price", "Enter A Valid Number")#prevents any other input
            return
        if newPriceInPoundsFloat < 0:
            dialogBox(self, "Invalid Price", "Price cannot be negative.")#prevents negative numbers
            return
        newPriceInPence=int(round(newPriceInPoundsFloat*100))#converts pounds into pence
        try:
            self.rows[self.selectedRowIndex]["topup_price_in_pence"]=str(newPriceInPence)#updates the csv price to have the new price
            CSVParser.saveCSVRows(self.rows,self.fieldnames)#saves the file
        except Exception:
            dialogBox(self,"Save Error","Could not write the updated price to the CSV.")
            return
        self.currentPriceText.configure(text=f"Current Price: £{newPriceInPoundsFloat:.2f}")#updates user interface to show updated price
        self.newPrice.delete(0, "end")
        dialogBox(self, "Success", "Ticket price updated in CSV.")

class manageTicketsView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.chooseTickets=ctk.CTkComboBox(self,values=["Choose Ticket Group","Valid Tickets","Used Tickets"],width=170,command=self.refreshLists)#lets the user either see valid or used tickets
        self.chooseTickets.grid(row=0,column=0,pady=(10,10))
        self.backButton=ctk.CTkButton(self,text="Back",command=self.root.userViewVisible)
        self.backButton.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="n")
        self.displayTicketsFrame=ctk.CTkScrollableFrame(self, width=700, height=500)#scrollable frame so the user can see all their tickets even when theres numerous tickets
        self.displayTicketsFrame.grid(row=2,column=0,columnspan=2,sticky="nsew",padx=20,pady=(0, 20))
        self.displayTicketsFrame.grid_columnconfigure(0,weight=1)

    def usedTickets(self,purchaseID:int):
        usedTicketDate=datetime.now()
        usedTicketDateString=usedTicketDate.strftime("%d/%m/%y %H:%M")
        cursor.execute("SELECT Duration,TotalUses,RemainingUses FROM Purchases WHERE PurchaseID=? AND Username=? AND RemainingUses>0",(purchaseID,self.root.loginUsername))#checks if ticket is unused and belongs to the user which is logged in
        row=cursor.fetchone()
        if not row:
            dialogBox(self,"Error","Ticket Already Used")
            return
        duration=int(row[0])
        totalUses = row[1]
        remainingUses = row[2]
        useNumber = totalUses - remainingUses + 1
        if duration==10:
            ticketExpiryDate=usedTicketDate+timedelta(minutes=duration)#instead of days it uses minutes since its a single ticket
        else:
            ticketExpiryDate=usedTicketDate+timedelta(days=duration)#gets the expiry date by adding the days to the current date and then converting into string
        ticketExpiryDateString=ticketExpiryDate.strftime("%d/%m/%y %H:%M")
        with database:
            cursor.execute("UPDATE Purchases SET RemainingUses=RemainingUses-1 WHERE PurchaseID=? AND Username=? AND RemainingUses>0",(purchaseID,self.root.loginUsername))
            if cursor.rowcount == 0:
                dialogBox(self,"Error","No uses remaining")
                return
            cursor.execute("INSERT INTO TicketUses(PurchaseID,UseNumber,UsedDate,ExpiryDate) VALUES(?,?,?,?)",(purchaseID,useNumber,usedTicketDateString,ticketExpiryDateString))
        database.commit()
        dialogBox(self,"Success",f"Ticket activated! Uses remaining: {remainingUses-1}")
        self.self.after(200, self.refreshLists)()

    def refreshLists(self,choice=None):
        if choice is None:
            choice=self.chooseTickets.get()
        for w in self.displayTicketsFrame.winfo_children():#clears previous entries
            w.destroy()
        username=self.root.loginUsername
        if choice=="Valid Tickets":
            cursor.execute("SELECT PurchaseID,TicketTitle,Duration,DatePurchased,TotalUses,RemainingUses FROM Purchases WHERE Username=? AND RemainingUses>0 ORDER BY PurchaseID DESC",(username,))
            rows=cursor.fetchall()
            if not rows:
                ctk.CTkLabel(self.displayTicketsFrame,text="No valid tickets").grid(row=0, column=0, pady=10)
                return
            r=0
            for row in rows:
                purchaseID=row[0]
                title=row[1]
                duration=row[2]
                datePurchased=row[3]
                totalUses = row[4]
                remainingUses = row[5]
                usedCount = totalUses - remainingUses
                ctk.CTkLabel(self.displayTicketsFrame,text=title,font=("MS Sans Serif",16)).grid(row=r,column=0,sticky="w",pady=(10,0))
                ctk.CTkLabel(self.displayTicketsFrame,text=f"Purchased: {datePurchased}  Duration: {self.durationFormat(int(duration))}").grid(row=r+1, column=0, sticky="w")
                ctk.CTkLabel(self.displayTicketsFrame,text=f"Uses: {remainingUses}/{totalUses} | Used: {usedCount}").grid(row=r+2,column=0,sticky="w")
                useButton=ctk.CTkButton(self.displayTicketsFrame,text="Use",command=lambda p=purchaseID:self.usedTickets(p))
                useButton.grid(row=r, column=1, rowspan=2, padx=10, pady=10)
                r+=4
        elif choice=="Used Tickets":
            cursor.execute("""SELECT Purchases.PurchaseID, Purchases.TicketTitle,TicketUses.UsedDate, TicketUses.ExpiryDate,TicketUses.UseNumber, Purchases.TotalUses 
            FROM TicketUses JOIN Purchases ON TicketUses.PurchaseID=Purchases.PurchaseID WHERE Purchases.Username=? ORDER BY TicketUses.UseID DESC """,(username,))
            rows=cursor.fetchall()
            if not rows:
                ctk.CTkLabel(self.displayTicketsFrame,text="No used tickets").grid(row=0,column=0,pady=10)
                return
            r=0
            for row in rows:
                purchaseID = row[0]
                title = row[1]
                usedDate = row[2]
                expiryDate = row[3]
                useNumber = row[4]
                totalUses = row[5]
                ctk.CTkLabel(self.displayTicketsFrame,text=f"{title} - Use {useNumber}/{totalUses}",font=("MS Sans Serif",16)).grid(row=r,column=0,sticky="w",pady=(10,0))
                ctk.CTkLabel(self.displayTicketsFrame,text=f"Used: {usedDate} | Expires: {expiryDate}").grid(row=r+1,column=0,sticky="w")
                r += 3
    def durationFormat(self,duration):# if duration is 10 then its displayed as minutes if 1 then day and else its days
        if duration==10:
            return "10 Minutes"
        if duration==1:
            return "1 day"
        return f"{duration} days"
class topUpMoneyView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
        self.backButton=ctk.CTkButton(self,text="Back",command=self.root.userViewVisible)
        self.backButton.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="n")
    def getTopUpValue(self):
        cursor.execute("SELECT BalanceInPennies FROM Users WHERE Username=?",(self.root.loginUsername,))#gets the users balance
        currentMoney=cursor.fetchone()[0]
        ctk.CTkLabel(self,text=f"Current Money: £{currentMoney/100}",fg_color="transparent",text_color="Black",anchor="center",font=("MS Sans Serif",15)).grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.topUp5Button=ctk.CTkButton(self,text="Top Up £5",command=lambda:self.topUp(5))
        self.topUp5Button.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="n")
        self.topUp10Button=ctk.CTkButton(self,text="Top Up £10",command=lambda:self.topUp(10))
        self.topUp10Button.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="n")
        self.topUp15Button=ctk.CTkButton(self,text="Top Up £15",command=lambda:self.topUp(15))
        self.topUp15Button.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")
        self.topUp20Button=ctk.CTkButton(self,text="Top Up £20",command=lambda:self.topUp(20))
        self.topUp20Button.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="n")
        self.topUp50Button=ctk.CTkButton(self,text="Top Up £50",command=lambda:self.topUp(50))
        self.topUp50Button.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="n")
        self.topUp100Button=ctk.CTkButton(self,text="Top Up £100",command=lambda:self.topUp(100))
        self.topUp100Button.grid(row=4, column=1, padx=20, pady=(0, 20), sticky="n")
        self.customTopUp = ctk.CTkEntry(self, placeholder_text="Custom Amount")
        self.customTopUp.grid(row=5,column=0,padx=20,pady=(0,20),sticky="n")
        self.customTopUpButton=ctk.CTkButton(self,text="Top Up In £",command=self.checkCustomAmount)
        self.customTopUpButton.grid(row=5, column=1, padx=20, pady=(0, 20), sticky="n")
    def checkCustomAmount(self):
        topUpValue=self.customTopUp.get()
        if not topUpValue.isdigit():
            dialogBox(self,"Invalid Top Up Value","Please enter a valid number without symbols")
            return
        topUpAmount=int(topUpValue)
        self.topUp(topUpAmount)
    def topUp(self,amountInPounds):
            amountInPennies=amountInPounds*100
            cursor.execute("UPDATE Users SET BalanceInPennies=BalanceInPennies+? WHERE Username=?",(amountInPennies,self.root.loginUsername,))#updates the users balance with the amount they wish to top up with
            database.commit()
            for widget in self.winfo_children():
                if widget is not self.backButton:
                    widget.destroy()
            self.getTopUpValue()



class viewAndBuyTicketsView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.data=self.csv_Reader=CSVParser.csvFile()
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1,weight=1)#dropdown to select ticket category
        self.ticketCategorySelection=ctk.CTkComboBox(self,values=["Choose Category","Single Use Tickets","24 Hour Tickets","7 Day Tickets","31 Day Tickets","Annual Tickets"],command=self.changeWidgets,width=200)
        self.ticketCategorySelection.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.backButton=ctk.CTkButton(self,text="Back",command=self.root.userViewVisible)
        self.backButton.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="n")
        #self.csv_Reader.readCSVForDayTickets()
        self.widgets=ctk.CTkFrame(self)
        self.widgets.grid(row=1,column=0,columnspan=2,padx=20,pady=10,sticky="nsew")

    def changeWidgets(self,choice):
        self.page=0
        self.pageNumber=15#15 tickets per page
        if choice=="Single Use Tickets":
            self.data = self.csv_Reader.readCSVForSingleTickets()
            self.viewTickets(self.data)
        elif choice=="24 Hour Tickets":
            self.data=self.csv_Reader.readCSVForDayTickets()
            self.viewTickets(self.data,showPaging=True)
        elif choice=="7 Day Tickets":
            self.data=self.csv_Reader.readCSVForWeekTickets()
            self.viewTickets(self.data)
        elif choice=="31 Day Tickets":
            self.data=self.csv_Reader.readCSVForMonthTickets()
            self.viewTickets(self.data)
        elif choice=="Annual Tickets":
            self.data=self.csv_Reader.readCSVForYearTickets()
            self.viewTickets(self.data)

    def buyTickets(self,ticket):
        ticketPriceInPennies=int(ticket["price"]*100)
        cursor.execute("SELECT BalanceInPennies FROM Users WHERE Username=?",(self.root.loginUsername,))#gets users balance
        balance=cursor.fetchone()[0]#if not enough money then they wont be able to purchase ticket
        if balance<ticketPriceInPennies:
            dialogBox(self,"Not enough money","You do not have enough money for this ticket.")
            return
        cursor.execute("UPDATE Users SET BalanceInPennies=BalanceInPennies-? WHERE Username=?",(ticketPriceInPennies,self.root.loginUsername))
        database.commit()#reduces balance to take away tickets price
        self.logPurchase(ticket,ticketPriceInPennies)
        dialogBox(self, "Success", f"You have sucessfully bought {ticket['title']}")

    def logPurchase(self,ticket,pricePaidInPennies:int):
        username=self.root.loginUsername
        title=ticket["title"]
        purchasedDate=datetime.now().strftime("%d/%m/%y %H:%M")
        duration=int(ticket.get("duration",0)) #duration set to 0 if missing
        totalUses = getTicketUses(title)
        cursor.execute("INSERT INTO Purchases(Username,TicketTitle,Duration,PricePaidInPennies,DatePurchased,TotalUses,RemainingUses) VALUES(?,?,?,?,?,?,?)",(username,title,duration,pricePaidInPennies,purchasedDate,totalUses,totalUses))
        database.commit()

    def viewTickets(self,tickets,showPaging=False):
        for widget in self.widgets.winfo_children():#clears previous widgets
            widget.destroy()
        if showPaging:
            start=self.page*self.pageNumber
            end=start+self.pageNumber
            pageItems=tickets[start:end]#shows 1st 15 items first
        else:
            pageItems = tickets[:15]
        for i,t in enumerate(pageItems):#layout 3 columns, 5 tickets per column below determines what column the ticket belongs to
                if i<5: 
                    textCol=0
                    buttonCol=1
                    row=i*4
                elif i<10:
                    textCol=2
                    buttonCol=3
                    row=(i-5)*4
                else:
                    textCol=4
                    buttonCol=5
                    row=(i-10)*4
                title=t.get("title","unknown")
                people=t.get("people",1)
                personText = "person" if int(people) == 1 else "people"
                desc=t.get("description","")
                price=t.get("price",0)
                ctk.CTkLabel(self.widgets,text=f"{title}-Valid for: {people} {personText}").grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=desc,wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{price}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda ticket=t:self.buyTickets(ticket)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))
        if showPaging:
            totalPages=(len(self.data)-1)//self.pageNumber+1#footer placed after 5 tickets columns
            footerRow=5*4 
            footer=ctk.CTkFrame(self.widgets,fg_color="transparent") 
            footer.grid(row=footerRow,column=0,columnspan=6,pady=(10,0),sticky="ew")
            footer.grid_columnconfigure((0,1,2),weight=1)
            previousPageButton=ctk.CTkButton(footer,text="Previous Page",command=self.previousPage)#page button and text
            nextPageButton=ctk.CTkButton(footer,text="Next Page",command=self.nextPage)
            currentPageNumber=ctk.CTkLabel(footer,text=f"Page{self.page+1}/{totalPages}")
            previousPageButton.grid(row=0,column=0,sticky="w")
            currentPageNumber.grid(row=0,column=1)
            nextPageButton.grid(row=0,column=2,sticky="e")

            if self.page==0:
                previousPageButton.configure(state="disabled")#disable buttons when at 1st and last page
            if self.page>=totalPages-1:
                nextPageButton.configure(state="disabled")

    def nextPage(self):
        self.page+=1
        self.viewTickets(self.data, showPaging=True)
    def previousPage(self):
        if self.page>0:
            self.page-=1
            self.viewTickets(self.data, showPaging=True)


class userView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)#different buttons navigating to different views
        self.welcomeUserText=ctk.CTkLabel(self,text="",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",15))
        self.welcomeUserText.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.viewAndBuyTicketsButton=ctk.CTkButton(self,text="View And Buy Tickets",command=self.root.buyAndViewTicketsVisible)
        self.viewAndBuyTicketsButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.manageTicketsButton=ctk.CTkButton(self,text="Manage Your Tickets",command=self.root.manageTicketVisible)
        self.manageTicketsButton.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="n")
        self.topupButton=ctk.CTkButton(self,text="Top Up Money",command=self.root.topUpMoneyVisible)
        self.topupButton.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")
        self.logoutButton=ctk.CTkButton(self,text="Log Out",command=self.root.homeViewVisible)
        self.logoutButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")

class loginView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
        self.loginText1=ctk.CTkLabel(self,text="Please Login with your username and password:",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",15))
        self.loginText1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginText2=ctk.CTkLabel(self,text="Username:",fg_color="transparent",text_color="Black",anchor="center",font=("MS Sans Serif",15))
        self.loginText2.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginUsernameBox=ctk.CTkEntry(self,placeholder_text="Username")
        self.loginUsernameBox.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginText3=ctk.CTkLabel(self,text="Password:",fg_color="transparent",text_color="Black",anchor="center",font=("MS Sans Serif",15))
        self.loginText3.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginPasswordBox=ctk.CTkEntry(self,placeholder_text="Password",show="*")
        self.loginPasswordBox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="n")
        self.buttonFrame = ctk.CTkFrame(self, fg_color="transparent")#to avoid the buttons extending the current frame
        self.buttonFrame.grid(row=5, column=0, pady=(0, 20))
        self.loginButton=ctk.CTkButton(self.buttonFrame,text="Login",command=self.usernameAndPasswordGetter)
        self.loginButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")
        self.backButton=ctk.CTkButton(self.buttonFrame,text="Back",command=self.root.homeViewVisible)
        self.backButton.grid(row=5, column=1, padx=20, pady=(0, 20), sticky="n")
        
    def usernameAndPasswordGetter(self):
        loginUsername=self.loginUsernameBox.get()
        loginPassword=self.loginPasswordBox.get()
        self.root.loginUsername=loginUsername
        cursor.execute("SELECT Username,Password,Role FROM Users WHERE Username=?", (loginUsername,))#gets the username and password and compares it in the database for a matching record
        result=cursor.fetchone()
        if result and passwordManager.verifyPassword(result[1], loginPassword):
            if result[2] == "admin":#if admin then they will get a special window
                self.root.adminViewVisible()
            else:
                self.root.user_View.welcomeUserText.configure(text=f"Welcome {loginUsername}!")
                self.root.userViewVisible()
        else:
            self.loginText4=ctk.CTkLabel(self,text="Wrong Username or Password",fg_color="transparent",text_color="Red",anchor="center",font=("MS Sans Serif",15))
            self.loginText4.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="n")
class registerView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
        self.registerText1=ctk.CTkLabel(self,text="Please register by entering a username and password:",fg_color="transparent",text_color="Black",anchor="center",wraplength=300,font=("Arial Rounded MT Bold",15))
        self.registerText1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerText2=ctk.CTkLabel(self,text="Username:",fg_color="transparent",text_color="Black",anchor="center",font=("MS Sans Serif",15))
        self.registerText2.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerUsernameBox=ctk.CTkEntry(self,placeholder_text="Username")
        self.registerUsernameBox.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerText3=ctk.CTkLabel(self,text="Password:",fg_color="transparent",text_color="Black",anchor="center",font=("MS Sans Serif",15))
        self.registerText3.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerPasswordBox=ctk.CTkEntry(self,placeholder_text="Password",show="*")
        self.registerPasswordBox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerText4=ctk.CTkLabel(self,text="Password must contain: \n8 characters\n1 special character\n 1 uppercase and lowercase letter",fg_color="transparent",text_color="Black",anchor="center",font=("Arial",15))
        self.registerText4.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")
        self.buttonFrame = ctk.CTkFrame(self, fg_color="transparent")#to avoid the buttons extending the current frame
        self.buttonFrame.grid(row=6, column=0, pady=(0, 20))
        self.registerButton=ctk.CTkButton(self.buttonFrame,text="Register",command=self.usernameAndPasswordSetter)
        self.registerButton.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="n")
        self.backButton=ctk.CTkButton(self.buttonFrame,text="Back",command=self.root.homeViewVisible)
        self.backButton.grid(row=6, column=1, padx=20, pady=(0, 20), sticky="n")
    def usernameAndPasswordSetter(self):
        registeredUsername=self.registerUsernameBox.get()#gets the username and password from the entry boxes
        registeredPassword=self.registerPasswordBox.get()
        if registeredUsername and registeredPassword:
            passwordError = passwordManager.validatePassword(registeredPassword)
            if passwordError:
                dialogBox(self,"Weak Password",passwordError)
                return
            try:
                hashedPassword = passwordManager.hashPassword(registeredPassword)
                cursor.execute("INSERT INTO Users (Username,Password,BalanceInPennies) VALUES (?,?,?)",(registeredUsername,hashedPassword,0))# inserts the registered username and password into the database
                database.commit()
                dialogBox(self,"Success!","Your Username and password have been successfully registered")
                self.root.homeViewVisible()
            except Exception as err: #if error shows then the username is taken
                self.registerText4=ctk.CTkLabel(self,text="Username Taken",fg_color="transparent",text_color="Red",anchor="center",font=("MS Sans Serif",15))
                self.registerText4.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="n")
        else:
            dialogBox(self,"Input Invalid","Username or Password field cannot be empty")

class dialogBox(ctk.CTkToplevel):
    def __init__(self,parent,title,message):
        super().__init__(parent)
        self.title(title)
        self.geometry("250x100")#dialog box size
        self.grid_columnconfigure(0, weight=1)
        self.dialogText1=ctk.CTkLabel(self,text=message,fg_color="transparent",text_color="Black",anchor="center",wraplength=200,font=("Arial Rounded MT Bold",15))
        self.dialogText1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.dialogButton=ctk.CTkButton(self,text="Ok",command=self.destroy)
        self.dialogButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.attributes('-topmost', True) #is on top and other program window cant be used until the dialog box is closed
        self.grab_set()

class homeView(ctk.CTkFrame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.root = root
        self.grid_columnconfigure(0, weight=1)

        self.homeText1=ctk.CTkLabel(self,text="Welcome to the NCTX Bus Application",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",18))
        self.homeText1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.homeText2=ctk.CTkLabel(self,text="Please either Login or Register as a user",fg_color="transparent",text_color="Black",anchor="center",font=("Arial",15))
        self.homeText2.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginViewButton=ctk.CTkButton(self,text="Login",command=self.root.loginViewVisible)
        self.loginViewButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerViewButton=ctk.CTkButton(self,text="Register",command=self.root.registerViewVisible)
        self.registerViewButton.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="n")



class mainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NCTX Bus Application")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame=ctk.CTkFrame(self)
        self.frame.grid(row=0,column=0,sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)        

        self.login_View=loginView(self.frame,self) #every line creates one page and attaches it to the controller(self)
        self.register_View=registerView(self.frame,self)
        self.home_View=homeView(self.frame,self)
        self.user_View=userView(self.frame,self)
        self.admin_View=adminView(self.frame,self)
        self.viewAndBuyTickets_View=viewAndBuyTicketsView(self.frame,self)
        self.topUpMoney_View=topUpMoneyView(self.frame,self)
        self.manageTickets_View=manageTicketsView(self.frame,self)
        self.all_views = [self.login_View,self.register_View,self.home_View,self.user_View,self.admin_View,self.viewAndBuyTickets_View,self.topUpMoney_View,self.manageTickets_View]
        self.homeViewVisible()
    def centreWindow(self):
        self.update_idletasks()

        windowWidth = self.winfo_width()
        windowHeight = self.winfo_height()

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        x = (screenWidth - windowWidth) // 2
        y = int((screenHeight - windowHeight) // 2.5)

        self.geometry(f"+{x}+{y}")

    def showFrame(self, frame, customSize=""):
        # Hide all existing frames
        for view in self.all_views:
            view.grid_remove()

        # Display the selected frame
        frame.grid(row=0, column=0, sticky="nsew")

        # Set window size or reset to automatic sizing
        if customSize:
            self.geometry(customSize)
        else:
            self.wm_geometry("")
        self.centreWindow()

    def homeViewVisible(self):
        self.showFrame(self.home_View,"400x250")

    def loginViewVisible(self):
        self.showFrame(self.login_View)

    def registerViewVisible(self):
        self.showFrame(self.register_View, "450x400")

    def userViewVisible(self):
        self.showFrame(self.user_View,"400x325")

    def adminViewVisible(self):
        self.showFrame(self.admin_View)

    def buyAndViewTicketsVisible(self):
        self.showFrame(self.viewAndBuyTickets_View, "1250x700")

    def topUpMoneyVisible(self):
        self.topUpMoney_View.getTopUpValue()
        self.showFrame(self.topUpMoney_View)

    def manageTicketVisible(self):
        self.manageTickets_View.chooseTickets.set("Valid Tickets")
        self.manageTickets_View.refreshLists("Valid Tickets")
        self.showFrame(self.manageTickets_View,"600x400")