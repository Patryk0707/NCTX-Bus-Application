# NCTX Bus Application
The NCTX Bus Application allows users to view, manage and buy bus tickets as well as top up account credit through an accessible user interface. Administrators can manage ticket pricing and check ticket sales within the month

**Use Case 1**
The application presents the user with the home page welcoming and introducing them to the application allowing them to access the login page or register page. This allows them to either login or register as a passenger or login as an administrator.

**Summary Of Use Case 1:**
<ins>Implemented:</ins>
New classes(adminView,userView,loginView,registerView,dialogBox,homeView)
1 window and 5 frames(Home Window, register window, login window,user window,admin window and a dialog window)
imported customtkinter for my graphical user interface and sqlite3 for my database

<ins>Issues during testing and fixes:</ins>
Had labeltext not working for my homeView, this was because i didnt write the code for the label text grid.

Login View wasnt opening when pressing the loginButton in homeView, this was because i put ctk.CTk not ctk.CTkToplevel inside the brackets of homeView. the 2nd issue to this was that i put loginView in command instead of loginView() as it was a class.

Not able to use the input from the entry boxes to use for my database. The finding was that the program was using the wrong directionary to find my database and would create a replacement in its directionary. To fix this i had to specify to use the same directionary as the python file. This also fixed another confusing issue which was that it couldnt find the users table because it would use the database the program created not the one i was using.

When a new window gets opened a additional root tk window gets opened too, the issue that caused this was that every view was a window instead of a frame meaning a root window got created as every window was a "main window". I changed majority of my code for the additional views to be frames and not windows.

**Use Case 2**
Once the user logs in, the program presents the user with the main screen where there is a button which lets the user buy or view tickets in a different view. The program will also let them view the tickets they have bought and lets them activate the ticket. Another button lets them top up money to buy the tickets. User purchases will be tracked using an sql database and ticket pricing will be changed using the mobile product.csv that NCTX has provided. The duration of the ticket sale will be tracking using the same SQL database but in another table.

**Summary of Use Case 2**
I created 3 buttons in the user view frame which navigates them to either the page where they buy tickets, manage their tickets or top up their money. i added database functionality so all the data can be stored and retrieved easily. for the buy or view tickets view i added a combo box for the user to change what ticket type they want to view(single, 1 day, 1 week, 1 month or annual ticket). This view lets them buy tickets and the ticket information is stored in the database in a purchases table. For the manage tickets view the tickets are retrieved from the database and shown to the user and they can see their activated tickets and tickets that are valid and ready to be used. Final view is top up view where the user can top up their amount.
<ins>Implemented:</ins>
new classes(viewAndBuyTicketsView,csvFile,topUpMoneyView,manageTicketsView)
<ins>Issues during testing and fixes:</ins>
Had issues with scrollable frame for one of my classes so i decided to revert back to ctkframes. after using scrollable frames later inside a view, it decided to work. Not sure what the issue was for it not to work the first time but i have figured out a way to get around the issue. when retrieving moneyInPennies from the database it was as a tuple meaning i couldnt show the amount a user has. the solution was to add a [0] after fetching the moneyInPennies which has since been renamed to amountInPennies for clarity.