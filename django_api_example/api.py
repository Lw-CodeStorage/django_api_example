from ninja import NinjaAPI
import pandas as pd
from django.conf import settings
from sqlalchemy import create_engine,text,Table, MetaData, select
from sqlalchemy.orm import sessionmaker

api = NinjaAPI()
db_config = settings.DATABASES["default"]
# connect 
engine = create_engine(f"postgresql+psycopg2://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}?options={db_config['OPTIONS']['options']}")

# 創建 Session 類別
Session = sessionmaker(bind=engine)
session = Session()


@api.get("/get_data")
def get_data(request):
    try:
        data = pd.read_sql(
            con=engine,
            sql=text('SELECT * FROM public.user where id = :user_id'),
            params={"user_id":1}
            ) 
        return data.to_dict(orient='records')
    
    except Exception as e:
        return e
    
@api.get("/insert_data")
def insert_data(request):
# session，不需要處理commit、rollback
    try:
       with engine.begin() as conn:
            user_data = [{"name":'A'},{"name":'B'}]
            post_data = [{"user_id":1,"title":"測試"}]
            user_df = pd.DataFrame(user_data)
            post_df = pd.DataFrame(post_data)
            user_df.to_sql('user', con=conn, if_exists='append', index=False) # type: ignore
            post_df.to_sql('post',con=conn,if_exists="append",index=False)
            # raise Exception("Test exception")  # 模擬異常 
            # session.commit()
    except Exception as e:
        # session.rollback()
        return e


@api.get("/add_session")
def add_session(request, text:str):
    request.session['name'] = text # 設置lucky_number
    return {"message": "Session has been set"}

@api.get("/get_sesion")
def get_sesion(request):
    return {"message": request.session.get("name")}