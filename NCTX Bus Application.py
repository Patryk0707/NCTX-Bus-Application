import customtkinter as ctk # type: ignore
import sqlite3,os.path,csv
from datetime import datetime,timedelta


baseDir=os.path.dirname(os.path.abspath(__file__))
dbPath=os.path.join(baseDir,"NCTX Database.db")
database=sqlite3.connect(dbPath)
cursor=database.cursor()




class manageTicketsView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.chooseTickets=ctk.CTkComboBox(self,values=["Choose Ticket Group","Valid Tickets","Used Tickets"],width=170,command=self.refreshLists)
        self.chooseTickets.grid(row=0,column=0,pady=(10,10))
        self.backButton=ctk.CTkButton(self,text="Back",command=self.root.userViewVisible)
        self.backButton.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="n")
        self.displayTicketsFrame=ctk.CTkScrollableFrame(self, width=700, height=500)
        self.displayTicketsFrame.grid(row=2,column=0,columnspan=2,sticky="nsew",padx=20,pady=(0, 20))
        self.displayTicketsFrame.grid_columnconfigure(0,weight=1)

    def usedTickets(self,purchaseID:int):
        usedTicketDate=datetime.now()
        usedTicketDateString=usedTicketDate.strftime("%d/%m/%y %H:%M")
        cursor.execute("SELECT Duration From Purchases WHERE PurchaseID=? AND Username=? AND UsedDate Is NULL",(purchaseID,self.root.loginUsername))
        row=cursor.fetchone()
        if not row:
            dialogBox(self,"Error","Ticket Already Used")
            return
        duration=int(row[0])
        if duration==10:
            ticketExpiryDate=usedTicketDate+timedelta(minutes=duration)
        else:
            ticketExpiryDate=usedTicketDate+timedelta(days=duration)
        ticketExpiryDateString=ticketExpiryDate.strftime("%d/%m/%y %H:%M")
        cursor.execute("UPDATE Purchases SET UsedDate=?,ExpiryDate=? WHERE PurchaseID=? AND Username=? AND UsedDate IS NULL",(usedTicketDateString,ticketExpiryDateString,purchaseID,self.root.loginUsername))
        database.commit()
        dialogBox(self,"Success","Ticket activated!")
        self.refreshLists()

    def refreshLists(self,choice=None):
        if choice is None:
            choice=self.chooseTickets.get()
        for w in self.displayTicketsFrame.winfo_children():
            w.destroy()
        username=self.root.loginUsername
        if choice=="Valid Tickets":
            cursor.execute("SELECT PurchaseID,TicketTitle,Duration,DatePurchased FROM Purchases WHERE Username=? AND UsedDate Is NULL ORDER BY PurchaseID DESC",(username,))
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
                ctk.CTkLabel(self.displayTicketsFrame,text=title,font=("MS Sans Serif",16)).grid(row=r,column=0,sticky="w",pady=(10,0))
                ctk.CTkLabel(self.displayTicketsFrame,text=f"Purchased: {datePurchased}  Duration: {self.durationFormat(int(duration))}").grid(row=r+1, column=0, sticky="w")
                useButton=ctk.CTkButton(self.displayTicketsFrame,text="Use",command=lambda p=purchaseID:self.usedTickets(p))
                useButton.grid(row=r, column=1, rowspan=2, padx=10, pady=10)
                r+=3
        else:
            cursor.execute("SELECT PurchaseID,TicketTitle,UsedDate,ExpiryDate FROM Purchases WHERE Username=? AND UsedDate IS NOT NULL ORDER BY PurchaseID DESC",(username,))
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
                ctk.CTkLabel(self.displayTicketsFrame,text=title,font=("MS Sans Serif", 16)).grid(row=r,column=0,sticky="w",pady=(10,0))
                ctk.CTkLabel(self.displayTicketsFrame,text=f"Used: {usedDate} | Expires: {expiryDate}").grid(row=r+1,column=0,sticky="w")
                r += 3
    def durationFormat(self,duration):
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
        cursor.execute("SELECT BalanceInPennies FROM Users WHERE Username=?",(self.root.loginUsername,))
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
            dialogBox(self,"Invalid Top Up Value","Please enter a valid number")
            return
        topUpAmount=int(topUpValue)
        self.topUp(topUpAmount)
    def topUp(self,amountInPounds):
            amountInPennies=amountInPounds*100
            cursor.execute("UPDATE Users SET BalanceInPennies=BalanceInPennies+? WHERE Username=?",(amountInPennies,self.root.loginUsername,))
            database.commit()
            for widget in self.winfo_children():
                if widget is not self.backButton:
                    widget.destroy()
            self.getTopUpValue()
