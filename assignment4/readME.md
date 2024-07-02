# Introduction
In this assignment, I have built a program that allows a client to interact with an API that makes queries to the 'nails' database to book and cancel nail appointments with different nail technicians.

## Instructions for using API
These are the instructions for how to use the API yourself!

### Create SQL database

1. Open MYSQL database and connect.
2. Open the 'create_db.sql' file.
3. Run lines 1-52 to create 'nails' database and populate 'nail_bookings' table with availability of 3 nail technicians for the next three months.
4. Run line 55 to get your SQL host name and user name for editing your config file in the next step. e.g., mine returns 'root@localhost', which means by user name is 'root' and my host is 'localhost'.

### Edit config file
1. Open your IDE (e.g., visual studio code or pycharm).
2. Open 'config.py' file.
3. Edit line 2 and 3 with your SQL host name and user name (see above).
3. Add your own MYSQL password to line 3.

### Install libraries in requirements.txt
1. Open requirements.txt.
2. In your IDE terminal, you can run 'pip install -r requirements.txt' to install necessary libraries.

### Create API
1. In your open IDE, open 'app.py'.
2. As a mac user, I have set port to '8000' on line 186, but you can change to '5001' if you prefer.
3. Run whole file to get API up and running.

### API client-side
1. Once the API is running, in your open IDE, open and run 'main.py'. This will present you with the following options:
    To book or cancel an appointment.
        If you want to cancel, it will ask for booking date, nail tech, and your contact number (and at each step, will make sure you provide valid input).
            - If the booking exists, it will confirm the booking has been deleted.
            - If the booking doesn't exist, it will tell you that your attempt has been unsuccessful.

        If you want to book, it will ask whether you want to see availability by date or by nail tech.
            - If you select by nail tech, it will ask you which one and show your their availability for the next 7 days.
            - If you select by date, it will show you availability for all nail techs for that date (as long as it's not in the past!)
                - If no slots are available for your chosen date, it will tell you and ask you to contact salon directly.

            - It will then ask you if you are ready to book an appointment.
            - If you select yes, it will ask you for the details (and validate each choice).
                - It will not allow you to make an appointment if the slot is not available!
                
            - If the booking is successful, it will print a confirmation as well as the details of the booking. Otherwise, it will tell you there has been a problem (and specify if it's a connection issue or a query issue with different messages.)

            - If you don't want to book, the program will end and you will see availability of selected nail stylist for the next two days OR the next 2 days available from the date selected.

        All the way through, it will make sure you are entering valid inputs (dates, nail stylists, time slots, contact number etc.) to reduce likelihood of errors.

        At any point, you can enter ctrl+c to exit program.