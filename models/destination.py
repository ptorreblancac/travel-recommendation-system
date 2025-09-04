class Destination:
    def __init__(self,name,temperature,country):
        self.name = name
        self.temperature = temperature
        self.country = country

    def get_temperature(self):
        return self.temperature
    
    def __repr__(self):
        return f"Destination({self.name}, {self.temperature}, {self.country})"