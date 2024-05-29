""" 

Written by: Bronte Mckeown

This program accesses the open weather map API
to present to user, depending on their preferences,
the current weather for a City of their choice and
optionally, for a random city, and they can choose
whether they get the full report or just temperature only.
Weather is presented as a pretty table to user.

Instructions for instructor:

Get your own API Key by signing up here:
https://home.openweathermap.org

Save your API key in a .txt file called 'api_key' in 
parent directory.

If you don't have them installed already, use pip
to install 'requests' and 'prettytable'.

Note: prettytable is for making printed tables more readable.

"""
##########################################################################

# Import modules
import random
import requests
from prettytable import PrettyTable
from datetime import datetime as dt

##########################################################################

# Define custom functions

def join_url(api_key_, city_, base_url_):
    """
    Creates a complete URL by combining the base URL, API key, and city name.

    Parameters:
    api_key (str): The API key required for authentication with the API.
    city (str): The name of the city for which data is being requested.
    base_url (str): The base URL of the API endpoint.

    Returns:
    str: A complete URL string with the API key and city name appended.
    """
    # Create full_url by adding api_key and city strings
    full_url_ = base_url_ + "appid=" + api_key_ + "&q=" + city_

    return full_url_

def convert_celsius(kelvin_):
    """
    Converts a temperature from Kelvin to Celsius.

    Parameters:
    kelvin (float): The temperature in Kelvin to be converted.

    Returns:
    int: The temperature in Celsius, rounded down to the nearest integer.
    """
    # Subtract constant to covert & covert to integer for readability
    celsius_ = int(kelvin_ - 273.15)

    return celsius_

def full_table_field_names():
    """
    Creates a full weather report table with predefined field names.

    Returns:
    PrettyTable: An empty PrettyTable object with field names set for a weather report.
    """
    # Create empty pretty table to add to
    table_ = PrettyTable()

    # Add field names to table
    table_.field_names = ["City", "Summary", "Actual Temp",
                        "Feels like", "Temp Min", "Temp Max",
                        "Pressure", "Humidity", "Visibility",
                        "Wind Speed"]
    
    return table_

def add_full_row(full_table_, city_, response_):
    """
    Adds a row of weather data to the provided full table.

    Parameters:
    table (PrettyTable): The table to which the row will be added. 
                        This table should have predefined field names.
    city (str): The name of the city for which the weather data is provided.
    response (dict): The API response containing weather data for the city.
    """
    # Add row where city is used as value in first column
    # The rest of the columns are filled by accessing response
    full_table_.add_row([city_,
                response_['weather'][0]['main'],
                convert_celsius(response_['main']['temp']),
                convert_celsius(response_['main']['feels_like']),
                convert_celsius(response_['main']['temp_min']),
                convert_celsius(response_['main']['temp_max']),
                response_['main']['pressure'],
                response_['main']['humidity'],
                response_['visibility'],
                response_['wind']['speed']])
    
    return full_table_

def temp_table_field_names():
    """
    Creates a temperature-only report table with predefined field names.

    Returns:
    PrettyTable: An empty PrettyTable object with field names set for temp report.
    """
    # Create empty pretty table to add to
    table_ = PrettyTable()

    # Add field names to table
    table_.field_names = ["City", "Actual Temp",
                        "Feels like", "Temp Min", "Temp Max"
                        ]
    
    return table_

def add_temp_row(temp_table_, city_, response_):
    """
    Adds a row of temperature data to the provided temperature-only table.

    Parameters:
    temp_table (PrettyTable): The table to which the row will be added. This table should have predefined field names.
    city (str): The name of the city for which the temperature data is provided.
    response (dict): The API response containing temperature data for the city.
    """
    # Add row where city is used as value in first column
    # The rest of the columns are filled by accessing response
    temp_table_.add_row([city_,
                convert_celsius(response_['main']['temp']),
                convert_celsius(response_['main']['feels_like']),
                convert_celsius(response_['main']['temp_min']),
                convert_celsius(response_['main']['temp_max'])]
                )
    
    return temp_table_

def write_table_to_csv(table_):
    """
    Writes weather report table out to csv file, with timestamp in filename.

    Parameters:
    table_ (PrettyTable): The table to be saved out as a csv file.
    """
    timestamp = dt.now().strftime("%Y%m%d-%H%M%S")
    with open(f'weather_report_{timestamp}.csv', 'w', newline='') as output:
        output.write(table_.get_csv_string())

##########################################################################

# Set variables needed in script

