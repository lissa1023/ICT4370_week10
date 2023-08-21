'''
Author: Melissa Lawrence
Date Created: 07/27/2023
Functionality: Complete Week 10 Assignment
Notes: Week 10 assignment involves creating a SQLITE db, 
populating with the raw csv files for stocks and bonds, 
and reading from the database back to the results tables 
we've been using. 
'''

#Import lots of objects and methods
from holdings_classes import *
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import sqlite3
import json 
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import os
import tkinter as tk
from tkinter import ttk

def add_user():
  '''adds a user or multiple users to a list'''
  user_count = len(users) +1
  user_list_name = ('user_' + str(user_count))
  user_list_name = User(user_count, 
                  entry_name.get(), 
                  entry_address.get(), 
                  entry_phone_num.get())
  verify_entry = (str(user_list_name.name) + ' ' +
                  str(user_list_name.address)  + ' ' +
                  str(user_list_name.phone_num) + ' ' +
                     'is assigned UserID: ' + str(user_list_name.userID))
  output_string.set(verify_entry) 
  print (verify_entry)
  users.append(user_list_name)

#add users with popup window
users = []

#window - create the window that pops up
window = tk.Tk()
window.title('Add Investor')
window.geometry('600x300')

#title - add text field widget for the title or prompt to input
title_label = ttk.Label(master = window, text = 
                        'Input the Investor Info', 
                        font = 'Calibri 12')
title_label.pack()

#input field - add the 3 widgets to accept input
input_frame =  ttk.Frame(master = window)
label_name = ttk.Label(master = window, text = 'Enter Name', 
                       font = 'Calibri 9')
entry_name = tk.StringVar()
entry_1 = ttk.Entry(master = input_frame, 
                    textvariable = entry_name)
label_address = ttk.Label(master = window, text = 'Enter Address', 
                          font = 'Calibri 9')
entry_address = tk.StringVar()
entry_2 = ttk.Entry(master = input_frame, 
                    textvariable = entry_address)
label_phone_num = ttk.Label(master = window, text = 'Enter Phone #', 
                            font = 'Calibri 9')
entry_phone_num = tk.StringVar()
entry_3 = ttk.Entry(master = input_frame, 
                    textvariable = entry_phone_num)
button_1 = ttk.Button(master = input_frame, 
                    text = 'Add User', command = add_user)
button_2 = ttk.Button(master = input_frame, 
                    text = 'Quit', command = window.quit)
label_name.pack()
entry_1.pack(pady = 5)
label_address.pack()
entry_2.pack(pady = 5)
label_phone_num.pack()
entry_3.pack(pady = 5)
button_1.pack(side = 'left', padx = 10, pady = 5)
button_2.pack(side = 'left', padx = 10, pady = 5)
input_frame.pack(pady = 10)

#output - add text field widget that reads back what was entered
output_string = tk.StringVar()
output_label = ttk.Label(
    master = window, 
    text = 'Output', 
    font = 'Calibri 12', 
    textvariable = output_string)
output_label.pack(pady = 5)

#run popup to add users
window.mainloop()

#idenitfy how many stocks and bonds are already in the lists
'''in this case, we are only retriving for one users, so I 
have hard-coded it for that user'''
user_1 = users[0]
stock_count = len(user_1.stock_holdings)
bond_count = len(user_1.bond_holdings)

#read the stock data file to stock classes
try:  
    df_stocks = pd.read_csv('Lesson6_Data_Stocks.csv')
    for index, row in df_stocks.iterrows():
        stock_count = stock_count + 1
        stock_list_name = ('stock_' + str(stock_count))
        stock_list_name = Stock(
            df_stocks['SYMBOL'].values[index], 
            df_stocks['PURCHASE_PRICE'].values[index],
            datetime.strptime(
              df_stocks['PURCHASE_DATE'].values[index],
              '%m/%d/%Y').date(),
            df_stocks['CURRENT_VALUE'].values[index],
            stock_count,
            df_stocks['NO_SHARES'].values[index])
        #add holding to list in account
        user_1.add_stock(stock_list_name)
except FileNotFoundError:
  print('The stock data file cannot be read.')
except Exception as e:
    print("Error:", str(e))
  
