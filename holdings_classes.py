'''
Author: Melissa Lawrence
Date Created: 07/15/2023
Functionality: build classes and methods for the stock problem
'''

#Import the date function
from datetime import datetime
from prettytable import PrettyTable

#Create user class
class User():
  '''Identify and store information pertaining to account holders.'''
  def __init__(self, userID, name, address, phone_num):
    self.userID = userID
    self.name = name
    self.address = address
    self.phone_num = phone_num
    self.stock_holdings = []
    self.bond_holdings = []  
                          
  def add_stock(self, new_stock):
    '''add new stock to the stock_holdings list for the user'''
    self.new_stock = self.stock_holdings.append(new_stock)

  def add_bond(self, new_bond):
    '''sdd new bond to the bond_holdngs list for the user'''
    self.new_bond = self.bond_holdings.append(new_bond)  

  def get_stock_table(self):
    '''generate tables for the stock and bond holdings'''
    stock_table = PrettyTable()
    #create table titles (person name)
    stock_table.title = ('Stock ownership for ' + self.name)
    #create column header names for stcok table
    stock_table.field_names = ['Stock Symbol', 'No. Shares', 
        'Holding Earnings', 'Avg Annual Earnings']
    for holding in self.stock_holdings:
        stock_table.add_row([holding.holding_symbol, holding.num_shares,
                           holding.earnings_per_stock_holding(),
                           holding.avg_ann_per_stock_share()],
                            divider = True)
    print(stock_table)

  def get_bond_table(self):
    '''generate table for the bond holdings'''
    bond_table = PrettyTable()  
    #create table titles (person name)
    bond_table.title = ('Bond ownership for ' + self.name)
    #create column header names for the stock table
    bond_table.field_names = ['Bond Symbol', 'Quantity', 
        'Holding Earnings', 'Avg Annual Earnings']
    for holding in self.bond_holdings:
        bond_table.add_row([holding.holding_symbol, holding.quantity,
                          holding.earnings_per_bond_holding(),
                          holding.avg_ann_per_bond_item()],
                          divider = True)
    print(bond_table)

  def user_summary_file(self):
    '''write the headings, stocks, and bonds for an account 
    to csv files'''
    try:
      with open('Lesson6_Results_Combined.csv', 'w') as write_file:
        write_file.write('Holding Symbol' + ','
                     + 'No. Shares/Quantity' + ',' 
                     + 'Holding Earnings' + ','
                     + 'Avg Annual Earnings' 
                     + '\n')
        for holding in self.stock_holdings:
            write_file.write(str(holding.holding_symbol) + ','
                      + str(holding.num_shares) + ','
                      + str(holding.earnings_per_stock_holding()) + ','
                      + str(holding.avg_ann_per_stock_share())
                      + '\n')      
        for holding in self.bond_holdings:
            write_file.write(str(holding.holding_symbol) + ','
                      + str(holding.quantity) + ','
                      + str(holding.earnings_per_bond_holding()) + ','
                      + str(holding.avg_ann_per_bond_item())
                      + '\n')  
        print('A summary table has been saved for stocks and bonds'  
              'in Lesson6_Results_Combined.csv.')
    except FileNotFoundError:
      print('The account results file cannot be written.')
    except IOError:
        print("Error: Unable to write to the output file.")
    except Exception as e:
        print("Error:", str(e))

  def largest_stock_earning(self):
    '''determine which stock has the most gain/least loss'''
    max_gain = float('-inf')
    for holding in self.stock_holdings:
      if max_gain <= float(holding.earnings_per_stock_holding()):
        biggest_earning = holding.holding_symbol
        max_gain = float(holding.earnings_per_stock_holding())
      else:  
        max_gain = max_gain
    if max_gain > 0:
      print('The stock with the most gain is ' + biggest_earning + '.')
    else:
      print('The stock with the least loss is ' + biggest_earning + '.')
      
  def largest_bond_earning(self):  
    '''determine which bond has the most gain/least loss'''
    max_gain = float('-inf')
    for holding in self.bond_holdings:
      if max_gain <= float(holding.earnings_per_bond_holding()):
        biggest_earning = holding.holding_symbol
        max_gain = float(holding.earnings_per_bond_holding())
      else:  
        max_gain = max_gain
    if max_gain > 0:
      print('The bond with the most gain is ' + biggest_earning + '.')
    else:
      print('The bond with the least loss is ' + biggest_earning + '.')

