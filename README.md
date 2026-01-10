# NCTX Bus Application
The NCTX Bus Application allows users to view, manage and buy bus tickets as well as top up account credit through an accessible user interface. Administrators can manage ticket pricing, control the quantity of tickets available and create limited time discounted tickets.

##Use Case 1
The application presents the user with the home page welcoming and introducing them to the application allowing them to access the login page or register page. This allows them to either login or register as a passenger or login as an administrator.

#Summary Of Use Case 1:
<ins>Implemented:</ins>
New classes(adminView,userView,loginView,registerView,dialogBox,homeView)
1 window and 5 frames(Home Window, register window, login window,user window,admin window and a dialog window)
imported customtkinter for my graphical user interface and sqlite3 for my database

<ins>Issues during testing and fixes:</ins>
Had labeltext not working for my homeView, this was because i didnt write the code for the label text grid.

Login View wasnt opening when pressing the loginButton in homeView, this was because i put ctk.CTk not ctk.CTkToplevel inside the brackets of homeView. the 2nd issue to this was that i put loginView in command instead of loginView() as it was a class.

Not able to use the input from the entry boxes to use for my database. The finding was that the program was using the wrong directionary to find my database and would create a replacement in its directionary. To fix this i had to specify to use the same directionary as the python file. This also fixed another confusing issue which was that it couldnt find the users table because it would use the database the program created not the one i was using.

When a new window gets opened a additional root tk window gets opened too, the issue that caused this was that every view was a window instead of a frame meaning a root window got created as every window was a "main window". I changed majority of my code for the additional views to be frames and not windows.