#read the bond data file to bond classes
try:  
    df_bonds = pd.read_csv('Lesson6_Data_Bonds.csv')
    for index, row in df_bonds.iterrows():
        bond_count = bond_count + 1
        bond_list_name = ('bond_' + str(bond_count))
        bond_list_name = Bond(
            df_bonds['SYMBOL'].values[index], 
            df_bonds['PURCHASE_PRICE'].values[index],
            datetime.strptime(
              df_bonds['PURCHASE_DATE'].values[index],
              '%m/%d/%Y').date(),
            df_bonds['CURRENT_VALUE'].values[index],
            bond_count,
            df_bonds['NO_SHARES'].values[index],
            df_bonds['Yield'].values[index],
            df_bonds['Coupon'].values[index])
        #add holding to list in account
        user_1.add_bond(bond_list_name)
except FileNotFoundError:
  print('The bond data file cannot be read.')
except Exception as e:
    print("Error:", str(e))

#create the database and tables 
# connect to sqlite database named investments and open a cursor
cx = sqlite3.connect('investments.db')  
cu = cx.cursor()

# using the sqlite cursor import csv file as table
cu.executescript("""
        DROP TABLE IF EXISTS data_stocks;
        DROP TABLE IF EXISTS data_bonds;
        DROP TABLE IF EXISTS stock_price_history;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS accounts
""")

cu.executescript("""
        CREATE TABLE users (
          userID INTEGER PRIMARY KEY
          ,username text
          ,address text
          ,phone_num text
        );
        
        CREATE TABLE accounts (
          accountID INTEGER PRIMARY KEY
          ,primary_owner INTEGER
          ,FOREIGN KEY (primary_owner) 
                 REFERENCES accounts (userID) 
        );
        
        CREATE TABLE data_stocks (
          stockID integer PRIMARY KEY
          ,account_num INTEGER
          ,holding_symbol text
          ,purchase_price text
          ,purchase_date text
          ,current_value text
          ,num_shares text
          ,earnings_per_stock_holding text
          ,avg_ann_per_stock_share text
          ,FOREIGN KEY (account_num) 
                 REFERENCES accounts (accountID)
        );
        
        CREATE TABLE data_bonds (
          bondID integer PRIMARY KEY 
          ,account_num integer
          ,holding_symbol text
          ,purchase_price text
          ,purchase_date text
          ,current_value text
          ,quantity text
          ,bond_yield text
          ,coupon text
          ,earnings_per_bond_holding text
          ,avg_ann_per_bond_item text
          ,FOREIGN KEY (account_num) 
                REFERENCES accounts (accountID)
        );

        CREATE TABLE stock_price_history(
          historyID integer PRIMARY KEY
          ,holding_symbol text
          ,history_date text
          ,open_value real
          ,high_value real
          ,low_value real
          ,close_value real
          ,trade_volume integer
          ,FOREIGN KEY (holding_symbol) 
               REFERENCES data_stocks (holding_symbol)
        )
""")

#populate the database from the classes
cu.executescript("""
        INSERT INTO users (
              userID
              ,username
              ,address
              ,phone_num) 
            VALUES (
              1,
              'Bob Smith',
              '123 Any Street, City, State Zip',
              '123.456.7890');
        INSERT INTO accounts (
              accountID
              ,primary_owner) 
            VALUES (1,1);
""")

'''write to stock table from DB. note that in this case 
all stocks and bonds go to account 1 therefore it is 
harcoded as accountID. normally this would either be 
an input function or it would have been read from somewhere.'''

for holding in user_1.stock_holdings:
  cu.execute("""INSERT INTO data_stocks (
                holding_symbol 
                ,purchase_price 
                ,purchase_date 
                ,current_value 
                ,stockID 
                ,num_shares
                ,earnings_per_stock_holding
                ,avg_ann_per_stock_share
                ,account_num
                )
                VALUES (?,?,?,?,?,?,?,?,?)
            """, 
                (holding.holding_symbol
                ,holding.purchase_price
                ,holding.purchase_date
                ,holding.current_value
                ,holding.stockID
                ,holding.num_shares
                ,holding.earnings_per_stock_holding() 
                ,holding.avg_ann_per_stock_share()
                ,1)      
            )
#write from DB to bond table. also hard coded account 1  
for holding in user_1.bond_holdings:
  cu.execute("""INSERT INTO data_bonds (
                holding_symbol 
                ,purchase_price 
                ,purchase_date 
                ,current_value 
                ,bondID 
                ,quantity
                ,bond_yield
                ,coupon
                ,earnings_per_bond_holding 
                ,avg_ann_per_bond_item 
                ,account_num
                )
                values (?,?,?,?,?,?,?,?,?,?,?)
            """, 
                (holding.holding_symbol
                ,holding.purchase_price
                ,holding.purchase_date
                ,holding.current_value
                ,holding.bondID
                ,holding.quantity
                ,holding.bond_yield
                ,holding.coupon
                ,holding.earnings_per_bond_holding()
                ,holding.avg_ann_per_bond_item()                
                ,1)
            )

