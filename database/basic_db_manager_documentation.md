# DbManager Class Documentation

## Overview
`DbManager` is a class that manages database operations for a system handling entries such as access records and user management.

## Methods

### `clear_database(insert_dummy_values: bool) -> None`
- **Description**: Clears and rebuilds the whole database.
- **Parameters**: 
  - `insert_dummy_values` (`bool`): Determines whether to insert dummy values after clearing the database.
- **Returns**: None.

### `read_all_odbicia() -> list[Odbicie]`
- **Description**: Retrieves a list of all access records (`Odbicie`).
- **Returns**: `list[Odbicie]` - A list of `Odbicie` objects.

### `read_odbicie(id_odbicia: str) -> Odbicie | None`
- **Description**: Retrieves a specific access record by its ID.
- **Parameters**:
  - `id_odbicia` (`str`): The ID of the access record to retrieve.
- **Returns**: `Odbicie` if found, otherwise `None`.

### `create_odbicie(id_karty: str, id_strefy: int, czas_wejscia: datetime, czas_wyjscia: datetime = None) -> int`
- **Description**: Adds a new access record to the database.
- **Parameters**:
  - `id_karty` (`str`): Card ID.
  - `id_strefy` (`int`): Zone ID.
  - `czas_wejscia` (`datetime`): Entry time.
  - `czas_wyjscia` (`datetime`, optional): Exit time.
- **Returns**: `int` - The ID of the newly created record.

### `update_odbicie(id_odbicia: int, new_id_karty: str, new_id_strefy: int, new_czas_wejscia: datetime, new_czas_wyjscia: datetime = None) -> bool`
- **Description**: Updates an existing access record.
- **Parameters**:
  - `id_odbicia` (`int`): The ID of the record to update.
  - `new_id_karty` (`str`): New card ID.
  - `new_id_strefy` (`int`): New zone ID.
  - `new_czas_wejscia` (`datetime`): New entry time.
  - `new_czas_wyjscia` (`datetime`, optional): New exit time.
- **Returns**: `bool` - True if the record exists and was updated, False otherwise.

### `delete_odbicie(id_odbicia: int) -> bool`
- **Description**: Deletes an access record from the database.
- **Parameters**:
  - `id_odbicia` (`int`): The ID of the record to delete.
- **Returns**: `bool` - True if the record existed and was deleted, False otherwise.

### `read_all_pracownicy() -> list[Pracownik]`
- **Description**: Retrieves a list of all employees (`Pracownik`).
- **Returns**: `list[Pracownik]` - A list of `Pracownik` objects.

### `read_pracownik(id_karty: str) -> Pracownik | None`
- **Description**: Retrieves a specific employee by their card ID.
- **Parameters**:
  - `id_karty` (`str`): The card ID of the employee.
- **Returns**: `Pracownik` if found, otherwise `None`.

### `create_pracownik(id_karty: str, imie: str, nazwisko: str) -> bool`
- **Description**: Adds a new employee to the database.
- **Parameters**:
  - `id_karty` (`str`): Card ID of the new employee.
  - `imie` (`str`): First name of the new employee.
  - `nazwisko` (`str`): Last name of the new employee.
- **Returns**: `bool` - True if the employee is successfully added, False if the card ID already exists.

### `update_pracownik(id_karty: str, new_imie: str, new_nazwisko: str) -> bool`
- **Description**: Updates an existing employee's details.
- **Parameters**:
  - `id_karty` (`str`): Card ID of the employee to update.
  - `new_imie` (`str`): New first name.
  - `new_nazwisko` (`str`): New last name.
- **Returns**: `bool` - True if the record exists and was updated, False otherwise.

### `delete_pracownik(id_karty: str) -> bool`
- **Description**: Deletes an employee from the database.
- **Parameters**:
  - `id_karty` (`str`): The card ID of the employee to delete.
- **Returns**: `bool` - True if the record existed and was deleted, False otherwise.

### `read_all_uprawnienia() -> list[Uprawnienia]`
- **Description**: Retrieves a list of all access permissions (`Uprawnienia`).
- **Returns**: `list[Uprawnienia]` - A list of `Uprawnienia` objects.

### `create_uprawnienia(id_karty: str, id_strefy: int) -> bool`
- **Description**: Adds new access permissions to the database.
- **Parameters**:
  - `id_karty` (`str`): Card ID.
  - `id_strefy` (`int`): Zone ID.
- **Returns**: `bool` - True if the permissions are successfully added, False if they already exist.

### `delete_uprawnienia(id_karty: str, id_strefy: int) -> bool`
- **Description**: Deletes access permissions from the database.
- **Parameters**:
  - `id_karty` (`str`): Card ID.
  - `id_strefy` (`int`): Zone ID.
- **Returns**: `bool` - True if the permissions existed and were deleted, False otherwise.

### `read_all_strefy() -> list[Strefa]`
- **Description**: Retrieves a list of all zones (`Strefa`).
- **Returns**: `list[Strefa]` - A list of `Strefa` objects.

