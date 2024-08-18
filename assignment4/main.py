from main_utils import * # Import all functions from main utils

# This main.py function enables client to make or cancel a booking. It uses functions from main_utils.py.
# It uses while loops to ensure valid selection at each point in the program, without needing
# to go back to the beginning each time!

def run():
    # Print welcome message to client.
    print('############################')
    print('Hello, welcome to our nail salon.')
    print('############################')
    print()

    # Start by asking client if they would like to book or cancel an appointment.
    # If they say cancel or book, it goes through that process, otherwise, the program ends with message.
    client_job = input("Would you like to book an appointment or cancel an appointment? (book/cancel) ")

    # If they want to cancel, it asks for the details needed to cancel.
    if client_job == 'cancel':

        # Ask for and validate input
        date, _ = get_valid_date(book = False)
        time, _ = get_valid_time(date, book = False)
        contact = get_valid_contact(book = False)

        # Print to client the details they have provided for their reference
        print (f"You asked to cancel an appointment on {date} at {time}, with the following contact number: {contact}")

        # Call delete_old_booking from main_utils (will raise error if cancel request has no effect)
        delete_old_booking(date, time, contact)

    # If they want to book, it asks the way they would like to view availability (by date or by nail tech)
    elif client_job == 'book':

        # Ask for, and validate, availability type
        availability_type = get_valid_availability_type()

        # If they want it by nail tech, asks which nail tech they want to see
        if availability_type == 'tech':

            # Ask for, and validate which nail technician
            nailTech = get_valid_nailTech()

            # Get availability by nail tech (from today's date)
            slots = get_availability_by_nailTech(nailTech)

            # Print availability to user
            print()
            print(f'####### AVAILABILITY for {nailTech} for the next 7 days. #######')
            print()
            print(display_availability(slots, nailTech=True))
            print()

            # Ask if they want to place a booking
            place_booking = want_to_book()

            # If they want to place a booking, ask for details
            if place_booking == 'yes':

                # Call user-defined function to ask for, and validate date of appointment they would like.
                date, date_obj = get_valid_date() # returns date string and datetime object.

                # Ask for, and validate which time slot
                # also returns datetime object of time slot start time for printing out below
                time, start_time = get_valid_time(date)

                # Check that date and time are actually available!
                date_availability = get_availability_by_date(date)
                stylist_availability = next((stylist for stylist in date_availability if stylist['Nail Stylist'] == nailTech), None)
                if stylist_availability[time] == 'Not Available':
                    # If it's not, tell user to try again
                    print ("This appointment is not available. Please try again.")
                
                # If it's available, allow them to continue
                else:
                    # Ask for, and validate which type of appointment they would like
                    appointmentType = get_valid_appointmentType()

                    # Ask for their name
                    cust = input("Please enter your name: ")

                    # Ask for and validate their contact number
                    contact = get_valid_contact()

                    # Provide their details to add_new_booking function to add booking
                    add_new_booking(date, nailTech, appointmentType, time, cust, contact)

                    # Print details of booking to user
                    message_booking(cust, nailTech, appointmentType, start_time)
            
            # If they do not want to book an appointment, print no booking message with next 2 days of availability
            elif place_booking == 'no':
                message_noBooking(nailTech = True)

        # If they would like to see availability by date, asks for date first
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
                # Print availability
                print()
                print('####### AVAILABILITY #######')
                print()
                print(display_availability(slots, nailTech=False))
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

                # Check that date and time actually available!
                date_availability = get_availability_by_date(date)
                stylist_availability = next((stylist for stylist in date_availability if stylist['Nail Stylist'] == nailTech), None)
                if stylist_availability[time] == 'Not Available':
                    # If it's not, tell user to try again
                    print ("This appointment is not available. Please try again.")
                
                # If it is, continue with booking
                else:
                    # Ask for, and validate which type of appointment they would like
                    appointmentType = get_valid_appointmentType()

                    # Ask for their name
                    cust = input("Please enter your name: ")

                    # Ask for and validate their contact number
                    contact = get_valid_contact()

                    # Provide their details to add_new_booking function to add booking
                    add_new_booking(date, nailTech, appointmentType, time, cust, contact)

                    # Print details of booking to user
                    message_booking(cust, nailTech, appointmentType, start_time)

            # If they do not want to book an appointment for that date, don't ask any further questions but present next 2 day availability.
            elif place_booking == 'no':
                message_noBooking(nailTech=False, date_obj=date_obj)

    # If they don't make a valid selection, program ends and they are prompted to try again.
    else:
        print("You did not make a valid selection. Please try again.")

if __name__ == '__main__':
    run()