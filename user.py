class User:
    def __init__(self,name,email,budget):
        self.name = name
        self.email = email
        self.budget = budget
        self.booked_flights = [] # list to store Flight objects
        self.preferred_destinations = {} # dictionary of countries as keys and list to store Destination objects

    def book_flight(self,flight):
        flight_price = flight.get_price()
        if flight_price <= self.budget:
            self.booked_flights.append(flight)
            self.budget -= flight_price
            print(f"{self.name} booked flight {flight.code} to {flight.destination} successfully!\n")
            print(f"The remaining budget is {self.budget}\n")
            return True
        else:
            print(f"{self.name} cannot currently book flight {flight.code}\n")
            return False
             
    def book_accommodation(self,accommodation):
        accommodation_price = accommodation.get_price()
        if accommodation_price <= self.budget:
            self.budget -= accommodation_price
            print(f"{self.name} has booked the accommodation {accommodation.name} successfully!")
            print(f"The remaining budget is {self.budget}\n")
            return True
        
        else:
            print(f"{self.name} cannot currently book {accommodation.name}\n")
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

    def set_budget(self,new_budget):
        self.budget = new_budget
        print(f"The budget has been updated successfully to {self.budget}!\n")
        return True
    
    def get_preferences(self):
        try:
            print("List of destinations:")
            for country,destinations in self.preferred_destinations.items():
                for destination in destinations:
                    print(f"{destination.name}, {country}")
        except AttributeError:
            print("-\n")
    
    def get_flights(self):
        if len(self.booked_flights) == 0:
            print(f"The user {self.name} currently has no booked flights\n")
        else:
            for row in self.booked_flights:
                print(f"Flight Code: {row.code}, Company: {row.company}, Date: {row.date}, Duration: {row.duration}h")
                print(f"From: {row.origin} To: {row.destination}, Price: {row.price}€, Max capacity: {row.max_capacity}")
                print("-" * 40)            

    def get_accommodations(self):
        if len(self.booked_accommodations) == 0:
            print(f"The user {self.name} currently has no booked accommodations\n")
        else:
            for row in self.booked_accommodations:
                print(f"Accommodation Name: {row.name}, Accommodation Type: {row.type}, Price: {row.price}€")
                print(f"Rating: {row.rating}, Location: {row.location}")
                print("-" * 40)


 


