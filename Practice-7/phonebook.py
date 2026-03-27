import csv
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """

    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()
    print("Table created successfully!")

def insert_from_console():
    conn = connect()
    cur = conn.cursor()

    username = input("Enter username: ")
    phone = input("Enter phone: ")

    try:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
            (username, phone)
        )
        conn.commit()
        print("Contact added successfully!")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def insert_from_csv():
    conn = connect()
    cur = conn.cursor()

    try:
        with open("contacts.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                username, phone = row
                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
                    (username, phone)
                )

        conn.commit()
        print("CSV data inserted successfully!")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook ORDER BY id;")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()

def search_by_name():
    conn = connect()
    cur = conn.cursor()

    name = input("Enter name to search: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE username ILIKE %s;",
        ("%" + name + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")

    cur.close()
    conn.close()

def search_by_phone_prefix():
    conn = connect()
    cur = conn.cursor()

    prefix = input("Enter phone prefix: ")

    cur.execute(
        "SELECT * FROM phonebook WHERE phone LIKE %s;",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")

    cur.close()
    conn.close()

def update_name():
    conn = connect()
    cur = conn.cursor()

    phone = input("Enter phone of contact to update name: ")
    new_name = input("Enter new username: ")

    try:
        cur.execute(
            "UPDATE phonebook SET username = %s WHERE phone = %s;",
            (new_name, phone)
        )
        conn.commit()

        if cur.rowcount > 0:
            print("Username updated successfully!")
        else:
            print("No contact found.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def update_phone():
    conn = connect()
    cur = conn.cursor()

    name = input("Enter username to update phone: ")
    new_phone = input("Enter new phone: ")

    try:
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE username = %s;",
            (new_phone, name)
        )
        conn.commit()

        if cur.rowcount > 0:
            print("Phone updated successfully!")
        else:
            print("No contact found.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def delete_by_name():
    conn = connect()
    cur = conn.cursor()

    name = input("Enter username to delete: ")

    try:
        cur.execute(
            "DELETE FROM phonebook WHERE username = %s;",
            (name,)
        )
        conn.commit()

        if cur.rowcount > 0:
            print("Contact deleted successfully!")
        else:
            print("No contact found.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def delete_by_phone():
    conn = connect()
    cur = conn.cursor()

    phone = input("Enter phone to delete: ")

    try:
        cur.execute(
            "DELETE FROM phonebook WHERE phone = %s;",
            (phone,)
        )
        conn.commit()

        if cur.rowcount > 0:
            print("Contact deleted successfully!")
        else:
            print("No contact found.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert contact from console")
        print("3. Insert contacts from CSV")
        print("4. Show all contacts")
        print("5. Search by name")
        print("6. Search by phone prefix")
        print("7. Update contact name")
        print("8. Update contact phone")
        print("9. Delete by username")
        print("10. Delete by phone")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            insert_from_csv()
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            search_by_name()
        elif choice == "6":
            search_by_phone_prefix()
        elif choice == "7":
            update_name()
        elif choice == "8":
            update_phone()
        elif choice == "9":
            delete_by_name()
        elif choice == "10":
            delete_by_phone()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

menu()