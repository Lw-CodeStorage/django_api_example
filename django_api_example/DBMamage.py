# 使用物件的好處，免若function參數很多，可以避免參數於程式碼中傳遞
# 可以做到開放封閉原則，新的功能修改，可繼承覆寫不須修改既有程式碼，減低風險

from abc import ABC, abstractmethod
from django.conf import settings
from sqlalchemy import create_engine,text,Table, MetaData, select
from sqlalchemy.orm import sessionmaker


class Database(ABC):
    def __init__(self,):
        self.engine = None
        self.Session = sessionmaker(bind=self.engine)
    
    @abstractmethod
    def _create_enging(self):
        """建立資料庫連接器"""
        pass

    @abstractmethod
    def dataframe_insert(self):
        pass

    @abstractmethod
    def dataframe_select(self):
        pass

class Postgresql(Database):

    def _create_enging(self,db_type):
        db_config = settings.DATABASES['default']
        self.engine = create_engine(f"postgresql+psycopg2://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}?options={db_config['OPTIONS']['options']}")
        


class Maria(Database):

    def __init__(self,db_type):
        self.engine = create_engine(db_type)

    def _create_enging(self,db_type):
        db_config = settings.DATABASES['maria']
        engine = create_engine(f"postgresql+psycopg2://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}")
        return 

