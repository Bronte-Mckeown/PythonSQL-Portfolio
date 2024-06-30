from flask import Flask, jsonify, request
from db_utils import get_all_booking_availability, add_booking

# Create flask instance (i.e., API) and save to app variable
app = Flask(__name__)

# First thing is to create first end point to create landing page
@app.route('/') # this creates the URL
def get_landingpage():
    return "Welcome to Our Nail Salon. Please go to our availability page to see available appointments."

@app.route('/availability/<date>')
def get_bookings(date):
    # use function from db_utils to get booking availability
    res = get_all_booking_availability(date) 
    return jsonify(res)

@app.route('/booking', methods=['PUT'])
def book_appt():
    booking = request.get_json()
    add_booking(
        _date=booking['_date'],
        nailTech=booking['nailTech'],
        appointmentType=booking['appointmentType'],
        time=booking['time'],
        customer=booking['customer']
    )
    return jsonify(booking)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
