from tkinter import *
import  mysql.connector

# Creating the window for return Rental
def return_rental_window():
    # Toplevel object for return Rental
    window = Toplevel(root)
    window.title("Return Rental")
    window.geometry("400x400")

    # Frames for input and Output
    query_f = Frame(window)
    result_f= Frame(window)

    #TextBoxes
    # Customer Name labeling and griding 
    cust_name_label = Label(query_f, text="Customer Name: ")
    cust_name_entry = Entry(query_f, width=30)
    cust_name_label.grid(row=0, column=0)
    cust_name_entry.grid(row=0, column=1)

    # Customer Car Return Date labeling and griding
    return_date_label = Label(query_f, text= "Return Date:")
    return_date_label.grid(row=1, column=0)
    return_date_entry = Entry(query_f, width=30)
    return_date_entry.grid(row=1, column=1)
  
    # Vehicle rented labeling and griding
    VIN_label = Label(query_f, text='VIN: ')
    Description_entry = Entry(query_f, width=30)
    VIN_label.grid(row=2, column=0)
    Description_entry.grid(row=2, column=1)

    #confirmation/submit query button
    # using lambda function to implemenmt the functions of the entry datas
    # Using get() for getting the data from each Entry from the label
    submit_button = Button(query_f, text='Submit', command=lambda: return_rental_output_result(return_date_entry.get(), cust_name_entry.get(), Description_entry.get(),result_f))
    submit_button.grid(row=7, column=1, sticky=E)

    # Attaching the frames to the window
    query_f.grid(row=0, column=0)
    result_f.grid(row=1, column=0)

# Function to run query and fetching the data on the output screen and console
# Attributes---------
# result_f is result frame
# return_date is return date of the vehicle
# cust_name is cusstomer name
# Vehicle_id is vehicle id which is unique for every vehicle that was rented
def return_rental_output_result(return_date, cust_name, vehicle_id, result_f):
    db=mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental")
    db_cur=db.cursor()

    # Writing query for returning the Rental
    query = "SELECT R.CustID, R.TotalAmount FROM RENTAL AS R JOIN CUSTOMER AS C ON R.CustID = C.CustID WHERE R.ReturnDate = '" + return_date + "' AND C.Name = '" + cust_name + "' AND R.VehicleID = '" + vehicle_id + "'"
    
    # printing query
    print(query)
    
    # Executing Query
    db_cur.execute(query)

    #Storing Result of query into result
    result = db_cur.fetchall()

    # Printing result
    print(result)

    # Showing Total Customer Payment due
    output_label= Label(result_f, text="Total Customer Payment Due: $" + str(result[0][1]))
    output_label.grid(row=0, column=0, columnspan=2, sticky=W)

    # Updating the Returned to 1 if the Vehicle got returned
    db_cur.execute("UPDATE RENTAL SET Returned = 1, PaymentDate = CASE WHEN PaymentDate = 'NULL' THEN '" + return_date + "' END WHERE CustID = " + str(result[0][0]) + " AND ReturnDate = '" + return_date + "' AND VehicleID = '" + vehicle_id + "'")
  
    # Commiting the database
    db.commit()
    # Closing the db connection
    db.close()

# Creating a window for adding a new Customer
def new_customer_window():
    # Toplevel object for New Customer
    window = Toplevel(root)
    window.title("Add Customer")
    window.geometry("400x400")

    # Frames for input and Output
    query_f = Frame(window)
    result_f= Frame(window)

        #TextBoxes
    # Customer Name labeling and griding 
    VIN_label = Label(query_f, text="Customer Name: ")
    Description_entry = Entry(query_f, width=30)
    VIN_label.grid(row=0, column=0)
    Description_entry.grid(row=0, column=1)

    # Customer Car Return Date labeling and griding
    phone_number_label = Label(query_f, text= "Phone Number: ")
    phone_number_label.grid(row=1, column=0)
    phone_number_entry = Entry(query_f, width=30)
    phone_number_entry.grid(row=1, column=1)
    
    # Making a button for for creating the customer
    # using lambda function to implemenmt the functions of the entry datas
    # Using get() for getting the data from each Entry from the label
    add_customer_btn = Button(query_f, text="Add Customer", command=lambda: add_new_customer(result_f,Description_entry.get(), phone_number_entry.get()))  
    add_customer_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Attaching the frames to the window
    query_f.grid(row=0, column=0)
    result_f.grid(row=1, column=0)


