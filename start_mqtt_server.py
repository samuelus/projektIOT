from database.db_manager import DbManager
from tms.mqtt_server import TMSLogicProcessor

if __name__ == '__main__':
    DbManager.clear_database(True)    
    tms_processor = TMSLogicProcessor()