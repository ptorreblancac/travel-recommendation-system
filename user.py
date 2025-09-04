class User:
    def __init__(self,name,email,budget):
        self.name = name
        self.email = email
        self.budget = budget
        self.travel_dates = None # tuple of a start date and end date
        self.booked_flights = [] # list to store Flight objects
        self.preferred_destinations = {} # dictionary of countries as keys and list to store Destination objects
        self.booked_accommodations = [] # list to store Acommodation objects

    def book_flight(self,flight):
        flight_price = flight.get_price()
        if flight_price <= self.budget and flight.is_available():
            self.booked_flights.append(flight)
            self.budget -= flight_price
            print(f"{self.name} booked flight {flight.code} to {flight.destination} successfully!\n")
            return True
        else:
            print(f"{self.name} cannot currently book flight {flight.code}\n")
            return False
            
    def add_preference(self,destination):
        country = destination.country
        if country not in self.preferred_destinations:
            self.preferred_destinations[country] = []
        
        if destination not in self.preferred_destinations[country]:
            self.preferred_destinations[country].append(destination)
            print(f"The destination {destination.name} has been added into your preferences.\n")
            return True
        else:
            print(f"The destination {destination.name} was already on your list.\n")
            return False
    
    def book_accommodation(self,accommodation):
        accommodation_price = accommodation.get_price()
        if accommodation_price <= self.budget and accommodation.is_available():
            self.booked_accommodations.append(accommodation)
            self.budget -= accommodation_price
            print(f"{self.name} has booked the accommodation {accommodation.name} successfully!")
            print(f"The remaining budget is {self.budget}\n")
            return True
        
        else:
            print(f"{self.name} cannot currently book {accommodation.name}\n")
            return False
            
    def set_budget(self,new_budget):
        self.budget = new_budget
        print(f"The budget has been updated successfully to {self.budget}!\n")
        return True
    
    def get_preferences(self):
        print("List of destinations:")
        for country,destinations in self.preferred_destinations.items():
            for destination in destinations:
                print(f"{destination.name}, {country}")
        return True
        
    def select_dates(self,start_date,end_date):
        if start_date < end_date:
            self.travel_dates = (start_date,end_date)
            print(f"Travel dates have been set from {start_date} to {end_date}\n")
            return True
        else:
            print(f"Invalid dates, please try again.\n")
            return False

    def show_booked_flights(self):
        for flight in self.booked_flights:
            print(f"Origin: {flight.origin}, Destination: {flight.destination}, Duration: {int(flight.duration)}")
    
    def show_booked_accommodations(self):
        for acc in self.booked_accommodations:
            print(f"Name: {acc.name}, Type: {acc.type}, Location: {acc.location}")