# Function for adding the Customer to the database using the Parameters
# Parametersn are -------------------
# cust_name is the Customer name to add in Database
# phone_number is the Phone Numvber of the Customer
# result_f is the frame where to display result
def add_new_customer(result_f,cust_name, phone_number):
    new_customer_connect = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental")
    new_customer_cur = new_customer_connect.cursor()

    #new_customer_cur.execute("INSERT INTO CUSTOMER VALUES(NULL, ?, ?)", (cust_name, phone_number))

    query = "Insert into Customer(Name, Phone) Values('" + cust_name + "', '" + phone_number + "')"

    print(query)

    new_customer_cur.execute(query)
    #Storing Result of query into result
    result = new_customer_cur.fetchall()

    #print(result)

    output_label = Label(result_f, text='Added new customer: ' + cust_name + ', ' + phone_number + ' (1 new row)')
    output_label.grid(row=0, column=0, columnspan=2, sticky=W)

    # commit changes
    new_customer_connect.commit()
    # close connection
    new_customer_connect.close()

# Creating a window for adding a new Vehicle
def new_vehicle_window():
    # Toplevel object for New Customer
    window = Toplevel(root)
    window.title("Add Vehicle")
    window.geometry("400x400")

    # Frames for input and Output
    query_f = Frame(window)
    result_f= Frame(window)

    # VIN labeling and griding 
    VIN_label = Label(query_f, text="VIN: ")
    VIN_entry = Entry(query_f, width=30)
    VIN_label.grid(row=0, column=0)
    VIN_entry.grid(row=0, column=1)

    # Description of Vehicle labeling and griding 
    Description_label = Label(query_f, text="Description: ")
    Description_entry = Entry(query_f, width=30)
    Description_label.grid(row=1, column=0)
    Description_entry.grid(row=1, column=1)

    # Year of a vehicle labeling and griding 
    Year_label = Label(query_f, text="Year: ")
    Year_entry = Entry(query_f, width=30)
    Year_label.grid(row=2, column=0)
    Year_entry.grid(row=2, column=1)

    # Type of vehicle labeling and griding 
    Type_label = Label(query_f, text="Type: ")
    Type_entry = Entry(query_f, width=30)
    Type_label.grid(row=3, column=0)
    Type_entry.grid(row=3, column=1)

    # Category of a vehicle labeling and griding 
    Category_label = Label(query_f, text="Category: ")
    Category_entry = Entry(query_f, width=30)
    Category_label.grid(row=4, column=0)
    Category_entry.grid(row=4, column=1)

    # Making a button for for creating the customer
    # using lambda function to implemenmt the functions of the entry datas
    # Using get() for getting the data from each Entry from the label
    add_vehicle_button = Button(result_f, text='Add Vehicle', command=lambda: 
    add_new_vehicle(VIN_entry.get(), Description_entry.get(), Year_entry.get(), Type_entry.get(), Category_entry.get()))
    add_vehicle_button.grid(row=7, column=0, columnspan=2,pady=10, padx=10, ipadx=100)

    # Attaching the frames to the window
    query_f.grid(row=0, column=0)
    result_f.grid(row=1, column=0)

# Function for adding the Vehicle to the database using the Parameters
# Parametersn are -------------------
# VIN as Vehicle Id which is primary key for vehicle in database
# Year is the model of car
# Description is the description of a vehicle 
# Type is the type of Vehicle
def add_new_vehicle(VIN, Description, Year, Type, Category):
    # Ensuring the connection with Database
    new_vehicle_connect = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental")
    new_vehicle_cur = new_vehicle_connect.cursor()

    # Spliting this into spl and val. SO that the Insert part in sql and the values are in val
    sql = ("INSERT INTO VEHICLE(VIN, Description, Year, Type, Category) VALUES(%s, %s, %s, %s, %s)")
    val = (VIN, Description, Year, Type, Category)
    new_vehicle_cur.execute(sql,val)

    #commit changes
    new_vehicle_connect.commit()
    #close connection
    new_vehicle_connect.close()

