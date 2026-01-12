import customtkinter as ctk # type: ignore
import sqlite3,os.path,csv

baseDir=os.path.dirname(os.path.abspath(__file__))
dbPath=os.path.join(baseDir,"NCTX Database.db")
database=sqlite3.connect(dbPath)
cursor=database.cursor()

class topUpMoneyView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
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
                widget.destroy()
            self.getTopUpValue()
class csvFile():
    def __init__(self):
        super().__init__()
    def readCSVForDayTickets(self):
        dayTicketsDict=[]
        csvPath=os.path.join(baseDir,"mobile_products.csv")
        with open(csvPath) as csvfile:
            csvReader=csv.DictReader(csvfile)
            for row in csvReader:
                if row['topup_entitlement_value']=='1':
                        price_in_pounds=int(row['topup_price_in_pence'])/100
                        dayTicketsDict.append({"title":row['topup_title'],"description":row['category_description'],"price":price_in_pounds})
        return dayTicketsDict
    def readCSVForSingleTickets(self):
        singleTicketsDict=[]
        csvPath=os.path.join(baseDir,"mobile_products.csv")
        with open(csvPath) as csvfile:
            csvReader=csv.DictReader(csvfile)
            for row in csvReader:
                if row['topup_entitlement_value']=='10':
                        price_in_pounds=int(row['topup_price_in_pence'])/100
                        singleTicketsDict.append({"title":row['topup_title'],"description":row['category_description'],"price":price_in_pounds})
        return singleTicketsDict
    def readCSVForWeekTickets(self):
        weekTicketsDict=[]
        csvPath=os.path.join(baseDir,"mobile_products.csv")
        with open(csvPath) as csvfile:
            csvReader=csv.DictReader(csvfile)
            for row in csvReader:
                if row['topup_entitlement_value']=='7':
                        price_in_pounds=int(row['topup_price_in_pence'])/100
                        weekTicketsDict.append({"title":row['topup_title'],"description":row['category_description'],"price":price_in_pounds})
        return weekTicketsDict
    def readCSVForMonthTickets(self):
        monthTicketsDict=[]
        csvPath=os.path.join(baseDir,"mobile_products.csv")
        with open(csvPath) as csvfile:
            csvReader=csv.DictReader(csvfile)
            for row in csvReader:
                if row['topup_entitlement_value']=='31':
                        price_in_pounds=int(row['topup_price_in_pence'])/100
                        monthTicketsDict.append({"title":row['topup_title'],"description":row['category_description'],"price":price_in_pounds})
        return monthTicketsDict
    def readCSVForYearTickets(self):
        yearTicketsDict=[]
        csvPath=os.path.join(baseDir,"mobile_products.csv")
        with open(csvPath) as csvfile:
            csvReader=csv.DictReader(csvfile)
            for row in csvReader:
                if row['topup_entitlement_value']=='365':
                        price_in_pounds=int(row['topup_price_in_pence'])/100
                        yearTicketsDict.append({"title":row['topup_title'],"description":row['category_description'],"price":price_in_pounds})
        return yearTicketsDict
