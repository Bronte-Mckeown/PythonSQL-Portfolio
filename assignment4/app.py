from flask import Flask, jsonify, request
from db_utils import get_all_booking_availability, get_nailTech_availability, add_booking, delete_booking

# Create flask instance (i.e., API) and save to app variable
app = Flask(__name__)

# First thing is to create first end point to create landing page
@app.route('/') # this creates the URL
def get_landingpage():
    return "Landing page for nail salon API."

# Uses method 'GET' to get availability based on date
@app.route('/date_availability/<date>')
def get_bookings(date):
    # use function from db_utils to get booking availability
    res = get_all_booking_availability(date) 
    return jsonify(res)

# Uses method 'GET' to get availability based on nail tech name
@app.route('/tech_availability/<nailTech>')
def get_nailTech_bookings(nailTech):
    # use function from db_utils to get availability of nail tech
    res = get_nailTech_availability(nailTech)
    return jsonify(res)

# Used method 'PUT' to add booking
@app.route('/booking', methods=['PUT'])
def book_appt():
    booking = request.get_json()
    add_booking(
        _date=booking['_date'],
        nailTech=booking['nailTech'],
        appointmentType=booking['appointmentType'],
        time=booking['time'],
        client=booking['client'],
        contact=booking['contact']
    )
    return jsonify(booking)

# Used method 'PUT' to delete booking
@app.route('/delete', methods=['PUT'])
def delete_appt():
    booking = request.get_json()
    delete_booking(
        _date=booking['_date'],
        time=booking['time'],
        contact=booking['contact']
    )
    return jsonify(booking)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
