import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.destination import Destination
from models.flight import Flight
from models.accomodation import Acommodation
from . import database as db

# Get root directory and data directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
data_folder_path = os.path.join(BASE_DIR,"data")


# Load into Destination objects
def load_destinations():
    try:
        with open(os.path.join(data_folder_path,"destination.json"),'r') as f:
            data = json.load(f)
            for destination in data:
                dest_obj = Destination(**destination)
                db.add_destination(dest_obj)
    except FileNotFoundError:
        print("System down.")

# Load into Flight objects
def load_flights():
    try:
        with open(os.path.join(data_folder_path,"flight.json"),'r') as f:
            data = json.load(f)
            for flight in data:
                flight_obj = Flight(**flight)
                db.add_flight(flight_obj)
    except FileNotFoundError:
        print("System down.")

# Load into Accommodation objects
def load_accommodations():
    try:
        with open(os.path.join(data_folder_path,"accommodation.json"),'r') as f:
            data = json.load(f)
            for accommodation in data:
                acc_obj = Acommodation(**accommodation)
                db.add_accommodation(acc_obj)
    except FileNotFoundError:
        print("System down.")

def load_all():
    load_accommodations()
    load_destinations()
    load_flights()

