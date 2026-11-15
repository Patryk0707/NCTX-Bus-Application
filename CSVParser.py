import os.path,csv
import Views

baseDir=os.path.dirname(os.path.abspath(__file__)) #gets the directionary of the python file
CSVName="mobile_products.csv" #CSV file name
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
            Views.dialogBox(self.root,"CSV Error","mobile_products.csv file not found, please ensure it is stored in the same folder as the python file")
            return []
        except Exception:
            Views.dialogBox(self.root,"CSV Error","The CSV file could not be read")
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


def loadCSVRows():  #method that loads the ticket data from the CSV File into python
    csvPath=os.path.join(baseDir,CSVName) #gets the file path for the CSV File
    with open(csvPath,newline="") as f: #opens the CSV file and newline="" prevents any blank lines from appearing
        reader=csv.DictReader(f)#reads every CSV row as a dictionary
        rows=list(reader) #converts all CSV rows into a list
        fieldnames=reader.fieldnames #Stores CSV column headers
    return rows,fieldnames
def saveCSVRows(rows,fieldnames): #overwrites the CSV file with new values
    csvPath=os.path.join(baseDir,CSVName)
    with open(csvPath,"w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
