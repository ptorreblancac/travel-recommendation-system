import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.accomodation import Acommodation

def test_accomodation():
    ac1 = Acommodation("Gran Plaza","hotel",50,4.3,"bcn")

    print(ac1.type)
    print(ac1.get_price())
    print(ac1.get_rating())

if __name__ == "__main__":
    test_accomodation()

