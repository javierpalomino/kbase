# A simple text-based knowledge base for individual use
# japcobos@gmail.com
# Last updated: 2020-06-19 

import database as db

conn = db.connect()
db.create_tables(conn)

def print_entries(entries):
    """Print KB entries"""
    if len(entries) > 0:
        print("Id______Title/Note______________________________Date_______________")

        for entry in entries:
            offset = " " * (40 - len(entry[1]))
            title = f"{entry[1][:36]}... " if len(entry[1]) > 40 else entry[1]
            print(f"{entry[0]}\t{title}{offset}{entry[2]}")

        print(f"\n({len(entries)} entries found)\n")
    else:
        print("\nNo entries found!\n")

def print_entry(entry):
    if entry:
        print("_" * 60)
        print(f"Entry ID:  {entry[0]}")
        print(f"Title:     {entry[1]}")
        print(f"Timestamp: {entry[2]}")

def entry_actions(entry_id):
    option = input("1. Add note | 2. Delete Entry | option: ").strip()

    if option == '1':
        notes = add_notes(entry_id)
        if notes > 0:
            print(f"{notes} added")
    elif option == '2':
        code = input("Type DELETE to proceed: ").strip()
        if code == 'DELETE':
            db.del_entry(conn, entry_id)
        else:
            print("\nNot deleted!\n")
    else:
        pass

def choose_entry(entries_count):
    """Actions for KB entries"""
    try:
        entry_id = int(input("Choose entry: "))
        if entry_id in range(1, entries_count):
            return entry_id
        else:
            return 0
    except ValueError:
        return 0

def print_notes(notes):
    """Print all KB entry notes"""
    if len(notes) > 0:
        print("Notes:")
        for note in notes:
            print(f"           {note[1]}")
    else:
        print("\nNo notes found!\n")
    print("_" * 60)

def add_entry():
    """Add a new Entry to Knowledge Base"""

    print("*** Adding a new KB Entry")
    title = input("Title (60 char max): ").strip()
    title = title[:60] if len(title) > 60 else title

    if title != '':
        entry_id = db.add_entry(conn, title)

        if entry_id > 0:
            notes = add_notes(entry_id)
            print(f"\nEntry #{entry_id} added to KB with {notes} notes.\n")
        else:
            print("\nUnable to add new Entry!\n")
    else:
        print("\nNothing added!\n")

def add_notes(entry_id):
    notes = []
    print(f"Type notes for Entry #{entry_id}, empty line to finish.")
    
    while True:
        note = input(f"Note {len(notes) + 1}: ").strip()
        if note != '':
            notes.append((entry_id, note))
        else:
            break
    
    db.add_notes(conn, notes)
    return len(notes)


def main_menu():
    """Main menu for the knowledge base"""
    while True:
        print("*** Knowledge Base menu")
        print("1. Search")
        print("2. Add entry")
        print("3. Show all entries")
        print("4. Show all notes")
        print()

        option = input("Choose your option, empty to exit: ").strip()

        if option == '1':
            keyword = input("Search keyword: ")

            if len(keyword) > 0:
                entries = db.search(conn, keyword)
                print_entries(entries) 
                if len(entries) > 0:           
                    entry_id = choose_entry(len(entries))

                    if entry_id != 0:
                        entry, notes = db.get_entry(conn, entry_id)
                        print_entry(entry)
                        print_notes(notes)
                        entry_actions(entry_id)
                    else:
                        print("\nInvalid entry!\n")

        elif option == '2':
            add_entry()
        elif option == '3':
            entries = db.get_all_entries(conn)
            print("Displaying all KB entries...")
            print_entries(entries)
        elif option == '4':
            notes = db.get_all_notes(conn)
            print("Displaying all notes...")
            print_entries(notes)
        elif option == '':
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid option!\n")

if __name__ == "__main__":
    main_menu()