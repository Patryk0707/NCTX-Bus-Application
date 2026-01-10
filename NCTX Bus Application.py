import customtkinter as ctk # type: ignore
import sqlite3,os.path
#class adminPanelView

baseDir=os.path.dirname(os.path.abspath(__file__))
dbPath=os.path.join(baseDir,"NCTX Database.db")
database=sqlite3.connect(dbPath)
cursor=database.cursor()

class adminView(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

class userView(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.viewAndBuyTicketsButton=ctk.CTkButton(self,text="View And Buy Tickets")
        self.viewAndBuyTicketsButton.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="n")

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
        cursor.execute("SELECT Username,Password FROM Users WHERE Username=? AND Password=?",(loginUsername,loginPassword))
        result=cursor.fetchone()
        if result:
            if loginUsername=="admin" and loginPassword=="admin":
                self.root.adminViewVisible()
            else:
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
                cursor.execute("INSERT INTO Users (Username,Password) VALUES (?,?)",(registeredUsername,registeredPassword))
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
        self.user_View=userView(self.frame)
        self.admin_View=adminView(self.frame)
        self.login_View.grid(row=0, column=0, sticky="nsew")
        self.register_View.grid(row=0, column=0, sticky="nsew")
        self.home_View.grid(row=0, column=0, sticky="nsew")
        self.user_View.grid(row=0, column=0, sticky="nsew")
        self.admin_View.grid(row=0, column=0, sticky="nsew")
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

window1 = homeView()
window1.mainloop()


        