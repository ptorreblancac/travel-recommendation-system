import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user import User
from models.flight import Flight
from models.accomodation import Acommodation
from models.destination import Destination

def test_user():
    u1 = User("Paula","torreblancapaula@gmail.com",100)
    f1 = Flight("ABC","RyanAir","09/06/2025","1h","bcn","berlin",50)
    ac1 = Acommodation("Gran Plaza","hotel",50,4.3,"bcn")
    d1 = Destination("Barcelona",21,"Spain")

    print(u1.name)
    u1.book_flight(f1)
    u1.book_accommodation(ac1)
    u1.add_preference(d1)
    u1.set_budget(150)
    u1.get_preferences()



if __name__ == "__main__":
    test_user()