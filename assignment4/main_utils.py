from datetime import datetime, timedelta
import string
import requests
import json
from db_utils import BookingNotFoundError

def get_availability_by_date(date):
    result = requests.get(
        'http://127.0.0.1:8000/date_availability/{}'.format(date),
        headers={'content-type': 'application/json'}
    )
    return result.json()

def get_availability_by_nailTech(nailTech):
    result = requests.get(
        'http://127.0.0.1:8000/tech_availability/{}'.format(nailTech),
        headers={'content-type': 'application/json'}
    )
    return result.json()

def add_new_booking(date, nailTech, appointmentType, time, client, contact):

    booking = {
         "_date": date,
         "nailTech": nailTech,
         "appointmentType" : appointmentType,
         "time": time,
         "client": client,
         "contact": contact
    }

    result = requests.put(
        'http://127.0.0.1:8000/booking',
        headers={'content-type': 'application/json'},
        data= json.dumps(booking)
    )

    return result.json()

def delete_old_booking(date, time, contact):

    booking = {
         "_date": date,
         "time": time,
         "contact": contact
    }

    # try:
    result = requests.put(
        'http://127.0.0.1:8000/delete',
        headers={'content-type': 'application/json'},
        data= json.dumps(booking)
    )

    return result.json()

    # except BookingNotFoundError as e:
    #     raise BookingNotFoundError("There are no bookings matching those details. Please check that the date, time, and your number are correct.")

def display_availability(records):
    # Print the names of the columns.
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
        'Nail Stylist', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18'))
    print('-' * 105)

    # print each data item.
    for item in records:
        print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
            item['Nail Stylist'], item['12-13'], item['13-14'], item['14-15'], item['15-16'], item['16-17'], item['17-18']
        ))

def display_tech_availability(records):
    # Print the names of the columns.
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
        'Date', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18'))
    print('-' * 105)

    # print each data item.
    for item in records:
        print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} ".format(
            item['Date'], item['12-13'], item['13-14'], item['14-15'], item['15-16'], item['16-17'], item['17-18']
        ))

def get_valid_date():

    date_selection = False
    while date_selection == False:

        # Ask what date they would like to try book an appointment for.
        date = input('What date would you like to book your appointment for (YYYY-MM-DD): ')

        try:
            # Convert string to a datetime object for checking it's not in the past and for giving alternatives below.
            date_format = '%Y-%m-%d'
            date_obj = datetime.strptime(date, date_format)

            # Store today's date and check that client's input isn't less than current date.
            today = datetime.now()
            if date_obj.date() < today.date():
                # If it is, tell client to try again.
                print ("You cannot book an appointment in the past! Please try again.")

            elif date_obj.date() == today.date() and today.hour >= 17:
                # If the date is today and it's after 6 PM, tell client to try again.
                print("You cannot book an appointment for today as it is past 5pm! Please try again.")
            
            else:
                date_selection = True
        
        except ValueError as ve:
            print(f'You entered {date}, which is not a valid date. Please try again.')
    
    return date, date_obj


def want_to_book():
    # If they input yes, continue with booking.
    booking_selection = False
    while booking_selection == False:
        # Ask client if they would like to book an appointment for that date.
        place_booking = input(f"Are you ready to book an appointment? yes/no: ").lower()

        if place_booking == 'yes':
            booking_selection = True

        elif place_booking == 'no':
            booking_selection = True

        else:
            print("You did not make a valid yes/no selection. Please try again.")
    
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
            print ("This is not a valid nail tech selection. Please try again.")
        
        elif nailTech in nailTech_list:
            # If so, break while loop and continue with booking.
            nailTech_selection = True

    return nailTech

def get_valid_time(date):
    timeslots = ['12-13', '13-14', '14-15', '15-16', '16-17', '17-18']

    time_selection = False
    # Check that the time provided is a valid time slot.
    while time_selection == False:
        time = input("What time? (12-13/13-14/14-15/15-16/16-17/17-18) ")

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
            print ("This is not a valid time slot. Please try again.")
        
        elif start_time < now:
            print ("You cannot book a time slot in the past! Please try again.")

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
            
            print (f"{appointmentType} is not a valid appointment type. Please try again.")
        
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

def get_valid_contact():
    valid_number = False
    while valid_number == False:
        contact = input("Please enter your phone number: ")

        if len(contact) != 11 or check_digits(contact) == False:
            print ("This is not a valid phone number. It must be 11 DIGITS long. Please try again.")
        
        elif len(contact) == 11 and check_digits(contact) == True:
            valid_number = True
    return contact

def twoDay_availability(date_obj):
    for num in range(2):
        next_date = str(date_obj.date() + timedelta(days=num+1))
        next_slots = get_availability_by_date(next_date)
        print()
        print(f'####### {next_date} AVAILABILITY #######')
        print()
        print(display_availability(next_slots))
        print()

    
