import csv
import json
from connect import get_connection


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


def get_group_id(cur, group_name):
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT(name) DO NOTHING;
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    return cur.fetchone()[0]


def filter_by_group():
    group = input("Enter group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name,
               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, g.name
        ORDER BY c.id;
    """, (group,))

    show_contacts(cur.fetchall())

    cur.close()
    conn.close()


def search_by_email():
    email = input("Enter email pattern: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name,
               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, g.name
        ORDER BY c.id;
    """, (f"%{email}%",))

    show_contacts(cur.fetchall())

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ").strip()

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.id"
    else:
        print("Invalid choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT c.id, c.name, c.surname, c.email, c.birthday,
               g.name,
               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
        ORDER BY {order_by};
    """)

    show_contacts(cur.fetchall())

    cur.close()
    conn.close()


def pagination_loop():
    limit = int(input("Enter page size: ").strip())
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    while True:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, c.birthday,
                   g.name,
                   COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
            ORDER BY c.id
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()
        show_contacts(rows)

        command = input("next / prev / quit: ").strip().lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Wrong command.")

    cur.close()
    conn.close()


def add_phone():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type(home/work/mobile): ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))

    conn.commit()
    print("Phone added.")

    cur.close()
    conn.close()


def move_to_group():
    name = input("Contact name: ").strip()
    group = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s);", (name, group))

    conn.commit()
    print("Contact moved to group.")

    cur.close()
    conn.close()


def advanced_search():
    query = input("Search query: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    show_contacts(cur.fetchall())

    cur.close()
    conn.close()


def export_to_json():
    filename = input("JSON filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.surname, c.email, c.birthday, g.name
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
    filename = input("JSON filename: ").strip()

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    conn = get_connection()
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

        group_id = get_group_id(cur, group)

        if existing:
            choice = input(f"{name} already exists. skip or overwrite? ").strip().lower()

            if choice == "skip":
                continue

            if choice == "overwrite":
                contact_id = existing[0]

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
    filename = input("CSV filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"].strip()
            surname = row["surname"].strip()
            email = row["email"].strip()
            birthday = row["birthday"].strip()
            group = row["group"].strip()
            phone = row["phone"].strip()
            phone_type = row["phone_type"].strip()

            group_id = get_group_id(cur, group)

            cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
            existing = cur.fetchone()

            if existing:
                contact_id = existing[0]

                cur.execute("""
                    UPDATE contacts
                    SET surname = %s,
                        email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE id = %s;
                """, (surname, email, birthday, group_id, contact_id))

            else:
                cur.execute("""
                    INSERT INTO contacts(name, surname, email, birthday, group_id)
                    VALUES(%s, %s, %s, %s, %s)
                    RETURNING id;
                """, (name, surname, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                SELECT %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM phones
                    WHERE contact_id = %s AND phone = %s
                );
            """, (contact_id, phone, phone_type, contact_id, phone))

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

        choice = input("Choose: ").strip()

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
            print("Invalid choice.")


if __name__ == "__main__":
    menu()