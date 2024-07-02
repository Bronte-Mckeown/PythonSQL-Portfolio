from datetime import datetime, timedelta
import string
import requests
import json

# NOTE: I used Chat-GPT to help propogate error handling from db_utils to main_utils.
# To do that, I provided it with the error handling I had set up in db_utils delete_booking function
# and explained that I couldn't get the error messages to propogate on client-side and that
# very general (hard to read) errors were being raised but not with the expected message.
# The parts of code I kept were 'response.raise_for_status()' and the raising of errors in app.py but
# I edited the rest of what it gave me to make it work as I wanted because I wanted it to 
# print a nice message to the client as a print statement rather than raise the error message from db_utils.
# I then modified as necessary for all the other functions.

# function that makes request to 'availability/date' endpoint to get booking availability by date
def get_availability_by_date(date):
    # Try to get availability by date and get response status code
    try:
        response = requests.get(
            'http://127.0.0.1:8000/date_availability/{}'.format(date),
            headers={'content-type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    
    # if http error occurs, print statements based on what code it is (500 = server error)
    except requests.exceptions.HTTPError:
        if response.status_code == 500:
            print('Could not connect to server. Please try again or call the salon.')
        else:
            print(f'There was a problem with that request (error code: {response.status_code}). Please try again or call the salon.')

# function that makes request to 'availability/nailTech' endpoint to get booking availability by nail tech
def get_availability_by_nailTech(nailTech):

    now = datetime.now()
    now_date = now.date()
    # Try to get availability by nail tech and get response status code
    try:
        response = requests.get(
            'http://127.0.0.1:8000/tech_availability/{}/{}'.format(nailTech, now_date),
            headers={'content-type': 'application/json'}
        )
        response.raise_for_status()
        return response.json()
    
    # if http error occurs, print statements based on what code it is (500 = server error)
    except requests.exceptions.HTTPError:
        if response.status_code == 500:
            print('Could not connect to server. Please try again or call the salon.')
        else:
            print(f'There was a problem with that request (error code: {response.status_code}). Please try again or call the salon.')

# function that makes request to 'booking' endpoint to make new appointment
def add_new_booking(date, nailTech, appointmentType, time, client, contact):

    booking = {
        "_date": date,
        "nailTech": nailTech,
        "appointmentType" : appointmentType,
        "time": time,
        "client": client,
        "contact": contact
    }

    try:
        # try to make request to API
        response = requests.put(
            'http://127.0.0.1:8000/booking',
            headers={'content-type': 'application/json'},
            data= json.dumps(booking)
        )

        response.raise_for_status()

        return response.json()
    
    except requests.exceptions.HTTPError:
        if response.status_code == 500:
            print('Could not connect to server. The appointment was not made. Please try again or call the salon.')
        else:
            print(f'There was a problem with that request (error code: {response.status_code}). The appointment was not made. Please try again or call the salon.')

# function to make request to 'delete' endpoint to delete existing appointment
def delete_old_booking(date, time, contact):

    booking = {
         "_date": date,
         "time": time,
         "contact": contact
    }

    try:
        # try to make request to API
        response = requests.put(
            'http://127.0.0.1:8000/delete',
            headers={'content-type': 'application/json'},
            data=json.dumps(booking)
        )

        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.HTTPError:
        # Extract error message from response
        error_message = response.json().get('error', 'Unknown error')
        if response.status_code == 500:
            print(f'Could not connect to server. The booking was not cancelled. Please try again or call the salon.')
        elif response.status_code == 400:
            print(f'Those details did not match any bookings in the database. The booking was not cancelled. Please try again or call the salon.')
        else:
            print(f'The booking was not cancelled (error code: {response.status_code}). Please try again or call the salon.')
            
        
def get_valid_availability_type():
    valid_selection = False
    while valid_selection == False:
        availability_type = input("Would you like to see availability by date or by nail technician? (date/tech) ").lower()
        if availability_type == 'date' or availability_type == 'tech':
            valid_selection = True
            return availability_type
        else:
            print("That is not a valid selection. Please try again by entering 'date' or 'tech' or enter ctrl+c to exit.")

# function that formats returned availability from API endpoint for printing out to user
def display_availability(records, nailTech = False):
    # if nail teach is true, make first column 'Date'
    if nailTech:
        first_col = 'Date'
    # otherwise, first column is 'Nail Stylist'
    else:
        first_col = 'Nail Stylist'

    # Print the names of the columns.
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
        first_col, '12-13', '13-14', '14-15', '15-16', '16-17', '17-18'))
    print('-' * 105)

    # print each data item.
    for item in records:
        print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
            item[first_col], item['12-13'], item['13-14'], item['14-15'], item['15-16'], item['16-17'], item['17-18']
        ))

# Function that adds user for what date they would like to book an appointment for / cancel and makes sure it's valid
def get_valid_date(book = True):

    # determine string for print statements depending on whether book is true or false
    if book:
        print_str = "book"
    else:
        print_str = "cancel"

    valid_date = False # Set valid date to false so loop continues until valid date provided
    while valid_date == False:

        # Ask user what date they would like to try book an appointment for.
        if book:
            date = input('What date would you like to book your appointment for (YYYY-MM-DD): ')
        else:
            date = input('What date is the appointment you would like to cancel (YYYY-MM-DD): ')

        # Use exception handling to handle value error if invalid date provided.
        try:
            # Convert string to a datetime object for checking it's not in the past and for giving alternatives below.
            date_format = '%Y-%m-%d'
            date_obj = datetime.strptime(date, date_format)

            # Store today's date and check that client's input isn't less than current date.
            today = datetime.now()
            if date_obj.date() < today.date():
                # If it is, tell client to try again.
                print (f"You cannot {print_str} an appointment in the past! Please try again or enter ctrl+c to exit.")
            elif date_obj.date() == today.date() and today.hour >= 17:
                # If the date is today and it's after 6 PM, tell client to try again.
                print(f"You cannot {print_str} an appointment for today as it is past 5pm! Please try again or enter ctrl+c to exit.")
            else:
                valid_date = True # if it's a valid date, return true to break the loop
        
        except ValueError as ve:
            print(f'You entered {date}, which is not a valid date. Please try again, with the format YYYY-MM-DD or enter ctrl+c to exit.')
    
    return date, date_obj # Return date string and datetime object for using later

