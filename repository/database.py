import sqlite3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.destination import Destination
from models.flight import Flight
from models.accomodation import Acommodation
from datetime import datetime

# Create Tables 
def create_tables():
    """Creates databases for persistence"""
    # Open connection to info file
    conn = sqlite3.connect('info.db')
    c = conn.cursor()

    # Create Table for Flight info
    c.execute("""CREATE TABLE IF NOT EXISTS flights (
            code text UNIQUE,
            company text,
            date text,
            duration integer,
            origin text,
            destination text,
            price integer,
            max_capacity integer,
            current_capacity integer
        )""")
    
# Create Table for Accommodation info
    c.execute("""CREATE TABLE IF NOT EXISTS accommodations (
            name text UNIQUE,
            type text,
            price integer,
            rating integer,
            location text
        )""")

# Create Table for Destination info
    c.execute("""CREATE TABLE IF NOT EXISTS destinations (
            name text,
            temperature integer,
            country text 
        )""")
    
# Create Table for User info
    c.execute("""CREATE TABLE IF NOT EXISTS users (
            name text,
            email text UNIQUE,
            budget integer
        )""")
    
    conn.commit()
    conn.close()

    # Open connection to bookings file
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    # Create Table for flight bookings 
    c.execute("""CREATE TABLE IF NOT EXISTS booked_flights (
            user text,
            code text,
            company text,
            date text,
            duration integer,
            origin text,
            destination text,
            price integer,
            max_capacity integer,
            current_date text
        )""")

    # Create Table for accommodation bookings
    c.execute("""CREATE TABLE IF NOT EXISTS booked_accommodations (
            user text,
            name text,
            type text,
            price integer,
            rating integer,
            location text,
            ini_date text,
            fin_date text,
            booking_time text
        )""")

    # Create Table for destination bookings
    c.execute("""CREATE TABLE IF NOT EXISTS liked_destinations (
            user text,
            name text,
            temperature integer,
            country text,
            PRIMARY KEY(user,name)
        )""")
    
    # Commit and Close
    conn.commit()
    conn.close()


# Add new user, booking or preference
def add_user(user):
    """Adds a new user into the database"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?)",
            (user.name,user.email,user.budget))
    conn.commit()
    conn.close()

def add_flight_booking(user,flight,current_date):
    """Adds a new flight booking into the database"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    current_capacity = show_capacity(flight.code)
    booked = True

    if current_capacity < flight.max_capacity:
        c.execute("INSERT OR IGNORE INTO booked_flights VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (user.email,flight.code,flight.company,flight.date,flight.duration,
                    flight.origin,flight.destination,flight.price,flight.max_capacity,
                    current_date))

        booked = modify_flight_capacity(flight.code,current_capacity+1)

    conn.commit()
    conn.close()

    return booked 

def add_accommodation_booking(user,acc,ini_date,end_date,booking_time):
    """Adds a new accommodation booking into the database"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO booked_accommodations VALUES (?,?,?,?,?,?,?,?,?)",
            (user.email,acc.name,acc.type,acc.price,acc.rating,
            acc.location,ini_date,end_date,booking_time))
    conn.commit()
    conn.close()

def add_liked_destination(user,dest):
    """Adds a new destination preference into the database"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO liked_destinations VALUES (?,?,?,?)",
            (user.email,dest.name,dest.temperature,dest.country))
    conn.commit()
    conn.close()


# Check
def destination_not_on_list(user,dest):
    """Checks if a destination is on the list"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM liked_destinations WHERE LOWER(user) = LOWER(?) AND LOWER(name) = LOWER(?)",(user.email,dest.name))
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result is None

def user_found(user_name,user_email):
    """Checks whether or not a user is in the database"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ? AND email = ?",(user_name,user_email))

    result = c.fetchone()
    conn.commit()
    conn.close()
    if result is None:
        return False
    else:
        return True


# Loading into info.db
def add_destination(dest):
    """Adds a new destination into the database"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT INTO destinations VALUES (?,?,?)",
            (dest.name,dest.temperature,dest.country))
    conn.commit()
    conn.close()

def add_flight(flight):
    """Adds a new flight into the database"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?)",
            (flight.code,flight.company,flight.date,flight.duration,
            flight.origin,flight.destination,flight.price,flight.max_capacity,0))
    conn.commit()
    conn.close()

