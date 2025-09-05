class Acommodation:
    def __init__(self,name,type,price,rating,location): #add date instead of availability
        self.name = name
        self.type = type
        self.price = price
        self.rating = rating
        self.location = location

    def get_price(self):
        return self.price
    
    def get_rating(self):
        return self.rating
    
    def __repr__(self):
        return f"Accommodation({self.name},{self.type},{self.price},{self.rating},{self.location})"