### `read_strefa(id_strefy: int) -> Strefa | None`
- **Description**: Retrieves a specific zone by its ID.
- **Parameters**: id_strefy (int): The ID of the zone to retrieve.
- **Returns**: Strefa if found, otherwise None.

### `create_strefa(nazwa: str) -> int`
- **Opis**: Dodaje nową strefę do bazy danych.
- **Parametry**:
  - `nazwa` (`str`): Nazwa nowej strefy.
- **Zwraca**: `int` - ID nowo utworzonej strefy.

### `update_strefa(id: int, new_nazwa: str) -> bool`
- **Opis**: Aktualizuje dane strefy o podanym ID.
- **Parametry**:
  - `id` (`int`): ID strefy do aktualizacji.
  - `new_nazwa` (`str`): Nowa nazwa strefy.
- **Zwraca**: `bool` - False, jeśli rekord z podanym ID nie istnieje.

### `delete_strefa(id_strefy: int) -> bool`
- **Opis**: Usuwa strefę o podanym ID.
- **Parametry**:
  - `id_strefy` (`int`): ID strefy do usunięcia.
- **Zwraca**: `bool` - False, jeśli rekord z podanym ID nie istnieje.

### `read_all_administratorzy() -> list[Admin]`
- **Opis**: Zwraca listę wszystkich administratorów.
- **Zwraca**: `list[Admin]` - Lista obiektów `Admin`.

### `create_administrator(login: str, haslo: str) -> bool`
- **Opis**: Dodaje nowego administratora do bazy danych.
- **Parametry**:
  - `login` (`str`): Login nowego administratora.
  - `haslo` (`str`): Hasło nowego administratora.
- **Zwraca**: `bool` - False, jeśli podany login już istnieje.

### `update_administrator(login: str, new_haslo: str) -> bool`
- **Opis**: Aktualizuje dane administratora o podanym loginie.
- **Parametry**:
  - `login` (`str`): Login administratora do aktualizacji.
  - `new_haslo` (`str`): Nowe hasło administratora.
- **Zwraca**: `bool` - False, jeśli rekord z podanym loginem nie istnieje.

### `delete_administrator(login: str) -> bool`
- **Opis**: Usuwa administratora o podanym loginie.
- **Parametry**:
  - `login` (`str`): Login administratora do usunięcia.
- **Zwraca**: `bool` - False, jeśli rekord z podanym loginem nie istnieje lub jest to 'root'.

### `odbij(id_karty: str, id_strefy: int, aktualny_czas: datetime) -> timedelta | None`
- **Opis**: Rejestruje odbicie karty w strefie; zwraca czas pracy, jeśli to odbicie wyjściowe.
- **Parametry**:
  - `id_karty` (`str`): ID karty.
  - `id_strefy` (`int`): ID strefy.
  - `aktualny_czas` (`datetime`): Aktualny czas.
- **Zwraca**: `timedelta` jeśli to odbicie wyjściowe, w przeciwnym razie `None`.

### `is_login_and_password_correct(login: str, haslo: str) -> bool`
- **Opis**: Sprawdza poprawność loginu i hasła administratora.
- **Parametry**:
  - `login` (`str`): Login administratora.
  - `haslo` (`str`): Hasło administratora.
- **Zwraca**: `bool` - True, jeśli dane są poprawne.

### `average_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> dict[Pracownik, timedelta]`
- **Opis**: Zwraca średni czas pracy każdego pracownika między podanymi datami.
- **Parametry**:
  - `start_date` (`datetime`): Data początkowa.
  - `end_date` (`datetime`): Data końcowa.
- **Zwraca**: `dict[Pracownik, timedelta]` - Słownik z pracownikami i ich średnim czasem pracy.

### `total_work_time_between_dates_report(start_date: datetime, end_date: datetime) -> dict[Pracownik, timedelta]`
- **Opis**: Oblicza całkowity czas pracy każdego pracownika w określonym przedziale czasowym.
- **Parametry**:
  - `start_date` (`datetime`, opcjonalnie): Data początkowa przedziału czasowego (domyślnie najwcześniejsza możliwa data).
  - `end_date` (`datetime`, opcjonalnie): Data końcowa przedziału czasowego (domyślnie najpóźniejsza możliwa data).
- **Zwraca**: `dict[Pracownik, timedelta]` - Słownik zawierający pracowników i ich całkowity czas pracy w przedziale czasowym.

### `total_work_units_between_dates_report(start_date: datetime, end_date: datetime) -> dict[Pracownik, int]`
- **Opis**: Oblicza całkowitą liczbę jednostek pracy (np. dni) dla każdego pracownika w określonym przedziale czasowym.
- **Parametry**:
  - `start_date` (`datetime`, opcjonalnie): Data początkowa przedziału czasowego (domyślnie najwcześniejsza możliwa data).
  - `end_date` (`datetime`, opcjonalnie): Data końcowa przedziału czasowego (domyślnie najpóźniejsza możliwa data).
- **Zwraca**: `dict[Pracownik, int]` - Słownik zawierający pracowników i liczbę ich jednostek pracy w przedziale czasowym.
