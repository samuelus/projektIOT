from database.db_manager import DbManager
from datetime import datetime

if (__name__ == '__main__'):
    DbManager.clear_database()

    print(DbManager.get_odbicia())
    DbManager.add_odbicie("ID_K", 100, datetime.now())
    print(DbManager.get_odbicia())
