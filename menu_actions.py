from repository import database as db
from datetime import datetime
from user import User
from repository import data_loader

# Dates
def transform_date_format(date):
    """Transforms date int datetime format"""
    formats = ["%d-%m-%Y","%d-%m-%y","%d %B %Y","%d/%m/%Y","%d/%m/%y"]
    while True:
        for fmt in formats:
            try:    
                return datetime.strptime(date,fmt).date()
            except ValueError:
                continue
        date = input("Please enter a valid date: ")

def dates_are_valid(start,end):
    """Checks that the start date is before the end date"""
    return start < end

def select_dates():
    """Select start and end dates for bookings"""
    while True:
        try:
            start_date = transform_date_format(input("Insert start date: \n"))
            end_date = transform_date_format(input("Insert end date: \n"))
            if dates_are_valid(start_date,end_date):
                return start_date,end_date
            else:
                print("The starting date cannot be later than the ending date. Please try again!\n")
        except ValueError:
            print("Please enter a valid date format\n")

# Manage budget
def select_budget(user):
    """Allows the user to set a budget"""
    new_budget = int(input("Insert the new budget you would like: "))
    user.set_budget(new_budget)
    db.set_new_budget(user,new_budget)

# Manage bookings & user preferences
def book_flight(user):
    """Allows the user to book a new flight"""
    city_org = input("What city are you travelling from: ")
    city_dest = input("Which destination would you like to book a flight for: ")
    date = transform_date_format(input("In which date are you travelling? "))

    options = db.find_flight(city_dest,city_org,date)
        
    if len(options) != 0:
        for i,opt in enumerate(options):
            print(i+1,list(vars(opt).values())[:3])
    
        try:
            select = int(input("Choose the number of the flight you would like to book: "))
            db.add_flight_booking(user,options[select-1],datetime.now().date())
            user.book_flight(options[select-1])
        except IndexError:
            print("Invalid selection.\n")
    else:
        print(f"Sorry, there are no flights available for {city_dest}\n")

def book_accommodation(user):
    """Allows the user to book a new accommodation"""
    city = input("Which destination would you like to book an accommodation for: ")
    start_date,end_date = select_dates()
    options = db.find_accommodation(city,start_date,end_date)
    
    if len(options) != 0:
        for i,opt in enumerate(options):
            print(i+1,list(vars(opt).values())[:3])
        
        try:
            select = int(input("Choose the number of the accommodation you would like to book: "))
            user.book_accommodation(options[select-1])
            db.add_accommodation_booking(user,options[select-1],start_date,end_date,datetime.now().date())
        except IndexError:
            print("Invalid selection.\n")
    else:
        print(f"There are no available accommodations ")

def select_new_destination(user):
    preference = input("Insert the destination you'd like to visit: ")
    destination = db.find_destination(preference)

    if destination is None: # Destination not in database
        print(f"Destination {preference} cannot be added right now\n")
    else:
        if db.destination_not_on_list(user,destination):
            db.add_liked_destination(user,destination)
            user.add_preference(destination)
        else:
            print(f"{preference} was already on {user.name}'s list\n")

# Manage loading of data at the beginning of the execution
def create_user(user_name, user_email):
    """Create and save in database a user with name, email and budget"""
    while True:
        try:
            budget = int(input("Please select your desired budget: "))
            if budget > 0:
                break
            else:
                print("The budget put has to be a positive number.\n")
        except ValueError:
            print("The budget has to be an integer.\n")

    user = User(name=user_name,email=user_email,budget=budget)
    db.add_user(user)

def load_user_data(user):
    """Load flights, accommodations and preferred destinations"""
    try:
        user.booked_flights = db.load_booked_flights(user)
        user.preferred_destinations = db.load_liked_destinations(user)
    except Exception as e:
        print("Error loading user data: ", e)

def initialize_user():
    """Initialize user"""
    while True:
        user_name = input("Please enter your name: ").strip()
        if user_name:
            break
        print("The username cannot be empty. Please try again.\n")

    while True:
        user_email = input("Please enter your email: ").strip()
        if '@' in user_email and '.' in user_email:
            break
        print("Please enter a valid email format")

    # Checks if user exists, create if not
    if not db.user_found(user_name,user_email):
        create_user(user_name,user_email)

    user_budget = db.user_budget(user_name,user_email)
    print(f"Welcome back {user_name}!\n")

    user = User(name=user_name,email=user_email,budget=user_budget)
    load_user_data(user)
    return user

def initialize():
    """Create database tables and load all flight & accommodation data"""
    db.create_tables()
    data_loader.load_all()
    user = initialize_user()
    return user

def print_options():
    print("Select the action you want to take:")
    print("1. Add a new destination into your list.")
    print("2. Book a new flight.")
    print("3. Book a new accommodation.")
    print("4. Set new budget.")
    print("5. Show all liked destinations.")
    print("6. Show current flight bookings: ")
    print("7. Show current accommodation bookings: ")
    print("8. Show current budget: ")