""" 

Written by: Bronte Mckeown

This program accesses the open weather map API
to present to the user the current weather for a City of
their choice as a prettytable, and saves this
table as a csv file in current directory.

They can also choose whether:
- to see full or abbreviated city name
- to also see weather for a random city
- they want full report or temperature only

Instructions for instructor:

Get your own API Key by signing up here:
https://home.openweathermap.org

Save your API key in a .txt file called 'api_key' in 
current directory.

If you don't have them installed already, use pip
to install 'requests' and 'prettytable' in terminal.

Note: prettytable is for making printed tables more readable!

LLM note: Chat GPT used to help improve doc strings for functions.
    - Specifically, used to do 'Parameters' and 'Returns' to save time.
    - Prompt: "Finish the doc string for this function:"
    - Edited where necessary to be accurate and/or clearer.

"""
##########################################################################

# Import modules
import random
import requests
from prettytable import PrettyTable
from datetime import datetime as dt
import sys

##########################################################################

# Define custom functions

def join_url(api_key_, city_, base_url_):
    """
    Creates a complete URL by combining the base URL, API key, and city name.

    Parameters:
    api_key_ (str): The API key required for authentication with the API.
    city_ (str): The name of the city for which data is being requested.
    base_url_ (str): The base URL of the API endpoint.

    Returns:
    str: A complete URL string with the API key and city name appended.
    """
    # Create full_url by adding api_key and city strings
    full_url = base_url_ + "appid=" + api_key_ + "&q=" + city_

    return full_url

def convert_celsius(kelvin_):
    """
    Converts a temperature from Kelvin to Celsius.

    Parameters:
    kelvin_ (float): The temperature in Kelvin to be converted.

    Returns:
    int: The temperature in Celsius, rounded down to the nearest integer.
    """
    # Subtract constant to covert & covert to integer for readability
    celsius = int(kelvin_ - 273.15)

    return celsius

def create_table(full_report = True):
    """
    Creates a weather report table with provided field names.

    Returns:
    PrettyTable: An empty PrettyTable object with field names set for a weather report.
    """
    # Create empty pretty table to add to
    table_ = PrettyTable()

    if full_report:
        # Add full field names to table
        table_.field_names = ["City", "Summary", "Actual Temp",
                        "Feels like", "Temp Min", "Temp Max",
                        "Pressure", "Humidity", "Visibility",
                        "Wind Speed"]

    else:
        table_.field_names = ["City", "Actual Temp",
                        "Feels like", "Temp Min", "Temp Max"
                        ]
        
    return table_

def add_row(table_, city_, response_, full_report = True):
    """
    Adds a row of weather data to the provided full table.

    Parameters:
    full_table_ (PrettyTable): The table to which the row will be added. 
                        This table should have predefined field names.
    city_ (str): The name of the city for which the weather data is provided.
    response_ (dict): The API response containing weather data for the city.
    """
    if full_report:
        # Add row where city is used as value in first column
        # The rest of the columns are filled by accessing response
        table_.add_row([city_,
                    response_['weather'][0]['main'],
                    convert_celsius(response_['main']['temp']),
                    convert_celsius(response_['main']['feels_like']),
                    convert_celsius(response_['main']['temp_min']),
                    convert_celsius(response_['main']['temp_max']),
                    response_['main']['pressure'],
                    response_['main']['humidity'],
                    response_['visibility'],
                    response_['wind']['speed']])
    else:
        table_.add_row([city_,
                convert_celsius(response_['main']['temp']),
                convert_celsius(response_['main']['feels_like']),
                convert_celsius(response_['main']['temp_min']),
                convert_celsius(response_['main']['temp_max'])]
                )
        
    return table_

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
# This will be used to create full URLs for city(s) below
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Read API key in from txt file titled "api_key.txt"
# Use .rstrip() to prevent python reading in newline character!
my_key = open("api_key.txt", "r").readline().rstrip()

##########################################################################

# Ask User what City they want to see Weather for, use capitalize method 
# to ensure it's in a nice format in the output table
user_city = input("\nWhat City would you like to know the weather for? "
                  "Type here: ").capitalize()

# Let user know what they have selected.
print (f"\nYou selected {user_city}.")

# Create full URL using api_key variable and city from user input
city_url = join_url(my_key, user_city, base_url)

# Use requests module to retrieve data from provided city URL
city_response = requests.get(city_url)

# If status code indicates error, print message to User and stop program
# This prevents user from progressing any further if request hasn't worked
status_code = city_response.status_code 
if status_code != 200:
    print(f"\nError: The API request has failed (code: {status_code}) "
          "You may have mis-spelt the city name. Try again.\n")
    sys.exit()

