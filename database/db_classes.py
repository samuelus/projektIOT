from datetime import datetime
from database.db_constants import DB_DATETIME_FORMAT

class Odbicie:
    def __init__(self, data: tuple) -> None:
        self.id_odbicia = data[0]
        self.id_karty = data[1]
        self.id_strefy = data[2]
        self.czas_wejscia = datetime.strptime(data[3], DB_DATETIME_FORMAT)
        self.czas_wyjscia = datetime.strptime(data[4], DB_DATETIME_FORMAT) if data[4] != None else None

    def __repr__(self) -> str:
        return f"Odbicie (id_odbicia: {self.id_odbicia}, id_karty: '{self.id_karty}', id_strefy: {self.id_strefy}, czas_wejscia: '{self.czas_wejscia}', czas_wyjscia: '{self.czas_wyjscia}')"

class Pracownik:
    def __init__(self, data: tuple) -> None:
        self.id_karty = data[0]
        self.imie = data[1]
        self.nazwisko = data[2]

    def __repr__(self) -> str:
        return f"Pracownik (id_karty: {self.id_karty}, imie: {self.imie}, nazwisko: {self.nazwisko})"

class Uprawnienia:
    def __init__(self, data: tuple) -> None:
        self.id_karty = data[0]
        self.id_strefy = data[1]
    
    def __repr__(self) -> str:
        return f"Uprawnienia (id_karty: {self.id_karty}, id_strefy: {self.id_strefy})"

class Strefa:
    def __init__(self, data: tuple) -> None:
        self.id_strefy = data[0]
        self.nazwa = data[1]

    def __repr__(self) -> str:
        return f"Strefa (id_strefy: {self.id_strefy}, nazwa: {self.nazwa})"

class Admin:
    def __init__(self, data: tuple) -> None:
        self.login = data[0]
        self.hash_hasla = data[1]

    def __repr__(self) -> str:
        return f"Admin (login: {self.login}, hash_hasla: {self.hash_hasla})"
