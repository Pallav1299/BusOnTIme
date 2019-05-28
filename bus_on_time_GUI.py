import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

Bus_Stop_Name = ("Ram Darbar", "Sector 47", "Sector 46 Market", "Sector 45 Market", "Sector 44 Market", "ISBT Sector 43", "Sector 42 Market", "Sector 41 Market", "Sector 40 Market", "Sector 39 Market", "Maloya", "Stoppage 39/38", "Stoppage 38 West/40", "Stoppage 38/37", "Stoppage 25/24", "Stoppage 14/15", "Sector 12 PGI", "Stoppage 11/15", "Stoppage 10/16", "Stoppage 9/17", "Stoppage 8/18", "Stoppage 19/7", "Stoppage 26/27", "Stoppage 28/27", "Stoppage 29/30", "Stoppage 31/32", "Stoppage 31/47", "Sector 47")

def _quit():
    win.quit()      # win will exist when this function is called
    win.destroy()
    exit()

#======================
# Create instance
win = tk.Tk()   

# Add a title       
win.title("BUS ON TIME")
# ---------------------------------------------------------------
# Creating a Menu Bar
menuBar = Menu()
win.config(menu=menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="New")
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=_quit)   # command callback
menuBar.add_cascade(label="File", menu=fileMenu)

# Add another Menu to the Menu Bar and an item
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="About")
menuBar.add_cascade(label="Help", menu=helpMenu)
# ---------------------------------------------------------------

# Tab Control / Notebook introduced here ------------------------
tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='Tab 1')      # Add the tab

tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='Tab 2')      # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ---------------------------------------------------------------
    
# We are creating a container frame to hold all other widgets
#bus_info = ttk.LabelFrame(tab1, text=' Bus Info ')
# using the tkinter grid layout manager
#bus_info.grid(column=0, row=0, padx=8, pady=4)

ENTRY_WIDTH = 30

#bus_info.grid_configure(column=0, row=1, padx=8, pady=4)

# create new labelframe
starting_bus_stop = ttk.LabelFrame(tab1, text=' Select Starting Bus Stop : ')
starting_bus_stop.grid(sticky="E", column=1, row=0, padx=8, pady=4)

# ---------------------------------------------------------------
# place label and combobox into new frame
ttk.Label(starting_bus_stop, text="Starting Bus Stop:    ").grid(column=0, row=0) # empty space for alignment

# ---------------------------------------------------------------
bus = tk.StringVar()
# initial_stop = ttk.Combobox(bus_info, width=12, textvariable=bus)    # before
initial_stop = ttk.Combobox(starting_bus_stop, width=24, textvariable=bus)          # assign different parent frame
initial_stop['values'] = Bus_Stop_Name
initial_stop.grid(column=1, row=0)
initial_stop.current(0)                 # highlight first bus
# ---------------------------------------------------------------

for child in starting_bus_stop.winfo_children(): 
        child.grid_configure(padx=6, pady=6) 




#bus_info.grid_configure(column=0, row=1, padx=8, pady=4)

# create new labelframe
ending_bus_stop = ttk.LabelFrame(tab1, text=' Select Destination Bus Stop : ')
ending_bus_stop.grid(sticky="E", column=1, row=1, padx=8, pady=4)

# ---------------------------------------------------------------
# place label and combobox into new frame
ttk.Label(ending_bus_stop, text="Destination Bus Stop:    ").grid(column=0, row=0) # empty space for alignment

# ---------------------------------------------------------------
bus = tk.StringVar()
# end_stop = ttk.Combobox(bus_info, width=12, textvariable=bus)    # before
end_stop = ttk.Combobox(ending_bus_stop, width=24, textvariable=bus)          # assign different parent frame
end_stop['values'] = Bus_Stop_Name
end_stop.grid(column=1, row=0)
end_stop.current(0)                 # highlight first bus
# ---------------------------------------------------------------

for child in ending_bus_stop.winfo_children(): 
        child.grid_configure(padx=6, pady=6)  



#bus_info.grid_configure(column=0, row=0, padx=8, pady=4)

# create new labelframe
bus_route_no = ttk.LabelFrame(tab1, text=' Select Bus Route No. : ')
bus_route_no.grid(sticky="W", column=0, row=0, padx=8, pady=4)

# ---------------------------------------------------------------
# place label and combobox into new frame
ttk.Label(bus_route_no, text="Bus Route:    ").grid(column=0, row=0) # empty space for alignment

# ---------------------------------------------------------------
bus = tk.StringVar()
# bus_route = ttk.Combobox(bus_info, width=12, textvariable=bus)    # before
bus_route = ttk.Combobox(bus_route_no, width=24, textvariable=bus)          # assign different parent frame
bus_route['values'] = ("Select bus route","5C","2A","239C","7C","2A","5A")
bus_route.grid(column=1, row=0)
#bus_route.
#bus_route.grid(sticky="W", row=0, column=0)
bus_route.current(0)                 # highlight first bus
# ---------------------------------------------------------------

for child in bus_route_no.winfo_children(): 
        child.grid_configure(padx=6, pady=6) 


bus_info = ttk.LabelFrame(tab2, text=' Bus Info ')
# using the tkinter grid layout manager
bus_info.grid(column=0, row=0, padx=8, pady=4)

ttk.Label(bus_info, text="Bus Registration No.:").grid(column=0, row=1, sticky='E')         # <== right-align
updated = tk.StringVar()
updatedEntry = ttk.Entry(bus_info, width=ENTRY_WIDTH, textvariable=updated, state='readonly')
updatedEntry.grid(column=1, row=1, sticky='W')



win.mainloop()

