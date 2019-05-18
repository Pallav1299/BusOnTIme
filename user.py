from pprint import pprint
#import tkinter as tk
#import googlemaps
from gmplot import gmplot
import webbrowser
import os


from sheetsu import SheetsuClient  # using sheetsu to 

#########################################################################################

# Function Name: create_tuple_location()
# Input : a string
# Use: converts the data extracted from the google sheet with string datatype using 
# 	   "sheetsu" client and converts it into a tuple of the following format:
# 	   					(latitude, longitude)
# Returns: tuple(latitude, longitude)
def create_tuple_location(string):
	
	if string == "":
		read_sheet_once()

	else:
		i = 0
		latitude = ""
		longitude = ""
		while string[i] != "(":
			i += 1
		i += 1
		while string[i] != ",":
			latitude = latitude + string[i]
			i += 1
		i += 1
		while string[i] != ")":
			longitude = longitude + string[i]
			i += 1
		#print((float(latitude), float(longitude)))

		return (float(latitude), float(longitude))


#########################################################################################

# Function Name: find_current_stop()
# Input: a tuple
# Use: fetches the bus-stop name corresponding to the current location fetched in the
#      form of a tuple from the google sheet using "sheetsu" client from the "Bus_Stop_Name" 
# 	   list, which contains the names of all the bus-stops of a particular bus route number 
# 	   (Here 5C).
# Returns : String(current bus stop name)
def find_current_stop(location_tuple):
	current_bus_stop = ""
	bus_lat = location_tuple[0]
	bus_lon = location_tuple[1]
	for i in range(len(Bus_Stop_Location)):
		(stop_lat,stop_lon) = (Bus_Stop_Location[i][0],Bus_Stop_Location[i][1])
		lat_data = 10000 * abs(stop_lat - bus_lat)
		lon_data = 10000 * abs(stop_lon - bus_lon)
		if (lat_data <= 3) and (lon_data <= 3):
			current_bus_stop = Bus_Stop_Name[i]
	return current_bus_stop

#########################################################################################


def take_data_from_user():
	global user_start_stop
	global user_end_stop

	for i in range(len(Bus_Stop_Name)):		  # Adding data to the above mentioned dictionary
		bus_stops_dict[i] = Bus_Stop_Name[i]  # from the provided lists.
	pprint(bus_stops_dict)
	print(" ")
	user_start_stop = input("Enter number corresponding to starting stop: ")  # Seeking starting bus-stop-name from the user
	while user_start_stop not in str(bus_stops_dict.keys()):  # Keeps on asking the user until a valid number is entered.
		user_start_stop = input("Enter number corresponding to starting stop: ")
	#print(user_start_stop)
	user_start_stop = Bus_Stop_Name[int(user_start_stop)]  # typecasting the String(user_start_stop) into int(user_start_stop)
														   # as we can iterate on a list only using an integer.
	print(" ") #prints an empty line
	user_end_stop = input("Enter number corresponding to end stop: ")  # Seeking end bus-stop-name from the user
	while user_end_stop not in str(bus_stops_dict.keys()):  # # Keeps on asking the user until a valid number is entered.
		user_end_stop = input("Enter number corresponding to end stop: ")
	user_end_stop = Bus_Stop_Name[int(user_end_stop)]  # typecasting the String(user_start_stop) into int(user_start_stop)
													   # as we can iterate on a list only using an integer.
	print(" ")
	print("User starting bus stop: " + user_start_stop)
	print("User end bus stop: " + user_end_stop)

def get_sheet():
	global x
	global sheet_dict, bus_list

	x = client.read(sheet="5C", limit=2) # read the data from the google sheet with the sheet-name: "5C" and assign it to "x". 
											 # the argument "limit" defines the number of rows to be fetched from the sheet.
											 # "x" is a list
	#print(x)
	sheet_dict = x[0] # read the first element (here the first element in the list is the dictionary containing the data from the sheet)
					  # from the list using the argument "0".
	del sheet_dict[""]
	bus_list = list(sheet_dict.keys()) # extract the list of keys from the above dictionary. 
	
	for i in bus_list:
		if sheet_dict[i] == "":
			get_sheet()
	

def retrieve_data():
	global i, j, k

	#print(dict_keys_list)
	i = find_current_stop(create_tuple_location(sheet_dict[bus_list[0]])) # updated bus-stop-name
	j = find_current_stop(create_tuple_location(sheet_dict[bus_list[1]])) # updated bus-stop-name
	k = find_current_stop(create_tuple_location(sheet_dict[bus_list[2]])) # updated bus-stop-name

	print(bus_list[0] + " with route no.: 5C has crossed: " + i)
	print(bus_list[1] + " with route no.: 5C has crossed: " + j)
	print(bus_list[2] + " with route no.: 5C has crossed: " + k)

