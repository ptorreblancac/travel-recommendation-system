from repository.data_loader import all_destinations, all_flights, all_accommodations
from user import User
from datetime import datetime
from repository import database as db

def print_objects():
    print(*all_destinations,sep='\n')
    print(*all_flights,sep='\n')
    print(*all_accommodations,sep='\n')

# Transforms date string into datetime format
def transform_date_format(date):
    # Transform dates into datetime
    formats = ["%d-%m-%Y","%d-%m-%y","%d %B %Y","%d/%m/%Y","%d/%m/%y"]
    while True:
        for fmt in formats:
            try:    
                return datetime.strptime(date,fmt).date()
            except ValueError:
                continue
        date = input("Please enter a valid date: ")

# Allows the user to add a new destination into the list of interests
def select_new_destination(user):
    preference = input("Insert the destination you'd like to visit: ")
    for destination in all_destinations:
        if destination.name.lower() == preference.lower():
            user.add_preference(destination)
            db.add_destination_booking(user,destination)
            print(f"{preference} has been added to your list!")
            return True
    print(f"{preference} cannot be added right now.")

# Allows the user to book a flight
def book_flight(user,city_dest, city_org):
    options = []
    for flight in all_flights:
        if city_dest.lower() == flight.destination.lower() and city_org.lower() == flight.origin.lower():
            options.append(flight)
        
    if len(options) != 0:
        for index,option in enumerate(options):
            print(index+1,option.code,option.company,option.date)
    
        index_chosen = int(input("Choose the number of the flight you would like to book: "))
        user.book_flight(options[index_chosen-1])
        db.add_flight_booking(user,options[index_chosen-1],datetime.now().date())
    else:
        print(f"Sorry, there are no flights available for {city}\n")

# Allows the user to book an accommodation
def book_accommodation(user,accommodation_location):
    start_date = input("Enter starting date of reservation: \n")
    start_date = transform_date_format(start_date)
    end_date = input("Enter end of reservation: \n")
    end_date = transform_date_format(end_date)

    options = []
    for accommodation in all_accommodations:
        if accommodation_location.lower() == accommodation.location.lower():
            available = db.accommodation_is_available(accommodation,start_date,end_date)
            if available:
                options.append(accommodation)
    
    if len(options) != 0:
        for index, option in enumerate(options):
            print(index+1,option.name,option.type,option.price,option.rating)
        
        index_chosen = int(input("Choose the number of the accommodation you would like to book: "))
        user.book_accommodation(options[index_chosen-1])
        db.add_accommodation_booking(user,options[index_chosen-1],start_date,end_date,datetime.now().date())
    else:
        print(f"There are no available accommodations ")

# Allows the user to select new dates
def select_dates(user):
    start_date = input("Insert start date: \n")
    start = transform_date_format(start_date)
    end_date = input("Insert end date: \n")
    end = transform_date_format(end_date)

    user.select_dates(start,end)
    return True


def create_user(user_name, user_email):
    budget = int(input("Please select your desired budget: "))
    user = User(name=user_name,email=user_email,budget=budget)
    db.add_user(user)

def initialize_user():
    user_name = input("Please enter your name: ")
    user_email = input("Please enter your email: ")

    user_budget = db.user_found(user_name,user_email)
    if user_budget is None: # The user was not in the db
        create_user(user_name,user_email)
    else: 
        print(f"Welcome back {user_name}!\n")

    user = User(name=user_name,email=user_email,budget=user_budget)
    return user

user = initialize_user()

db.create_tables()

while True:
    print("Select the action you want to take:")
    print("1. Add a new destination into your list.")
    print("2. Book a new flight.")
    print("3. Book a new accommodation.")
    print("4. Set new budget.")
    print("5. Select new dates.")
    print("6. Show all liked destinations.")
    print("7. Show current flight bookings: ")
    print("8. Show current accommodation bookings: ")

    try:
        request = int(input())
    except ValueError:
        print("Invalid input, please try again!\n")

    if request == 1:
        select_new_destination(user1)

    elif request == 2:
        city_org = input("What city are you travelling from: ")
        city_dest = input("Which destination would you like to book a flight for: ")
        book_flight(user1,city_dest,city_org)

    elif request == 3:
        city = input("Which destination would you like to book an accommodation for: ")
        book_accommodation(user1,city)
    
    elif request == 4:
        new_budget = int(input("Insert the new budget you would like: "))
        user1.set_budget(new_budget)
    
    elif request == 5:
        select_dates(user1)
    
    elif request == 6:
        user1.get_preferences()
    
    elif request == 7:
        db.show_booked_flights(user1)

    elif request == 8:
        db.show_booked_accommodations(user1)

    else:
        print("Please enter a valid request index\n")

