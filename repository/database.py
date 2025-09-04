import sqlite3

# Create Table for Flights
def create_tables():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
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

    # Create Table for Accommodations
    c.execute("""CREATE TABLE IF NOT EXISTS accommodations (
            name text,
            type text,
            price integer,
            rating integer,
            location text,
            availability integer      
        )""")

    # Create Table for Destinations
    c.execute("""CREATE TABLE IF NOT EXISTS destinations (
            name text,
            temperature integer,
            country text
        )""")
    
    # Commit and Close
    conn.commit()
    conn.close()

def add_flight_booking(flight):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?)",
            (flight.code,flight.company,flight.date,flight.duration,
            flight.origin,flight.destination,flight.price,flight.available))
    conn.commit()
    conn.close()

def add_accommodation_booking(acc):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO accommodations VALUES (?,?,?,?,?,?)",
            (acc.name,acc.type,acc.price,acc.rating,
            acc.location,acc.availability))
    conn.commit()
    conn.close()

def add_destination_booking(dest):
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO destinations VALUES (?,?,?)",
            (dest.name,dest.temperature,dest.country))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
