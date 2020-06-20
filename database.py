import sqlite3

# SQL Scripts
CREATE_ENTRY = """
    CREATE TABLE IF NOT EXISTS entry (
        title TEXT NOT NULL,
        timestamp DATETIME NOT NULL
    );
"""

CREATE_NOTE = """
    CREATE TABLE IF NOT EXISTS note (
        entry_rowid INTEGER NOT NULL, 
        note_text TEXT NOT NULL,
        timestamp DATETIME NOT NULL
    );
"""

SELECT_ENTRIES_ALL = """
    SELECT rowid, title, timestamp
    FROM entry
    ORDER BY rowid;
"""

SELECT_ENTRY_BY_KEYWORD = """
    SELECT rowid AS id, title, timestamp
    FROM entry
    WHERE title LIKE ? 
    UNION ALL
    SELECT entry_rowid AS id, note_text AS title, timestamp
    FROM note
    WHERE note_text LIKE ?;
"""

SELECT_ENTRY_BY_ID = """
    SELECT rowid AS id, title, timestamp
    FROM entry
    WHERE rowid = ?; 
"""

DELETE_ENTRY_BY_ID = """
    DELETE FROM entry
    WHERE rowid = ?;
"""

DELETE_NOTES_BY_ENTRY_ID = """
    DELETE FROM note
    WHERE entry_rowid = ?;
"""

SELECT_NOTES_ALL = """
    SELECT rowid, note_text, timestamp, entry_rowid 
    FROM note
    ORDER BY rowid;
"""

SELECT_NOTES_BY_ENTRY_ID = """
    SELECT rowid, note_text, timestamp, entry_rowid 
    FROM note
    WHERE entry_rowid = ?
    ORDER BY rowid;
"""

INSERT_ENTRY = """
    INSERT INTO entry (title, timestamp)
    VALUES (?, datetime('now', 'localtime'));
"""

INSERT_NOTE = """
    INSERT INTO note (entry_rowid, note_text, timestamp)
    VALUES (?, ?, datetime('now', 'localtime'));
"""

def connect():
    return sqlite3.connect("kbase.db")

def create_tables(connection):
    with connection:
        connection.execute(CREATE_ENTRY)
        connection.execute(CREATE_NOTE)

def get_all_entries(connection):
    with connection:
        return connection.execute(SELECT_ENTRIES_ALL).fetchall()

def get_all_notes(connection):
    with connection:
        return connection.execute(SELECT_NOTES_ALL).fetchall()

def search(connection, keyword):
    with connection:
        return connection.execute(SELECT_ENTRY_BY_KEYWORD, (f"%{keyword}%", f"%{keyword}%")).fetchall()

def get_entry(connection, entry_id):
    with connection:
        entry = connection.execute(SELECT_ENTRY_BY_ID, (entry_id,)).fetchone()
        notes = connection.execute(SELECT_NOTES_BY_ENTRY_ID, (entry_id,)).fetchall()

        return entry, notes

def del_entry(connection, entry_id):
    with connection:
        cursor = connection.cursor()
        cursor.execute(DELETE_ENTRY_BY_ID, (entry_id,))
        cursor.execute(DELETE_NOTES_BY_ENTRY_ID, (entry_id,))
        connection.commit()

def add_entry(connection, title):
    with connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_ENTRY, (title,))
        return cursor.lastrowid

def add_notes(connection, notes):
    with connection:
        for n in notes:
            connection.execute(INSERT_NOTE, n)