# Set base_url to the openweathermap API URL
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Read API key in from txt file titled "api_key.txt"
# Use .rstrip() to prevent python reading in newline character
my_key = open("api_key.txt", "r").readline().rstrip()

# Ask User what City they want to see Weather for, use capitalize method 
# to ensure nice format in table
user_city = input("""What City would you like to know the weather for? Type here: """).capitalize()

# Create full URL using api_key variable and city from user input
city_url = join_url(my_key, user_city, base_url)

# Use requests module to retrieve data from provided city URL
city_response = requests.get(city_url).json()

# Ask User if they want to see the full city name or an abbreviation
view_option = input("""\nWould you like to see the full city name or an abbreviation? Type 'full' or 'abbrev': """).lower()

# Use if/else statement to set display city name based on User selection
if view_option == 'full':
    display_city_name = user_city
elif view_option == 'abbrev':
    # If they want abbreviation, select first three characters
    display_city_name = user_city[:3]
    # If they enter incorrectly, default to full name with warning
else:
    print("\nYou entered an invalid selection. Defaulting to full name.")
    display_city_name = user_city

"""
We now want to ask user if they want a random 
city's weather to be shown as well.

We use a while loop so that if they input the wrong
values (anything other than yes or no), it asks again.
"""

# Set report_type_selected to False
random_selection_selected = False

# While it is False, ask the question to user
while random_selection_selected == False:

    # Ask user if they want a random city selection
    random_selection = input("""\nWould you like to get the weather for a random City? Type 'yes' or 'no': """).lower()

    # If User selects yes, randomly select a City from list
    # Use .lower() so it is case insensitive
    if random_selection == 'yes':

        # Set to true, which breaks the loop
        random_selection_selected =  True
        
        # List of possible cities to randomly chose from
        # Only created if user selects yes
        city_list = ["London", "New York", "Paris", "Berlin",
                    "Perpignan", "Brighton", "Leeds"]
        
        # Select random city from list using random.choice()
        random_city = random.choice(city_list)
        
        """
        To prevent the user's city and the random city
        being the same, use a While loop.
        While the random_city is equal to city,
        random selection will repeat.
        """
        while random_city == user_city:
            random_city = random.choice(city_list)
        
        # Create random URL once random city selected
        random_url = join_url(my_key, random_city, base_url)

        # Use requests module to retrieve data from city URL
        random_response = requests.get(random_url).json()

    elif random_selection == 'no':
        # Set to true, which breaks the loop
        random_selection_selected =  True

    else:
        # If not yes or no, tell user to try again.
        # Random selection selected stays false so question asked again.
        print("""\nPlease try again. Input should either be: Type 'yes' or 'no'.""")

"""
We now want to ask user if they want a full report
or just the temperature.

Again, we use a while loop so that if they input the wrong
values (anything other than 1 or 2), it asks again.
"""

# Set report_type_selected to False
report_type_selected = False

# While it is False, ask the question to user
while report_type_selected == False:

    # Ask User for report type (full or just temperature)
    report_type = input("""\nWould you like a (1) full weather report or (2) just temperature? Type 1 or 2: """)

    # If 1 or 2 selected, set report_type_selected to True
    if int(report_type) == 1:

        # Let user know what they have selected.
        print ("\nYou selected full report.\n")

        # Set report_type_selected to True (breaks loop)
        report_type_selected = True

        # Call function to create full table with field names
        full_table = full_table_field_names()

        # Call function to add row of data to full table for user_city
        full_table = add_full_row(full_table, display_city_name, city_response)
        
        # If user has asked for random city, add row of data for random_city
        if random_selection == 'yes':
            full_table = add_full_row(full_table, random_city, random_response)

        # Print the full_table to user
        print (full_table)

        write_table_to_csv(full_table)

    elif int(report_type) == 2:

        # Let user know what they have selected.
        print ("\nYou selected temperature only.\n")

        # Set report_type_selected to True (breaks loop)
        report_type_selected = True

        # Call function to create temp only table with field names
        temp_table = temp_table_field_names()

        # Call function to add row of data to temp only table for user_city
        temp_table = add_temp_row(temp_table, user_city, city_response)

         # If user has asked for random city, add row of data for random_city
        if random_selection == 'yes':
            temp_table = add_temp_row(temp_table, random_city, random_response)

         # Print the temp_table to user
        print (temp_table)

        write_table_to_csv(temp_table)

    else:
        # If not 1 or 2, tell user to try again.
        # Report type selected stays false so question asked again.
        print("""\nPlease try again. Input should either be: 1 or 2.\n""")