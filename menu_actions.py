from repository import database as db
from datetime import datetime
from user import User
from repository import data_loader

# Map of all months
months = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

# Sort
def sort_by_time(options):
    return sorted(options, key=lambda f: f.duration)

def sort_by_price(options):
    return sorted(options, key=lambda f: f.price)

def sort_by_rank(options):
    return sorted(options, key=lambda f: f.rating, reverse=True)

def smart_sort(options,type):
    """Sorts taking in different parameters"""
    if type == "accommodation":
        for o in options:
            o.score = 2*o.rating - o.price/20
    else:
        for o in options:
            o.score = 100 - o.duration - o.price/20
    return sorted(options, key=lambda o: o.score,reverse=True) 

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

def dates_are_valid(start,end):
    """Checks that the start date is before the end date and that dates are later than current dates"""
    current_date = datetime.now().date()
    return start < end and current_date <= start and current_date <= end

def select_dates():
    """Select start and end dates for bookings"""
    while True:
        try:
            start_date = transform_date_format(input("Insert start date: \n"))
            end_date = transform_date_format(input("Insert end date: \n"))
            if dates_are_valid(start_date,end_date):
                return start_date,end_date
            else:
                print("Invalid dates. Please try again.\n")
                continue
        except ValueError:
            print("Please enter a valid date format\n")
            continue

# Manage budget
def select_budget(user):
    """Allows the user to set a budget"""
    new_budget = int(input("Insert the new budget you would like: "))
    user.set_budget(new_budget)
    db.set_new_budget(user,new_budget)

# Manage bookings & user preferences
def book_flight(user): # TO DO: sort by departure hours
    """Allows the user to book a new flight"""
    #User input
    city_org = input("What city are you travelling from: ")
    city_dest = input("Which destination would you like to book a flight for: ")

    all_flights = db.find_flight(city_dest,city_org,user.budget)

    print("(1)Select flexible dates.")
    print("(2)Select exact dates.")

    if int(input("Pick your date selection method: ")) == 1:
        month = months[(input("Choose the traveling month: ")).lower()]
        options = [f for f in all_flights if datetime.strptime(f.date, "%Y-%m-%d").month == month]
    else:
        date = transform_date_format(input("Enter date of flight: "))
        options = [f for f in all_flights if f.date == date]

    # Allow users to sort results
    sorting_selected = input("Sort results [Y/N]")
    if sorting_selected in ('y','Y'):
        print("1. Fastest option first.")
        print("2. Cheapest option first.")
        print("3. Best value for money.")

        sort_choice = int(input("Select option: "))
        if sort_choice == 1:
            options = sort_by_time(options)
        elif sort_choice == 2:
            options = sort_by_price(options)
        else:
            options = smart_sort(options,"flight")
        
    if len(options) != 0:
        print(f"Flights from {str.capitalize(city_org)} to {str.capitalize(city_dest)}:")
        for i,opt in enumerate(options):
            print(f"{i+1}. Code: {opt.code}, Company: {opt.company},")
            print(f"Duration: {opt.duration}, Price: {opt.price}, Date: {opt.date}")
            print("-" * 40)

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

    options = db.find_accommodation(city,start_date,end_date,user.budget)

    # Allow users to sort results
    sorting_selected = input("Sort results [Y/N]")
    if sorting_selected in ('y','Y'):
        print("1. Highest ranking option first.")
        print("2. Cheapest option first.")
        print("3. Best value for money.")

        sort_choice = int(input("Select option: "))
        if sort_choice == 1:
            options = sort_by_rank(options)
        elif sort_choice == 2:
            options = sort_by_price(options)
        else:
            options = smart_sort(options,"accommodation")
    
    if len(options) != 0:
        for i,opt in enumerate(options):
            print(f"{i+1}. Accommodation Name: {opt.name}, Type: {opt.type},")
            print(f"Price: {opt.price}, Rating: {opt.rating}, Location: {opt.location}")
            print("-" * 40)
        
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
    else:
        print(f"Welcome back {str.capitalize(user_name)}!\n")

    user_budget = db.user_budget(user_name,user_email)

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