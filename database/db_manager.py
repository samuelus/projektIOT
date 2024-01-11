from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from database.db_classes import Odbicie, Pracownik, Uprawnienia, Strefa, Admin
from database.db_constants import DB_NAME, DB_DATETIME_FORMAT
from database.db_creator import reset_db
from database.cryptography import hash_password, verify_password

class DbManager:
    @staticmethod
    def clear_database(insert_dummy_values: bool) -> None:
        """Clears and rebuilds the whole database"""
        reset_db(insert_dummy_values)

    ### ADMIN PANEL CRUD FUNCTIONS

    @staticmethod
    def read_all_odbicia() -> list[Odbicie]:
        """Lista wszystkich odbić"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Odbicia''')
        odbicia = [Odbicie(data) for data in cursor.fetchall()]
        conn.close()
        return odbicia
    
    @staticmethod
    def read_odbicie(id_odbicia: str) -> Odbicie | None:
        """Odbicie o podanym id lub None w przypadku, kiedy takie nie istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Odbicia WHERE id_odbicia = ?''', (id_odbicia,))
        result = cursor.fetchone()
        odbicie = Odbicie(result) if result is not None else None
        conn.close()
        return odbicie

    @staticmethod
    def create_odbicie(id_karty: str, id_strefy: int, czas_wejscia: datetime, czas_wyjscia: datetime = None) -> int:
        """Dodaje nowe odbicie. Zwraca id nowo utworzonego odbicia"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if czas_wyjscia is None:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia) VALUES (?, ?, ?)''', (id_karty, id_strefy, czas_wejscia.strftime(DB_DATETIME_FORMAT)))
        else:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia, czas_wyjscia) VALUES (?, ?, ?, ?)''', (id_karty, id_strefy, czas_wejscia.strftime(DB_DATETIME_FORMAT), czas_wyjscia.strftime(DB_DATETIME_FORMAT)))
        id = cursor.lastrowid
        conn.commit()
        conn.close()
        return id
    
    @staticmethod
    def update_odbicie(id_odbicia: int, new_id_karty: str, new_id_strefy: int, new_czas_wejscia: datetime, new_czas_wyjscia: datetime = None) -> bool:
        """Modyfikuje dane odbicia o danym id. Zwraca czy rekord z podanym id istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Odbicia WHERE id_odbicia = ?', (id_odbicia,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            if new_czas_wyjscia is not None:
                cursor.execute('''UPDATE Odbicia SET id_karty = ?, id_strefy = ?, czas_wejscia = ?, czas_wyjscia = ? WHERE id_odbicia = ?''', (new_id_karty, new_id_strefy, new_czas_wejscia.strftime(DB_DATETIME_FORMAT), new_czas_wyjscia.strftime(DB_DATETIME_FORMAT), id_odbicia))
            else:
                cursor.execute('''UPDATE Odbicia SET id_karty = ?, id_strefy = ?, czas_wejscia = ?, czas_wyjscia = NULL WHERE id_odbicia = ?''', (new_id_karty, new_id_strefy, new_czas_wejscia.strftime(DB_DATETIME_FORMAT), id_odbicia))
            conn.commit()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def delete_odbicie(id_odbicia: int) -> bool:
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
    def read_all_pracownicy() -> list[Pracownik]:
        """Lista wszystkich pracowników"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Pracownicy''')
        pracownicy = [Pracownik(data) for data in cursor.fetchall()]
        conn.close()
        return pracownicy
    
    @staticmethod
    def read_pracownik(id_karty: str) -> Pracownik | None:
        """Pracownik o podanym id lub None w przypadku, kiedy taki nie istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Pracownicy WHERE id_karty = ?''', (id_karty,))
        result = cursor.fetchone()
        pracownik = Pracownik(result) if result is not None else None
        conn.close()
        return pracownik

    @staticmethod
    def create_pracownik(id_karty: str, imie: str, nazwisko: str) -> bool:
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
    def delete_pracownik(id_karty: str) -> bool:
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
    def read_all_uprawnienia() -> list[Uprawnienia]:
        """Lista wszystkich uprawnień"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM UprawnieniaDostepu''')
        uprawnienia = [Uprawnienia(data) for data in cursor.fetchall()]
        conn.close()
        return uprawnienia

    @staticmethod
    def create_uprawnienia(id_karty: str, id_strefy: int) -> bool:
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
    def delete_uprawnienia(id_karty: str, id_strefy: int) -> bool:
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
    def read_all_strefy() -> list[Strefa]:
        """Lista wszystkich stref"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Strefy''')
        strefy = [Strefa(data) for data in cursor.fetchall()]
        conn.close()
        return strefy
    
    @staticmethod
    def read_strefa(id_strefy: str) -> Strefa | None:
        """Strefa o podanym id lub None w przypadku, kiedy taka nie istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Odbicia WHERE id_strefy = ?''', (id_strefy,))
        result = cursor.fetchone()
        strefa = Strefa(result) if result is not None else None
        conn.close()
        return strefa

    @staticmethod
    def create_strefa(nazwa: str) -> int:
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
    def delete_strefa(id_strefy: int) -> bool:
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
    def read_all_administratorzy() -> list[Admin]:
        """Lista wszystkich adminów"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Administratorzy''')
        admini = [Admin(data) for data in cursor.fetchall()]
        conn.close()
        return admini

    @staticmethod
    def create_administrator(login: str, haslo: str) -> bool:
        """Dodaje nowego admina. Zwraca false, jeżeli podany login już istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            hashed_password = hash_password(haslo)
            cursor.execute('''INSERT INTO Administratorzy (login, hash_hasla) VALUES (?, ?)''', (login, hashed_password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        
    @staticmethod
    def update_administrator(login: str, new_haslo: str) -> bool:
        """Modyfikuje dane ADMINA o danym loginie. Zwraca false, jeżeli rekord z podanym loginem istnieje"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Administratorzy WHERE login = ?', (login,))
        existing_record = cursor.fetchone()
        if existing_record is not None:
            hashed_password = hash_password(new_haslo)
            cursor.execute('''UPDATE Administratorzy SET hash_hasla = ? WHERE login = ?''', (hashed_password, login))
            conn.commit()
            conn.close()
            return True
        else:
            return False

    @staticmethod
    def delete_administrator(login: str) -> bool:
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
        
    @staticmethod
    def odbij(id_karty: str, id_strefy: int, aktualny_czas: datetime) -> timedelta | None:     
        """Jeżeli odbicie to oznacza rozpoczęcie pracy - zwraca None; jeżeli zakończenie - zwraca długość pracy"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Odbicia WHERE id_karty = ? AND czas_wyjscia IS NULL', (id_karty,))
        odbicieWejsciowe = cursor.fetchone()
        if odbicieWejsciowe is not None:
            cursor.execute('''UPDATE Odbicia SET czas_wyjscia = ? WHERE id_strefy = ?''', (aktualny_czas.strftime(DB_DATETIME_FORMAT), id_strefy))
            workTime = aktualny_czas - Odbicie(odbicieWejsciowe).czas_wejscia
            conn.commit()
            conn.close()
            return workTime
        else:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia) VALUES (?, ?, ?)''', (id_karty, id_strefy, aktualny_czas.strftime(DB_DATETIME_FORMAT)))
            conn.commit()
            conn.close()
            return None


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
            return verify_password(haslo, admin.hash_hasla)
        else:
            conn.commit()
            conn.close()
            return False

    ### REPORTS

    @staticmethod
    def average_work_time_between_dates_report(start_date: datetime = datetime.min, end_date: datetime = datetime.max) -> dict[Pracownik, timedelta]:
        """Zwraca średni czas pracy każdego pracownika pomiędzy określonymi datami"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Pracownicy.id_karty, COALESCE(AVG(strftime('%s', czas_wyjscia) - strftime('%s', czas_wejscia)), 0) AS avg_work_time
            FROM Pracownicy
            LEFT JOIN Odbicia ON Pracownicy.id_karty = Odbicia.id_karty AND czas_wyjscia IS NOT NULL AND czas_wejscia BETWEEN ? AND ?
            GROUP BY Pracownicy.id_karty
        ''', (start_date.strftime(DB_DATETIME_FORMAT), end_date.strftime(DB_DATETIME_FORMAT)))

        average_times = {}
        rows = cursor.fetchall()

        for row in rows:
            id_karty, avg_work_time = row
            average_times[DbManager.read_pracownik(id_karty)] = timedelta(seconds=avg_work_time)

        conn.close()
        return average_times

    @staticmethod
    def total_work_time_between_dates_report(start_date: datetime = datetime.min, end_date: datetime = datetime.max) -> dict[Pracownik, timedelta]:
        """Zwraca całkowity czas pracy każdego pracownika pomiędzy określonymi datami"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Pracownicy.id_karty, SUM(COALESCE(strftime('%s', czas_wyjscia) - strftime('%s', czas_wejscia), 0)) AS total_work_time
            FROM Pracownicy
            LEFT JOIN Odbicia ON Pracownicy.id_karty = Odbicia.id_karty AND czas_wyjscia IS NOT NULL  AND czas_wejscia BETWEEN ? AND ?
            GROUP BY Pracownicy.id_karty
        ''', (start_date.strftime(DB_DATETIME_FORMAT), end_date.strftime(DB_DATETIME_FORMAT)))

        total_times = {}
        rows = cursor.fetchall()

        for row in rows:
            id_karty, total_work_time_seconds = row
            total_times[DbManager.read_pracownik(id_karty)] = timedelta(seconds=total_work_time_seconds)

        conn.close()
        return total_times

    @staticmethod
    def total_work_units_between_dates_report(start_date: datetime = datetime.min, end_date: datetime = datetime.max) -> dict[Pracownik, int]:
        """Zwraca ile razy w pracy był każdy pracownik pomiędzy określonymi datami"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Pracownicy.id_karty, COUNT(Odbicia.id_odbicia) AS total_work_units
            FROM Pracownicy
            LEFT JOIN Odbicia ON Pracownicy.id_karty = Odbicia.id_karty and czas_wyjscia IS NOT NULL AND czas_wejscia BETWEEN ? AND ?
            GROUP BY Pracownicy.id_karty
        ''', (start_date.strftime(DB_DATETIME_FORMAT), end_date.strftime(DB_DATETIME_FORMAT)))

        total_work_units = {}
        rows = cursor.fetchall()

        for row in rows:
            id_karty, count = row
            total_work_units[DbManager.read_pracownik(id_karty)] = count

        conn.close()
        return total_work_units