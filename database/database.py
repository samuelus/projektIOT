import sqlite3
from datetime import datetime, timedelta
from typing import Dict

### ADMIN PANEL CRUD FUNCTIONS

#TODO: Funkcje get dla każdej tabeli zwracające odpowiedni typ danych

def add_odbicie(id_karty: str, id_strefy: int, czas_wejscia: datetime, czas_wyjscia: datetime = None) -> bool:
    """Dodaje nowe odbicie. Zwraca czy operacja się powiodła"""

def remove_odbicie(id_odbicia: int) -> bool:
    """Usuwa odbiecie. Zwraca czy operacja się powiodła"""

def add_pracownik(id_karty: str, imie: str, nazwisko: str) -> bool:
    """Tworzy nowego pracownika. Zwraca czy operacja się powiodła"""

def update_pracownik(id_karty: str, new_imie: str, new_nazwisko: str) -> bool:
    """Modyfikuje dane pracownika o danym numerze karty. Zwraca czy operacaj się powiodła"""

def remove_pracownik(id_karty: str) -> bool:
    """Usuwa pracownika o podanym numerze karty. Zwraca czy operacaj się powiodła"""

def add_uprawnienia(id_karty: str, id_strefy: int) -> bool:
    """Dodaje nowe uprawnienia. Zwraca czy operacja się powiodła"""

def remove_uprawnienia(id_karty: str, id_strefy: int) -> bool:
    """Usuwa uprawnienia. Zwraca czy operacja się powiodła"""

def add_strefa(nazwa: str):
    """Dodaje nową strefę"""

def update_strefa(id: int, new_nazwa: str) -> bool:
    """Modyfikuje dane strefy. zwraca czy operacaj się powiodła"""

def remove_strefa(id: int) -> bool:
    """Usuwa strefe o podanym id. Zwraca czy operacja się powiodła"""

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

def average_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> Dict[str, timedelta]:
    """Zwraca średni czas pracy każdego pracownika pomiędzy określonymi datami"""

def total_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> Dict[str, timedelta]:
    """Zwraca całkowity czas pracy każdego pracownika pomiędzy określonymi datami"""

def total_work_units_between_dates_report(start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Zwraca ile razy w pracy był każdy pracownik pomiędzy określonymi datami"""