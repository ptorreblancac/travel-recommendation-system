class Flight:
    def __init__(self,code,company,date,duration,origin,destination,price,available=True):
        self.code = code
        self.company = company
        self.date = date 
        self.duration = duration
        self.origin = origin
        self.destination = destination
        self.price = price
        self.available = available
    
    def get_duration(self):
        return self.duration

    def get_price(self):
        return self.price
    
    def is_available(self):
        return self.available
    
    def __repr__(self):
        return f"Flight({self.code,self.company,self.date,self.duration,self.origin,self.destination,self.price,self.available})"