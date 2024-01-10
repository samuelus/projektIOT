import sqlite3
from database.db_constants import DB_NAME
from database.db_constants import ROOT_LOGIN, DEFAULT_ROOT_HASHED_PASSWORD, DUMMY_PRACOWNICY, DUMMY_ODBICIA, DUMMY_ADMINISTRATORZY, DUMMY_STREFY, DUMMY_UPRAWNIENIA

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Pracownicy")
    cursor.execute("DROP TABLE IF EXISTS Odbicia")
    cursor.execute("DROP TABLE IF EXISTS UprawnieniaDostepu")
    cursor.execute("DROP TABLE IF EXISTS Strefy")
    cursor.execute("DROP TABLE IF EXISTS Administratorzy")

    #Pracownicy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pracownicy (
            id_karty TEXT PRIMARY KEY,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL
        )
    ''')

    #Odbicia
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Odbicia (
            id_odbicia INTEGER PRIMARY KEY,
            id_karty TEXT NOT NULL,
            id_strefy INTEGER NOT NULL,
            czas_wejscia DATETIME NOT NULL,
            czas_wyjscia DATETIME,
            FOREIGN KEY (id_karty) REFERENCES Pracownicy(id_karty)
            FOREIGN KEY (id_strefy) REFERENCES Strefy(id_strefy)
        )
    ''')

    #UprawnieniaDostepu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UprawnieniaDostepu (
            id_karty TEXT NOT NULL,
            id_strefy INTEGER NOT NULL,
            FOREIGN KEY (id_karty) REFERENCES Pracownicy(id_karty),
            FOREIGN KEY (id_strefy) REFERENCES Strefy(id_strefy),
            PRIMARY KEY (id_karty, id_strefy)
        )
    ''')

    #Strefy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Strefy (
            id_strefy INTEGER PRIMARY KEY,
            nazwa_strefy TEXT NOT NULL
        )
    ''')

    #Administratorzy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Administratorzy (
            login TEXT PRIMARY KEY,
            hash_hasla TEXT NOT NULL
        )
    ''')

    #Create 'root' admin
    cursor.execute('''
        INSERT INTO Administratorzy (login, hash_hasla) VALUES (?, ?)
    ''', (ROOT_LOGIN, DEFAULT_ROOT_HASHED_PASSWORD))

    conn.commit()
    conn.close()

def insert_dummy_values():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #Pracownicy
    cursor.executemany('''
        INSERT INTO Pracownicy (id_karty, imie, nazwisko) VALUES (?, ?, ?)
    ''', DUMMY_PRACOWNICY)

    #Odbicia
    cursor.executemany('''
        INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia, czas_wyjscia) VALUES (?, ?, ?, ?)
    ''', DUMMY_ODBICIA)

    #UprawnieniaDostepu
    cursor.executemany('''
        INSERT INTO UprawnieniaDostepu (id_karty, id_strefy) VALUES (?, ?)
    ''', DUMMY_UPRAWNIENIA)

    #Strefy
    cursor.executemany('''
        INSERT INTO Strefy (nazwa_strefy) VALUES (?)
    ''', DUMMY_STREFY)

    #Administratorzy
    cursor.executemany('''
        INSERT INTO Administratorzy (login, hash_hasla) VALUES (?, ?)
    ''', DUMMY_ADMINISTRATORZY)

    conn.commit()
    conn.close()

def print_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #Pracownicy
    cursor.execute('''SELECT * FROM Pracownicy''')
    print("***PRACOWNICY***")
    print(cursor.fetchall())

    # Wyświetlanie zawartości tabeli Odbicia
    cursor.execute('''SELECT * FROM Odbicia''')
    print("\n***ODBICIA***")
    print(cursor.fetchall())

    # Wyświetlanie zawartości tabeli UprawnieniaDostepu
    cursor.execute('''SELECT * FROM UprawnieniaDostepu''')
    print("\n***UPRAWNIENIA DOSTEPU***")
    print(cursor.fetchall())

    # Wyświetlanie zawartości tabeli Strefy
    cursor.execute('''SELECT * FROM Strefy''')
    print("\n***STREFY***")
    print(cursor.fetchall())

    # Wyświetlanie zawartości tabeli Administratorzy
    cursor.execute('''SELECT * FROM Administratorzy''')
    print("\n***ADMINISTRATORZY***")
    print(cursor.fetchall())

    conn.close()

def reset_db(insert_dummy: bool):
    create_tables()
    if (insert_dummy):
        insert_dummy_values()