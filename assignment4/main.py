import requests
import json
from datetime import datetime, timedelta

def get_availability_by_date(date):
    result = requests.get(
        'http://127.0.0.1:8000/availability/{}'.format(date),
        headers={'content-type': 'application/json'}
    )
    return result.json()

def add_new_booking(date, nailTech, appointmentType, time, customer):

    booking = {
         "_date": date,
         "nailTech": nailTech,
         "appointmentType" : appointmentType,
         "time": time,
         "customer": customer
    }

    result = requests.put(
        'http://127.0.0.1:8000/booking',
        headers={'content-type': 'application/json'},
        data=json.dumps(booking)
    )

    return result.json()

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

def run():
    print('############################')
    print('Hello, welcome to our nail salon.')
    print('############################')
    print()
    date = input('What date you would like to book your appointment for (YYYY-MM-DD): ')

    # Convert string to a datetime object for checking it's not in the past and for alternatives below.
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date, date_format)

    # Store today's date and check that client's input isn't less than current date.
    today = datetime.now()
    if date_obj.date() < today.date():
        # If it is, tell client to try again.
        print ("You cannot book an appointment in the past! Please try again.")
    
    else:
        # If it's not, continue to show availability to client.
        slots = get_availability_by_date(date)
        print()
        print('####### AVAILABILITY #######')
        print()
        print(display_availability(slots))
        print()
        # Ask client if they would like to book an appointment for that date.
        place_booking = input(f"Would you like to book an appointment on {date}? yes/no: ").lower()

        # If they input yes, allow them to continue with booking.
        if place_booking == 'yes':
            nailTech = input("Which nail Technician? (Bronte/Finn/Max) ")
            cust = input("Enter your name: ")
            time = input("What time? (e.g., 13-14)")
            type = input("What would you like to get done? ")

            add_new_booking(date, nailTech, type, time, cust)

            print (f"Thanks {cust}, Booking complete with {nailTech} for a {type} on {date} at {time}. See you soon!")

        elif place_booking == 'no':
            print (f"You have selected not to book an appointment on {date}, but here is availability for the next 3 days.")

            for num in range(3):
                next_date = str(date_obj.date() + timedelta(days=num))
                next_slots = get_availability_by_date(next_date)
                print()
                print('####### AVAILABILITY #######')
                print()
                print (next_date)
                print(display_availability(next_slots))
                print()
            
            print("If you would still like to book another appointment on a different day, please just start again!")

if __name__ == '__main__':
    run()