# Function that asks user if they want to book an appointment
def want_to_book():
    booking_selection = False # Set booking selection to false so loop continues until valid selection provided
    while booking_selection == False:
        # Ask client if they would like to book an appointment for that date.
        place_booking = input(f"Are you ready to book an appointment? yes/no: ").lower()

        if place_booking == 'yes':
            booking_selection = True
        elif place_booking == 'no':
            booking_selection = True
        else:
            print("You did not make a valid yes/no selection. Please try again or enter ctrl+c to exit.")
    
    return place_booking

def get_valid_nailTech():
    nailTech_list = ['bronte', 'finn', 'max']
    # Create while loop so that only valid nail tech name is allowed and keep getting them to try again
    # until they make a valid selection.
    nailTech_selection = False # Keeps loop going until valid selection made.
    # Check that the nail tech provided is a valid nail tech.
    while nailTech_selection == False:
        nailTech = input("Which nail Technician? (bronte/finn/max) ").lower()
        if nailTech not in nailTech_list:
            # If not, tell user and ask them to try again.
            print ("This is not a valid nail tech selection. Please try again or enter ctrl+c to exit.")
        
        elif nailTech in nailTech_list:
            # If so, break while loop and continue with booking.
            nailTech_selection = True

    return nailTech

def get_valid_time(date, book = True):

    if book:
        print_str = 'book'
    else:
        print_str = 'cancel'

    timeslots = ['12-13', '13-14', '14-15', '15-16', '16-17', '17-18']

    time_selection = False
    # Check that the time provided is a valid time slot.
    while time_selection == False:
        if book:
            time = input("What time? (12-13/13-14/14-15/15-16/16-17/17-18) ")
        else:
            time = input("Please enter the time of your appointment: (12-13/13-14/14-15/15-16/16-17/17-18) ")

        # Split the string into start and end times, and select start time
        start_time_str = time.split('-')[0]
        date_time_str = date + " " + start_time_str + ":00:00"

        # Define the format
        date_time_format = '%Y-%m-%d %H:%M:%S'
        # Convert the string to time object
        start_time = datetime.strptime(date_time_str, date_time_format)

        now = datetime.now()
        if time not in timeslots:
            # If not, tell user and ask them to try again.
            print ("This is not a valid time slot. Please try again or enter ctrl+c to exit.")
        
        elif start_time < now:
            print (f"You cannot {print_str} a time slot in the past! Please try again or enter ctrl+c to exit.")

        elif time in timeslots and start_time > now:
            # If so, break while loop and continue with booking.
            time_selection = True

    return(time, start_time)

def get_valid_appointmentType():
    appointmentType_list = ['regular manicure', 'gel manicure', 'regular pedicure', 'gel pedicure']
    appointmentType_selection = False
    while appointmentType_selection == False:
        mani_ped = input ("Would you like a manicure or pedicure? (manicure/pedicure) ").lower()
        type = input("Would you like regular or gel? (regular/gel) ").lower()

        appointmentType = type + " " + mani_ped

        if appointmentType not in appointmentType_list:
            
            print (f"{appointmentType} is not a valid appointment type. Please try again or enter ctrl+c to exit.")
        
        elif appointmentType in appointmentType_list:
            appointmentType_selection = True

    return appointmentType


# Helper function to check phone number provided contains only digits
# https://stackoverflow.com/questions/21388541/how-do-you-check-in-python-whether-a-string-contains-only-numbers
def check_digits(contact):
    for ch in contact:
        if not ch in string.digits:
            return False
    return True

def get_valid_contact(book = True):

    valid_number = False
    while valid_number == False:
        if book:
            contact = input("Please enter your phone number: ")
        else:
            contact = input("Please enter the phone number you provided upon booking: ")

        if len(contact) != 11 or check_digits(contact) == False:
            print ("This is not a valid phone number. It must be 11 DIGITS long. Please try again or enter ctrl+c to exit.")
        
        elif len(contact) == 11 and check_digits(contact) == True:
            valid_number = True
    return contact

def message_booking(cust, nailTech, appointmentType, start_time):
    print (f"Thanks {cust}, booking confirmed with {nailTech} for a {appointmentType} on {start_time.date()} at {start_time.time()}. See you soon!")

def message_noBooking(nailTech = False, date_obj = None):
    print()
    if nailTech:
        date = datetime.now()
        print (f"You have selected not to book an appointment. For your reference, here is the availability for all nail techs for the next 2 days.")
        twoDay_availability(date)
    else:
        date = date_obj
        print (f"You have selected not to book an appointment. For your reference, here is the availability for all nail techs for the next 2 days.")
        twoDay_availability(date)
    print("If you would still like to book another appointment, please just start again!")
   

def twoDay_availability(date_obj):
    for num in range(2):
        next_date = str(date_obj.date() + timedelta(days=num+1))
        next_slots = get_availability_by_date(next_date)
        print()
        print(f'####### {next_date} AVAILABILITY #######')
        print()
        print(display_availability(next_slots))
        print()