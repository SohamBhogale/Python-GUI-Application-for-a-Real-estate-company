from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import re, pymysql, os

import tkinter as tk
from tkinter.filedialog import askdirectory # for selecting our particular directory# for UI
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import collections 

from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = pd.read_excel("F:\\py intern\\DataSet.xlsx") 

# This function is used for adjusting window size and making the necessary configuration on start of window
def adjustWindow(window):
    w = 800 # width for the window size
    h = 600 # height for the window size
    ws = screen.winfo_screenwidth() # width of the screen
    hs = screen.winfo_screenheight() # height of the screen
    x = (ws/2) - (w/2) # calculate x and y coordinates for the Tk window
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y)) # set the dimensions of the screen and where it is placed
    window.resizable(False, False) # disabling the resize option for the window
    window.configure(background='white') # making the background white of the window
    
#===============================================================================================================    
#report module 3
def generate():
    connection = pymysql.connect(host="localhost", user="root", port=3308,database="Sales") # database connection
    cursor = connection.cursor()
    select_query = "SELECT orders.ORD_NUM,orders.ORD_AMOUNT,orders.ADVANCE_AMOUNT,(orders.ORD_AMOUNT-orders.ADVANCE_AMOUNT)"+" balance_amount,agents.AGENT_CODE,agents.AGENT_NAME " +"FROM orders INNER JOIN agents ON orders.AGENT_CODE = agents.AGENT_CODE  ORDER BY balance_amount DESC" +";" # queries forretrieving values
    cursor.execute(select_query) # executing the queries
    balance_record = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if len(balance_record) > 0:
        for i in range(len(balance_record)):
            for j in range(6):
                Label(fcanvas, text=balance_record[i][j], font=("Open Sans", 10, 'bold'),fg='black', bg='white').grid(row=i+4,column=j,padx=33,pady=15)
    else:
        messagebox.showerror("Error", "Connection Error",parent=screen9)
        
    fcanvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))      

def balance():
    global screen9,canvas,frame_main,vsb,fcanvas
    screen9 = tk.Tk()
    screen9.title("Balance Report")
    adjustWindow(screen9)
    screen9.configure(bg='khaki1')

    frame_main = tk.Frame(screen9,width="1000",height="600" ,bg="khaki1")
    frame_main.pack(side="top")
    
    Label(frame_main, text="Balance Amount Report", font=("Calibri", 22, 'bold'), fg='white',bg='gold').grid(row=0,columnspan=6, pady=(15,10))   
    label1 = tk.Label(frame_main, text="Click The Following Button To Generate The Report",font=("Open Sans",11) ,fg="black",bg='khaki1')
    label1.grid(row=1, columnspan=6, pady=(15, 5))
    
    Button(frame_main, text='Generate Report',width=15, font=("Open Sans", 10,'bold'),bg='black', fg='white',command=generate).grid(row=2,columnspan=6, pady=(15,15))
   
    Label(frame_main, text="Order Number", font=("Open Sans", 10, 'bold'), fg='black',bg='khaki1').grid(row=3,column=0,padx=10 ,pady=(15,15))
    Label(frame_main, text="Order Amount", font=("Open Sans", 10, 'bold'), fg='black',bg='khaki1').grid(row=3,column=1,padx=10  ,pady=(15,15))
    Label(frame_main, text="Advance Amount", font=("Open Sans", 10, 'bold'), fg='black',bg='khaki1').grid(row=3,column=2,padx=10 , pady=(15,15))
    Label(frame_main, text="Balance Amount",font=("Open Sans", 10, 'bold'), fg='black',bg='khaki1').grid(row=3,column=3,padx=10  ,pady=(15,15))
    Label(frame_main, text="Agent Code", font=("Open Sans", 10, 'bold'), fg='black',bg='khaki1').grid(row=3,column=4,padx=10  ,pady=(15,15))
    Label(frame_main, text="Agent Name", font=("Open Sans", 10, 'bold'), fg='black',bg='khaki1').grid(row=3,column=5,padx=10 ,pady=(15,15))
    
    canvas = tk.Canvas(frame_main,bg="white")
    canvas.grid(row=4, columnspan=6, sticky="news")   
    canvas.grid_propagate(False)
    
    vsb=tk.Scrollbar(frame_main,orient="vertical",command=canvas.yview)      
    canvas.configure(yscrollcommand=vsb.set)
    vsb.grid(row=4, column=7, sticky='ns')
    
    fcanvas=tk.Frame(canvas,bg="white")
    canvas.create_window((0, 0), window=fcanvas,anchor='nw')
    
    Button(screen9, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screen9.destroy).place(x=670, y=550) 
    