#create holding class    
class Holding():
  '''establish a holding for either stock or 
  bond that consists of purchase transaction'''
  def __init__(self, holding_symbol,  
               purchase_price, purchase_date, 
               current_value):
    self.holding_symbol = holding_symbol
    self.purchase_price = purchase_price
    self.purchase_date = purchase_date
    self.current_value = current_value
   
  def current_date(self): 
    '''use datetime to return today's date'''
    current_date = datetime.today().date()
    return current_date

  def earnings_per_stock_share():
    pass
  def earnings_per_stock_holding():
    pass
  def avg_ann_per_stock_share(): 
    pass
  def bond_coupon_valuation():
    pass
  def earnings_per_bond_holding():
    pass
  def avg_ann_per_bond_item(): 
    pass

#create a subclass of holding to add stock shares
class Stock(Holding):
  '''establish a stock purchase transaction'''
  def __init__(self, holding_symbol,  
               purchase_price, purchase_date, 
               current_value, stockID, num_shares):
    super().__init__(holding_symbol, 
                     purchase_price, purchase_date, 
                     current_value)
    self.stockID = stockID
    self.num_shares = num_shares
  
  def earnings_per_stock_share(self):
    '''Create method to calculate earnings or loss per share'''
    earnings_per_stock_share = round((float(self.current_value) - 
                  float(self.purchase_price)),2)
    return earnings_per_stock_share

  def earnings_per_stock_holding(self):
    '''Create method to calculate earnings 
    or loss per holding position'''
    earnings_per_stock_holding = round(((float(self.current_value) - 
                  float(self.purchase_price)) * 
                  float(self.num_shares)),2)
    return earnings_per_stock_holding 

  def avg_ann_per_stock_share(self):
    '''Create method to calculate average 
    annual yield/loss per stock share'''
    avg_ann_per_stock_share = round(((float(self.current_value) - 
                  float(self.purchase_price))/
                  float(self.purchase_price)/((self.current_date() - 
                  self.purchase_date).days/365)*100),2)
    return avg_ann_per_stock_share

#create a subclass of holding to add bond shares
class Bond(Holding):
  '''establish a bond purchase transaction'''
  def __init__(self, holding_symbol,  
                purchase_price, purchase_date, 
                current_value, bondID, quantity, bond_yield, coupon):
    super().__init__(holding_symbol,
                     purchase_price, purchase_date, 
                     current_value)
    self.bondID = bondID
    self.quantity = quantity
    self.bond_yield = bond_yield
    self.coupon = coupon

  def bond_coupon_valuation(self):
    '''assume annual coupon interest payments and maturity 
    at 25 years to return earnings to date'''
    coupon_payment = round(float(self.coupon)/100*
                      float(self.purchase_price),2)
    num_periods = int((self.current_date() - self.purchase_date).days)
    for period in range(1, num_periods):
      value_coupons = round(coupon_payment/(1 + 
                      (float(self.bond_yield) / 100)**period),2)
    face_value = round(float(self.purchase_price)/(1 + 
                      (float(self.bond_yield) / 100)**num_periods),2)
    bond_coupon_valuation = round((value_coupons + face_value),2)
    return bond_coupon_valuation

  def earnings_per_bond_holding(self):
    '''returns value for each bond time total quantity'''
    earnings_per_bond_holding = round((float(self.bond_coupon_valuation())
                - float(self.purchase_price)),2) * float(self.quantity)
    return earnings_per_bond_holding

  def avg_ann_per_bond_item(self):
    '''determines average annual return per bond item'''
    avg_ann_per_bond_item = round(((float(self.bond_coupon_valuation()) - 
                  float(self.purchase_price))/
                  float(self.purchase_price)/((self.current_date() - 
                  self.purchase_date).days/365)*100),2)
    return avg_ann_per_bond_item

class StockHist():
  '''store a history of stock trading by date'''
  def __init__(self, holding_symbol, history_date, open_value, 
               high_value, low_value, close_value, trade_volume):
    self.holding_symbol = holding_symbol
    self.history_date = history_date
    self.open_value = open_value
    self.high_value = high_value
    self.low_value = low_value 
    self.close_value = close_value 
    self.trade_volume = trade_volume