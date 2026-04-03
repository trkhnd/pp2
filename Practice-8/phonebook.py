from connect import connect

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS invalid_contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        surname VARCHAR(100),
        phone VARCHAR(20),
        reason TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully!")

def load_sql_file(filename):
    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql_code = file.read()
        cur.execute(sql_code)

    conn.commit()
    cur.close()
    conn.close()
    print(f"{filename} loaded successfully!")

def search_contacts():
    conn = connect()
    cur = conn.cursor()

    pattern = input("Enter search pattern: ")

    cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")

    cur.close()
    conn.close()

def upsert_contact():
    conn = connect()
    cur = conn.cursor()

    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")

    cur.execute("CALL upsert_contact(%s, %s, %s);", (name, surname, phone))
    conn.commit()

    print("Upsert completed successfully!")
    cur.close()
    conn.close()

def insert_many_contacts():
    conn = connect()
    cur = conn.cursor()

    n = int(input("How many contacts do you want to insert? "))

    names = []
    surnames = []
    phones = []

    for _ in range(n):
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        phone = input("Enter phone: ")

        names.append(name)
        surnames.append(surname)
        phones.append(phone)

    cur.execute("CALL insert_many_contacts(%s, %s, %s);", (names, surnames, phones))
    conn.commit()

    print("Bulk insert completed!")
    print("Check invalid_contacts table for incorrect rows if any.")

    cur.close()
    conn.close()

def show_paginated():
    conn = connect()
    cur = conn.cursor()

    limit_value = int(input("Enter limit: "))
    offset_value = int(input("Enter offset: "))

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit_value, offset_value))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found.")

    cur.close()
    conn.close()

def delete_contact():
    conn = connect()
    cur = conn.cursor()

    choice = input("Delete by phone or full name? (phone/name): ").strip().lower()

    if choice == "phone":
        phone = input("Enter phone: ")
        cur.execute("CALL delete_contact(NULL, NULL, %s);", (phone,))
    elif choice == "name":
        name = input("Enter name: ")
        surname = input("Enter surname: ")
        cur.execute("CALL delete_contact(%s, %s, NULL);", (name, surname))
    else:
        print("Invalid option.")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("Delete completed successfully!")

    cur.close()
    conn.close()

def show_invalid_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM invalid_contacts ORDER BY id;")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No invalid contacts found.")

    cur.close()
    conn.close()

def menu():
    while True:
        print("\n--- PRACTICE 8 PHONEBOOK MENU ---")
        print("1. Create tables")
        print("2. Load functions.sql")
        print("3. Load procedures.sql")
        print("4. Search contacts by pattern")
        print("5. Upsert contact")
        print("6. Insert many contacts")
        print("7. Show paginated contacts")
        print("8. Delete contact")
        print("9. Show invalid contacts")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_tables()
        elif choice == "2":
            load_sql_file("functions.sql")
        elif choice == "3":
            load_sql_file("procedures.sql")
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            upsert_contact()
        elif choice == "6":
            insert_many_contacts()
        elif choice == "7":
            show_paginated()
        elif choice == "8":
            delete_contact()
        elif choice == "9":
            show_invalid_contacts()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

menu()