# Convert to json format after if code indicates if has worked
city_response = city_response.json()

##########################################################################

# Ask User if they want to see the full city name or an abbreviation
# Make lower case so you can safely use in if/else statement below
view_option = input("\nIn the output, would you like to see the full city name "
                    "or an abbreviation? Type 'full' or 'abbrev': ").lower()

# Use if/else statement to set display city name based on User selection
if view_option == 'full':
    # If full, stays the same
    display_city_name = user_city
    # Let user know what they have selected.
    print ("\nYou selected to see the full city name in the output.")

elif view_option == 'abbrev':
    # If they want abbreviation, select first three characters
    display_city_name = user_city[:3]
    # Let user know what they have selected.
    print ("\nYou selected to see an abbreviation of city name in the output.")

# If they enter incorrectly, default to full name with printed warning
else:
    print("\nYou entered an invalid selection. Defaulting to full name.")
    display_city_name = user_city

##########################################################################

"""
We now want to ask user if they want a random
city's weather to be shown as well.

We use a while loop so that if they input the wrong
values (anything other than yes or no), it asks again.
"""

# Set report_type_selected to False for while loop below
random_selection_selected = False

# While it is False, ask the question to User
while random_selection_selected == False:

    # Ask User if they want a random city selection
    random_selection = input("\nWould you like to get the weather "
                            "for a random City? Type 'yes' or 'no': ").lower()

    # If User selects yes, randomly select a City from list
    if random_selection == 'yes':

        # Set to true to break the while loop
        random_selection_selected =  True

        # Let user know what they have selected.
        print ("\nYou selected  to see a random city too.")
        
        # Create list of possible cities to randomly chose from
        # For efficiency, only created if user selects yes
        city_list = ["London", "New York", "Paris", "Berlin",
                    "Perpignan", "Brighton", "Leeds"]
        
        # Select random city from list using random.choice()
        random_city = random.choice(city_list)
        
        """
        To prevent the user's city and the random city
        being the same, we use another While loop.
        While the random_city is equal to city,
        random selection will repeat.
        """
        while random_city == user_city:
            random_city = random.choice(city_list)
        
        # Create random URL once random city selected
        random_url = join_url(my_key, random_city, base_url)

        # Use requests module to retrieve data from random URL
        random_response = requests.get(random_url).json()

    # If random_selection is no, then let User know and break loop.
    elif random_selection == 'no':
        
        # Set to true to break the loop
        random_selection_selected =  True

        # Let user know what they have selected.
        print ("\nYou selected to NOT see a random city.")

    else:
        # If not yes or no, tell user to try again.
        # Random selection selected stays false so question asked again.
        print("\nPlease try again. Input should either be: "
                "Type 'yes' or 'no'.")

##########################################################################
"""
We now want to ask user if they want a full report
or just the temperature.

Again, we use a while loop so that if they input the wrong
values (anything other than 1 or 2), it asks again.
"""

# Set report_type_selected to False for While loop
report_type_selected = False

# While it is False, ask the question to user
while report_type_selected == False:

    # Ask User for report type (full or just temperature)
    report_type = input("\nWould you like a (1) full weather report or "
                        "(2) just temperature? Type 1 or 2: ")

    # If 1 or 2 selected, set report_type_selected to True
    if report_type == '1':

        # Let user know what they have selected.
        print ("\nYou selected full report.\n")

        # Set report_type_selected to True (breaks loop)
        report_type_selected = True

        # Call function to create full table with field names
        table = create_table()

        # Call function to add row of data to full table for user_city
        table = add_row(table, display_city_name, city_response)
        
        # If user has asked for random city, add row of data for random_city
        if random_selection == 'yes':
            table = add_row(table, random_city, random_response)

        # Print the full_table to user
        print(table)

    # If equal to 2, make temp only table
    elif report_type == '2':

        # Let user know what they have selected.
        print ("\nYou selected temperature only.")

        # Set report_type_selected to True (breaks loop)
        report_type_selected = True

        # Call function to create temp only table with field names
        table = create_table(full_report = False)

        # Call function to add row of data to temp only table for user_city
        table = add_row(table, user_city, city_response, full_report = False)

         # If user has asked for random city, add row of data for random_city
        if random_selection == 'yes':
            table = add_row(table, random_city, random_response, full_report = False)

        # Print the temp_table to user
        print (table)

    else:
        # If not 1 or 2, tell user to try again.
        # Report type selected stays false so question asked again.
        print("\nPlease try again. Input should either be: 1 or 2.\n")

# Save the full_table as a csv to current directory
write_table_to_csv(table)