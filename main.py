from database.db_manager import DbManager
from datetime import datetime

if (__name__ == '__main__'):
    DbManager.clear_database(insert_dummy_values=True)

    print(DbManager.is_login_and_password_correct("root", "root"))
    print(DbManager.is_login_and_password_correct("root", "root1"))
    print(DbManager.is_login_and_password_correct("root1", "root1"))
    print(DbManager.is_login_and_password_correct("root1", "root"))
