class Flight:
    def __init__(self,code,company,date,duration,origin,destination,price,max_capacity):
        self.code = code
        self.company = company
        self.date = date 
        self.duration = duration
        self.origin = origin
        self.destination = destination
        self.price = price
        self.max_capacity = max_capacity
    
    def get_duration(self):
        return self.duration

    def get_price(self):
        return self.price

    def __repr__(self):
        return f"Flight({self.code,self.company,self.date,self.duration,self.origin,self.destination,self.price,self.max_capacity})"