class csvFile():
    def __init__(self):
        super().__init__()
    def readCSVTicketInfo(self,durationValue):
        TicketsDict=[]
        csvPath=os.path.join(baseDir,"mobile_products.csv")
        try:
            with open(csvPath) as csvfile:
                csvReader=csv.DictReader(csvfile)
                for row in csvReader:
                    if row["topup_entitlement_value"]==durationValue:
                            price_in_pounds=int(row['topup_price_in_pence'])/100
                            TicketsDict.append({"title":row['topup_title'],"description":row['category_description'],"price":price_in_pounds,"duration": int(row["topup_entitlement_value"]),"people": int(row["topup_passenger_class_quantity"])})
        except FileNotFoundError:
            dialogBox(self.root,"CSV Error","mobile_products.csv file not found, please ensure it is stored in the same folder as the python file")
            return []
        except Exception:
            dialogBox(self.root,"CSV Error","The CSV file could not be read")
            return []
        return TicketsDict
    def readCSVForSingleTickets(self):
        return self.readCSVTicketInfo("10")
    def readCSVForDayTickets(self):
        return self.readCSVTicketInfo("1")
    def readCSVForWeekTickets(self):
        return self.readCSVTicketInfo("7")
    def readCSVForMonthTickets(self):
        return self.readCSVTicketInfo("31")
    def readCSVForYearTickets(self):
        return self.readCSVTicketInfo("365")
class adminView(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

class viewAndBuyTicketsView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.data=self.csv_Reader=csvFile()
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.ticketCategorySelection=ctk.CTkComboBox(self,values=["Choose Category","Single Use Tickets","24 Hour Tickets","7 Day Tickets","31 Day Tickets","Annual Tickets"],command=self.changeWidgets)
        self.ticketCategorySelection.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.backButton=ctk.CTkButton(self,text="Back",command=self.root.userViewVisible)
        self.backButton.grid(row=0, column=1, padx=20, pady=(0, 20), sticky="n")
        #self.csv_Reader.readCSVForDayTickets()
        self.widgets=ctk.CTkFrame(self)
        self.widgets.grid(row=1,column=0,columnspan=2,padx=20,pady=10,sticky="nsew")

    def changeWidgets(self,choice):
        self.page=0
        self.pageNumber=15
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
        cursor.execute("SELECT BalanceInPennies FROM Users WHERE Username=?",(self.root.loginUsername,))
        balance=cursor.fetchone()[0]
        if balance<ticketPriceInPennies:
            dialogBox(self,"Not enough money","You do not have enough money for this ticket.")
            return
        cursor.execute("UPDATE Users SET BalanceInPennies=BalanceInPennies-? WHERE Username=?",(ticketPriceInPennies,self.root.loginUsername))
        database.commit()
        self.logPurchase(ticket,ticketPriceInPennies)
        dialogBox(self, "Success", f"You have sucessfully bought {ticket['title']}")

    def logPurchase(self,ticket,pricePaidInPennies:int):
        username=self.root.loginUsername
        title=ticket["title"]
        purchasedDate=datetime.now().strftime("%d/%m/%y %H:%M")
        duration=int(ticket.get("duration",0)) 
        cursor.execute("INSERT INTO Purchases(Username,TicketTitle,Duration,PricePaidInPennies,DatePurchased,UsedDate,ExpiryDate)VALUES(?,?,?,?,?,NULL,NULL)",(username,title,duration,pricePaidInPennies,purchasedDate))
        database.commit()

    def viewTickets(self,tickets,showPaging=False):
        for widget in self.widgets.winfo_children():
            widget.destroy()
        if showPaging:
            start=self.page*self.pageNumber
            end=start+self.pageNumber
            pageItems=tickets[start:end]
        else:
            pageItems = tickets[:15]
        for i,t in enumerate(pageItems):
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
                desc=t.get("description","")
                price=t.get("price",0)
                ctk.CTkLabel(self.widgets,text=f"{title}-Valid for:{people} people").grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=desc,wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{price}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda ticket=t:self.buyTickets(ticket)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))
        if showPaging:
            totalPages=(len(self.data)-1)//self.pageNumber+1
            footerRow=5*4 
            footer=ctk.CTkFrame(self.widgets,fg_color="transparent") 
            footer.grid(row=footerRow,column=0,columnspan=6,pady=(10,0),sticky="ew")
            footer.grid_columnconfigure((0,1,2),weight=1)
            previousPageButton=ctk.CTkButton(footer,text="Previous Page",command=self.previousPage)
            nextPageButton=ctk.CTkButton(footer,text="Next Page",command=self.nextPage)
            currentPageNumber=ctk.CTkLabel(footer,text=f"Page{self.page+1}/{totalPages}")
            previousPageButton.grid(row=0,column=0,sticky="w")
            currentPageNumber.grid(row=0,column=1)
            nextPageButton.grid(row=0,column=2,sticky="e")

            if self.page==0:
                previousPageButton.configure(state="disabled")
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
        self.grid_columnconfigure(0, weight=1)
        self.welcomeUserText=ctk.CTkLabel(self,text="",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",15))
        self.welcomeUserText.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.viewAndBuyTicketsButton=ctk.CTkButton(self,text="View And Buy Tickets",command=self.root.buyAndViewTicketsVisible)
        self.viewAndBuyTicketsButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.manageTicketsButton=ctk.CTkButton(self,text="Manage Your Tickets",command=self.root.manageTicketVisible)
        self.manageTicketsButton.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="n")
        self.topupButton=ctk.CTkButton(self,text="Top Up Money",command=self.root.topUpMoneyVisible)
        self.topupButton.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")

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
        self.loginPasswordBox=ctk.CTkEntry(self,placeholder_text="Password")
        self.loginPasswordBox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginButton=ctk.CTkButton(self,text="Login",command=self.usernameAndPasswordGetter)
        self.loginButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")
        
    def usernameAndPasswordGetter(self):
        loginUsername=self.loginUsernameBox.get()
        loginPassword=self.loginPasswordBox.get()
        self.root.loginUsername=loginUsername
        cursor.execute("SELECT Username,Password FROM Users WHERE Username=? AND Password=?",(loginUsername,loginPassword))
        result=cursor.fetchone()
        if result:
            if loginUsername=="admin" and loginPassword=="admin":
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
        self.registerPasswordBox=ctk.CTkEntry(self,placeholder_text="Password")
        self.registerPasswordBox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerButton=ctk.CTkButton(self,text="Register",command=self.usernameAndPasswordSetter)
        self.registerButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")

    def usernameAndPasswordSetter(self):
        registeredUsername=self.registerUsernameBox.get()
        registeredPassword=self.registerPasswordBox.get()
        if registeredUsername and registeredPassword:
            try:
                cursor.execute("INSERT INTO Users (Username,Password,BalanceInPennies) VALUES (?,?,?)",(registeredUsername,registeredPassword,0))
                database.commit()
                dialogBox(self,"Success!","Your Username and password have been successfully registered")
                self.root.homeViewVisible()
            except Exception as err:
                self.registerText4=ctk.CTkLabel(self,text="Username Taken",fg_color="transparent",text_color="Red",anchor="center",font=("MS Sans Serif",15))
                self.registerText4.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="n")
        else:
            dialogBox(self,"Input Invalid","Username or Password field cannot be empty")