# Creating a window for adding a new Reservation
def new_rental_window():
    # Toplevel object for New Customer
    window = Toplevel(root)
    window.title("Add Reservation")
    window.geometry("400x400")

    # Frames for input and Output
    query_f = Frame(window)
    result_f= Frame(window)
    
    # Category of a vehicle labeling and griding 
    Customer_label = Label(query_f, text="Customer: ")
    Customer_entry = Entry(query_f, width=30)
    Customer_label.grid(row=0, column=0)
    Customer_entry.grid(row=0, column=1)

    # VIN of a vehicle labeling and griding 
    VIN_label = Label(query_f, text="VIN: ")
    VIN_entry = Entry(query_f, width=30)
    VIN_label.grid(row=1, column=0)
    VIN_entry.grid(row=1, column=1)

    # Start_Date of a vehicle labeling and griding 
    Start_Date_label = Label(query_f, text="Start Date (MM-DD-YYYY): ")
    Start_Date_entry = Entry(query_f, width=30)
    Start_Date_label.grid(row=2, column=0)
    Start_Date_entry.grid(row=2, column=1)

    # Order_Date of a vehicle labeling and griding 
    Order_Date_label = Label(query_f, text="Order Date (MM-DD-YYYY): ")
    Order_Date_entry = Entry(query_f, width=30)
    Order_Date_label.grid(row=3, column=0)
    Order_Date_entry.grid(row=3, column=1)\
    
    # Rental_type of a vehicle labeling and griding 
    Rental_Type_label = Label(query_f, text="Rental Type: ")
    Rental_Type_entry = Entry(query_f, width=30)
    Rental_Type_label.grid(row=4, column=0)
    Rental_Type_entry.grid(row=4, column=1)

    # Quantity of a vehicle labeling and griding 
    Quantity_label = Label(query_f, text="Quantity: ")
    Quantity_entry = Entry(query_f, width=30)
    Quantity_label.grid(row=5, column=0)
    Quantity_entry.grid(row=5, column=1)

    # Return_Date of a vehicle labeling and griding 
    Return_Date_label = Label(query_f, text="Return Date (MM-DD-YYYY): ")
    Return_Date_entry = Entry(query_f, width=30)
    Return_Date_label.grid(row=6, column=0)
    Return_Date_entry.grid(row=6, column=1)

    # Total_Amount of a vehicle labeling and griding 
    Total_Amount_label = Label(query_f, text="Total Amount: ")
    Total_Amount_entry = Entry(query_f, width=30)
    Total_Amount_label.grid(row=7, column=0)
    Total_Amount_entry.grid(row=7, column=1)

    # Total_Amount of a vehicle labeling and griding 
    Payment_Date_label = Label(query_f, text="Payment Date (MM-DD-YYYY): ")
    Payment_Date_entry = Entry(query_f, width=30)
    Payment_Date_label.grid(row=8, column=0)
    Payment_Date_entry.grid(row=8, column=1)

    # Making a button for for creating the customer
    # using lambda function to implemenmt the functions of the entry datas
    # Using get() for getting the data from each Entry from the label
    add_reservation_button = Button(query_f, text='Add Reservation', command=lambda: 
    add_new_reservation(Customer_entry.get(), VIN_entry.get(), Start_Date_entry.get(), Order_Date_entry.get(), Rental_Type_entry.get(), Quantity_entry.get(), Return_Date_entry.get(), Total_Amount_entry.get(), Payment_Date_entry.get()))
    add_reservation_button.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Attaching the frames to the window
    query_f.grid(row=0, column=0)
    result_f.grid(row=1, column=0)


