""" 

Written by: Bronte Mckeown

Followed: https://www.youtube.com/watch?v=9P5MY_2i7K8
for demonstration on how to access weather API.

Get your own API Key by signing up here:
https://home.openweathermap.org

Save your API key in a .txt file called 'api_key' in 
parent directory.

If you don't have them installed already, use pip
to install 'requests' and 'prettytable' in terminal.

"""
# Import datetime and requests
import datetime as dt
import random
import requests
from prettytable import PrettyTable

# Define custom functions

def join_url(api_key, city):
    """
    Join base URL with api_key and city
    """
    # Set base_url to the openweathermap API URL
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Create full_url by adding api_key and city strings
    full_url = base_url + "appid=" + api_key + "&q=" + city
    
    return full_url

def convert_celsius(kelvin):
    """
    Convert kelvin temp to celsius
    """
    # Subtract constant to covert & covert to integer
    celsius = int(kelvin -273.15)

    return celsius

# Read API key in from txt file titled "api_key.txt"
# Use .rstrip() to prevent python reading in newline character
my_key = open("api_key.txt", "r").readline().rstrip()

# Ask User what City they want to see Weather for
user_city = input("""What City would you like to know the weather for? """)

# Create full URL using api_key variable and city from user input
city_url = join_url(my_key, user_city)

# Use requests module to retrieve data from city URL
city_response = requests.get(city_url).json()

# Ask user if they want a random city selection.
random_selection = input("""Would you like to get the weather for a 
                    random City? yes/no: """)

# If User selects yes, randomly select a City from list
if random_selection.lower() == 'yes':
    
    # List of possible cities to randomly chose from
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
    random_url = join_url(my_key, random_city)

    # Use requests module to retrieve data from city URL
    random_response = requests.get(random_url).json()

"""
We now want to ask user if they want a full report
or just the temperature.

We use a while loop so that if they input the wrong
values (anything other than 1 or 2), it asks again.

"""

# Set report_type_selected to False
report_type_selected = False

def full_table_field_names():
    """
    Creates full weather report for provided response.
    """
    # Create empty pretty table to add to
    table = PrettyTable()

    # Add data to table
    table.field_names = ["City name", "Summary", "Actual Temp",
                        "Feels like", "Temp Min", "Temp Max",
                        "Pressure", "Humidity", "Visibility",
                        "Wind Speed"]
    
    return table

def add_full_row(table, city, response):
    
    # Add row
    table.add_row([city,
                response['weather'][0]['main'],
                convert_celsius(response['main']['temp']),
                convert_celsius(response['main']['feels_like']),
                convert_celsius(response['main']['temp_min']),
                convert_celsius(response['main']['temp_max']),
                response['main']['pressure'],
                response['main']['humidity'],
                response['visibility'],
                response['wind']['speed']])
    
    return table

def temp_table_field_names():
    """
    Creates full weather report for provided response.
    """
    # Create empty pretty table to add to
    table = PrettyTable()

    # Add data to table
    table.field_names = ["City name", "Actual Temp",
                        "Feels like", "Temp Min", "Temp Max"
                        ]
    
    return table


def add_temp_row(table, city, response):
    
    # Add row
    table.add_row([city,
                convert_celsius(response['main']['temp']),
                convert_celsius(response['main']['feels_like']),
                convert_celsius(response['main']['temp_min']),
                convert_celsius(response['main']['temp_max'])]
                )
    
    return table


# While it is False, ask question
while report_type_selected == False:
    # Ask User for report type (full or just temperature)
    report_type = input("""Would you like a (1) full weather report or 
    (2) just temperature? Input 1 or 2:""")

    # If 1 or 2 selected, set report_type_selected to True
    if int(report_type) == 1:
        print ("\nYou selected full report.\n")
        report_type_selected = True

        full_table = full_table_field_names()

        full_table = add_full_row(full_table, user_city, city_response)
        
        if random_selection == 'yes':
            full_table = add_full_row(full_table, random_city, random_response)

        print (full_table)

    elif int(report_type) == 2:
        print ("\nYou selected temperature only.\n")
        report_type_selected = True

        temp_table = temp_table_field_names()

        temp_table = add_temp_row(temp_table, user_city, city_response)

        if random_selection == 'yes':
            temp_table = add_temp_row(temp_table, random_city, random_response)

        print (temp_table)

    else:
        # If not 1 or 2, tell user to try again.
        # Report type selected stays false so question asked again.
        print("""\nPlease try again. Input should either be: 1 or 2.\n""")
        report_type_selected = False