class dialogBox(ctk.CTkToplevel):
    def __init__(self,parent,title,message):
        super().__init__(parent)
        self.title(title)
        self.geometry("250x100")
        self.grid_columnconfigure(0, weight=1)
        self.dialogText1=ctk.CTkLabel(self,text=message,fg_color="transparent",text_color="Black",anchor="center",wraplength=200,font=("Arial Rounded MT Bold",15))
        self.dialogText1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.dialogButton=ctk.CTkButton(self,text="Ok",command=self.destroy)
        self.dialogButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.attributes('-topmost', True)
        self.grab_set()

class homeView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NCTX Bus Application")
        self.geometry("400x325")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame=ctk.CTkFrame(self)
        self.frame.grid(row=0,column=0,sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)        

        self.login_View=loginView(self.frame,self)
        self.register_View=registerView(self.frame,self)
        self.home_View=ctk.CTkFrame(self.frame)
        self.user_View=userView(self.frame,self)
        self.admin_View=adminView(self.frame)
        self.viewAndBuyTickets_View=viewAndBuyTicketsView(self.frame,self)
        self.topUpMoney_View=topUpMoneyView(self.frame,self)
        self.manageTickets_View=manageTicketsView(self.frame,self)
        self.login_View.grid(row=0, column=0, sticky="nsew")
        self.register_View.grid(row=0, column=0, sticky="nsew")
        self.home_View.grid(row=0, column=0, sticky="nsew")
        self.user_View.grid(row=0, column=0, sticky="nsew")
        self.admin_View.grid(row=0, column=0, sticky="nsew")
        self.viewAndBuyTickets_View.grid(row=0,column=0,sticky="nsew")
        self.topUpMoney_View.grid(row=0,column=0,sticky="nsew")
        self.manageTickets_View.grid(row=0,column=0,sticky="nsew")
        self.homeText1=ctk.CTkLabel(self.home_View,text="Welcome to the NCTX Bus Application",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",18))
        self.homeText1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.homeText2=ctk.CTkLabel(self.home_View,text="Please either Login or Register as a user",fg_color="transparent",text_color="Black",anchor="center",font=("MS Sans Serif",15))
        self.homeText2.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginViewButton=ctk.CTkButton(self.home_View,text="Login",command=self.loginViewVisible)
        self.loginViewButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")
        self.registerViewButton=ctk.CTkButton(self.home_View,text="Register",command=self.registerViewVisible)
        self.registerViewButton.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="n")
        self.homeViewVisible()

    def homeViewVisible(self):
        self.home_View.tkraise()

    def loginViewVisible(self):
        self.login_View.tkraise()

    def registerViewVisible(self):
        self.register_View.tkraise()

    def userViewVisible(self):
        self.user_View.tkraise()

    def adminViewVisible(self):
        self.admin_View.tkraise()

    def buyAndViewTicketsVisible(self):
        self.geometry("1250x700")
        self.viewAndBuyTickets_View.tkraise()
    def topUpMoneyVisible(self):
        self.topUpMoney_View.getTopUpValue()
        self.topUpMoney_View.tkraise()
    
    def manageTicketVisible(self):
        self.geometry("600x325")
        self.manageTickets_View.tkraise()

window1 = homeView()
window1.mainloop()


        