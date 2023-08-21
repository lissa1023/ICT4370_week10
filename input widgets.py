import tkinter as tk
from tkinter import ttk
from holdings_classes import user

users = []

def add_user():
  user_count = len(users) + 1
  user_list_name = ('user_' + str(user_count))
  user_list_name = User(user_count, 
                  entry_name.get(), 
                  entry_address.get(), 
                  entry_phone_num.get())
  verify_entry = (str(user_list_name.name) + ' ' +
                  str(user_list_name.address)  + ' '+
                     str(user_list_name.phone_num) + ' '+
                     'is assigned UserID: ' + str(user_list_name.userID))
  output_string.set(verify_entry) 
  print (verify_entry)
  users.append(user_list_name)

#window - create the window that pops up
window = tk.Tk()
window.title('Add Investor')
window.geometry('400x300')

#title - add text field widget for the title or prompt to input
title_label = ttk.Label(master = window, text = 
                        'Input the Investor Info', 
                        font = 'Calibri 12')
title_label.pack()

#input field - add the 3 widgets to accept input
input_frame =  ttk.Frame(master = window)
label_name = ttk.Label(master = window, text = 'Enter Name', font = 'Calibri 9')
entry_name = tk.StringVar()
entry_1 = ttk.Entry(master = input_frame, 
                    textvariable = entry_name)
label_address = ttk.Label(master = window, text = 'Enter Address', font = 'Calibri 9')
entry_address = tk.StringVar()
entry_2 = ttk.Entry(master = input_frame, 
                    textvariable = entry_address)
label_phone_num = ttk.Label(master = window, text = 'Enter Phone #', font = 'Calibri 9')
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

#run
window.mainloop()