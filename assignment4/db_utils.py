# NOTE: Chat GPT used to create doc strings for each finished function, which are then edited for accuracy.

import mysql.connector  # Import the MySQL connector to enable Python to interact with the MySQL database
from config import USER, PASSWORD, HOST  # Import database connection details from configuration file
from datetime import datetime # for testing

# Define a custom exception to handle database connection errors.
class DbConnectionError(Exception):
    pass

# Define a custom exception to handle SQL query errors.
class DbQueryError(Exception):
    pass

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

def _connection_and_cur_(db_name):
    """
    This function establishes a connection to the database using the provided database name,
    creates a cursor object to execute SQL queries, and prints a message indicating a successful connection.
    
    Parameters:
    db_name (str): The name of the database to connect to.

    Returns:
    tuple: A tuple containing the database connection object and the cursor object.

    """
    # Establish a connection to the database using the provided database name.
    db_connection = _connect_to_db(db_name)  # Calls user-defined function
    cur = db_connection.cursor()  # Create a cursor object to execute SQL queries.
    print("Connected to DB: %s" % db_name)  # Print a message indicating a successful connection.
    return db_connection, cur # Return connection object and cursor object.

def _map_values(schedule, nailTech = None):
    """
    Helper function to map values from booking schedule returned by SQL query to a more readable format.

    It iterates over each item in the booking schedule and maps the availability for each 
    time slot (12-13 ..., 17-18) to 'Available' or 'Not Available'. If the nailTech 
    parameter is provided, the date is included in the mapped values. Otherwise, the nail technician's 
    name is included.

    Parameters:
    schedule (list): A list of schedule items, where each item is expected to be a list
                     containing the following elements:
                     [nail_tech_name, 12-13, ..., 17-18, date]
    nailTech (str, optional): The name of the nail technician. If provided, the date is included
                              in the mapped values and the technician's name is omitted.

    Returns:
    list: A list of dictionaries, where each dictionary represents the availability of a nail
          technician or a specific date, depending on the presence of the nailTech parameter.
    """
    mapped = []  # Initialize empty list to store mapped values
    for item in schedule:  # Iterate over each item in the schedule
        # If nailtech specified (i.e., not None), date included (but not nail tech name).
        if nailTech:
            date = item[7].strftime('%Y-%m-%d') # Convert date for adding to mapped
            mapped.append({'Date' : date,
                           '12-13': 'Not Available' if item[1] else 'Available',  
                           '13-14': 'Not Available' if item[2] else 'Available',  
                            '14-15': 'Not Available' if item[3] else 'Available',  
                            '15-16': 'Not Available' if item[4] else 'Available',  
                            '16-17': 'Not Available' if item[5] else 'Available',  
                            '17-18': 'Not Available' if item[6] else 'Available',
                           })
        # Otherwise, nail tech name is included and date isn't.
        else:
            mapped.append({'Nail Stylist': item[0],
                           '12-13': 'Not Available' if item[1] else 'Available',
                           '13-14': 'Not Available' if item[2] else 'Available',
                            '14-15': 'Not Available' if item[3] else 'Available',
                            '15-16': 'Not Available' if item[4] else 'Available',
                            '16-17': 'Not Available' if item[5] else 'Available',
                            '17-18': 'Not Available' if item[6] else 'Available',
                           })

    return mapped  # Return the list of mapped values

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

    Raises:
    DbConnectionError: If the function fails to connect to the database.
    DbQueryError: If the function connects to the database but fails to retrieve availability.
    """
    availability = []  # Initialize empty list to store the availability information
    db_name = 'nails'  # The name of the database to connect to

    # First, try to esetablish a connection to the database.
    try: 
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object

    # If connection unsuccessful, raise exception (and query is never attempted).
    except Exception as e:
            raise DbConnectionError(f"Failed to connect to database {db_name}.")

    # If connection established, try SQL query to get booking availability for a specific date
    try:
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
    except Exception as e:
        raise DbQueryError(f"Query to database {db_name} failed. Make sure table and columns exist!") from e

    # If connection is establised, always closes the connection.
    finally:
        db_connection.close()  # Close the database connection
        print("DB connection is closed")  # Print a message indicating the connection is closed

    return availability  # Return the availability information in nice format

def get_nailTech_availability(nailTech, date):
    """
    This function retrieves the booking availability for a specific nail technician from the database.
    It connects to the database, executes a query to fetch the nail tech data, maps the results
    into a user-friendly format, handles any exceptions that occur during the process, and
    ensures the database connection is closed properly.

    Parameters:
    _date (str): The nail tech for which to retrieve booking availability.

    Returns:
    availability (list): A list of dictionaries representing the booking availability of that nail tech.

    Raises:
    DbConnectionError: If the function fails to connect to the database.
    DbQueryError: If the function connects to the database but fails to retrieve availability.
    """

    availability = []  # Initialize empty list to store the availability information
    db_name = 'nails'  # The name of the database to connect to

    # First, try to esetablish a connection to the database.
    try: 
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object
    
    # If connection isn't established, this exception will be raised (and query won't be attempted)
    except Exception as e:  # Catch any exceptions that occur
        # Raise a custom exception if an error occurs while trying to connect to data base
        raise DbConnectionError(f"Failed to connect to database {db_name}") from e
    
    try:
        # If connection established, try SQL query to get booking availability for a specific nail tech
            query = """
                SELECT  nailTech, `12-13`, `13-14`, `14-15`, `15-16`, `16-17`, `17-18`, `bookingDate`
                FROM nail_bookings 
                WHERE nailTech = '{}' AND bookingDate > '{}'
                LIMIT 7
                """.format(nailTech, date)

            cur.execute(query)  # Execute the SQL query
            result = cur.fetchall()  # Fetch all results from the executed query, which returns a list of tuples
            availability = _map_values(result, nailTech)  # Map the raw results to a user-friendly format using helper function!
            cur.close()  # Close the cursor object

    # If query isn't successful, this exception will be raised.
    except Exception as e:  # Catch any exceptions that occur
        # Raise a custom exception if an error occurs
        raise DbQueryError(f"Query to database {db_name} failed. Make sure table and columns exist!") from e

    # If connection is establised, always closes the connection.
    finally:
        db_connection.close()  # Close the database connection
        print("DB connection is closed")  # Print a message indicating the connection is closed

    return availability  # Return the availability information in nice format.

def add_booking(_date, nailTech, appointmentType, time, client, contact):
    """
    Adds a new booking to the nail salon's database.

    Parameters:
    _date (str): The date of the booking in 'YYYY-MM-DD' format.
    nailTech (str): The name of the nail technician (e.g., bronte)
    appointmentType (str): The type of appointment (e.g., gel manicure, gel pedicure).
    time (str): The time slot for the appointment (e.g., '12-13', '13-14').
    client (str): The name of the client (e.g., sayo)
    contact (str): The contact information of the client (e.g., 07518222626)

    Raises:
    DbConnectionError: If the function fails to connect to the database.
    DbQueryError: If the function connects to the database but fails to add the booking.

    This function attempts to connect to the 'nails' database. If the connection is successful,
    it executes an SQL query to update the booking information for the specified date and nail
    technician. If the query is successful, the booking is added to the database. If any error
    occurs during the connection or query execution, appropriate exceptions are raised. Finally,
    the database connection is closed.
    """
    db_name = 'nails' # name of data base
    
    # Try to connect to database first.
    try:
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object
    
    # If connection isn't established, this exception will be raised (and query won't be attempted)
    except Exception as e:  # Catch any exceptions that occur
        # Raise a custom exception if an error occurs while trying to connect to data base
        raise DbConnectionError(f"Failed to connect to database {db_name}") from e
        
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
        raise DbQueryError(f"Appointment booking unsuccessful: Connected to DB {db_name}, but failed to update with new booking.") from e

    # If the connection was established, close the DB.
    finally:
        db_connection.close()
        print(f"DB {db_name} connection is now closed.")
    
def delete_booking(_date, time, contact):
    """
    Deletes a booking from the nail salon's database.

    Parameters:
    _date (str): The date of the booking in 'YYYY-MM-DD' format.
    time (str): The time slot for the booking (e.g., '12-13', '13-14').
    contact (str): The contact information of the client.

    Raises:
    DbConnectionError: If the function fails to connect to the database.
    DbQueryError: If the function connects to the database but fails to delete the booking.

    This function attempts to connect to the 'nails' database. If the connection is successful,
    it executes an SQL query to delete the booking information for the specified date, time slot,
    and contact information. If the query is successful, the booking is removed from the database.
    If any error occurs during the connection or query execution, appropriate exceptions are raised.
    Finally, the database connection is closed.
    """
    db_name = 'nails'
    # Try to connect to database first.
    try:
        db_connection, cur = _connection_and_cur_(db_name) # Connect to database and create cursor object

    # If connection unsuccessful, raise exception (and query is never attempted).
    except Exception as e:
            raise DbConnectionError(f"Booking not deleted. Failed to connect to DB {db_name}.") from e
    
    # If connection sucessful, proceed to delete booking via SQL query.
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

        # If rows changed is equal to zero, raise exception.
        if cur.rowcount == 0:
            raise DbQueryError("There are no bookings matching those details. Please check that the date, time, and your number are correct.")
    
    except Exception as e:
        raise DbQueryError(f"Appointment cancellation unsuccessful: Connected to DB {db_name}, but failed to cancel booking.") from e

    # If the connection was established, close the DB.
    finally:
        db_connection.close()
        print(f"DB {db_name} connection is now closed.")


# If the script is run directly, execute the following code (for testing)
if __name__ == '__main__':
    pass
    # Call the function with a specific date for testing purposes
    # now = datetime.now()
    # now_date = now.date()
    # print (get_nailTech_availability(now_date, 'bronte'))
    # print(get_all_booking_availability('2024-06-30'))
    # add_booking('2024-06-30', 'bronte','gel manicure', '15-16', 'Sayo', '07876347982')
    # delete_booking('2024-06-30', '15-16', '07876347982')