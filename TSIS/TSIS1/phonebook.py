import psycopg2
import csv
import json
from config import DB_CONFIG


def connect():
    return psycopg2.connect(**DB_CONFIG)


def show_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 60)
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Surname: {row[2]}")
        print(f"Email: {row[3]}")
        print(f"Birthday: {row[4]}")
        print(f"Group: {row[5]}")
        print(f"Phones: {row[6]}")


def filter_by_group():
    group = input("Enter group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, g.name
        ORDER BY c.id;
    """, (group,))

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def search_by_email():
    email = input("Enter email pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, g.name
        ORDER BY c.id;
    """, (f"%{email}%",))

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.id"
    else:
        print("Invalid choice")
        return

    conn = connect()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name,
               STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
        ORDER BY {order_by};
    """)

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def pagination_loop():
    limit = int(input("Enter page size: "))
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, c.birthday,
                   g.name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
            ORDER BY c.id
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()
        show_contacts(rows)

        command = input("next / prev / quit: ").lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command")

    cur.close()
    conn.close()


def add_phone():
    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type(home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))

    conn.commit()
    print("Phone added.")

    cur.close()
    conn.close()


def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s);", (name, group))

    conn.commit()
    print("Contact moved to group.")

    cur.close()
    conn.close()


def advanced_search():
    query = input("Search query: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    rows = cur.fetchall()

    show_contacts(rows)

    cur.close()
    conn.close()


def export_to_json():
    filename = input("JSON filename: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id;
    """)

    contacts = []

    for contact in cur.fetchall():
        contact_id = contact[0]

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = []
        for p in cur.fetchall():
            phones.append({
                "phone": p[0],
                "type": p[1]
            })

        contacts.append({
            "name": contact[1],
            "surname": contact[2],
            "email": contact[3],
            "birthday": str(contact[4]) if contact[4] else None,
            "group": contact[5],
            "phones": phones
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

    print("Exported to JSON.")

    cur.close()
    conn.close()


def import_from_json():
    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = connect()
    cur = conn.cursor()

    for contact in contacts:
        name = contact["name"]
        surname = contact["surname"]
        email = contact["email"]
        birthday = contact["birthday"]
        group = contact["group"]
        phones = contact["phones"]

        cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} already exists. skip or overwrite? ")

            if choice.lower() == "skip":
                continue

            if choice.lower() == "overwrite":
                contact_id = existing[0]

                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES(%s)
                    ON CONFLICT(name) DO NOTHING;
                """, (group,))

                cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
                group_id = cur.fetchone()[0]

                cur.execute("""
                    UPDATE contacts
                    SET surname = %s,
                        email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE id = %s;
                """, (surname, email, birthday, group_id, contact_id))

                cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))

                for p in phones:
                    cur.execute("""
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES(%s, %s, %s);
                    """, (contact_id, p["phone"], p["type"]))

        else:
            cur.execute("""
                INSERT INTO groups(name)
                VALUES(%s)
                ON CONFLICT(name) DO NOTHING;
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, surname, email, birthday, group_id)
                VALUES(%s, %s, %s, %s, %s)
                RETURNING id;
            """, (name, surname, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            for p in phones:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES(%s, %s, %s);
                """, (contact_id, p["phone"], p["type"]))

    conn.commit()
    print("Imported from JSON.")

    cur.close()
    conn.close()


def import_from_csv():
    filename = input("CSV filename: ")

    conn = connect()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            surname = row["surname"]
            email = row["email"]
            birthday = row["birthday"]
            group = row["group"]
            phone = row["phone"]
            phone_type = row["phone_type"]

            cur.execute("""
                INSERT INTO groups(name)
                VALUES(%s)
                ON CONFLICT(name) DO NOTHING;
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE name = %s;", (group,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, surname, email, birthday, group_id)
                VALUES(%s, %s, %s, %s, %s)
                ON CONFLICT(name) DO UPDATE
                SET surname = EXCLUDED.surname,
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id;
            """, (name, surname, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES(%s, %s, %s);
            """, (contact_id, phone, phone_type))

    conn.commit()
    print("CSV imported.")

    cur.close()
    conn.close()


def menu():
    while True:
        print("\nPHONEBOOK TSIS1")
        print("1. Filter by group")
        print("2. Search by email")
        print("3. Sort contacts")
        print("4. Paginated navigation")
        print("5. Add phone")
        print("6. Move contact to group")
        print("7. Advanced search")
        print("8. Export to JSON")
        print("9. Import from JSON")
        print("10. Import from CSV")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            filter_by_group()
        elif choice == "2":
            search_by_email()
        elif choice == "3":
            sort_contacts()
        elif choice == "4":
            pagination_loop()
        elif choice == "5":
            add_phone()
        elif choice == "6":
            move_to_group()
        elif choice == "7":
            advanced_search()
        elif choice == "8":
            export_to_json()
        elif choice == "9":
            import_from_json()
        elif choice == "10":
            import_from_csv()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()