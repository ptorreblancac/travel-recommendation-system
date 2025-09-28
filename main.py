from repository import database as db
import menu_actions as act
import atexit

def option1(user): act.select_new_destination(user)
def option2(user): act.book_flight(user)
def option3(user): act.book_accommodation(user)
def option4(user): act.select_budget(user)
def option5(user): db.get_preferences(user)
def option6(user): db.get_flights(user)
def option7(user): db.get_accommodations(user)
def option8(user): print(user.budget)

options = {
    1: option1,
    2: option2,
    3: option3,
    4: option4,
    5: option5,
    6: option6,
    7: option7,
    8: option8,
}

def main():
    user = act.initialize()
    atexit.register(db.set_new_budget,user,user.budget) # Ensures budget persistence

    while True:
        act.print_options()
        try:
            request = int(input("Select an option: "))
        except ValueError:
            print("Invalid input, please try again!\n")
            continue

        action = options.get(request)
        if action:
            action(user)
        else:
            print("Please enter a valid request index\n")

        
if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print("Program terminated by user. Exiting...")

   