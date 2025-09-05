import sqlite3

# Create Tables 
def create_tables():
    # Open connection to info file
    conn = sqlite3.connect('info.db')
    c = conn.cursor()

    # Create Table for Flight info
    c.execute("""CREATE TABLE IF NOT EXISTS flights (
            code text,
            company text,
            date text,
            duration integer,
            origin text,
            destination text,
            price integer,
            availability integer      
        )""")
    
# Create Table for Accommodation info
    c.execute("""CREATE TABLE IF NOT EXISTS accommodations (
            name text,
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
            email text,
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
            availability integer,  
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
            country text
        )""")
    
    # Commit and Close
    conn.commit()
    conn.close()

def add_user(user):
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?)",
            (user.name,user.email,user.budget))
    conn.commit()
    conn.close()

def add_flight_booking(user,flight,current_date):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO booked_flights VALUES (?,?,?,?,?,?,?,?,?,?)",
            (user.name,flight.code,flight.company,flight.date,flight.duration,
            flight.origin,flight.destination,flight.price,flight.available,
            current_date))
    conn.commit()
    conn.close()

def add_accommodation_booking(user,acc,ini_date,end_date,booking_time):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO booked_accommodations VALUES (?,?,?,?,?,?,?,?,?)",
            (user.name,acc.name,acc.type,acc.price,acc.rating,
            acc.location,ini_date,end_date,booking_time))
    conn.commit()
    conn.close()

def add_destination_booking(user,dest):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO liked_destinations VALUES (?,?,?,?)",
            (user.name,dest.name,dest.temperature,dest.country))
    conn.commit()
    conn.close()

def accommodation_is_available(acc,start_date,end_date):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM booked_accommodations 
              WHERE name = ? AND NOT ? > fin_date or ? < ini_date
              """,(acc.name,start_date,end_date))
    
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result is None # If there is already a booking, returns False

def add_destination(dest):
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT INTO destinations VALUES (?,?,?)",
            (dest.name,dest.temperature,dest.country))
    conn.commit()
    conn.close()

def add_flight(flight):
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?)",
            (flight.code,flight.company,flight.date,flight.duration,
            flight.origin,flight.destination,flight.price,flight.available))
    conn.commit()
    conn.close()

def add_accommodation(acc):
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("INSERT INTO accommodations VALUES (?,?,?,?,?)",
            (acc.name,acc.type,acc.price,acc.rating,acc.location))
    conn.commit()
    conn.close()

def show_booked_flights(user):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM booked_flights WHERE user = ?",(user.name,))
    
    rows = c.fetchall()
    if rows:
        for row in rows:
            print(f"Flight Code: {row[1]}, Company: {row[2]}, Date: {row[3]}, Duration: {row[4]}h")
            print(f"From: {row[5]} To: {row[6]}, Price: ${row[7]}, Available: {bool(row[8])}")
            print("-" * 40)
    else:
        print("No booked flights found.")    
    conn.commit()
    conn.close()

def show_booked_accommodations(user):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM booked_accommodations WHERE user = ?",(user.name,))
    
    rows = c.fetchall()
    if rows:
        for row in rows:
            print(f"Accommodation Name: {row[1]}, Type: {row[2]}, Price: ${row[3]}, Rating: {row[4]}/5")
            print(f"Location: {row[5]}, Start Date: {row[6]}, End Date: {row[7]}, Booking Time: {row[8]}")
            print("-" * 50)
    else:
        print("No booked accommodations found.")

    conn.commit()
    conn.close()

def user_found(user_name,user_email):
    conn = sqlite3.connect('info.db')
    c = conn.cursor()
    c.execute("SELECT budget FROM users WHERE name = ? AND email = ?",(user_name,user_email))
    
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result 

if __name__ == "__main__":
    create_tables()
