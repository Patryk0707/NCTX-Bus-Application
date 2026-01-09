import customtkinter as ctk

class homeView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Home Window")
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.Label1=ctk.CTkLabel(self,text="Please either Login or register as a user",fg_color="transparent",text_color="Black")
        #self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")

window1 = homeView()
window1.mainloop()