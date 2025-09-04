from repository.data_loader import all_destinations, all_flights, all_accommodations
from user import User
from datetime import datetime
from repository import database as db

def print_objects():
    print(*all_destinations,sep='\n')
    print(*all_flights,sep='\n')
    print(*all_accommodations,sep='\n')

# Allows the user to add a new destination into the list of interests
def select_new_destination(user):
    preference = input("Insert the destination you'd like to visit: ")
    for destination in all_destinations:
        if destination.name.lower() == preference.lower():
            user.add_preference(destination)
            db.add_destination_booking(destination)
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
        db.add_flight_booking(options[index_chosen-1])
    else:
        print(f"Sorry, there are no flights available for {city}\n")

# Allows the user to book an accommodation
def book_accommodation(user,accommodation_location):
    options = []
    for accommodation in all_accommodations:
        if accommodation_location.lower() == accommodation.location.lower():
            options.append(accommodation)
    
    if len(options) != 0:
        for index, option in enumerate(options):
            print(index+1,option.name,option.type,option.price,option.rating)
        
        index_chosen = int(input("Choose the number of the accommodation you would like to book: "))
        user.book_accommodation(options[index_chosen-1])
        db.add_accommodation_booking(options[index_chosen-1])
    else:
        print(f"There are no available accommodations ")

# Checks correct format of the dates
def check_date(date):
    # Transform dates into datetime
    formats = ["%d-%m-%Y","%d-%m-%y","%d %B %Y","%d/%m/%Y","%d/%m/%y"]
    for fmt in formats:
        try:    
            date = datetime.strptime(date,fmt).date()
            return True
        except ValueError:
            continue
    return False

# Allows the user to select new dates
def select_dates(user):
    correct_date = False
    while not correct_date:
        start_date = input("Insert start date: ")
        correct_date = check_date(start_date)
        if not correct_date:
            print("Please enter a valid date.")
    correct_date = False

    while not correct_date:
        end_date = input("Insert end date: ")
        correct_date = check_date(end_date)
        if not correct_date:
            print("Please enter a valid date.")

    user.select_dates(start_date,end_date)
    return True

user1 = User("Paula","torreblancapaula@gmail.com",200)

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
        user1.show_booked_flights()

    elif request == 8:
        user1.show_booked_accommodations()

    else:
        print("Please enter a valid request index\n")