def add_accommodation(acc):
    """Adds a new accommodation into the database"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO accommodations VALUES (?,?,?,?,?)",
            (acc.name,acc.type,acc.price,acc.rating,acc.location))
    conn.commit()
    conn.close()


# Loading into bookings.db
def load_booked_flights(user):
    """Loads booked flights into the database"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("""SELECT code,company,date,duration,origin,destination,price,max_capacity
              FROM booked_flights WHERE user = ?""",(user.email,))
    rows = c.fetchall()    
    conn.commit()
    conn.close()
    return [Flight(*row) for row in rows] if rows else []

def load_booked_accommodations(user):
    """Loads booked accommodations into the database"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT name,type,price,rating,location FROM booked_accommodations WHERE user = ?", (user.email,))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return [Acommodation(*row) for row in rows] if rows else []

def load_liked_destinations(user):
    """Loads liked destinations into the database"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT name,temperature,country FROM liked_destinations WHERE user = ?", (user.email,))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    dest_by_country = {}
    for row in rows:
        dest = Destination(*row)
        if dest.country not in dest_by_country:
            dest_by_country[dest.country] = []
        dest_by_country[dest.country].append(dest)
    return dest_by_country

# Show
def show_capacity(code):
    """Returns capacity for a given flight"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("SELECT current_capacity FROM flights WHERE code == ?",(code,))
    capacity = c.fetchone()[0]
    conn.commit()
    conn.close()
    return capacity

def get_accommodations(user):
    """Prints all accommodation information for a given user"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM booked_accommodations WHERE user = ?",(user.email,))
    rows = c.fetchall()
    print("-" * 40)
    for row in rows:
        print(f"Accommodation Name: {row[1]}, Accommodation Type: {row[2]}, Price: {row[3]}€")
        print(f"Rating: {row[4]}, Location: {row[5]}, Start Date: {row[6]}, End Date: {row[7]}")
        print("-" * 40)
    conn.commit()
    conn.close()

def get_flights(user):
    """Prints all flight information for a given user"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM booked_flights WHERE user = ?",(user.email,))
    rows = c.fetchall()
    print("-" * 40)
    for row in rows:
        print(f"Flight Code: {row[1]}, Company: {row[2]}, Date: {row[3]}, Duration: {row[4]}h")
        print(f"From: {row[5]} To: {row[6]}, Price: {row[7]}€")
        print("-" * 40)
    conn.commit()
    conn.close()   

def get_preferences(user):
    """Prints all destination information for a given user"""
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM liked_destinations WHERE user = ?",(user.email,))
    rows = c.fetchall()
    if rows is None:
        print("-\n")
    else:
        print("-" * 40)
        for row in rows:
            print(f"{row[1]}, {row[3]}")
            print("-" * 40)
    conn.commit()
    conn.close()  

def user_budget(user_name,user_email):
    """Returns budget for a given user"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("SELECT budget FROM users WHERE name = ? AND email = ?",(user_name,user_email))
    
    result = c.fetchone()
    conn.commit()
    conn.close()
    if result is None:
        return None
    else:
        return result[0]
    

# Find
def find_accommodation(location,start_date,end_date,budget):
    """Returns all accommodations in a location, whithin given dates and within budget"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    
    # Attach bookings.db as bdb
    c.execute("ATTACH DATABASE 'bookings.db' AS bdb")

    c.execute("""SELECT a.name,a.type,a.price,a.rating,a.location
              FROM accommodations a
              WHERE LOWER(a.location) = LOWER(?) AND a.price <= ?
              AND NOT EXISTS (SELECT * FROM bdb.booked_accommodations b
                            WHERE b.name = a.name 
                            AND NOT (? < b.ini_date OR ? > b.fin_date))""",(location,budget,end_date,start_date))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return[Acommodation(*row) for row in rows]

def find_flight(city_dest,city_org,budget):
    """Returns all flights with common origin and destination and within budget"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("""SELECT code,company,date,duration,origin,destination,price,max_capacity 
              FROM flights WHERE LOWER(destination) = LOWER(?) AND price <= ? 
              AND LOWER(origin) = LOWER(?)""",(city_dest,budget,city_org))
    rows = c.fetchall()
    flights = [Flight(*row) for row in rows]
    conn.commit()
    conn.close()
    return flights

def find_destination(dest):
    """Returns destination"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("SELECT name,temperature,country FROM destinations WHERE LOWER(name) = LOWER(?)",(dest,))
    d = c.fetchone()
    conn.commit()
    conn.close()
    if d:  
        return Destination(*d)
    else:
        return None


# Update
def set_new_budget(user,new_budget):
    """Updates a given user's budget to the new_budget"""
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("UPDATE users SET budget = ? WHERE email = ?",(new_budget,user.email))
    conn.commit()
    conn.close()

def modify_flight_capacity(code,new_capacity):
    """Modifies flight (with code) capacity to the new number """
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("""UPDATE flights SET current_capacity = ? 
              WHERE code == ?
            """,(new_capacity,code))
    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":
    create_tables()
