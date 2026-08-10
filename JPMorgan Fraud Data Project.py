import mysql.connector
import numpy as np
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

conn = mysql.connector.connect(
    host = "Input Host",
    username = "Please Enter Your Username",
    password = "Enter Your Password",
    database = "Enter Your Database"
)

np.random.seed(50)

Fraud_list = 50

fraud_teams = np.random.choice(
    ['Fraud Ops','Card Services','Claims','Wire Recall','Escalations'],
    size = Fraud_list,
    p = [0.16,0.16,0.16, 0.29, 0.23] # p would have to equal to a value of 1 or else it will raises an error...
)

reference = [f'AGT{i:05d}' for i in range (1, Fraud_list + 1)]

Fraud_sites = 50

fraud_locations = np.random.choice(
    ['Columbus','Tempe','San Antonio','Manila'],
    size = Fraud_sites, 
    p = [0.250, 0.130, 0.407,0.213] # Value will equal to 1
)

offsets = np.random.randint(0, 2190, size = Fraud_list)
hire_dates = [date.today() - timedelta(days = int(d)) for d in offsets]

rows = list(zip(reference, fraud_teams.tolist(), hire_dates, fraud_locations.tolist()))

SQL = "INSERT INTO agents (agent_ref, team, hire_date, site) VALUES (%s, %s, %s, %s)"

cursor = conn.cursor()
cursor.executemany(SQL, rows)
conn.commit()
print(rows[:5])



