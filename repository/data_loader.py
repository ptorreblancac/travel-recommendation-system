import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.destination import Destination
from models.flight import Flight
from models.accomodation import Acommodation
from . import database as db

db.create_tables()

# Get root directory and data directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
data_folder_path = os.path.join(BASE_DIR,"data")

all_destinations = []
all_flights = []
all_accommodations = []

def print_destinations():
    print(*all_destinations,sep='\n')

def print_flights():
    print(*all_flights,sep="\n")

def print_accommodations():
    print(*all_accommodations,sep="\n")

# Load into Destination objects
def load_destinations():
    destination_list = []
    with open(os.path.join(data_folder_path,"destination.json"),'r') as f:
        data = json.load(f)
        for destination in data:
            dest_obj = Destination(**destination)
            destination_list.append(dest_obj)
            db.add_destination(dest_obj)

    return destination_list

# Load into Flight objects
def load_flights():
    flight_list = []
    with open(os.path.join(data_folder_path,"flight.json"),'r') as f:
        data = json.load(f)
        for flight in data:
            flight_obj = Flight(**flight)
            flight_list.append(flight_obj)
            db.add_flight(flight_obj)
    return flight_list

# Load into Accommodation objects
def load_accommodations():
    accommodation_list = []
    with open(os.path.join(data_folder_path,"accommodation.json"),'r') as f:
        data = json.load(f)
        for accommodation in data:
            acc_obj = Acommodation(**accommodation)
            accommodation_list.append(acc_obj)
            db.add_accommodation(acc_obj)
    return accommodation_list

all_destinations = load_destinations()
all_flights = load_flights()
all_accommodations = load_accommodations()

if __name__ == "__main__":
    print_destinations()
    print_flights()
    print_accommodations()

