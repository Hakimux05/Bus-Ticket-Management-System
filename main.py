import mysql.connector
from mysql.connector import Error

class BusTicketSystem:

    def __init__(self):
        self.db = None
        self.connect_database()

    def connect_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bus_system"
            )

            if conn.is_connected():
                self.db = conn
                print("Database Connected")
                return conn

        except Error as e:
            print("Database Error :", e)
            self.db = None
            return None
        
    def get_connection(self):
        if self.db is None or not self.db.is_connected():
            print("Reconnecting to database...")
            self.connect_database()
        return self.db

    def book_ticket(self):
        print("\n ----- BOOK NEW TICKET -----")

        name = input("Passenger Name : ").strip()
        phone = input("Phone Number   : ").strip()
        destination = input("Destination    : ").strip()

        try:
            seat = int(input("Seat Number    : ").strip())
            price = float(input("Ticket Price   : ").strip())
        except ValueError:
            print("Invalid input! Seat and Price must be numbers.")
            return
        
        sql = """
        INSERT INTO tickets
        (name, phone, destination, seat, price)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, phone, destination, seat, price)

        conn = self.get_connection()
        if not conn:
            print("Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
            print("\n Ticket Booked Successfully")
            print("Ticket ID :", cursor.lastrowid)
            cursor.close()
        except Error as e:
            print("Error booking ticket:", e)
            conn.rollback()

    def view_all_tickets(self):
        print("\n --- ALL BUS TICKETS ---")

        conn = self.get_connection()
        if not conn:
            print("Database Error.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tickets ORDER BY id ASC")
            tickets = [dict(row) for row in cursor.fetchall()]

            if not tickets:
                print("Ticket not Found.")
                cursor.close()
                return

            for ticket in tickets:
                print("------------------------------------")
                print(f"Ticket ID   : {ticket['id']}")
                print(f"Passenger   : {ticket['name']}")
                print(f"Phone       : {ticket['phone']}")
                print(f"Destination : {ticket['destination']}")
                print(f"Seat Number : {ticket['seat']}")
                print(f"Price       : RM {ticket['price']:.2f}")
                print(f"Booked On   : {ticket['booking_date']}")
                print("------------------------------------")

            cursor.close()
        except Error as e:
            print("Error viewing tickets:", e)

    def update_ticket(self):
        print("\n ---- UPDATE TICKET ----")

        try:
            ticket_id = int(input("Enter Ticket ID : ").strip())
            name = input("New Passenger Name : ").strip()
            phone = input("New Phone Number   : ").strip()
            destination = input("New Destination    : ").strip()
            seat = int(input("New Seat Number    : ").strip())
            price = float(input("New Ticket Price   : ").strip())
        except ValueError:
            print("Invalid input! ID, Seat and Price must be numbers.")
            return

        sql = """
        UPDATE tickets
        SET name=%s, phone=%s, destination=%s, seat=%s, price=%s
        WHERE id=%s
        """
        values = (name, phone, destination, seat, price, ticket_id)

        conn = self.get_connection()
        if not conn:
            print("Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
            if cursor.rowcount > 0:
                print("Ticket Updated Successfully")
            else:
                print("Ticket ID Not Found")
            cursor.close()
        except Error as e:
            print("Error updating ticket:", e)
            conn.rollback()

    def delete_ticket(self):
        print("\n ---- DELETE TICKET ----")

        try:
            ticket_id = int(input("Enter Ticket ID : ").strip())
        except ValueError:
            print("Invalid Ticket ID! Must be a number.")
            return

        conn = self.get_connection()
        if not conn:
            print("Cannot connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tickets WHERE id=%s", (ticket_id,))
            conn.commit()
            if cursor.rowcount > 0:
                print("Ticket Deleted Successfully")
            else:
                print("Ticket ID Not Found")
            cursor.close()
        except Error as e:
            print("Error delete ticket:", e)
            conn.rollback()

    def menu(self):
        while True:
            print("""
[--- BUS TICKET MANAGEMENT SYSTEM ---]
1. Book New Ticket
2. View All Tickets
3. Update Ticket
4. Delete Ticket
5. Exit
""")

            choice = input("Enter Your Choice : ").strip()

            if choice == "1":
                self.book_ticket()
            elif choice == "2":
                self.view_all_tickets()
            elif choice == "3":
                self.update_ticket()
            elif choice == "4":
                self.delete_ticket()
            elif choice == "5":
                print("Thank You")
                if self.db and self.db.is_connected():
                    self.db.close()
                break
            else:
                print("Error choice. Try again.")

if __name__ == "__main__":
    app = BusTicketSystem()
    app.menu()