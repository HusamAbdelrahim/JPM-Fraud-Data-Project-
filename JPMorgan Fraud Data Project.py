import mysql.connector
import numpy as np
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

conn = mysql.connector.connect(
    host = "",
    username = "",
    password = "",
    database = ""
)

import mysql.connector
import numpy as np
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv

np.random.seed(50)

N_AGENTS = 50

fraud_teams = np.random.choice(
    ['Fraud Ops','Card Services','Claims','Wire Recall','Escalations'],
    size = N_AGENTS,
    p = [0.16, 0.16, 0.16, 0.29, 0.23]
)

fraud_locations = np.random.choice(
    ['Columbus','Tempe','San Antonio','Manila'],
    size = N_AGENTS,
    p = [0.250, 0.130, 0.407, 0.213]
)

agent_reference = [f'AGT{i:05d}' for i in range(1, N_AGENTS + 1)]

offsets = np.random.randint(0, 2190, size = N_AGENTS)
hire_dates = [date.today() - timedelta(days = int(d)) for d in offsets]

agent_rows = list(zip(
    agent_reference,
    fraud_teams.tolist(),
    hire_dates,
    fraud_locations.tolist()
))

SQL_AGENTS = "INSERT INTO agents (agent_ref, team, hire_date, site) VALUES (%s, %s, %s, %s)"

cursor = conn.cursor()
cursor.executemany(SQL_AGENTS, agent_rows)
conn.commit()

print(agent_rows[:5])
print(min(hire_dates), max(hire_dates))

N_CUSTOMERS = 3000

age_band = np.random.choice(
    ['18-24','25-34','35-44','45-54','55-64','65+'],
    size = N_CUSTOMERS,
    p = [0.08, 0.22, 0.20, 0.18, 0.15, 0.17]
)

segment = np.random.choice(
    ['Consumer Banking','Private Client Banking','Financial Banking'],
    size = N_CUSTOMERS,
    p = [0.74, 0.16, 0.10]
)

states = np.random.choice(
    ['NY','CA','PA','MI','TX','MA','WA','KS','NJ','FL'],
    size = N_CUSTOMERS,
    p = [0.0733, 0.1600, 0.0333, 0.0800, 0.2067, 0.0267, 0.0200, 0.1600, 0.0933, 0.1467]
)

cities_by_state = {
    'NY': ['Buffalo', 'Albany', 'New York'],
    'CA': ['San Francisco', 'San Diego', 'Los Angeles'],
    'PA': ['Pittsburgh', 'Harrisburg', 'Philadelphia'],
    'MI': ['Grand Rapids', 'Lansing', 'Detroit'],
    'TX': ['Dallas', 'Austin', 'Houston'],
    'MA': ['Worcester', 'Springfield', 'Boston'],
    'WA': ['Spokane', 'Tacoma', 'Seattle'],
    'KS': ['Overland Park', 'Topeka', 'Wichita'],
    'NJ': ['Jersey City', 'Trenton', 'Newark'],
    'FL': ['Orlando', 'Tampa', 'Miami'],
}

city = [np.random.choice(cities_by_state[s]) for s in states]

digital_enrolled   = np.random.choice([True, False], size = N_CUSTOMERS, p = [0.85, 0.15])
paperless_flag     = np.random.choice([True, False], size = N_CUSTOMERS, p = [0.74, 0.26])
prior_fraud_claims = np.random.choice([0, 1, 2, 3], size = N_CUSTOMERS, p = [0.85, 0.10, 0.04, 0.01])

tenure_years = np.minimum(
    np.round(np.random.exponential(scale = 6, size = N_CUSTOMERS), 1),
    35
)

products_by_segment = {
    'Consumer Banking':       ['Total Checking', 'Premier Savings', 'Sapphire Preferred', 'Freedom Unlimited', 'Auto Loan'],
    'Private Client Banking': ['Private Client Checking', 'Private Client Savings', 'Financial Investment Account'],
    'Financial Banking':      ['Business Checking', 'Business Savings', 'Business Platinum'],
}

ZELLE_PRODUCTS = {
    'Total Checking', 'Premier Savings',
    'Private Client Checking', 'Private Client Savings',
    'Business Checking', 'Business Savings',
}

CARD_PRODUCTS = {
    'Debit Card', 'Sapphire Preferred', 'Freedom Unlimited',
    '', '', '',
}