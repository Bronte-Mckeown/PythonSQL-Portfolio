import mysql.connector  # Importing the MySQL connector to enable Python to interact with the MySQL database
from config import USER, PASSWORD, HOST  # Importing database connection details from a configuration file

# Define a custom exception to handle database connection errors specifically.
class DbConnectionError(Exception):
    pass

# Define a custom exception to raise error if request to delete booking doesn't do anything.
class BookingNotFoundError(Exception):
    pass

# Function to establish a connection to the database.
def _connect_to_db(db_name):
    """
    This function creates a connection to a MySQL database using the provided database name.
    It uses the mysql.connector.connect method to establish the connection with the necessary
    credentials and returns the connection object.

    Parameters:
    db_name (str): The name of the database to connect to.

    Returns:
    cnx: A MySQLConnection object representing the database connection.
    """
    cnx = mysql.connector.connect(
        host=HOST,  # The address of the database server
        user=USER,  # The username to log in to the database
        password=PASSWORD,  # The password to log in to the database
        auth_plugin='mysql_native_password',  # The authentication plugin to use for the connection
        database=db_name  # The name of the database to connect to
    )
    return cnx  # Return the connection object

# Helper function for connecting to database and creating cursor object.
def _connection_and_cur_(db_name):
    # Establish a connection to the database using the provided database name.
    db_connection = _connect_to_db(db_name)  
    cur = db_connection.cursor()  # Create a cursor object to execute SQL queries.
    print("Connected to DB: %s" % db_name)  # Print a message indicating a successful connection.
    return db_connection, cur # Return connection object and cursor object.

# Function to map raw database query results into a user-friendly format
def _map_values(schedule, nailTech = None):
    """
    This function transforms the raw results from a database query into a list of dictionaries
    where each dictionary represents the availability of a team member for different time slots.
    The function checks each time slot and marks it as 'Available' or 'Not Available'.

    Parameters:
    schedule (list): A list of tuples where each tuple represents the availability of a team member for various time slots.

    Returns:
    mapped (list): A list of dictionaries with keys as time slots and values as availability status.
    """
    mapped = []  # Initialize an empty list to store the mapped values
    for item in schedule:  # Iterate over each item in the schedule

        # If nailtech specified (i.e., not None), date included (but not nail tech name).
        if nailTech:
            date = item[7].strftime('%Y-%m-%d')
            mapped.append({'Date' : date,
                           '12-13': 'Not Available' if item[1] else 'Available',  # Check availability for 12-1 PM slot
                           '13-14': 'Not Available' if item[2] else 'Available',  # Check availability for 1-2 PM slot
                            '14-15': 'Not Available' if item[3] else 'Available',  # Check availability for 2-3 PM slot
                            '15-16': 'Not Available' if item[4] else 'Available',  # Check availability for 3-4 PM slot
                            '16-17': 'Not Available' if item[5] else 'Available',  # Check availability for 4-5 PM slot
                            '17-18': 'Not Available' if item[6] else 'Available',  # Check availability for 5-6 PM slot
                           })
        # Otherwise, nail tech name is included and date isn't needed.
        else:
            mapped.append({'Nail Stylist': item[0],
                           '12-13': 'Not Available' if item[1] else 'Available',  # Check availability for 12-1 PM slot
                           '13-14': 'Not Available' if item[2] else 'Available',  # Check availability for 1-2 PM slot
                            '14-15': 'Not Available' if item[3] else 'Available',  # Check availability for 2-3 PM slot
                            '15-16': 'Not Available' if item[4] else 'Available',  # Check availability for 3-4 PM slot
                            '16-17': 'Not Available' if item[5] else 'Available',  # Check availability for 4-5 PM slot
                            '17-18': 'Not Available' if item[6] else 'Available',  # Check availability for 5-6 PM slot
                           })

    return mapped  # Return the list of mapped values

# Function to get booking availability for a specific date
def get_all_booking_availability(_date):
    """
    This function retrieves the booking availability for a specific date from the database.
    It connects to the database, executes a query to fetch the booking data, maps the results
    into a user-friendly format, handles any exceptions that occur during the process, and
    ensures the database connection is closed properly.

    Parameters:
    _date (str): The date for which to retrieve booking availability in the format 'YYYY-MM-DD'.

    Returns:
    availability (list): A list of dictionaries representing the booking availability of team members for the given date.
    """
    availability = []  # Initialize an empty list to store the availability information

    db_name = 'nails'  # The name of the database to connect to

    # First, try to esetablish a connection to the database.
    try: 
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object

        try:
        # If connection established, try SQL query to get booking availability for a specific date
            query = """
                SELECT  nailTech, `12-13`, `13-14`, `14-15`, `15-16`, `16-17`, `17-18`
                FROM nail_bookings 
                WHERE bookingDate = '{}'
                """.format(_date)

            cur.execute(query)  # Execute the SQL query
            result = cur.fetchall()  # Fetch all results from the executed query, which returns a list of tuples
            availability = _map_values(result)  # Map the raw results to a user-friendly format using helper function!
            cur.close()  # Close the cursor object

        # If query isn't successful, this exception will be raised.
        except Exception as e:  # Catch any exceptions that occur
            # Raise a custom exception if an error occurs
            raise DbConnectionError(f"Query to database {db_name} failed. Make sure table and columns exist!") from e
    
        # If connection is establised, always closes the connection.
        finally:
            db_connection.close()  # Close the database connection
            print("DB connection is closed")  # Print a message indicating the connection is closed
    
    # If connection isn't established, this exception will be raised (and query won't be attempted.)
    except Exception as e:  # Catch any exceptions that occur
        # Raise a custom exception if an error occurs while trying to connect to data base
        raise DbConnectionError(f"Failed to connect to data base {db_name}") from e

    return availability  # Return the availability information in nice format.