#commit to db
cx.commit()

#read from stock price history file
try:
  history_file_path = 'AllStocks.json' 
  with open(history_file_path) as json_file: 
    data_set = json.load(json_file)
except FileNotFoundError:
    print('The account results file cannot be written.')
except IOError:
    print("Error: Unable to write to the output file.")
except Exception as e:
    print("Error:", str(e))

# connect to sqlite database named investments and open a cursor
cx = sqlite3.connect('investments.db')  
cu = cx.cursor()

#write to stock price history table
cu.execute("SELECT MAX(historyID) FROM stock_price_history") 
max_hist_ID = cu.fetchone()
if max_hist_ID[0] is None:
    count = 0
else: 
    count = int(max_hist_ID[0])
for item in data_set:
  cu.execute("""INSERT INTO stock_price_history (
                historyID 
                ,holding_symbol
                ,history_date
                ,open_value
                ,high_value
                ,low_value
                ,close_value
                ,trade_volume
                )
                values (?,?,?,?,?,?,?,?)
             """,
                (#this will be the variable from the json directly
                count
                ,item['Symbol']
                ,item['Date']
                ,item['Open']
                ,item['High']
                ,item['Low']
                ,item['Close']
                ,item['Volume']
                )
            )
  count = count + 1
#commit to db
cx.commit()

'''at this point, eveyrthing is in tables in my investments DB. 
from here, it is time to generate results (tables and charts).'''

#print stocks and bond summary tables to the screen from the class information
user_1.get_stock_table()
user_1.largest_stock_earning()
user_1.get_bond_table()
user_1.largest_bond_earning()

#generate summary tables in csv files from the class information
user_1.user_summary_file()

'''print the history of the stocks in the user_1 
stock holdings on a chart'''

#read the contents of the investments DB price history table 
#created from the json file into a memory table for future use
cu.execute("""SELECT 
               holding_symbol
               ,history_date
               ,close_value
               FROM stock_price_history""")
raw_stock_history = cu.fetchall()

'''read the username for the stock ID and bond  to save as the title header for the summary table. i based this on knowing that i only had one primary owner linking all the stocks in the holidings list, but really it should be an index query on which account are you creating a summary for and then all these results populate from the WHERE userID = ? instead'''
cu.execute("""SELECT username 
            FROM users 
            WHERE userID  = (SELECT primary_owner 
                             FROM accounts 
                             WHERE accountID = (SELECT account_num 
                                                FROM data_stocks
                                                WHERE stockID = 1)
                             )                   
           """)
stock_owner = cu.fetchone()
cu.execute("""SELECT username 
            FROM users 
            WHERE userID  = (SELECT primary_owner 
                             FROM accounts 
                             WHERE accountID = (SELECT account_num 
                                                FROM data_bonds
                                                WHERE bondID = 1)
                             )                   
           """)
bond_owner = cu.fetchone()
#read the entirety of the users table into a memory table
cu.execute("SELECT * FROM users") 
raw_user_table  = cu.fetchall()
#read the entirety of the accounts table into a memory table
cu.execute("SELECT * FROM accounts") 
raw_accounts_table  = cu.fetchall()
#close db connection
cx.close()

#create plot of stock price histories from the investments DB data
fig, ax = plt.subplots()
ax.set_title("Stock History Values", fontsize=24)
ax.set_xlabel("Date", fontsize=10)
ax.set_ylabel("Dollars", fontsize=10)
ax.tick_params(axis='both', labelsize=10)

#retrieve stock history and add to each line of the plot
for holding in user_1.stock_holdings:
  stock_label = holding.holding_symbol
  chart_shares = holding.num_shares
  x = []
  y = []
  for entry in (entry for entry in raw_stock_history if 
                entry[0] == stock_label):
    x.append(datetime.strptime(entry[1], '%d-%b-%y'))
    y.append(float(entry[2])*float(chart_shares))
  plt.plot(x, y, label = stock_label, linewidth = 1)

#add legend to plot
plt.legend(bbox_to_anchor=(1.05, 1),
           loc='upper left', borderaxespad=0.)

#save plot as a png file
try: 
  plt.savefig('stock_hist_chart.png', bbox_inches = 'tight')
  print('The stock history plot has saved in stock_hist_chart.png')
except:
  print('The stock history plot was unable to save to file')