class adminView(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

class viewAndBuyTicketsView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.data=self.csv_Reader=csvFile()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.ticketCategorySelection=ctk.CTkComboBox(self,values=["Choose Category","Single Use Tickets","24 Hour Tickets","7 Day Tickets","31 Day Tickets","Annual Tickets"],command=self.changeWidgets)
        self.ticketCategorySelection.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        #self.csv_Reader.readCSVForDayTickets()
        self.widgets=ctk.CTkFrame(self)
        self.widgets.grid(row=1,column=0,padx=20,pady=10,sticky="nsew")

    def changeWidgets(self,choice):
        self.page=0
        self.pageNumber=15
        self.currentChoice=None
        for widget in self.widgets.winfo_children():
            widget.destroy()
        if choice=="Single Use Tickets":
            self.data=self.csv_Reader.readCSVForSingleTickets()
            for i,singleTickets in enumerate(self.data):
                if i>=15:
                    break
                elif i<5:
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
                ctk.CTkLabel(self.widgets,text=singleTickets["title"]).grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=singleTickets["description"],wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{singleTickets['price']}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda ticket=singleTickets:self.buyTickets(ticket)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))
        elif choice=="24 Hour Tickets":
            self.data=self.csv_Reader.readCSVForDayTickets()
            self.view24HourTickets()
        elif choice=="7 Day Tickets":
            self.data=self.csv_Reader.readCSVForWeekTickets()
            for i,weekTickets in enumerate(self.data):
                if i>=15:
                    break
                elif i<5:
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
                ctk.CTkLabel(self.widgets,text=weekTickets["title"]).grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=weekTickets["description"],wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{weekTickets['price']}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda ticket=weekTickets:self.buyTickets(ticket)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))
        elif choice=="31 Day Tickets":
            self.data=self.csv_Reader.readCSVForMonthTickets()
            for i,monthTickets in enumerate(self.data):
                if i>=15:
                    break
                elif i<5:
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
                ctk.CTkLabel(self.widgets,text=monthTickets["title"]).grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=monthTickets["description"],wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{monthTickets['price']}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda ticket=monthTickets:self.buyTickets(ticket)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))
        elif choice=="Annual Tickets":
            self.data=self.csv_Reader.readCSVForYearTickets()
            for i,yearTickets in enumerate(self.data):
                if i>=15:
                    break
                elif i<5:
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
                ctk.CTkLabel(self.widgets,text=yearTickets["title"]).grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=yearTickets["description"],wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{yearTickets['price']}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda ticket=yearTickets:self.buyTickets(ticket)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))

    def buyTickets(self,ticket):
        ticketPrice=int(ticket["price"]*100)
        cursor.execute("SELECT BalanceInPennies FROM Users WHERE Username=?",(self.root.loginUsername,))
        balance=cursor.fetchone()[0]
        if balance<ticketPrice:
            dialogBox(self,"Not enough money","You do not have enough money for this ticket.")
            return
        cursor.execute("UPDATE Users SET BalanceInPennies=BalanceInPennies-? WHERE Username=?",(ticketPrice,self.root.loginUsername))
        database.commit()
        dialogBox(self, "Success", f"You have sucessfully bought {ticket['title']}")

    def view24HourTickets(self):
        for widget in self.widgets.winfo_children():
            widget.destroy()
        start=self.page*self.pageNumber
        end=start+self.pageNumber
        pageItems=self.data[start:end]
        for i,dayTickets in enumerate(pageItems):
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
                ctk.CTkLabel(self.widgets,text=dayTickets["title"]).grid(row=row,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=dayTickets["description"],wraplength=300).grid(row=row+1,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkLabel(self.widgets,text=f"Price: £{dayTickets['price']}").grid(row=row+2,column=textCol,sticky="w",pady=(5,0))
                ctk.CTkButton(self.widgets,width=60,text="Buy",command=lambda t=dayTickets:self.buyTickets(t)).grid(row=row+1,column=buttonCol,sticky="w",padx=(10,30),pady=(5,0))
        totalPages=(len(self.data)-1)//self.pageNumber+1
        viewFor24HourTickets=ctk.CTkFrame(self.widgets,fg_color="transparent")  
        viewFor24HourTickets.grid(row=1000,column=0,columnspan=6,pady=(10,0),sticky="ew")
        viewFor24HourTickets.grid_columnconfigure((0,1,2),weight=1)
        previousPageButton=ctk.CTkButton(viewFor24HourTickets,text="Previous Page",command=self.previousPage)
        nextPageButton=ctk.CTkButton(viewFor24HourTickets,text="Next Page",command=self.nextPage)
        currentPageNumber=ctk.CTkLabel(viewFor24HourTickets,text=f"Page{self.page+1}/{totalPages}")
        previousPageButton.grid(row=0,column=0,sticky="w")
        currentPageNumber.grid(row=0,column=1)
        nextPageButton.grid(row=0,column=2,sticky="e")

        if self.page==0:
            previousPageButton.configure(state="disabled")
        if self.page>=totalPages-1:
            nextPageButton.configure(state="disabled")

    def nextPage(self):
        self.page+=1
        self.view24HourTickets()
    def previousPage(self):
        if self.page>0:
            self.page-=1
        self.view24HourTickets()
class userView(ctk.CTkFrame):
    def __init__(self,parent,root):
        super().__init__(parent)
        self.root=root
        self.grid_columnconfigure(0, weight=1)
        self.welcomeUserText=ctk.CTkLabel(self,text="",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",15))
        self.welcomeUserText.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.viewAndBuyTicketsButton=ctk.CTkButton(self,text="View And Buy Tickets",command=self.root.buyAndViewTicketsVisible)
        self.viewAndBuyTicketsButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
        self.manageTicketsButton=ctk.CTkButton(self,text="Manage Your Tickets")
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
        self.login_View.grid(row=0, column=0, sticky="nsew")
        self.register_View.grid(row=0, column=0, sticky="nsew")
        self.home_View.grid(row=0, column=0, sticky="nsew")
        self.user_View.grid(row=0, column=0, sticky="nsew")
        self.admin_View.grid(row=0, column=0, sticky="nsew")
        self.viewAndBuyTickets_View.grid(row=0,column=0,sticky="nsew")
        self.topUpMoney_View.grid(row=0,column=0,sticky="nsew")
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

window1 = homeView()
window1.mainloop()


        