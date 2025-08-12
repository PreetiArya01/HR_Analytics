from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="RISHI@garv1222",  
    host="localhost",
    port=3306,
    database="hr_analytics",
    query={"charset": "utf8mb4"}
)

engine = create_engine(connection_url)


for name in ["employees","performance","salaries","trainings","exits"]:
    df = pd.read_csv(f"Data/{name}.csv")
    df.to_sql(name, con=engine, if_exists="append", index =False)
    print("Loaded:",name)
