import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.destination import Destination

def test_destination():
    d1 = Destination("Barcelona",21,"Spain")

    print(d1.country)
    print(d1.get_temperature())

if __name__ == "__main__":
    test_destination()