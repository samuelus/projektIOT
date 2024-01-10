import sqlite3
from datetime import datetime, timedelta
from database.db_classes import Odbicie, Pracownik, Uprawnienia, Strefa, Admin
from database.db_constants import DB_NAME, DB_DATE_FROMAT
from database.db_creator import reset_db

class DbManager:
    @staticmethod
    def clear_database(insert_dummy_values: bool) -> None:
        """Clears and rebuilds the whole database"""
        reset_db(insert_dummy_values)

    ### ADMIN PANEL CRUD FUNCTIONS

    @staticmethod
    def get_odbicia() -> list[Odbicie]:
        """Lista wszystkich odbić"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Odbicia''')
        odbicia = [Odbicie(data) for data in cursor.fetchall()]
        conn.close()
        return odbicia

    @staticmethod
    def add_odbicie(id_karty: str, id_strefy: int, czas_wejscia: datetime, czas_wyjscia: datetime = None) -> int:
        """Dodaje nowe odbicie. Zwraca id nowo utworzonego odbicia"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if czas_wyjscia is None:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia) VALUES (?, ?, ?)''', (id_karty, id_strefy, czas_wejscia.strftime(DB_DATE_FROMAT)))
        else:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia, czas_wyjscia) VALUES (?, ?, ?, ?)''', (id_karty, id_strefy, czas_wejscia.strftime(DB_DATE_FROMAT), czas_wyjscia.strftime(DB_DATE_FROMAT)))
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return id

    @staticmethod
    def remove_odbicie(id_odbicia: int) -> bool:
        """Usuwa odbiecie. Zwraca czy operacja się powiodła"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Odbicia WHERE id_odbicia = ?', (id_odbicia,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('DELETE FROM Odbicia WHERE id_odbicia = ?', (id_odbicia,))
            conn.commit()
            conn.close()
            return True  
        else:
            conn.close()
            return False

    @staticmethod
    def get_pracownicy() -> list[Pracownik]:
        """Lista wszystkich pracowników"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Pracownicy''')
        pracownicy = [Pracownik(data) for data in cursor.fetchall()]
        conn.close()
        return pracownicy

    @staticmethod
    def add_pracownik(id_karty: str, imie: str, nazwisko: str) -> bool:
        """Dodaje nowego pracownika. Zwraca false, jeżeli podany numer karty już istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO Pracownicy (id_karty, imie, nazwisko) VALUES (?, ?, ?)''', (id_karty, imie, nazwisko))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def update_pracownik(id_karty: str, new_imie: str, new_nazwisko: str) -> bool:
        """Modyfikuje dane pracownika o danym numerze karty. Zwraca czy rekord z podanym id istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Pracownicy WHERE id_karty = ?', (id_karty,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('''UPDATE Pracownicy SET imie = ?, nazwisko = ? WHERE id_karty = ?''', (new_imie, new_nazwisko, id_karty))
            conn.commit()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def remove_pracownik(id_karty: str) -> bool:
        """Usuwa pracownika o podanym numerze karty. Zwraca false, jeżeli rekord z podanym id nie istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Pracownicy WHERE id_karty = ?', (id_karty,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('DELETE FROM Pracownicy WHERE id_karty = ?', (id_karty,))
            conn.commit()
            conn.close()
            return True  
        else:
            conn.close()
            return False

    @staticmethod
    def get_uprawnienia() -> list[Uprawnienia]:
        """Lista wszystkich uprawnień"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM UprawnieniaDostepu''')
        uprawnienia = [Uprawnienia(data) for data in cursor.fetchall()]
        conn.close()
        return uprawnienia

    @staticmethod
    def add_uprawnienia(id_karty: str, id_strefy: int) -> bool:
        """Dodaje nowe uprawnienia. Zwraca false, jeżeli podane uprawniania już istnieją"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO UprawnieniaDostepu (id_karty, id_strefy) VALUES (?, ?)''', (id_karty, id_strefy))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def remove_uprawnienia(id_karty: str, id_strefy: int) -> bool:
        """Usuwa uprawnienia. Zwraca false, jeżeli dane uprawnienia już nie istnieją"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM UprawnieniaDostepu WHERE id_karty = ? AND id_strefy = ?', (id_karty, id_strefy))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('DELETE FROM UprawnieniaDostepu WHERE id_karty = ? AND id_strefy = ?', (id_karty, id_strefy))
            conn.commit()
            conn.close()
            return True  
        else:
            conn.close()
            return False

    @staticmethod
    def get_strefy() -> list[Strefa]:
        """Lista wszystkich stref"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Strefy''')
        strefy = [Strefa(data) for data in cursor.fetchall()]
        conn.close()
        return strefy

    @staticmethod
    def add_strefa(nazwa: str) -> int:
        """Dodaje nową strefę. Zwraca id nowo utworzonej strefy"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Strefy (nazwa_strefy) VALUES (?)''', (nazwa,))
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return id

    @staticmethod
    def update_strefa(id: int, new_nazwa: str) -> bool:
        """Modyfikuje dane strefy o danym id. Zwraca false, jeżeli rekord z podanym id nie istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Strefy WHERE id_strefy = ?', (id,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('''UPDATE Strefy SET nazwa_strefy = ? WHERE id_strefy = ?''', (new_nazwa, id))
            conn.commit()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def remove_strefa(id_strefy: int) -> bool:
        """Usuwa strefe o podanym id. Zwraca false, jeżeli rekord z podanym id nie istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Strefy WHERE id_strefy = ?', (id_strefy,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('DELETE FROM Strefy WHERE id_strefy = ?', (id_strefy,))
            conn.commit()
            conn.close()
            return True  
        else:
            conn.close()
            return False

    @staticmethod
    def get_admins() -> list[Admin]:
        """Lista wszystkich adminów"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Administratorzy''')
        admini = [Admin(data) for data in cursor.fetchall()]
        conn.close()
        return admini

    @staticmethod
    def add_admin(login: str, haslo: str) -> bool:
        """Dodaje nowego admina. Zwraca false, jeżeli podany login już istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            #TODO: ZMIENIĆ NA HASH
            cursor.execute('''INSERT INTO Administratorzy (login, hash_hasla) VALUES (?, ?)''', (login, haslo))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        
    @staticmethod
    def update_admin(login: str, new_haslo: str) -> bool:
        """Modyfikuje dane ADMINA o danym loginie. Zwraca false, jeżeli rekord z podanym loginem istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Administratorzy WHERE login = ?', (login,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            #TODO: ZMIENIĆ NA HASH
            cursor.execute('''UPDATE Administratorzy SET hash_hasla = ? WHERE login = ?''', (new_haslo, login))
            conn.commit()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def remove_admin(login: str) -> bool:
        """Usuwa admina o podanym loginie. Zwraca false, jeżeli rekord z podanym id nie istnieje lub jest to 'root'"""
        if (login == 'root'): return False
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Administratorzy WHERE login = ?', (login,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            cursor.execute('DELETE FROM Administratorzy WHERE login = ?', (login,))
            conn.commit()
            conn.close()
            return True  
        else:
            conn.close()
            return False

    ### UTILITY
        
    def odbij(id_karty: str, id_strefy: int, aktualny_czas: datetime) -> timedelta:
        """Jeżeli odbicie to oznacza rozpoczęcie pracy - zwraca None; jeżeli zakończenie - zwraca długość pracy"""

    @staticmethod
    def is_login_and_password_correct(login: str, haslo: str) -> bool:
        """Sprawdza czy podane dane logowania admina są poprawne"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Administratorzy WHERE login = ?', (login,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            admin = Admin(existing_record)
            conn.commit()
            conn.close()
            #TODO: ZMIENIĆ NA HASH
            return admin.hash_hasla == haslo
        else:
            conn.commit()
            conn.close()
            return False

    ### REPORTS

    def average_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> dict[str, timedelta]:
        """Zwraca średni czas pracy każdego pracownika pomiędzy określonymi datami"""

    def total_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> dict[str, timedelta]:
        """Zwraca całkowity czas pracy każdego pracownika pomiędzy określonymi datami"""

    def total_work_units_between_dates_report(start_date: datetime, end_date: datetime) -> dict[str, int]:
        """Zwraca ile razy w pracy był każdy pracownik pomiędzy określonymi datami"""