def add_new_reservation(CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate):
    # Ensuring the Connection with the Database
    rental_reservation_connect = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental") 
    rental_reservation_cur = rental_reservation_connect.cursor()

    # Spliting this into spl and val. SO that the Insert part in sql and the values are in val
    sql = ("INSERT INTO Rental(CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate)
    rental_reservation_cur.execute(sql,val)

    #commit changes
    rental_reservation_connect.commit()
    #close connection
    rental_reservation_connect.close()

# Creating a window for retrieving customer
def retrieve_customer_window():
    # Toplevel object for New Customer
    window = Toplevel(root)
    window.title("Retrieve Customer Info ")
    window.geometry("400x400")

    # Frames for input and Output
    query_f = Frame(window)
    result_f= Frame(window)

    # Customer ID labeling and griding 
    CustID_label = Label(query_f, text="CustID: ")
    CustID_entry = Entry(query_f, width=30)
    CustID_label.grid(row=0, column=0)
    CustID_entry.grid(row=0, column=1)

    # Customer Name labeling and griding 
    Cname_label = Label(query_f, text="Customer Name: ")
    Cname_entry = Entry(query_f, width=30)
    Cname_label.grid(row=1, column=0)
    Cname_entry.grid(row=1, column=1)
    
    # Making a button for for creating the customer
    # using lambda function to implemenmt the functions of the entry datas
    # Using get() for getting the data from each Entry from the label
    ret_customer_button = Button( query_f, text='Retrieve Customer', command=lambda: 
    retrieve_customer_information(result_f, CustID_entry.get(), Cname_entry.get()))
    ret_customer_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Attaching the frames to the window
    query_f.grid(row=0, column=0)
    result_f.grid(row=1, column=0)

# Q5a
def retrieve_customer_information(result_f, CustID, Cname):
    # Ensuring the Connection with the Database
    retrieve_customer_connect = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental") 
    retrieve_customer_cur = retrieve_customer_connect.cursor()

    RowCount = 0

    if CustID != '':
        sql = "SELECT CustomerID, CustomerName, SUM(RentalBalance) FROM vRentalInfo WHERE CustomerID = %s AND CustomerName = %s GROUP BY CustomerID ORDER BY COUNT(RentalBalance) DESC"
        val = (CustID,Cname)
        retrieve_customer_cur.execute(sql,val)
    elif Cname != '':
        sql = "SELECT CustomerID, CustomerName, SUM(RentalBalance) FROM vRentalInfo WHERE CustomerName LIKE %s GROUP BY CustomerName ORDER BY COUNT(RentalBalance) DESC" 
        retrieve_customer_cur.execute(sql,Cname)  
    else:
        retrieve_customer_cur.execute("SELECT CustomerID, CustomerName, SUM(RentalBalance) FROM vRentalInfo GROUP BY CustomerName ORDER BY COUNT(RentalBalance) DESC")
    
    cust_out_result = retrieve_customer_cur.fetchall()
    print(cust_out_result)
  
    print_cust = ""

    for customer in cust_out_result:
        print_cust += str((str(customer[0])) + " | " + str(customer[1]) + " | $" + str(customer[2]) + ".00\n")
        RowCount+=1

    print("Count: " + str(RowCount))

    print(print_cust)

    retrieve_cust_label = Label(result_f, text=("Customer ID | Customer Name | Remaining Balance\n\n")+print_cust+("\nCount: " + str(RowCount)))
    retrieve_cust_label.grid(row=3, column=0, columnspan=2)

def retrieve_vehicle_window():
    # Toplevel object for New Customer
    window = Toplevel(root)
    window.title("Retrieve Vehicle Info ")
    window.geometry("400x400")

    # Frames for input and Output
    query_f = Frame(window)
    result_f= Frame(window)

    # VIN of a vehicle labeling and griding 
    VIN_label = Label(query_f, text="VIN: ")
    VIN_entry = Entry(query_f, width=30)
    VIN_label.grid(row=0, column=0)
    VIN_entry.grid(row=0, column=1)

    # Total_Amount of a vehicle labeling and griding 
    Description_label = Label(query_f, text="Description: ")
    Description_entry = Entry(query_f, width=30)
    Description_label.grid(row=1, column=0)
    Description_entry.grid(row=1, column=1)

    find_vehicle_button = Button(query_f, text='Find Vehicle', command=lambda: 
    retrieve_vehicle_information(result_f, VIN_entry.get(), Description_entry.get()))
    find_vehicle_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    # Attaching the frames to the window
    query_f.grid(row=0, column=0)
    result_f.grid(row=1, column=0)    


def retrieve_vehicle_information(result_f,VIN, Vdescription):
    
    # Ensuring the Connection with the Database
    retrieve_vehicle_connenct = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental")
    retrieve_vehicle_cur = retrieve_vehicle_connenct.cursor()

    RowCount=0

    if VIN != "" and Vdescription != "":
        sql ="SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo WHERE VIN LIKE %s AND Vehicle LIKE %s GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC"
        val=(VIN, Vdescription)
        retrieve_vehicle_cur.execute(sql,val)
    elif VIN != "":
        sql="SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo WHERE VIN LIKE %s GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC"
        retrieve_vehicle_cur.execute(sql,VIN)
    elif Vdescription != "":
        sql="SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo WHERE Vehicle LIKE %s GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC"
        retrieve_vehicle_cur.execute(sql,Vdescription)
    else:
        retrieve_vehicle_cur.execute("SELECT VIN, Vehicle, (ROUND(CAST(SUM(OrderAmount) AS float)/SUM(TotalDays), 2)) FROM vRentalInfo GROUP BY VIN ORDER BY (SUM(OrderAmount)/SUM(TotalDays)) ASC")
    
    vehicle_output_result = retrieve_vehicle_cur.fetchall()

    print(vehicle_output_result)

    print_vehicle = ''
    for vehicle in vehicle_output_result:
        print_vehicle += str((str(vehicle[0])) + "  |  " + str(vehicle[1]) + "  |  $" + str(vehicle[2])+"\n")
        RowCount+=1
  
    print("Count: " + str(RowCount))
  
    retrieve_cust_label = Label(result_f, text=("VIN # | Vehicle Description  |  Daily Rate \n\n") + print_vehicle+("\nCount: " + str(RowCount)))
    retrieve_cust_label.grid(row=7, column=0, columnspan=2)

def view_vehicle_window():
    # Toplevel object for New Customer
    view_window = Toplevel(root)
    view_window.title("Retrieve Vehicle Info ")
    view_window.geometry("400x400")

    # Frames for input and Output
    #query_f = Frame(view_window)
    #result_f= Frame(view_window)

    view_vehicle_button = Button(view_window, text='View Available Vehicles',
    command=lambda: view_vehicle_information(view_window))
    view_vehicle_button.grid(row=2, column=0, columnspan=2,
                           pady=10, padx=10, ipadx=100)

    
    # Attaching the frames to the window
    #query_f.grid(row=0, column=0)
    #result_f.grid(row=1, column=0) 
    

def view_vehicle_information(view_window):
    # connecting to the mysql database
    view_vehicle_connect = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental") 
    view_vehicle_cur = view_vehicle_connect.cursor()
    # cursor to access to connection

    print("Viewing Available Vehicles")

    view_vehicle_cur.execute("SELECT V.Description FROM VEHICLE AS V, RENTAL AS R WHERE R.VehicleID = V.VIN AND R.Returned = 1 GROUP BY V.Description",)

    print_list = ''

    result = view_vehicle_cur.fetchall()

    RowCount = 0

    for vehicle_pos in result:
      print_list += str((str(vehicle_pos[0])) + "\n")
      RowCount += 1

    list_label = Label(view_window, text=("List of all Vehicles \n\n") + print_list + "\n\nCount: " + str(RowCount))
    list_label.grid(row=9, column=0, columnspan=2)


# connect to mysql database
root = Tk()
root.title('Car Rental Database')

# setting the size of the window
root.geometry("350x400")

# connecting to the mysql database
car_rental = mysql.connector.connect(host ="localhost", user ="root", password = "sweety123",database="CarRental") 

# cursor to access to connection
car_rental_cur = car_rental.cursor()

# building gui components
title = Label(root, text='Car Rental Database', font='50')
title.grid(row=0, column=0, columnspan=2, pady=10, ipadx=100)

# create buttons
return_rental_btn = Button(root, text='Return Rental', command=return_rental_window)
return_rental_btn.grid(row=1, column=0, columnspan=2, pady=10, ipadx=100)

new_customer_btn = Button(root, text='Add New Customer', command=new_customer_window)
new_customer_btn.grid(row=2, column=0, columnspan=2, pady=10, ipadx=100)

new_vehicle_btn = Button(root, text='Add New Vehicle', command=new_vehicle_window)
new_vehicle_btn.grid(row=3, column=0, columnspan=2, pady=10, ipadx=100)

new_reservation_btn = Button(root, text='Add New Reservation', command=new_rental_window)
new_reservation_btn.grid(row=4, column=0, columnspan=2, pady=10, ipadx=100)

get_cust_btn = Button(root, text='Retrieve Customer Info', command=retrieve_customer_window)
get_cust_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=100)

get_vhcl_btn = Button(root, text='Retrieve Vehicle Info',command=retrieve_vehicle_window)
get_vhcl_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=100)


view_vehicle_btn = Button(root, text='View Available Vehicles', command=view_vehicle_window)
view_vehicle_btn.grid(row=7, column=0, columnspan=2, pady=10, ipadx=100)

# execute the tkinter components
root.mainloop()
