# Python Extract Transform Load Example
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, URL


load_dotenv()

DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")


conn = psycopg2.connect(
    database = DATABASE,
    user= USER,
    password= PASSWORD,
    host = HOST,
    port= PORT,     
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM collegename")
               
               #INSERT INTO collegename(id,name,alphatwocode, webpages, state, country, domain) values ('1','Marywood University','US','http://www.marywood.edu','null','United States', 'marywood.edu' ) 

data = cursor.fetchall()
for d in data:   
    print (d)     
conn.close()

def extract()-> dict:
    "This API extracts data from  http://universities.hipolabs.com/search?country=United+States "
    API_URL ="http://universities.hipolabs.com/search?country=United+States"
    data = requests.get(API_URL).json()
    return data

def transform(data:dict)-> pd.DataFrame:
    "Transforms the data set into desired structure and filters"
    df = pd.DataFrame(data)
    print(f"Total Number of Universities from API {len(data)}")
    df = df[df["name"].str.contains('California')]
    print(f"Number of universities in California {len(df)}")
    df["domains"] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(str,l))for l in df['web_pages']]
    df = df.reset_index(drop= True)
    return df[["domains", "country", "web_pages","name"]]

def load(df:pd.DataFrame)-> None:
     "loads data into Postgresql database" 
     
     connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=USER,
        password=PASSWORD,
        host=HOST,
        port=int(PORT),
        database=DATABASE
    )
     #disk_engine = create_engine('sqlite:///my_lite_store')
     #disk_engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:5432/{database}')
     disk_engine = create_engine(connection_url)
         
         #f'postgresql://{user}:{password}@{server}:{port}/{database}')
     
      #disk_engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, database))
     df.to_sql('cal_uni', disk_engine, if_exists='replace')
     print(f"Successfully loaded {len(df)} records into PostgreSQL!")
     
     
     
data = extract()
df= transform(data)
load(df)          
     
     