from flask import Flask, jsonify, request
from db_utils import get_all_booking_availability, get_nailTech_availability, add_booking, delete_booking, DbConnectionError, DbQueryError

# Create flask instance (i.e., API) and save to app variable
app = Flask(__name__)

# First thing is to create first end point to create landing page
@app.route('/') # this creates the URL
def get_landingpage():
    return "Landing page for nail salon API."

# Uses method 'GET' to get availability based on date provided
@app.route('/date_availability/<date>')
def get_bookings(date):
    try:
        # use function from db_utils to get booking availability for that date
        res = get_all_booking_availability(date) 
        return jsonify(res)
    # use imported DbConnectionError class to raise error
    # NOTE: asked Chat GPT for help with this to help propogate errors from db_utils (see main_utils for more info)
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
    try:
        # use function from db_utils to get availability of nail tech
        res = get_nailTech_availability(nailTech, date)
        return jsonify(res)
    
    # use imported DbConnectionError class to raise error
    # NOTE: asked Chat GPT for help with this to help propogate errors from db_utils (see main_utils for more info)
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
        return jsonify(booking)
    
    # use imported DbConnectionError class to raise error
    # NOTE: asked Chat GPT for help with this to help propogate errors from db_utils (see main_utils for more info)
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
