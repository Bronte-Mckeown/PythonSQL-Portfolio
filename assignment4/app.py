from flask import Flask, jsonify, request
from db_utils import get_all_booking_availability, get_nailTech_availability, add_booking, delete_booking, DbConnectionError, DbQueryError

# NOTE: I used Chat GPT to generate doc strings for finished functions, which I then edited as required.

# Create flask instance (i.e., API) and save to app variable
app = Flask(__name__)

# First thing is to create first end point to create landing page
@app.route('/') # this creates the URL
def get_landingpage():
    return "Landing page for nail salon API."

# Uses method 'GET' to get availability based on date provided
@app.route('/date_availability/<date>')
def get_bookings(date):
    """
    Fetches booking availability for a given date and returns it as a JSON response.
    
    This function uses the `get_all_booking_availability` function from the `db_utils` 
    module to retrieve booking availability for the specified date.

    Args:
        date (str): The date for which booking availability is requested, formatted as 'YYYY-MM-DD'.

    Returns:
        Response: A Flask `jsonify` response containing booking availability data if successful,
                  or an error message with an appropriate HTTP status code if an exception occurs.
    
    Raises:
        DbConnectionError: If there is an error connecting to the database.
        DbQueryError: If there is an error querying the database.
    """
    try:
        # use function from db_utils to get booking availability for that date
        res = get_all_booking_availability(date) 
        return jsonify(res)
    # use imported DbConnectionError class to raise error
    # NOTE: asked Chat GPT for help with this to help propogate errors from db_utils (see main_utils.py for more info)
    except DbConnectionError as e:
        # prints error message from add_booking() function
        return jsonify({"error": str(e)}), 500 # server error code
    
    # use imported DbQueryError class to raise error
    except DbQueryError as e:
        # prints error message from add_booking() function
        return jsonify({"error": str(e)}), 400 # bad request code
    

# Uses method 'GET' to get availability based on nail tech name
@app.route('/tech_availability/<nailTech>/<date>')
def get_nailTech_bookings(nailTech, date):
    """
    Fetches booking availability for a specified nail technician on a given date (should be today's date)
    and returns it as a JSON response.
    
    This function uses the `get_nailTech_availability` function from the `db_utils` 
    module to retrieve the availability of the specified nail technician for the given date.

    Args:
        nailTech (str): The name of the nail technician.
        date (str): The date for which the nail technician's availability is requested, formatted as 'YYYY-MM-DD'.

    Returns:
        Response: A Flask `jsonify` response containing the nail technician's availability data if successful,
                  or an error message with an appropriate HTTP status code if an exception occurs.
    
    Raises:
    DbConnectionError: If there is an error connecting to the database.
    DbQueryError: If there is an error querying the database.
    """
    try:
        # use function from db_utils to get availability of nail tech
        res = get_nailTech_availability(nailTech, date)
        return jsonify(res)
    
    # use imported DbConnectionError class to raise error
    # NOTE: asked Chat GPT for help with this to help propogate errors from db_utils (see main_utils.py for more info)
    except DbConnectionError as e:
        # prints error message from add_booking() function
        return jsonify({"error": str(e)}), 500 # server error code
    
    # use imported DbQueryError class to raise error
    except DbQueryError as e:
        # prints error message from add_booking() function
        return jsonify({"error": str(e)}), 400 # bad request code

# Used method 'PUT' to add new booking
@app.route('/booking', methods=['PUT'])
def book_appt():
    """
    Books a new appointment and returns a confirmation message as a JSON response.
    
    This function reads booking details from a JSON request, and uses the `add_booking` 
    function from the `db_utils` module to add the new booking to the database. It handles 
    exceptions related to database connection and query errors, and returns appropriate 
    error messages and HTTP status codes.

    The booking details include:
        - _date: The date of the booking (formatted as 'YYYY-MM-DD').
        - nailTech: The name of the nail technician.
        - appointmentType: The type of appointment.
        - time: The time slot for the appointment.
        - client: The name of the client.
        - contact: The contact number of the client.

    Returns:
        Response: A Flask `jsonify` response containing a success message if the booking 
                  is made successfully, or an error message with an appropriate HTTP status 
                  code if an exception occurs.
    
    Raises:
        DbConnectionError: If there is an error connecting to the database.
        DbQueryError: If there is an error querying the database.
    """
    booking = request.get_json()

    try:

        # use function from db_utils to add new booking
        add_booking(
            _date=booking['_date'], # date of booking
            nailTech=booking['nailTech'], # name of nail tech
            appointmentType=booking['appointmentType'], # appointment type
            time=booking['time'], # time slot
            client=booking['client'], # client's name
            contact=booking['contact'] # contact number of client
        )
        return jsonify({"message": "Booking made successfully."}), 200 # success code
    
    # use imported DbConnectionError class to raise error
    # NOTE: asked Chat GPT for help with this to help propogate errors from db_utils (see main_utils.py for more info)
    except DbConnectionError as e:
        # prints error message from add_booking() function
        return jsonify({"error": str(e)}), 500 # server error code
    
    # use imported DbQueryError class to raise error
    except DbQueryError as e:
        # prints error message from add_booking() function
        return jsonify({"error": str(e)}), 400 # bad request code
    
# Used method 'PUT' to delete booking
@app.route('/delete', methods=['PUT'])
def delete_appt():
    """
    Deletes an existing appointment and returns a confirmation message as a JSON response.
    
    This function reads booking details from a JSON request, and uses the `delete_booking` 
    method from the `db_utils` module to remove the booking from the database. It handles 
    exceptions related to database connection and query errors, and returns appropriate 
    error messages and HTTP status codes.

    The booking details required for deletion include:
        - _date: The date of the booking (formatted as 'YYYY-MM-DD').
        - time: The time slot of the appointment.
        - contact: The contact number of the client.

    Returns:
        Response: A Flask `jsonify` response containing a success message if the deletion 
                  is successful, or an error message with an appropriate HTTP status code 
                  if an exception occurs.
    
    Raises:
        DbConnectionError: If there is an error connecting to the database.
        DbQueryError: If there is an error querying the database.
    """
    booking = request.get_json()

    try:
        delete_booking(
            _date=booking['_date'],
            time=booking['time'],
            contact=booking['contact']
        )
        return jsonify({"message": "Booking deleted successfully."}), 200 # success code

    except DbConnectionError as e:
        # prints error message from delete_booking()
        return jsonify({"error": str(e)}), 500 # server error code
    
    except DbQueryError as e:
        # prints error message from delete_booking()
        return jsonify({"error": str(e)}), 400 # bad request code

if __name__ == '__main__':
    app.run(debug=True, port=8000)
