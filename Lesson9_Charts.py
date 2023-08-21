'''
Author: Melissa Lawrence
Date Created: 08/05/2023
Functionality: Complete Week 9 Discussion B
Notes: Week 9 discussion involves data anlysis of the stocks from our stock problem using pandas. 
'''

#Import objects and methods
import matplotlib.pyplot as plt
import pandas as pd
import os

#get lists of the filenames and stocks in the data files
file_path = 'Data/'
file_names = os.listdir(file_path)
print(file_names)

#create a list that will have the stock names in the order the file is read
try:
  stock_names = []
  for file in file_names:
    read_file_name = str(file.rsplit('.',1)[0])
    stock_names.append(read_file_name)
  print(stock_names)  
except FileNotFoundError:
    print('The data file could not be read for ' + read_file_name + '.')
except Exception as e:
    print("Error:", str(e))  
  
#create a list that will store the dataframe for each stock in the order the file is read
stock_pandas_df = []
for file in range(len(stock_names)):
  pandas_name = str('df_' + stock_names[file])
  pandas_name = pd.read_csv(file_path + file_names[file])
  stock_pandas_df.append(pandas_name)

#compute mean and standard deviation of each stock's daily closing price from the listed dataframes and place in table
means = []
std_dev = []
cor_coeff = []
count = 0
for df in stock_pandas_df:
  means.append(df['Close'].mean(axis = 0, 
              skipna = True, numeric_only = True))
  std_dev.append(df['Close'].std(axis = 0, 
              skipna = True, numeric_only = True))
  cor_coeff.append(df['Close'].corr(
              stock_pandas_df[len(stock_names)-1]['Close']))
  count = count + 1
computations_df = pd.DataFrame({'Mean':means, 
                  'Standard Deviation': std_dev, 
                  'Correlation Coefficient to SPY': cor_coeff}, 
                  index = stock_names)
print(computations_df)

#create a merged dataframe of all the outer join dates and closing price for each stock
closing_price_df = stock_pandas_df[0][['Date','Close']].rename(
  columns = {'Close':stock_names[0]})
for item in range(1,len(stock_names)):
  closing_price_df = pd.merge(
      closing_price_df, stock_pandas_df[item][['Date','Close']]
      .rename(columns = {'Close':stock_names[item]})
      , how = 'outer', on = 'Date' )
print(closing_price_df)                              

#create the plot of all the closing prices
closing_price_df.plot(x = 'Date',y = stock_names)
plt.legend(loc='center',ncol=len(stock_names)/2)

#save plot as a png file
try: 
  plt.savefig('Lesson9_hist_chart2.png', bbox_inches = 'tight')
  print('The stock history plot has saved in Lesson9_hist_chart2.png')
except:
  print('The stock history plot was unable to save to file')