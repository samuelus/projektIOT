import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
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

    conn.commit()
    conn.close()

def insert_dummy_values():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    #Pracownicy
    cursor.execute('''
        INSERT INTO Pracownicy (id_karty, imie, nazwisko) VALUES 
        ('aff123f5agg2', 'Marcin', 'Kowalski'),
        ('h231yu8x21f3', 'Anna', 'Nowak'),
        ('ddzp81l38vj1', 'Piotr', 'Wiśniewski')
    ''')

    #Odbicia
    cursor.execute('''
        INSERT INTO Odbicia (id_odbicia, id_karty, id_strefy, czas_wejscia, czas_wyjscia) VALUES 
        (1, 'aff123f5agg2', '1', '2023-01-01 08:00:00', '2023-01-01 16:00:00'),
        (2, 'aff123f5agg2', '1', '2023-01-02 09:00:00', '2023-01-02 17:00:00'),
        (3, 'ddzp81l38vj1', '1', '2023-01-03 07:30:00', '2023-01-03 15:30:00')
    ''')

    #UprawnieniaDostepu
    cursor.execute('''
        INSERT INTO UprawnieniaDostepu (id_karty, id_strefy) VALUES 
        ('aff123f5agg2', 1),
        ('h231yu8x21f3', 1),
        ('ddzp81l38vj1', 1)
    ''')

    #Strefy
    cursor.execute('''
        INSERT INTO Strefy (id_strefy, nazwa_strefy) VALUES 
        (1, 'Strefa A'),
        (2, 'Strefa B')
    ''')

    #Administratorzy
    cursor.execute('''
        INSERT INTO Administratorzy (login, hash_hasla) VALUES 
        ('admin1', 'haslo1'),
        ('admin2', 'haslo2'),
        ('admin3', 'haslo3')
    ''')

    conn.commit()
    conn.close()

def print_tables():
    conn = sqlite3.connect('database.db')
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


if (__name__ == '__main__'):
    create_tables()
    insert_dummy_values()
    print_tables()