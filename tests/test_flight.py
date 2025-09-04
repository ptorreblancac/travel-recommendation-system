import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models.flight import Flight

def test_flight():
    f1 = Flight("ABC","RyanAir","09/06/2025","1h","bcn","berlin",50)

    print(f1.company)
    print(f1.get_price())
    print(f1.get_duration())

if __name__ == "__main__":
    test_flight()
    