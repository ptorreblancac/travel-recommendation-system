import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.destination import Destination
from models.flight import Flight
from models.accomodation import Acommodation

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
    with open(os.path.join(data_folder_path,"destination.json"),'r') as f:
        data = json.load(f)
        return [Destination(**destination) for destination in data]

# Load into Flight objects
def load_flights():
    with open(os.path.join(data_folder_path,"flight.json"),'r') as f:
        data = json.load(f)
        return [Flight(**flight) for flight in data]

# Load into Accommodation objects
def load_accommodations():
    with open(os.path.join(data_folder_path,"accommodation.json"),'r') as f:
        data = json.load(f)
        return [Acommodation(**accommodation) for accommodation in data]

all_destinations = load_destinations()
all_flights = load_flights()
all_accommodations = load_accommodations()

if __name__ == "__main__":
    print_destinations()
    print_flights()
    print_accommodations()