#===============================================================================================================   
#module 4   
def evaluate11():#The total property area sold vs total property are leased in Sq-M only.
    global a,b,c
    a=[]
    connection = pymysql.connect(host="localhost", user="root", port=3308,database="Sales") # database connection
    cursor = connection.cursor()
    select_query= "select CUST_COUNTRY from customer group by CUST_COUNTRY having count(CUST_COUNTRY) = ( select max(total) as highest_total from ( select CUST_COUNTRY , count(CUST_COUNTRY) as total from customer group by CUST_COUNTRY ) as t )" # queries forretrieving values
    cursor.execute(select_query) # executing the queries
    a = cursor.fetchall()
    a = [tuple(str(item) for item in t) for t in a]
    #a.append( str(cursor.fetchall()).strip('(),"') )
    Label(screen2, text="Country with maximum number of registered customer:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=445)
    Label(screen2, text=a, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=550, y=445)

    b=[]
    select_query1= "SELECT SUM(PAYMENT_AMT) as collective FROM customer WHERE CUST_COUNTRY=( select CUST_COUNTRY as country from customer group by CUST_COUNTRY having count(CUST_COUNTRY) = ( select max(total) as highest_total from ( select CUST_COUNTRY, count(CUST_COUNTRY) as total from customer group by CUST_COUNTRY ) as t ) )" # queries forretrieving values
    cursor.execute(select_query1) # executing the queries
    b = cursor.fetchall()
    b = [tuple(str(item) for item in t) for t in b]
    #b.append( str(cursor.fetchall()).strip('(),"') )
    Label(screen2, text="Collective payment amount for all these customers:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=470)
    Label(screen2, text=b, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=550, y=470)
 
    c=[]
    select_query3= "SELECT SUM(OUTSTANDING_AMT) as collective FROM customer WHERE CUST_COUNTRY=( select CUST_COUNTRY as country from customer group by CUST_COUNTRY having count(CUST_COUNTRY) = ( select max(total) as highest_total from ( select CUST_COUNTRY, count(CUST_COUNTRY) as total from customer group by CUST_COUNTRY ) as t ) )" # queries forretrieving values
    cursor.execute(select_query3) # executing the queries
    c = cursor.fetchall()
    c = [tuple(str(item) for item in t) for t in c]
    #c.append( str(cursor.fetchall()).strip('(),"') )
    Label(screen2, text="Collective outstanding amount for all these customers:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=495)
    Label(screen2, text=c, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=550, y=495)

    connection.commit() # commiting the connection then closing it.
    connection.close()
    
#===============================================================================================================   
#add customer      
def register_customer():
    if custcodee.get() and custname.get() and custcity.get() and custwork.get() and custcont.get() and custgrade.get() and openamt.get() and receiveamt.get() and payamt.get() and outamt.get() and custphone.get() and agentcodeee.get() :# checking for all empty values in entry field        
            #custcodee
            if all(x.isalnum() for x in custcodee.get()) and (len(custcodee.get())> 0): 
                #custname
                if all(x.isalpha() or x.isspace() for x in custname.get()) and (len(custname.get())> 0):
                    #custcity
                    if all(x.isalpha() or x.isspace() for x in custcity.get()) and (len(custcity.get())> 0): 
                        #custwork
                        if all(x.isalpha() or x.isspace()for x in custwork.get()) and (len(custwork.get())> 0): 
                            #custcont
                            if all(x.isalpha() or x.isspace()for x in custcont.get()) and (len(custcont.get())> 0): 
                                #custgrade
                                if all(x.isdigit() for x in custgrade.get()) and (len(custgrade.get())> 0):
                                    #openamt
                                    if all(x.isdecimal() or x.isdigit() for x in openamt.get()) and (len(openamt.get())> 0): 
                                        #receiveamt
                                        if all(x.isdecimal() or x.isdigit() for x in receiveamt.get()) and (len(receiveamt.get())> 0): 
                                            #payamt
                                            if all(x.isdecimal() or x.isdigit() for x in payamt.get()) and (len(payamt.get())> 0): 
                                                #outamt
                                                if all(x.isdecimal() or x.isdigit() for x in outamt.get()) and (len(outamt.get())> 0): 
                                                    #custphone
                                                    if len(custphone.get()) == 10 and custphone.get().isdigit(): #checking no of digits and integer
                                                        #agentcodeee
                                                        if all(x.isalnum() for x in agentcodeee.get()) and (len(agentcodeee.get())> 0): 
                                                            #if u enter in this block everything is fine just enter the values in database
                                                            connection = pymysql.connect(port=3308, host="localhost", user="root",password="", database="sales") # database connection
                                                            cursor = connection.cursor()
                                                            #insert_query =   # queries for inserting values
                                                            cursor.execute("""INSERT INTO customer (CUST_CODE,CUST_NAME,CUST_CITY,WORKING_AREA,CUST_COUNTRY,GRADE,OPENING_AMT,RECEIVE_AMT,PAYMENT_AMT,OUTSTANDING_AMT,PHONE_NO,AGENT_CODE)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(custcodee.get(),custname.get(),custcity.get(),custwork.get(),custcont.get(),custgrade.get(),openamt.get(),receiveamt.get(),payamt.get(),outamt.get(),custphone.get(),agentcodeee.get())) # executing the queries
                                                            connection.close() # closing the connection of the database
                                                            Label(screend, text="Registration Sucessful", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580) #printing successful registration message
                                                            Button(screend, text="Main Menu", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=screend.destroy).place(x=230, y=500) # button to navigate back              
                                                            Button(screend, text="Add New Customer", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=clearcustomer).place(x=430, y=500)   
                                                        else:
                                                            Label(screend, text="Please enter proper Agent Code", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                                            return
                                                    else:
                                                        Label(screend, text="Mobile No should be 10 digits in length, Only numbers are accepted", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                                        return 
                                                else:
                                                    Label(screend, text="Outstanding Amount can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                                    return
                                            else:
                                                Label(screend, text="Payment Amount can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                                return
                                        else:
                                            Label(screend, text="Receive Amount can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                            return 
                                    else:
                                        Label(screend, text="Opening Amount can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                        return                  
                                else:
                                    Label(screend, text="Grade can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                    return
                            else:
                                Label(screend, text="Country name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                return 
                        else:
                            Label(screend, text="Working area cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                            return
                    else:
                        Label(screend, text="City name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                        return
                else:
                    Label(screend, text="Customer name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                    return
            else:
                Label(screend, text="Please enter proper customer code", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                return
    else:
        Label(screend, text="Please fill all the details", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
        return
  
def clearcustomer():
    custcodee.set("")
    custname.set("")
    custcity.set("") 
    custwork.set("")
    custcont.set("")
    custgrade.set("")
    openamt.set("")
    receiveamt.set("")
    payamt.set("")
    outamt.set("")
    custphone.set("")
    agentcodeee.set("")
    Label(screend, text="", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580)                             

def addcustomer():
    global screend,custcodee,custname,custcity,custwork,custcont,custgrade,openamt,receiveamt,payamt,outamt,custphone,agentcodeee # making all entry field variable global
    custcodee = StringVar()
    custname = StringVar()
    custcity = StringVar()
    custwork= StringVar()    
    custcont = StringVar()
    custgrade = StringVar()
    openamt = StringVar()
    receiveamt = StringVar()
    payamt = StringVar()
    outamt = StringVar()
    custphone = StringVar()
    agentcodeee = StringVar()

    screend = Toplevel(screen2)
    screend.title("Add Customer")
    adjustWindow(screend) # configuring the window
    Label(screend, text="Add New Customers", width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    Label(screend, text="", bg='khaki1', width='70', height='27').place(x=150, y=90)
    screend.configure(bg='white')
    Label(screend, text="Customer Code:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=100)
    Entry(screend, textvar=custcodee).place(x=410, y=100)
    Label(screend, text="Customer Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=130)
    Entry(screend, textvar=custname).place(x=410, y=130)
    Label(screend, text="Customer City:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=160)
    Entry(screend, textvar=custcity).place(x=410, y=160)  
    Label(screend, text="Working Area:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=190)
    Entry(screend, textvar=custwork).place(x=410, y=190)
    Label(screend, text="Customer Country:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=220)
    Entry(screend, textvar=custcont).place(x=410, y=220)    
    Label(screend, text="Grade:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=250)
    Entry(screend, textvar=custgrade).place(x=410, y=250)
    Label(screend, text="Opening Amt:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=280)
    Entry(screend, textvar=openamt).place(x=410, y=280)   
    Label(screend, text="Receive Amt:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=310)
    Entry(screend, textvar=receiveamt).place(x=410, y=310)   
    Label(screend, text="Payment Amt:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=340)
    Entry(screend, textvar=payamt).place(x=410, y=340)   
    Label(screend, text="Outstanding Amt:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=370)
    Entry(screend, textvar=outamt).place(x=410, y=370)   
    Label(screend, text="Phone No:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=400)
    Entry(screend, textvar=custphone).place(x=410, y=400)   
    Label(screend, text="Agent Code:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=430)
    Entry(screend, textvar=agentcodeee).place(x=410, y=430)   
    Button(screend, text='Submit', width=16, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=register_customer).place(x=330, y=465)       
    Button(screend, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screend.destroy).place(x=670, y=550) 
    
#===============================================================================================================   
#add order      
def register_order():
    dayy=cbx11.get()
    monthh=cbx22.get()
    yearr=cbx33.get()
    o=ordamount.get()
    a=advamount.get()
    bal=int(o)-int(a)
    print(bal)
    if custcode.get() and ordnum.get() and ordamount.get() and advamount.get() and agentcodee.get() and orddes.get(): # checking for all empty values in entry field        
            #ordnum
            if all(x.isdigit() for x in ordnum.get()) and (len(ordnum.get())> 0): 
                #ordamount
                if all(x.isdecimal() or x.isdigit() for x in ordamount.get()) and (len(ordamount.get())> 0):
                    #advamount
                    if all(x.isdecimal() or x.isdigit() for x in advamount.get()) and (len(advamount.get())> 0): 
                        #custcode
                        if all(x.isalnum() for x in custcode.get()) and (len(custcode.get())> 0): 
                            #agentcodee
                            if all(x.isalnum() for x in agentcodee.get()) and (len(agentcodee.get())> 0): 
                                #orddes
                                if all(x.isalpha() for x in orddes.get()) and (len(orddes.get())> 0):
                                    #if u enter in this block everything is fine just enter the values in database
                                    connection = pymysql.connect(port=3308, host="localhost", user="root",password="", database="sales") # database connection
                                    cursor = connection.cursor()
                                    #insert_query =   # queries for inserting values
                                    cursor.execute("""INSERT INTO orders (ORD_NUM,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_DATE,CUST_CODE,AGENT_CODE,ORD_DESCRIPTION,Balance)values(%s,%s,%s,%s,%s,%s,%s,%s)""",(ordnum.get(),ordamount.get(),advamount.get(),yearr+"-"+monthh+"-"+dayy,custcode.get(),agentcodee.get(),orddes.get(),bal)) # executing the queries
                                    #connection.commit() # commiting the connection then closing it.
                                    connection.close() # closing the connection of the database
                                    Label(screenc, text="Registration Sucessful", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580) #printing successful registration message
                                    Button(screenc, text="Main Menu", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=screenc.destroy).place(x=230, y=470) # button to navigate back               
                                    Button(screenc, text="Add New Order", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=clearorder).place(x=430, y=470)                                                         
                                else:
                                    Label(screenc, text="Order Description cannot contain digits or special characters", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                    return
                            else:
                                Label(screenc, text="Please enter proper Agent Code", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                return 
                        else:
                            Label(screenc, text="Please enter proper Customer Code", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                            return
                    else:
                        Label(screenc, text="Advance Amount can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                        return
                else:
                    Label(screenc, text="Order Amount can contain only digits", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                    return
            else:
                Label(screenc, text="Please enter proper order number. No character allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                return
    else:
        Label(screenc, text="Please fill all the details", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
        return
  
def clearorder():
    ordnum.set("")
    ordamount.set("")
    advamount.set("") 
    custcode.set("")
    agentcodee.set("")
    orddes.set("")
    cbx11.set("1")
    cbx22.set("1")
    cbx33.set("2000")
    Label(screenc, text="", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580)                             

def addorder():
    global screenc, ordnum, ordamount, advamount, custcode, agentcodee, orddes,cbx11, cbx22, cbx33 # making all entry field variable global
    ordnum = StringVar()
    ordamount = StringVar()
    advamount= StringVar()    
    orddate = StringVar()
    custcode = StringVar()
    agentcodee = StringVar()
    orddes = StringVar()

    screenc = Toplevel(screen2)
    screenc.title("Add Orders")
    adjustWindow(screenc) # configuring the window
    Label(screenc, text="Add New Orders", width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    Label(screenc, text="", bg='khaki1', width='70', height='24').place(x=150, y=100)
    screenc.configure(bg='white')
    Label(screenc, text="Order No:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=120)
    Entry(screenc, textvar=ordnum).place(x=410, y=120)
    Label(screenc, text="Order Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=160)
    Entry(screenc, textvar=ordamount).place(x=410, y=160)
    Label(screenc, text="Advance Amount:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=200)
    Entry(screenc, textvar=advamount).place(x=410, y=200)
    
    #order date
    Label(screenc, text="Order Date:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=240)
    
    # create combo boxes
    dayy=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
    cbx11 = ttk.Combobox(screenc,width=2,state='readonly',values=dayy,font=("Open Sans", 11, 'bold'),height=5)
    cbx11.place(x=280,y=260)
    cbx11.current(0)
    Label(screenc, text="Day:",font=("Open Sans", 10), fg='black',bg='khaki1', anchor=W).place(x=245, y=260)
    
    monthh=('1','2','3','4','5','6','7','8','9','10','11','12')    
    cbx22 = ttk.Combobox(screenc,values=monthh,state='readonly',width=2,font=("Open Sans", 10,'bold'),height=5)
    cbx22.place(x=400,y=260)
    cbx22.current(0)
    Label(screenc,text="Month:",width=5,font=("Open Sans", 10),fg='black',bg='khaki1', anchor=W).place(x=350,y=260)     
 
    yearr=('2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020')
    cbx33 = ttk.Combobox(screenc,values=yearr,width=4,font=("Open Sans", 10,'bold'),state='readonly')
    cbx33.place(x=500,y=260)
    cbx33.current(0)    
    Label(screenc,text="Year:",width=4,font=("Open Sans", 10),fg='black',bg='khaki1', anchor=W).place(x=460,y=260)   
    #date End
    
    Label(screenc, text="Customer Code:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=300)
    Entry(screenc, textvar=custcode).place(x=410, y=300)
    Label(screenc, text="Agent Code:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=340)
    Entry(screenc, textvar=agentcodee).place(x=410, y=340)    
    Label(screenc, text="Order Desc:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=265, y=380)
    Entry(screenc, textvar=orddes).place(x=410, y=380)   
    Button(screenc, text='Submit', width=16, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=register_order).place(x=330, y=420)       
    Button(screenc, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screenc.destroy).place(x=670, y=550) 

#===============================================================================================================   
#add agent  
def register_agent():
    if agentcode.get() and agentname.get() and workingarea.get() and commission.get() and mobilenoagent.get() and countrynameagent.get(): # checking for all empty values in entry field
        #Agentcode
        if all(x.isalnum() for x in agentcode.get()) and (len(agentcode.get())> 0): 
            #Agentname
            if all(x.isalpha() or x.isspace() for x in agentname.get()) and (len(agentname.get())> 0):
                #workingarea
                if all(x.isalpha() or x.isspace() for x in workingarea.get()) and (len(workingarea.get())> 0): 
                    #commission
                    if all(x.isdecimal() or x.isdigit() for x in commission.get()) and (len(commission.get())> 0):
                        #mobile
                        if len(mobilenoagent.get()) == 10 and mobilenoagent.get().isdigit(): #checking no of digits and integer
                            #countryname
                            if all(x.isalpha() or x.isspace() for x in countrynameagent.get()) and (len(countrynameagent.get())> 0):
                                #if u enter in this block everything is fine just enter the values in database
                                connection = pymysql.connect(port=3308, host="localhost", user="root",password="", database="sales") # database connection
                                cursor = connection.cursor()
                                #insert_query =   # queries for inserting values
                                cursor.execute("""INSERT INTO agents (AGENT_CODE,AGENT_NAME,WORKING_AREA,COMMISSION,PHONE_NO,COUNTRY)values(%s,%s,%s,%s,%s,%s)""",(agentcode.get(),agentname.get(),workingarea.get(),commission.get(),mobilenoagent.get(),countrynameagent.get())) # executing the queries
                                #connection.commit() # commiting the connection then closing it.
                                connection.close() # closing the connection of the database
                                Label(screena, text="Agent Registered Sucessfully", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580) #printing successful registration message
                                Button(screena, text="Main Menu", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=screena.destroy).place(x=230, y=375) # button to navigate back              
                                Button(screena, text="Add New Agent", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=clearagents).place(x=430, y=375)                                                         
                            else:
                                Label(screena, text="Country name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                return 
                        else:
                            Label(screena, text="Mobile No should be 10 digits in length, Only numbers are accepted", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                            return
                    else:
                        Label(screena, text="Only numbers are accepted in Commission", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                        return
                else:
                    Label(screena, text="Working area cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                    return
            else:
                Label(screena, text="Agent Name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                return
        else:
            Label(screena, text="Please enter proper Agent Code", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
            return
    else:
        Label(screena, text="Please fill all the details", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
        return
    
def clearagents():
    agentcode.set("")
    agentname.set("")
    workingarea.set("") 
    commission.set("")
    mobilenoagent.set("")
    countrynameagent.set("")
    Label(screena, text="", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580)                             

def addagent():
    global screena, agentcode, agentname, workingarea, commission , mobilenoagent, countrynameagent# making all entry field variable global
    agentcode = StringVar()
    agentname = StringVar()
    workingarea= StringVar()    
    commission = StringVar()
    mobilenoagent = StringVar()
    countrynameagent = StringVar()

    screena = Toplevel(screen2)
    screena.title("Add Agent")
    adjustWindow(screena) # configuring the window
    Label(screena, text="Register New Agents", width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    Label(screena, text="", bg='khaki1', width='70', height='18').place(x=150, y=90)
    screena.configure(bg='white')
    Label(screena, text="Agent Code:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=100)
    Entry(screena, textvar=agentcode).place(x=400, y=100)
    Label(screena, text="Agent Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=140)
    Entry(screena, textvar=agentname).place(x=400, y=140)
    Label(screena, text="Working Area:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=180)
    Entry(screena, textvar=workingarea).place(x=400, y=180)
    Label(screena, text="Commission:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=220)
    Entry(screena, textvar=commission).place(x=400, y=220)
    Label(screena, text="Mobile No:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=260)
    Entry(screena, textvar=mobilenoagent).place(x=400, y=260)
    Label(screena, text="Country Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=300)
    Entry(screena, textvar=countrynameagent).place(x=400, y=300)    
    Button(screena, text='Submit', width=16, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=register_agent).place(x=330, y=330)   
    
    photo=Image.open('p.jpg')
    photo1 = photo.resize((180,170), Image.ANTIALIAS) 
    photo1 =  ImageTk.PhotoImage(photo1)
    label = Label(screena, image=photo1, text="",bd=0) # attaching image to the label
    label.place(x=310, y=410)
    label.Image = photo1
    Button(screena, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screena.destroy).place(x=670, y=550) 

#===============================================================================================================   
#add company
def register_company():
    if compid.get() and compname.get() and compcity.get(): # checking for all empty values in entry field
        #id
        if all(x.isdigit() for x in compid.get()) and (len(compid.get())> 0): 
            #compname
            if all(x.isalpha() or x.isspace() for x in compname.get()) and (len(compname.get())> 0):
                #compcity
                if all(x.isalpha() or x.isspace() for x in compcity.get()) and (len(compcity.get())> 0): 
                    #if u enter in this block everything is fine just enter the values in database
                    connection = pymysql.connect(port=3308, host="localhost", user="root",password="", database="sales") # database connection
                    cursor = connection.cursor()
                    #insert_query =   # queries for inserting values
                    cursor.execute("""INSERT INTO company (COMPANY_ID,COMPANY_NAME,COMPANY_CITY)values(%s,%s,%s)""",(compid.get(),compname.get(),compcity.get())) # executing the queries
                    #connection.commit() # commiting the connection then closing it.
                    connection.close() # closing the connection of the database
                    Label(screenb, text="Company Registered Sucessfully", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580) #printing successful registration message
                    Button(screenb, text="Main Menu", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=screenb.destroy).place(x=230, y=330) # button to navigate back to login page               
                    Button(screenb, text="Add New Company", width=16, font=("Open Sans", 10,'bold'), bg='red', fg='white',command=clearcompany).place(x=430, y=330)                                                         
                else:
                    Label(screenb, text="Company City cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                    return
            else:
                Label(screenb, text="Company Name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                return
        else:
            Label(screenb, text="Please enter proper Company Id", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
            return
    else:
        Label(screenb, text="Please fill all the details", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
        return
    
def clearcompany():
    compid.set("")
    compname.set("")
    compcity.set("") 
    Label(screenb, text="", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580)                           

def addcompany():
    global screenb, compid, compname, compcity# making all entry field variable global
    compid = StringVar()
    compname = StringVar()
    compcity= StringVar()    

    screenb = Toplevel(screen2)
    screenb.title("Add Company")
    adjustWindow(screenb) # configuring the window
    Label(screenb, text="Register New Company", width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    Label(screenb, text="", bg='khaki1', width='70', height='13').place(x=150, y=100)
    screenb.configure(bg='white')
    Label(screenb, text="Company Id:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=275, y=120)
    Entry(screenb, textvar=compid).place(x=400, y=120)
    Label(screenb, text="Company Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=275, y=160)
    Entry(screenb, textvar=compname).place(x=400, y=160)
    Label(screenb, text="Company City:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=275, y=200)
    Entry(screenb, textvar=compcity).place(x=400, y=200)
    
    photo=Image.open('i.png')
    photo1 = photo.resize((220,192), Image.ANTIALIAS) 
    photo1 =  ImageTk.PhotoImage(photo1)
    label = Label(screenb, image=photo1, text="",bd=0) # attaching image to the label
    label.place(x=288, y=380)
    label.Image = photo1
    
    Button(screenb, text='Submit', width=16, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=register_company).place(x=330, y=250)    
    Button(screenb, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screenb.destroy).place(x=670, y=550) 
    
#===============================================================================================================        
# welcome window
def welcome_page(student_info):
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Welcome")
    adjustWindow(screen2) # configuring the window
    Label(screen2, text="Welcome " + student_info[0][0], width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    screen2.configure(bg='white')

    photo=Image.open('mm.jpg')
    photo1 = photo.resize((220, 220), Image.ANTIALIAS) 
    photo1 =  ImageTk.PhotoImage(photo1)
    label = Label(screen2, image=photo1, text="",bd=0) # attaching image to the label
    label.place(x=570, y=90)
    label.Image = photo1

    Label(screen2, text="Click on any given button to enter a record", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=90)
    Button(screen2, text='Add Agent', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=addagent).place(x=20, y=115)
    Button(screen2, text='Add Company', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=addcompany).place(x=200, y=115)
    Button(screen2, text='Add Customer', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=addcustomer).place(x=20, y=160)
    Button(screen2, text='Add Order', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=addorder).place(x=200, y=160)
    
    Label(screen2, text="Click on the Order look up button to search based on the following criteria", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=200) 
    Label(screen2, text="a) Order number     b) Order Date     c) Customer code", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=225)    
    Label(screen2, text="Note: You can use either one or all of them together at a time", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=250)
    Button(screen2, text='View Orders', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=order_lookup).place(x=20, y=280)
    
    Label(screen2, text="Report regarding the balance amount of all orders can be viewed by clicking the button below", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=320)     
    Button(screen2, text='View Report', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=balance).place(x=20, y=350)
    
    Label(screen2, text="Which is the country with maximum number of registered customers and what is the collective payment", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=390)
    Label(screen2, text="amount and outstanding amount for all these customers collctively", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=415)   
    Button(screen2, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=evaluate11).place(x=20, y=445)
   
    Button(screen2, text='Insights1', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=insights_page).place(x=20, y=550)
    Button(screen2, text='Insights2', width=12, font=("Open Sans", 10, 'bold'),bg='black', fg='white',command=insights_page2).place(x=345, y=550)   
    Button(screen2, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screen2.destroy).place(x=670, y=550) 
    
#===============================================================================================================   
#insights
def evaluate1():#The total property area sold vs total property are leased in Sq-M only.
    year2=cbx4.get()
    o=int(year2)
    a=data[(data.UoM=='SQ-M')&(data.Tenure=='Owned')&(data.Year==o)].Tenure.count()
    Label(screen3, text="Total Property Area Sold:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=115)
    Label(screen3, text="        ", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=350, y=115)
    Label(screen3, text=a, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=350, y=115)
    b=data[(data.UoM=='SQ-M')&(data.Tenure=='Leased')&(data.Year==o)].Tenure.count()
    Label(screen3, text="Total Property Area Leased:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=140)
    Label(screen3, text="        ", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=350, y=140)
    Label(screen3, text=b, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=350, y=140)
    
def evaluate2():#Of the years 2017,2018,2019- which year got maximum leased area in CA and WS countries.
    c=data[(data.Country=='CA')&(data.Tenure=='Leased')].Area.max()
    Label(screen3, text="Maximum Leased Area For CA Country:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=190)
    Label(screen3, text=c, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=500, y=190)
    
    d=(data[(data.Area==c)].Year).tolist()
    Label(screen3, text="Maximum Area Was Leased In Year:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=215)
    Label(screen3, text=d[0], font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=500, y=215)

    e=data[(data.Country=='WS')&(data.Tenure=='Leased')].Area.max()
    Label(screen3, text="Maximum Leased Area For WS Country:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=250)
    Label(screen3, text=e, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=500, y=250)
    
    f=(data[(data.Area==e)].Year).tolist()
    Label(screen3, text="Maximum Area Was Leased In Year:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=275)
    Label(screen3, text=f[0], font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=500, y=275)
    
def evaluate3():#What are the Agent codes of all the agents who have got deals in ‘OWNED’ categories across the years.
    agnt=((data[data.Tenure=='Owned'].Agent.str.strip()).drop_duplicates(keep='first')).tolist()
    agnt1 = str(agnt)[1:-1] 
    Label(screen3, text=agnt1, font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=350)
    
    agent_codes=[]
    #now apply select query for each agent and get the output!
    for i in agnt:
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT AGENT_CODE FROM agents where AGENT_NAME = '" + i +"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        agent_codes.append( str(cursor.fetchall()).strip('(),') )
        connection.commit() # commiting the connection then closing it.
        connection.close()
    
    res = str(agent_codes)[1:-1] 
    Label(screen3, text=res, font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=375)
    
def evaluate4():#For the city of chillwalk, which agent hs got the maximum deals in leased form.
    z=data[(data.City=='Chilliwack')&(data.Tenure=='Leased')].Agent.value_counts().idxmax()
    Label(screen3, text="For the City of Chilliwalk, The Agent with maximum deals in leased form:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=425)
    Label(screen3, text=z, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=650, y=425)

def evaluate5():#What is the amount of property area sold for the month of july for all the years.
    Samt=data[(data.Month=='JUL')&(data.Tenure=='Owned')&(data.UoM=='SQ-M')].Area.sum()
    Hamt=data[(data.Month=='JUL')&(data.Tenure=='Owned')&(data.UoM=='HA')].Area.sum()
    #adding the converted
    Samt=Samt+(Hamt*10000)
    Label(screen3, text="Property area sold in the month of July in all the years:", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=140, y=480)
    Label(screen3, text=Samt, font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=550, y=480)

# Insight window
def insights_page():
    global screen3,cbx4
    screen3 = Toplevel(screen2)
    screen3.title("Insights")
    adjustWindow(screen3) # configuring the window
    Label(screen3, text="Welcome to Insights ", width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    screen2.configure(bg='white')

    Label(screen3, text="The total property area sold vs total property are leased in Sq-M only", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=90)
    Label(screen3,text="Year:",width=4,font=("Open Sans", 11,'bold'),fg='black',bg='white', anchor=W).place(x=550,y=90)   
    year2=('2017','2018','2019','2020')
    cbx4 = ttk.Combobox(screen3,values=year2,width=4,font=("Open Sans", 11,'bold'),state='readonly')
    cbx4.place(x=600,y=90)
    cbx4.current(0)    
    Button(screen3, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=evaluate1).place(x=20, y=115)    
    
    Label(screen3, text="Of the years 2017,2018,2019 which year got maximum leased area in CA and WS Countries", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=165)
    Button(screen3, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=evaluate2).place(x=20, y=190)
   
    Label(screen3, text="Agent codes of all the agents who have got deals in ‘OWNED’ categories across the years", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=300)
    Button(screen3, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=evaluate3).place(x=20, y=325)
    
    Label(screen3, text="For the city of Chilliwalk, which agent has got the maximum deals in leased form", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=400)
    Button(screen3, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=evaluate4).place(x=20, y=425)
   
    Label(screen3, text="The amount of property area sold for the month of july for all the years", font=("Open Sans", 11, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=455)
    Button(screen3, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=evaluate5).place(x=20, y=480)
   
    Button(screen3, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screen3.destroy).place(x=670, y=550)

#===============================================================================================================       
# Insight window
def insights_page2():
    global screen4
    screen4 = Toplevel(screen2)
    screen4.title("Insights")
    adjustWindow(screen4) # configuring the window
    Label(screen4, text="Welcome to Insights ", width="550", height="2", font=("Calibri", 22,'bold'), fg='white', bg='gold').pack()
    screen4.configure(bg='white')

    Label(screen4, text="Compare the performance of all agents based on the area leased and owned for the years", font=("Open Sans", 12, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=100)
    Label(screen4, text="2017,2018 and 2019. Who has been the best performer?", font=("Open Sans", 12, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=125) 
    Button(screen4, text='Calculate:', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=years_report).place(x=20, y=150)    
    
    Label(screen4, text="Time series analysis report of the orders received", font=("Open Sans", 12, 'bold'), fg='red',bg='white', anchor=W).place(x=20, y=210) 
    Label(screen4, text="Order Date Vs Order Amount", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=240) 
    Button(screen4, text='View', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=time1).place(x=300, y=240)    
    Label(screen4, text="Order Date Vs Advance Amount", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=280) 
    Button(screen4, text='View', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=time2).place(x=300, y=280)    
    Label(screen4, text="Order Date Vs Balance Amount", font=("Open Sans", 11, 'bold'), fg='black',bg='white', anchor=W).place(x=20, y=320) 
    Button(screen4, text='View', width=12, font=("Open Sans", 10, 'bold'), bg='black',fg='white',command=time3).place(x=300, y=320)    

    photo=Image.open('b.jpg')
    photo1 = photo.resize((150,150), Image.ANTIALIAS) 
    photo1 =  ImageTk.PhotoImage(photo1)
    label = Label(screen4, image=photo1, text="",bd=0) # attaching image to the label
    label.place(x=330, y=400)
    label.Image = photo1
   
    Button(screen4, text='Back', width=12, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screen4.destroy).place(x=670, y=550)

#===============================================================================================================  
def time1():
    connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
    cursor = connection.cursor()
    SQLCommand="select ORD_DATE,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_AMOUNT-ADVANCE_AMOUNT as Balance from orders ORDER BY ORD_DATE ASC;"
    sql = SQLCommand
    df = pd.read_sql(sql, connection)
    df.to_csv('1.csv', index=False)
    connection.close()

    df = pd.read_csv('1.csv')
    df1 = DataFrame(df,columns=['ORD_DATE','ORD_AMOUNT'])
    
    root1= tk.Tk() 
    root1.title("Order Date Vs Order Amount")
    adjustWindow(root1) 
    
    figure1 = plt.Figure(figsize=(15,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    line1 = FigureCanvasTkAgg(figure1, root1)
    line1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df1 = df1[['ORD_DATE','ORD_AMOUNT']].groupby('ORD_DATE').sum()
    df1.plot(kind='line', legend=True, ax=ax1, color='r',marker='o', fontsize=10)
    ax1.set_title('Order Date Vs Order Amount')
 
    Button(root1, text='Back', width=12, font=("Open Sans", 10, 'bold'),bg='green2', fg='black',command=root1.destroy).place(x=675, y=555)    
 
def time2():
    connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
    cursor = connection.cursor()
    SQLCommand="select ORD_DATE,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_AMOUNT-ADVANCE_AMOUNT as Balance from orders ORDER BY ORD_DATE ASC;"
    sql = SQLCommand
    df = pd.read_sql(sql, connection)
    df.to_csv('1.csv', index=False)
    connection.close()

    df = pd.read_csv('1.csv')
    df2 = DataFrame(df,columns=['ORD_DATE','ADVANCE_AMOUNT'])
    
    root2= tk.Tk() 
    root2.title("Order Date Vs Advance Amount")
    adjustWindow(root2) 
    
    figure2 = plt.Figure(figsize=(15,5), dpi=100)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, root2)
    line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df2 = df2[['ORD_DATE','ADVANCE_AMOUNT']].groupby('ORD_DATE').sum()
    df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
    ax2.set_title('Order Date Vs Advance Amount')
 
    Button(root2 , text='Back', width=12, font=("Open Sans", 10, 'bold'),bg='green2', fg='black',command=root2.destroy).place(x=675, y=555)    
 
def time3():
    connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
    cursor = connection.cursor()
    SQLCommand="select ORD_DATE,ORD_AMOUNT,ADVANCE_AMOUNT,ORD_AMOUNT-ADVANCE_AMOUNT as Balance from orders ORDER BY ORD_DATE ASC;"
    sql = SQLCommand
    df = pd.read_sql(sql, connection)
    df.to_csv('1.csv', index=False)
    connection.close()

    df = pd.read_csv('1.csv')
    df3 = DataFrame(df,columns=['ORD_DATE','Balance'])
    
    root3= tk.Tk() 
    root3.title("Order Date Vs Balance Amount")
    adjustWindow(root3) 
    
    figure3 = plt.Figure(figsize=(15,5), dpi=100)
    ax3 = figure3.add_subplot(111)
    line3 = FigureCanvasTkAgg(figure3, root3)
    line3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df3 = df3[['ORD_DATE','Balance']].groupby('ORD_DATE').sum()
    df3.plot(kind='line', legend=True, ax=ax3, color='r',marker='o', fontsize=10)
    ax3.set_title('Order Date Vs Balance Amount')
 
    Button(root3, text='Back', width=12, font=("Open Sans", 10, 'bold'),bg='green2', fg='black',command=root3.destroy).place(x=675, y=555)    
 
#===============================================================================================================  
def generate17():
    global Owned17,Leased17,y17
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=0,column=4, pady=(15,15))
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=2,column=4, pady=(15,15))  
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=4,column=4, pady=(15,15)) 
    data = pd.read_excel("F:\\py intern\\DataSet.xlsx") 
    Owned17=data[(data.Tenure=='Owned')&(data.Year==2017)].Agent.value_counts().idxmax()
    Leased17=data[(data.Tenure=='Leased')&(data.Year==2017)].Agent.value_counts().idxmax()
    y17=2017
    Label(freport, text=y17, font=("Open Sans", 14), fg='red',bg='white').grid(row=0,column=4, pady=(15,15))
    Label(freport, text=Owned17, font=("Open Sans", 14),fg='red',bg='white').grid(row=2,column=4, pady=(15,15))  
    Label(freport, text=Leased17, font=("Open Sans", 14),fg='red',bg='white').grid(row=4,column=4, pady=(15,15)) 
    
def generate18():
    global Owned18,Leased18,y18
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=0,column=4, pady=(15,15))
    Label(freport, text="*************", font=("Open Sans", 12), fg='White',bg='White').grid(row=2,column=4, pady=(15,15))  
    Label(freport, text="*************", font=("Open Sans", 12), fg='White',bg='White').grid(row=4,column=4, pady=(15,15)) 
    data = pd.read_excel("F:\\py intern\\DataSet.xlsx") 
    Owned18=data[(data.Tenure=='Owned')&(data.Year==2018)].Agent.value_counts().idxmax()
    Leased18=data[(data.Tenure=='Leased')&(data.Year==2018)].Agent.value_counts().idxmax()
    y18=2018
    Label(freport, text=y18, font=("Open Sans", 14), fg='red',bg='white').grid(row=0,column=4, pady=(15,15))
    Label(freport, text=Owned18, font=("Open Sans", 14), fg='red',bg='white').grid(row=2,column=4, pady=(15,15))  
    Label(freport, text=Leased18, font=("Open Sans", 14), fg='red',bg='white').grid(row=4,column=4, pady=(15,15))

def generate19():
    global Owned19,Leased19,y19
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=0,column=4, pady=(15,15))
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=2,column=4, pady=(15,15))  
    Label(freport, text="*************", font=("Open Sans", 14), fg='White',bg='White').grid(row=4,column=4, pady=(15,15)) 
    data = pd.read_excel("F:\\py intern\\DataSet.xlsx") 
    Owned19=data[(data.Tenure=='Owned')&(data.Year==2019)].Agent.value_counts().idxmax()
    Leased19=data[(data.Tenure=='Leased')&(data.Year==2019)].Agent.value_counts().idxmax()
    y19=2019        
    Label(freport, text=y19, font=("Open Sans", 14), fg='red',bg='white').grid(row=0,column=4, pady=(15,15))
    Label(freport, text=Owned19, font=("Open Sans", 14),fg='red',bg='white').grid(row=2,column=4, pady=(15,15))  
    Label(freport, text=Leased19, font=("Open Sans", 14),fg='red',bg='white').grid(row=4,column=4, pady=(15,15))

def years_report():
    global screen22,frame_main,freport    
    screen22 = tk.Tk()
    screen22.title("Report Over All Years")
    adjustWindow(screen22)
    screen22.configure(bg='khaki1')    

    frame_main = tk.Frame(screen22,width="1000",height="600" ,bg="khaki1")
    frame_main.pack(side="top")
    
    Label(frame_main, text="REPORT OVER ALL YEARS", font=("Calibri", 22, 'bold'), fg='white',bg='gold').grid(row=0,columnspan=3, pady=(15,15))
    
    label1 = tk.Label(frame_main, text="Click On Any Of The Following Button To Generate The Report",font=("Open Sans", 14) ,fg="black",bg='khaki1')
    label1.grid(row=1, columnspan=3, pady=(15, 5))
    
    Button(frame_main, text='YEAR 2017', font=("Open Sans", 12, 'bold'),bg='black', fg='white',command=generate17).grid(row=2,column=0, pady=(15,15))
    Button(frame_main, text='YEAR 2018', font=("Open Sans", 12, 'bold'),bg='black', fg='white',command=generate18).grid(row=2,column=1, pady=(15,15))
    Button(frame_main, text='YEAR 2019', font=("Open Sans", 12, 'bold'),bg='black', fg='white',command=generate19).grid(row=2,column=2, pady=(15,15))    
  
    freport=tk.Frame(frame_main,bg="White")
    freport.grid(row=3, columnspan=3, sticky="news") 
    
    Label(freport, text="Best Performers For Year:", font=("Open Sans", 14), fg='black',bg='white').grid(row=0,columnspan=3, pady=(15,15))
    Label(freport, text="____", font=("Open Sans", 14), fg='white',bg='white').grid(row=0,column=4, pady=(15,15))
          
    Label(freport, text="For Properties Owned:", font=("Open Sans", 14), fg='black',bg='white').grid(row=2,columnspan=3, pady=(15,15))
    Label(freport, text="________", font=("Open Sans", 12), fg='white',bg='white').grid(row=2,column=4, pady=(15,15))      
    
    Label(freport, text="For Properties Leased:", font=("Open Sans", 14), fg='black',bg='white').grid(row=4,columnspan=3, pady=(15,15))
    Label(freport, text="_______", font=("Open Sans", 12), fg='white',bg='white').grid(row=4,column=4, pady=(15,15))      

    Button(screen22, text='Back', width=12, font=("Open Sans", 10, 'bold'),bg='green2', fg='black',command=screen22.destroy).place(x=670, y=550)    

#===============================================================================================================   
#order look up
def fetch_order():
    for i in range(7): # reset
        for j in range(7):
            Label(screen5, text="888888888", font=("Open Sans", 12),fg='khaki1', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
    if ((orderno.get()!='') and (custcode.get()!='') and (date.get()!='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where ORD_NUM = '" +orderno.get() + "' AND CUST_CODE = '" +custcode.get()+ "' AND ORD_DATE = '" +date.get()+"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)): # this loop will display the information to theuser
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Order Inputs!",parent=screen5)
    if((orderno.get()!='') and (custcode.get()=='') and (date.get()=='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where ORD_NUM = '" +orderno.get() +"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)):
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Order Number!",parent=screen5)
    if((orderno.get()=='') and (custcode.get()!='') and (date.get()=='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where CUST_CODE = '" +custcode.get() +"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)): # this loop will display the information to theuser
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Customer Code!",parent=screen5)
    if((orderno.get()=='') and (custcode.get()=='') and (date.get()!='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where ORD_DATE = '" +date.get() +"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)): # this loop will display the information to theuser
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Order Date!",parent=screen5)
            
    if ((orderno.get()!='') and (custcode.get()!='') and (date.get()=='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where ORD_NUM = '" +orderno.get() + "' AND CUST_CODE = '" +custcode.get()+"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)): # this loop will display the information to theuser
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Order Inputs!",parent=screen5)        
    if ((orderno.get()!='') and (custcode.get()=='') and (date.get()!='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where ORD_NUM = '" +orderno.get() + "' AND ORD_DATE = '" +date.get()+"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)): # this loop will display the information to theuser
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Order Inputs!",parent=screen5)
    if ((orderno.get()=='') and (custcode.get()!='') and (date.get()!='')):
        connection = pymysql.connect(host="localhost", user="root", port=3308,database="sales") # database connection
        cursor = connection.cursor()
        select_query = "SELECT * FROM orders where CUST_CODE = '" +custcode.get()+ "' AND ORD_DATE = '" +date.get()+"';" # queries forretrieving values
        cursor.execute(select_query) # executing the queries
        order_record = cursor.fetchall()
        connection.commit() # commiting the connection then closing it.
        connection.close() # closing the connection of the database
        if len(order_record) > 0:
            for i in range(len(order_record)): # this loop will display the information to theuser
                for j in range(7):
                    Label(screen5, text=order_record[i][j], font=("Open Sans", 12),fg='black', bg='khaki1').grid(row=i+7+4,column=j, pady=(5,1))
        else:
            messagebox.showerror("Error", "Invalid Order Inputs!",parent=screen5)
            
    if((orderno.get()=='') and (custcode.get()=='') and (date.get()=='')):
        messagebox.showerror("Error", "EMPTY FIELDS!",parent=screen5)
    
def order_lookup():
    global screen5,orderno,custcode,date
    screen5 =Toplevel(screen2)
    #screen2.destroy()
    screen5.title("ORDER LOOKUP")
    adjustWindow(screen5) # configuring the window 
    screen5.configure(bg='khaki1')
    orderno=StringVar()
    custcode=StringVar()
    date=StringVar()
    Label(screen5, text="Order Lookup ", height="2",font=("Open Sans", 15, 'bold'), fg='white', bg='gold').grid(row=0, sticky=W, columnspan=7)
    Label(screen5, text="", bg='khaki1').grid(row=1,columnspan=7)
    Label(screen5, text="   Order No:   ", font=("Open Sans", 11), fg='black',bg='khaki1', anchor=W).grid(row=2,column=0, pady=(4,1))
    Entry(screen5, textvar=orderno,font=("Open Sans", 11),width='12',bd=2).grid(row=2,column=1, pady=(4,1))
    Label(screen5, text="   Customer Code:   ", font=("Open Sans", 11), fg='black',bg='khaki1', anchor=W).grid(row=2,column=2, pady=(4,1))
    Entry(screen5, textvar=custcode,font=("Open Sans", 11),width='12',bd=2).grid(row=2,column=3, pady=(4,1))
    Label(screen5, text="Date:" ,font=("Open Sans", 11), fg='black',bg='khaki1', anchor=W).grid(row=2,column=4, pady=(4,1))
    Entry(screen5, textvar=date,font=("Open Sans", 11),bd=2).grid(row=2,column=5, pady=(4,1))
    Button(screen5, text='Search', width=5, font=("Open Sans", 10, 'bold'),bg='green2', fg='black',command=fetch_order).grid(row=2,column=6, pady=(4,1))
    Label(screen5, text="", bg='khaki1').grid(row=3,columnspan=7)
    #GRID FOR ORDER
    Label(screen5, text="   Order No", font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=0, pady=(4,1))
    Label(screen5, text="Amount", font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=1, pady=(4,1))
    Label(screen5, text="Advance", font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=2, pady=(4,1))
    Label(screen5, text="Date",font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=3, pady=(4,1))
    Label(screen5, text="Customer Code", font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=4, pady=(4,1))
    Label(screen5, text="Agent Code", font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=5, pady=(4,1))
    Label(screen5, text="Description", font=("Open Sans", 11), fg='black',bg='khaki1').grid(row=4,column=6, pady=(4,1))
          
    Button(screen5, text='Back', width=12, font=("Open Sans", 10, 'bold'),bg='green2', fg='black',command=screen5.destroy).place(x=670, y=550)    
    
#===============================================================================================================   
#reg
def clear():
    fullname.set("")
    email.set("")
    username.set("") 
    mobileno.set("")
    countryname.set("")
    password.set("")
    repassword.set("")
    cbx1.set("1")
    cbx2.set("1")
    cbx3.set("1950")
    gender.set(0)
    tnc.set(0)

def register_user():
    day=cbx1.get()
    month=cbx2.get()
    year=cbx3.get()
    if fullname.get() and email.get() and username.get() and mobileno.get() and countryname.get() and password.get() and repassword.get() and gender.get(): # checking for all empty values in entry field        
            #Fullname
            if all(x.isalpha() or x.isspace() for x in fullname.get()) and (len(fullname.get())> 0): #checking if digits in username and special char
                #Email
                if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email.get()):
                    #username
                    if all(x.isalpha() or x.isspace() for x in username.get()) and (len(username.get())> 0):
                        #mobile
                        if len(mobileno.get()) == 10 and mobileno.get().isdigit(): #checking no of digits and integer
                            #countryname
                            if all(x.isalpha() or x.isspace() for x in countryname.get()) and (len(countryname.get())> 0):
                                #password
                                if (len(password.get()) >= 4 and len(password.get()) <= 10):
                                    if password.get() == repassword.get(): # checking both password match or not
                                        #gender
                                        gender_value = 'Male'
                                        if gender.get() == 2:                           
                                            gender_value = 'Female'
                                        #tnc
                                        if tnc.get(): # checking for acceptance of agreement                               
                                            #if u enter in this block everything is fine just enter the values in database
                                            connection = pymysql.connect(port=3308, host="localhost", user="root",password="", database="sales") # database connection
                                            cursor = connection.cursor()
                                            #insert_query =   # queries for inserting values
                                            cursor.execute("""INSERT INTO registration (fullname,email,username,mobileno,countryname,password,dob,gender)values(%s,%s,%s,%s,%s,%s,%s,%s)""",(fullname.get(),email.get(),username.get(),mobileno.get(),countryname.get(),password.get(),year+"-"+month+"-"+day,gender_value)) # executing the queries
                                            #connection.commit() # commiting the connection then closing it.
                                            connection.close() # closing the connection of the database
                                            Label(screen1, text="Registration Sucess", fg="green", font=("Open Sans", 11), width='70', anchor=W, bg='white').place(x=0, y=580) #printing successful registration message
                                            clear()
                                            Button(screen1, text='Proceed to Login ->', width=16, font=("Open Sans", 13,'bold'), bg='red', fg='white',command=screen1.destroy).place(x=320, y=560) # button to navigate back to login page
                                        else:
                                            Label(screen1, text="Please accept the agreement", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                            return                                        
                                    else: 
                                        Label(screen1, text="Password does not match", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                        return
                                else:
                                    Label(screen1, text="The Length of Password should be between 4 and 10", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                    return
                            else:
                                Label(screen1, text="Country name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                                return 
                        else:
                            Label(screen1, text="Mobile No should be 10 digits in length, Only numbers are accepted", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                            return
                    else:
                        Label(screen1, text="User Name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                        return
                else:
                    Label(screen1, text="Please enter valid Email Id", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                    return
            else:
                Label(screen1, text="Full Name cannot contain digits or special characters. Spaces are allowed", fg="red", font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
                return
    else:
        Label(screen1, text="Please fill all the details", fg="red",font=("Open Sans", 11,'bold'), width='70', anchor=W, bg='white').place(x=0, y=580)
        return

# registration window
def register():
    global screen1, fullname, email, username, mobileno , countryname, password,repassword, cbx1, cbx2, cbx3 , gender, tnc # making all entry field variable global
    fullname = StringVar()
    email = StringVar()
    username= StringVar()
    mobileno = StringVar()
    countryname = StringVar()
    password = StringVar()
    repassword = StringVar()
    gender = IntVar()
    tnc = IntVar()
    screen1 = Toplevel(screen)
    screen1.title("Registeration")
    adjustWindow(screen1) # configuring the window
    Label(screen1, text="Welcome To Sunville Properties", width="550", height="1", font=("Open Sans", 22,'bold'), fg='white', bg='gold').pack()
    Label(screen1, text="Please Sign Up To Contiue", width="550", height="2", font=("Open Sans", 10,'bold'), fg='white', bg='gold').pack()
    Label(screen1, text="", bg='khaki1', width='72', height='31').place(x=150, y=100)
    screen1.configure(bg='white')
    Label(screen1, text="Full Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=120)
    Entry(screen1, textvar=fullname).place(x=400, y=120)
    Label(screen1, text="Email ID:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=160)
    Entry(screen1, textvar=email).place(x=400, y=160)
    Label(screen1, text="User Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=200)
    Entry(screen1, textvar=username).place(x=400, y=200)
    Label(screen1, text="Mobile No:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=240)
    Entry(screen1, textvar=mobileno).place(x=400, y=240)
    Label(screen1, text="Country Name:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=280)
    Entry(screen1, textvar=countryname).place(x=400, y=280)
    Label(screen1, text="Password:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=320)
    Entry(screen1, textvar=password, show="*").place(x=400, y=320)
    Label(screen1, text="Re-Password:", font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=360)
    entry_4 = Entry(screen1, textvar=repassword, show="*")
    entry_4.place(x=400, y=360)
    
    #DOB
    Label(screen1, text="Date of Birth:",font=("Open Sans", 11, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=285, y=400)
    
    # create combo boxes
    day=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
    cbx1 = ttk.Combobox(screen1,width=2,state='readonly',values=day,font=("Open Sans", 11, 'bold'),height=5)
    cbx1.place(x=300,y=420)
    cbx1.current(0)
    Label(screen1, text="Day:",font=("Open Sans", 10), fg='black',bg='khaki1', anchor=W).place(x=260, y=420)
    
    month=('1','2','3','4','5','6','7','8','9','10','11','12')    
    cbx2 = ttk.Combobox(screen1,values=month,state='readonly',width=2,font=("Open Sans", 10,'bold'),height=5)
    cbx2.place(x=400,y=420)
    cbx2.current(0)
    Label(screen1,text="Month:",width=5,font=("Open Sans", 10),fg='black',bg='khaki1', anchor=W).place(x=350,y=420)     
 
    year=('1950','1951','1952','1953','1954','1955','1956','1957','1958','1959','1960','1961','1962','1963','1964','1965','1966','1967','1968','1969','1970','1971','1972','1973','1974','1975','1976','1977','1978','1999','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020')
    cbx3 = ttk.Combobox(screen1,values=year,width=4,font=("Open Sans", 10,'bold'),state='readonly')
    cbx3.place(x=500,y=420)
    cbx3.current(0)    
    Label(screen1,text="Year:",width=4,font=("Open Sans", 10),fg='black',bg='khaki1', anchor=W).place(x=460,y=420)   
    #Dob End

    Label(screen1, text="Gender:", font=("Open Sans", 11, 'bold'), fg='black', bg='khaki1',anchor=W).place(x=285, y=460)
    Radiobutton(screen1, text="Male", variable=gender,font=("Open Sans", 10, 'bold'), value=1,bg='khaki1').place(x=400, y=460)
    Radiobutton(screen1, text="Female", variable=gender,font=("Open Sans", 10, 'bold'), value=2,bg='khaki1').place(x=470, y=460)
    Checkbutton(screen1, text="I accept all terms and conditions", variable=tnc,bg='khaki1', font=("Open Sans", 9, 'bold'), fg='red').place(x=300, y=490)
    Button(screen1, text='Submit', width=16, font=("Open Sans", 13, 'bold'), bg='black',fg='white',command=register_user).place(x=320, y=520)
    
    Button(screen1, text='Back', width=10, font=("Open Sans", 10,'bold'), bg='green2', fg='black',command=screen1.destroy).place(x=690, y=555) 

# login creditentials verification
def login_verify():
    global studentID
    connection = pymysql.connect(port=3308, host="localhost", user="root", password="", database="sales") # database connection
    cursor = connection.cursor()
    select_query = "SELECT * FROM registration where username = '" + username_verify.get() + "' AND password = '" + password_verify.get() + "';" # queries for retrieving values 
    cursor.execute(select_query) # executing the queries
    student_info = cursor.fetchall()
    connection.commit() # commiting the connection then closing it.
    connection.close() # closing the connection of the database
    if student_info:
        messagebox.showinfo("Congratulation", "Login Succesfull") # displaying message for successful login
        studentID = student_info[0][0]
        welcome_page(student_info) # opening welcome window
        clearlogin()
    else:
        messagebox.showerror("Error", "Invalid Username or Password") # displaying message for invalid details  
        clearlogin()
        
def clearlogin():
    username_verify.set("")
    password_verify.set("")

# login window
def main_screen():
    global screen, username_verify, password_verify
    screen = Tk() # initializing the tkinter window
    username_verify = StringVar()
    password_verify = StringVar()
    screen.title("Sunville Properties") # mentioning title of the window
    adjustWindow(screen) # configuring the window
    Label(screen, text="Sunville Properties", width="550", height="2",font=("Calibri", 22, 'bold'), fg='white', bg='gold').pack()
    Label(text="", bg='khaki1').pack() # for leaving a space in between
    screen.configure(bg='khaki1')
    Label(screen, text="", bg='khaki1').pack() # for leaving a space in between
    photo=Image.open('apaart.PNG')
    photo1 = photo.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
    photo2 =  ImageTk.PhotoImage(photo1)
    label = Label(screen, image=photo2, text="") # attaching image to the label
    label.place(x=275, y=100)
    Label(screen, text="Username:", font=("Open Sans", 13, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=260, y=390)
    Entry(screen, textvar=username_verify,font=("Open Sans", 13, 'bold'),bd=4).place(x=350, y=390)
    Label(screen, text="Password:", font=("Open Sans", 13, 'bold'), fg='black',bg='khaki1', anchor=W).place(x=260, y=430)
    Entry(screen, textvar=password_verify,font=("Open Sans", 13, 'bold'),bd=4,show="*").place(x=350, y=430)
    Button(screen, text='Login', width=16, font=("Open Sans", 13, 'bold'),bg='black', fg='white',command=login_verify).place(x=320, y=490)
    Button(screen, text='New to Sunville?', width=16, font=("Open Sans", 13, 'bold'),bg='black', fg='white',command=register).place(x=320, y=540)
    screen.mainloop()
main_screen()