def find_nearest_bus():
	global nearest_bus
	(l0,l1,l2) = (len(Bus_Stop_Name),len(Bus_Stop_Name),len(Bus_Stop_Name)) # initializing l0,l1,l2 variables to maximum length of the Bus_Stop_Name list.
	if Bus_Stop_Name.index(user_start_stop) > Bus_Stop_Name.index(i):
		l0 = Bus_Stop_Name.index(user_start_stop) - Bus_Stop_Name.index(i)
	if Bus_Stop_Name.index(user_start_stop) > Bus_Stop_Name.index(j):
		l1 = Bus_Stop_Name.index(user_start_stop) - Bus_Stop_Name.index(j)
	if Bus_Stop_Name.index(user_start_stop) > Bus_Stop_Name.index(k):
		l2 = Bus_Stop_Name.index(user_start_stop) - Bus_Stop_Name.index(k)

	least_stops_count = min(l0,l1,l2) 

	if least_stops_count == l0:
		nearest_bus = bus_list[0]  # finds the nearest bus to the user's starting bus stop.
		current_bus_stop = i 	   # current bus stop of the bus
	elif least_stops_count == l1:  
		nearest_bus = bus_list[1]  # finds the nearest bus to the user's starting bus stop.
		current_bus_stop = j 	   # current bus stop of the bus
	elif least_stops_count == l2:
		nearest_bus = bus_list[2]  # finds the nearest bus to the user's starting bus stop.
		current_bus_stop = k       # current bus stop of the bus

	print("")
	print("Nearest 5C with registration no.: " + nearest_bus + " has crossed: " + current_bus_stop)  # Displaying the data to the user.
	print("")
	print("")

def update_current_bus_stop_of_assigned_bus():
	if nearest_bus == bus_list[0]:
			a = create_tuple_location(sheet_dict[bus_list[0]])
			show_map(a[0], a[1])
			i = find_current_stop(a) # updated bus-stop-name
			print("")
			print("Nearest 5C with registration no.: " + nearest_bus + " has crossed: " + i)  # Displaying the data to the user.
			print("")
			print("")

	elif nearest_bus == bus_list[1]:
			b = create_tuple_location(sheet_dict[bus_list[1]])
			show_map(b[0], b[1])
			j = find_current_stop(b) # updated bus-stop-name
			print("")
			print("Nearest 5C with registration no.: " + nearest_bus + " has crossed: " + j)  # Displaying the data to the user.
			print("")
			print("")

	elif nearest_bus == bus_list[2]:
			c = create_tuple_location(sheet_dict[bus_list[2]])
			show_map(c[0], c[1])
			k = find_current_stop(c) # updated bus-stop-name
			print("")
			print("Nearest 5C with registration no.: " + nearest_bus + " has crossed: " + k)  # Displaying the data to the user.
			print("")
			print("")

def show_map(lati, longi):
	gmap = gmplot.GoogleMapPlotter(lati, longi, 13 ) 
	gmap.marker(lati, longi, "red")
	#gmap.apikey = "AIzaSyAbFI4apqatNnLKhJdHJxVbL_L07ywQaYs"
	os.chdir("/home/pallav/Documents/BusOnTime")
	gmap.draw("map.html")
	#time.sleep(0.05)
	#os.remove("map.html")

	



if __name__ == '__main__':

	client = SheetsuClient("https://sheetsu.com/apis/v1.0su/5f35666cf66d")

	####LIST OF BUS STOPS & THEIR LOCATION OF BUS WITH ROUTE NO.:"5C" #######################

	Bus_Stop_Name = ["Ram Darbar", "Sector 47", "Sector 46 Market", "Sector 45 Market", "Sector 44 Market", "ISBT Sector 43", "Sector 42 Market", "Sector 41 Market", "Sector 40 Market", "Sector 39 Market", "Maloya", "Stoppage 39/38", "Stoppage 38 West/40", "Stoppage 38/37", "Stoppage 25/24", "Stoppage 14/15", "Sector 12 PGI", "Stoppage 11/15", "Stoppage 10/16", "Stoppage 9/17", "Stoppage 8/18", "Stoppage 19/7", "Stoppage 26/27", "Stoppage 28/27", "Stoppage 29/30", "Stoppage 31/32", "Stoppage 31/47", "Sector 47"]
	Bus_Stop_Location = [(30.6975,76.7901), (30.6947,76.7697), (30.7026,76.7639), (30.7057,76.7572), (30.7128,76.7529), (30.7190,76.7487), (30.7233,76.7448), (30.7318,76.7389), (30.7394,76.7380), (30.7442,76.7293), (30.72589,76.75787), (30.7449,76.7372), (30.7417,76.7398), (30.7390,76.7442), (30.7478,76.7580), (30.7554,76.7699), (30.7662,76.7784), (30.6855,76.8460), (30.7513,76.7817), (30.7444,76.7877), (30.7401,76.7986), (30.7313,76.7994), (30.7280,76.8025), (30.7229,76.8061), (30.7137,76.7913), (30.7083,76.7827), (30.6999,76.7746), (30.6947,76.7697)]

	bus_stops_dict = {}  # initializing the python dictionary to be displayed to the user 
					 # for selecting the starting and end bus-stop of the user.
	
	take_data_from_user()
	
	get_sheet()
	retrieve_data()
	find_nearest_bus()
	url  = "/home/pallav/Documents/BusOnTime/map.html"
	webbrowser.open(url)

	while 1:
		get_sheet()
		update_current_bus_stop_of_assigned_bus()		