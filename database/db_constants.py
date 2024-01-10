from database.cryptography import hash_password

DB_NAME = 'database.db'
DB_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

ROOT_LOGIN = 'root'
DEFAULT_ROOT_HASHED_PASSWORD = hash_password('root')

DUMMY_PRACOWNICY = [
    ('aff123f5agg2', 'Marcin', 'Kowalski'),
    ('h231yu8x21f3', 'Anna', 'Nowak'),
    ('ddzp81l38vj1', 'Piotr', 'Wiśniewski')
]
DUMMY_ODBICIA = [
    ('aff123f5agg2', '1', '2023-01-01 08:00:00', '2023-01-01 16:00:00'),
    ('aff123f5agg2', '1', '2023-01-02 10:00:00', '2023-01-02 16:00:00'),
    ('ddzp81l38vj1', '1', '2023-01-02 07:30:00', '2023-01-03 15:30:00'),
    ('ddzp81l38vj1', '1', '2023-01-03 07:30:00', None)
]
DUMMY_UPRAWNIENIA = [
    ('aff123f5agg2', 1),
    ('h231yu8x21f3', 1),
    ('ddzp81l38vj1', 1)
]
DUMMY_STREFY = [
    ('Strefa A',),
    ('Strefa B',)
]
DUMMY_ADMINISTRATORZY = [
    ('admin1', hash_password('haslo1')),
    ('admin2', hash_password('haslo2'))
]