def get_nailTech_availability(nailTech):
    """
    This function retrieves the booking availability for a specific nail technician from the database.
    It connects to the database, executes a query to fetch the nail tech data, maps the results
    into a user-friendly format, handles any exceptions that occur during the process, and
    ensures the database connection is closed properly.

    Parameters:
    _date (str): The nail tech for which to retrieve booking availability.

    Returns:
    availability (list): A list of dictionaries representing the booking availability of that nail tech.
    """

    availability = []  # Initialize an empty list to store the availability information

    db_name = 'nails'  # The name of the database to connect to

    # First, try to esetablish a connection to the database.
    try: 
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object

        try:
        # If connection established, try SQL query to get booking availability for a specific nail tech
            query = """
                SELECT  nailTech, `12-13`, `13-14`, `14-15`, `15-16`, `16-17`, `17-18`, `bookingDate`
                FROM nail_bookings 
                WHERE nailTech = '{}'
                LIMIT 7
                """.format(nailTech)

            cur.execute(query)  # Execute the SQL query
            result = cur.fetchall()  # Fetch all results from the executed query, which returns a list of tuples
            availability = _map_values(result, nailTech)  # Map the raw results to a user-friendly format using helper function!
            cur.close()  # Close the cursor object

        # If query isn't successful, this exception will be raised.
        except Exception as e:  # Catch any exceptions that occur
            # Raise a custom exception if an error occurs
            raise DbConnectionError(f"Query to database {db_name} failed. Make sure table and columns exist!") from e
    
        # If connection is establised, always closes the connection.
        finally:
            db_connection.close()  # Close the database connection
            print("DB connection is closed")  # Print a message indicating the connection is closed
    
    # If connection isn't established, this exception will be raised (and query won't be attempted.)
    except Exception as e:  # Catch any exceptions that occur
        # Raise a custom exception if an error occurs while trying to connect to data base
        raise DbConnectionError(f"Failed to connect to data base {db_name}") from e

    return availability  # Return the availability information in nice format.

# Function to add new booking to DB.
def add_booking(_date, nailTech, appointmentType, time, client, contact):
    db_name = 'nails'
    # Try to connect to database first.
    try:
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object
    
    # If connection unsuccessful, raise exception (and query is never attempted).
    except Exception as e:
            raise DbConnectionError(f"Appointment booking unsuccessful: Failed to connect to DB {db_name}.")
        
    # If connection sucessful, proceed to add booking via SQL query.
    try:
        query = """
            UPDATE  nail_bookings
            SET 
                `{time}` = '{appointmentType}', 
                `{time_id}` = '{client}', 
                `{time_contact}` = '{contact}'
            WHERE bookingDate = '{date}' AND nailTech = '{nailTech}'
            """.format(time=time, appointmentType = appointmentType, time_id=time +'-client', client=client, time_contact=time +'-contact',
                        contact = contact, date=_date, nailTech =nailTech)

        cur.execute(query)
        db_connection.commit()
        print(f"Success. Updated DB {db_name} with new booking.")
        cur.close()

    # If exception occurs, inform user that the connection was successful, but adding the booking wasn't.
    except Exception as e:
        raise DbConnectionError(f"Appointment booking unsuccessful: Connected to DB {db_name}, but failed to update with new booking.") from e

    # If the connection was established, close the DB.
    finally:
        db_connection.close()
        print(f"DB {db_name} connection is now closed.")
    
# Function to add new booking to DB.
def delete_booking(_date, time, contact):
    db_name = 'nails'
    # Try to connect to database first.
    try:
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object

    # If connection unsuccessful, raise exception (and query is never attempted).
    except Exception as e:
            raise DbConnectionError(f"Booking not deleted. Failed to connect to DB {db_name}.") from e
    
    # If connection sucessful, proceed to add booking via SQL query.
    try:
        query = """
            UPDATE  nail_bookings
            SET 
                `{time}` = NULL, 
                `{time_id}` = NULL, 
                `{time_contact}` = NULL
            WHERE bookingDate = '{date}' AND `{time_contact}` = '{contact}'
            """.format(time=time, time_id=time +'-client', time_contact=time +'-contact',
                        date=_date, contact=contact)

        cur.execute(query)
        db_connection.commit()
        cur.close()

        # if cur.rowcount == 0:
            # raise BookingNotFoundError("There are no bookings matching those details. Please check that the date, time, and your number are correct.")
    
    except Exception as e:
        raise DbConnectionError(f"Appointment cancellation unsuccessful: Connected to DB {db_name}, but failed to cancel booking.") from e

    # If the connection was established, close the DB.
    finally:
        db_connection.close()
        print(f"DB {db_name} connection is now closed.")


# If the script is run directly, execute the following code (for testing)
if __name__ == '__main__':
    pass
    # Call the function with a specific date for testing purposes
    # print (get_nailTech_availability('bronte'))
    # print(get_all_booking_availability('2024-06-30'))
    add_booking('2024-06-30', 'bronte','gei manicure', '15-16', 'Sayo', '07876347982')
    delete_booking('2024-06-30', '15-16', '07876347982')