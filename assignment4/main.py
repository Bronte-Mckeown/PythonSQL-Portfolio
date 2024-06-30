from main_utils import *

# This main.py function enables user to make booking. It uses functions from main_utils.py.
def run():

    # Print welcome message to client.
    print('############################')
    print('Hello, welcome to our nail salon.')
    print('############################')
    print()

    client_job = input("Would you like to book an appointment or cancel an appointment? (book/cancel) ")

    if client_job == 'cancel':

        date = input("Please enter the date of your appointment: (YYYY-MM-DD) ")
        time = input("Please enter the time of your appointment: (12-13/13-14/14-15/15-16/16-17/17-18) ")
        contact = input("Please enter the phone number you provided upon booking: ")

        delete_old_booking(date, time, contact)

    elif client_job == 'book':

        availability_type = input("Would you like to see availability by date or by nail technician? (date/tech) ")

        if availability_type == 'tech':

            # Ask for, and validate which nail technician
            nailTech = get_valid_nailTech()

            # Get availability by nail tech
            slots = get_availability_by_nailTech(nailTech)

            print()
            print(f'####### AVAILABILITY for {nailTech} for the next 7 days. #######')
            print()
            print(display_tech_availability(slots))
            print()

            # Ask if they want to place a booking.
            place_booking = want_to_book()

            if place_booking == 'yes':
                # Call user-defined function to ask for, and validate date of appointment they would like.
                date, date_obj = get_valid_date() # returns date string and datetime object.

                # Ask for, and validate which time slot
                # also returns datetime object of time slot start time for printing out below
                time, start_time = get_valid_time(date)

                # Ask for, and validate which type of appointment they would like
                appointmentType = get_valid_appointmentType()

                # Ask for their name
                cust = input("Please enter your name: ")

                # Ask for and validate their contact number
                contact = get_valid_contact()

                # Provide their details to add_new_booking function to add booking
                add_new_booking(date, nailTech, appointmentType, time, cust, contact)

                # Print details of booking to user
                print (f"Thanks {cust}, booking confirmed with {nailTech} for a {appointmentType} on {start_time.date()} at {start_time.time()}. See you soon!")
            
            # If they do not want to book an appointment
            elif place_booking == 'no':
                print()
                print (f"You have selected not to book an appointment. For your reference, here is the availability for all nail techs for the next 2 days.")
                now = datetime.now()
                twoDay_availability(now)
                print("If you would still like to book another appointment, please just start again!")

        elif availability_type == 'date':

            # Call user-defined function to ask for, and validate date of appointment they would like.
            date, date_obj = get_valid_date() # returns date string and datetime object

            # Get slots for the date provided
            slots = get_availability_by_date(date)

            # Check the slots aren't empty.
            if len(slots) == 0:
                # If they are, the program stops so they can either start again or call the salon.
                print (f"Slots for {date} have not been released yet. They are usually released up to three months in advance. Please start again to select a new date or call the salon.")

            # If slots are not empty, continue program.
            else:
                print()
                print('####### AVAILABILITY #######')
                print()
                print(display_availability(slots))
                print()

                # Ask if they want to place a booking
                place_booking = want_to_book()

            # If they do, continue to ask for further details.
            if place_booking == 'yes':
                
                # Ask for, and validate which nail technician
                nailTech = get_valid_nailTech()

                # Ask for, and validate which time slot
                # also returns datetime object of time slot start time for printing out below
                time, start_time = get_valid_time(date)

                # Ask for, and validate which type of appointment they would like
                appointmentType = get_valid_appointmentType()

                # Ask for their name
                cust = input("Please enter your name: ")

                # Ask for and validate their contact number
                contact = get_valid_contact()

                # Provide their details to add_new_booking function to add booking
                add_new_booking(date, nailTech, appointmentType, time, cust, contact)

                # Print details of booking to user
                print (f"Thanks {cust}, booking confirmed with {nailTech} for a {appointmentType} on {start_time.date()} at {start_time.time()}. See you soon!")

            # If they do not want to book an appointment for that date, don't ask any further questions but present next 2 day availability.
            elif place_booking == 'no':
                print()
                print (f"You have selected not to book an appointment. For your reference, here is the availability for all nail techs for the next 2 following days.")
                twoDay_availability(date_obj)
                print("If you would still like to book another appointment, please just start again!")

    else:
        print("You did not make a valid selection. Try again.")

if __name__ == '__main__':
    run()
