import customtkinter as ctk

class loginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Home Window")
        self.geometry("400x400")
        self.grid_columnconfigure(0, weight=1)

class homeView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Home Window")
        self.geometry("400x400")
        self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure((0, 1), weight=1)
        self.label1=ctk.CTkLabel(self,text="Please either Login or Register as a user",fg_color="transparent",text_color="Black",anchor="center",font=("Arial Rounded MT Bold",15))
        self.label1.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="n")
        self.loginButton=ctk.CTkButton(self,text="Login",command=lambda:(self.destroy(),loginView))
        self.loginButton.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")
window1 = homeView()
window1.mainloop()


        