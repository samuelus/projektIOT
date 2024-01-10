import sqlite3
from datetime import datetime, timedelta
from database.db_classes import Odbicie, Pracownik, Uprawnienia, Strefa, Admin
from database.db_constants import DB_NAME
from database.db_creator import reset_db

class DbManager:

    @staticmethod
    def clear_database(insert_dummy_values: bool = True) -> None:
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
    def add_odbicie(id_karty: str, id_strefy: int, czas_wejscia: datetime, czas_wyjscia: datetime = None) -> bool:
        """Dodaje nowe odbicie. Zwraca czy operacja się powiodła"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if czas_wyjscia is None:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia) VALUES (?, ?, ?)''', (id_karty, id_strefy, czas_wejscia.strftime('%Y-%m-%d %H:%M:%S')))
        else:
            cursor.execute('''INSERT INTO Odbicia (id_karty, id_strefy, czas_wejscia, czas_wyjscia) VALUES (?, ?, ?, ?)''', (id_karty, id_strefy, czas_wejscia.strftime('%Y-%m-%d %H:%M:%S'), czas_wyjscia.strftime('%Y-%m-%d %H:%M:%S')))
        changed_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return changed_rows > 0

    def remove_odbicie(id_odbicia: int) -> bool:
        """Usuwa odbiecie. Zwraca czy operacja się powiodła"""

    @staticmethod
    def get_pracownicy() -> list[Pracownik]:
        """Lista wszystkich pracowników"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Pracownicy''')
        pracownicy = [Pracownik(data) for data in cursor.fetchall()]
        conn.close()
        return pracownicy

    def add_pracownik(id_karty: str, imie: str, nazwisko: str) -> bool:
        """Tworzy nowego pracownika. Zwraca czy operacja się powiodła"""

    def update_pracownik(id_karty: str, new_imie: str, new_nazwisko: str) -> bool:
        """Modyfikuje dane pracownika o danym numerze karty. Zwraca czy operacaj się powiodła"""

    def remove_pracownik(id_karty: str) -> bool:
        """Usuwa pracownika o podanym numerze karty. Zwraca czy operacaj się powiodła"""

    @staticmethod
    def get_uprawnienia() -> list[Uprawnienia]:
        """Lista wszystkich uprawnień"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM UprawnieniaDostepu''')
        uprawnienia = [Uprawnienia(data) for data in cursor.fetchall()]
        conn.close()
        return uprawnienia

    def add_uprawnienia(id_karty: str, id_strefy: int) -> bool:
        """Dodaje nowe uprawnienia. Zwraca czy operacja się powiodła"""

    def remove_uprawnienia(id_karty: str, id_strefy: int) -> bool:
        """Usuwa uprawnienia. Zwraca czy operacja się powiodła"""

    @staticmethod
    def get_strefy() -> list[Strefa]:
        """Lista wszystkich stref"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Strefy''')
        strefy = [Strefa(data) for data in cursor.fetchall()]
        conn.close()
        return strefy

    def add_strefa(nazwa: str):
        """Dodaje nową strefę"""

    def update_strefa(id: int, new_nazwa: str) -> bool:
        """Modyfikuje dane strefy. zwraca czy operacaj się powiodła"""

    def remove_strefa(id: int) -> bool:
        """Usuwa strefe o podanym id. Zwraca czy operacja się powiodła"""

    @staticmethod
    def get_admini() -> list[Admin]:
        """Lista wszystkich adminów"""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM Administratorzy''')
        admini = [Admin(data) for data in cursor.fetchall()]
        conn.close()
        return admini

    def add_admin(login: str, haslo: str) -> bool:
        """Dodaje nowego admina z podanym loginem i haslem. Zwraca czy operacaj sie powiodła"""

    def update_admin(login: str, new_haslo: str) -> bool:
        """Modyfikuje dane admina. Zwraca czy operacaj sie powiodła"""

    def remove_admin(login: str) -> bool:
        """Usuwa admina. Zwraca czy operacaj sie powiodła"""

    ### UTILITY
        
    def odbij(id_karty: str, id_strefy: int, aktualny_czas: datetime) -> timedelta:
        """Jeżeli odbicie to oznacza rozpoczęcie pracy - zwraca None; jeżeli zakończenie - zwraca długość pracy"""

    def is_login_and_password_correct(login: str, haslo: str) -> bool:
        """Sprawdza czy podane dane logowania admina są poprawne"""

    ### REPORTS

    def average_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> dict[str, timedelta]:
        """Zwraca średni czas pracy każdego pracownika pomiędzy określonymi datami"""

    def total_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> dict[str, timedelta]:
        """Zwraca całkowity czas pracy każdego pracownika pomiędzy określonymi datami"""

    def total_work_units_between_dates_report(start_date: datetime, end_date: datetime) -> dict[str, int]:
        """Zwraca ile razy w pracy był każdy pracownik pomiędzy określonymi datami"""