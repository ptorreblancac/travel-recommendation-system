from repository import database as db
import menu_actions as act
import atexit

def option1(): act.select_new_destination(user)
def option2(): act.book_flight(user)
def option3(): act.book_accommodation(user)
def option4(): act.select_budget(user)
def option5(): user.get_preferences()
def option6(): user.get_flights()
def option7(): db.get_accommodations(user)
def option8(): print(user.budget)

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

user = act.initialize()
atexit.register(db.update_budget,user) # Ensures budget persistence

while True:
    act.print_options()
    try:
        request = int(input("Select an option: "))
    except ValueError:
        print("Invalid input, please try again!\n")
        continue

    action = options.get(request)
    if action:
        action()
    else:
        print("Please enter a valid request index\n")

        

   