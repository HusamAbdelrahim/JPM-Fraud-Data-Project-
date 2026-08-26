import math
import mysql.connector
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

conn = mysql.connector.connect(
    host = "",
    user = "",
    password = "",
    database = ""
)


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

city = [str(np.random.choice(cities_by_state[s])) for s in states]

digital_enrolled = np.random.choice([True, False], size = N_CUSTOMERS, p = [0.85, 0.15])
paperless_flag = np.random.choice([True, False], size = N_CUSTOMERS, p = [0.74, 0.26])
prior_fraud_claims = np.random.choice([0, 1, 2, 3], size = N_CUSTOMERS, p = [0.85, 0.10, 0.04, 0.01])

tenure_years = np.minimum(
    np.round(np.random.exponential(scale = 6, size = N_CUSTOMERS), 1),
    35
)

customer_id = list(range(1, N_CUSTOMERS + 1))
customer_ref = [f'CUS{i:07d}' for i in customer_id]

customer_rows = list(zip(
    customer_id,
    customer_ref,
    age_band.tolist(),
    segment.tolist(),
    states.tolist(),
    city,
    tenure_years.tolist(),
    digital_enrolled.tolist(),
    paperless_flag.tolist(),
    prior_fraud_claims.tolist()
))

SQL_CUSTOMERS = """INSERT INTO customers
(customer_id, customer_ref, age_band, segment, state, city,
tenure_years, digital_enrolled, paperless_flag, prior_fraud_claims)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

cursor.executemany(SQL_CUSTOMERS, customer_rows)
conn.commit()

print(customer_rows[:5])

accts = N_CUSTOMERS

account_id = list(range(1, accts + 1))
account_ref = [f'ACC{i:09d}' for i in account_id]

products_by_segment = {
    'Consumer Banking': ['Total Checking', 'Premier Savings', 'Sapphire Preferred', 'Freedom Unlimited', 'Auto Loan'],
    'Private Client Banking':['Private Client Checking', 'Private Client Savings', 'Financial Investment Account'],
    'Financial Banking': ['Business Checking', 'Business Savings', 'Business Platinum'],
}

ZELLE_PRODUCTS = {
    'Total Checking', 'Premier Savings',
    'Private Client Checking', 'Private Client Savings',
    'Business Checking', 'Business Savings',
}

CARD_PRODUCTS = {
    'Total Checking', 'Sapphire Preferred', 'Freedom Unlimited',
    'Private Client Checking', 'Business Checking', 'Business Platinum',
}

product_name = [str(np.random.choice(products_by_segment[s])) for s in segment]

open_date = [date.today() - timedelta(days = int(np.random.randint(0, max(1, int(t * 365))))) for t in tenure_years]

balance_band = np.random.choice(
    ['<$1K','$1K-5K','$5K-25K','$25K-100K','$100K+'],
    size = accts,
    p = [0.28, 0.30, 0.24, 0.13, 0.05]
)

account_status = np.random.choice(
    ['active','closed','restricted'],
    size = accts,
    p = [0.92, 0.06, 0.02]
)

zelle_enabled = [p in ZELLE_PRODUCTS for p in product_name]
card_present_capable = [p in CARD_PRODUCTS for p in product_name]

account_rows = list(zip(
    account_id,
    account_ref,
    customer_id,
    product_name,
    open_date,
    balance_band.tolist(),
    zelle_enabled,
    card_present_capable,
    account_status.tolist()
))

SQL_ACCOUNTS = """INSERT INTO accounts
(account_id, account_ref, customer_id, product_name, open_date,
balance_band, zelle_enabled, card_present_capable, account_status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

cursor.executemany(SQL_ACCOUNTS, account_rows)
conn.commit()

print(account_rows[:5])

N_CASES = 10000

WINDOW_START = date(2024, 1, 1)
WINDOW_END = date(2026, 6, 30)

cursor.execute("""SELECT fraud_type_id, type_code, category, is_scam,
baseline_recovery_rate, median_loss_target FROM fraud_types""")

type_params = {}
for row in cursor.fetchall():
    type_params[row[1]] = {
        'id': row[0],
        'category': row[2],
        'is_scam': bool(row[3]),
        'baseline_recovery': float(row[4]),
        'median_loss': float(row[5])
    }

TYPE_CONFIG = {
    'CNP_CARD': dict(weight = 0.30, sigma = 0.85, detect_med = 12, report_med = 8, decay_h = 3000, txn_lam = 2.4, channels = [1, 2, 6], cross_border = 0.22),
    'SKIMMING': dict(weight = 0.08, sigma = 0.80, detect_med = 48, report_med = 18, decay_h = 2000, txn_lam = 3.1, channels = [3, 6], cross_border = 0.10),
    'PHISHING': dict(weight = 0.12, sigma = 1.00, detect_med = 72, report_med = 20, decay_h = 800, txn_lam = 2.0, channels = [1, 2], cross_border = 0.18),
    'ATO': dict(weight = 0.09, sigma = 1.10, detect_med = 96, report_med = 24, decay_h = 600, txn_lam = 3.6, channels = [1, 2], cross_border = 0.24),
    'ZELLE_SCAM': dict(weight = 0.15, sigma = 0.95, detect_med = 6, report_med = 10, decay_h = 100, txn_lam = 1.6, channels = [2, 1], cross_border = 0.04),
    'CHECK_FRAUD': dict(weight = 0.07, sigma = 1.05, detect_med = 240, report_med = 48, decay_h = 1200, txn_lam = 1.4, channels = [4, 3], cross_border = 0.05),
    'BEC_WIRE': dict(weight = 0.03, sigma = 1.20, detect_med = 48, report_med = 12, decay_h = 40, txn_lam = 1.2, channels = [7, 1], cross_border = 0.55),
    'SYNTH_ID': dict(weight = 0.08, sigma = 1.15, detect_med = 2400, report_med = 72, decay_h = 2000, txn_lam = 2.8, channels = [1, 4], cross_border = 0.16),
    'ELDER_EXP': dict(weight = 0.04, sigma = 1.25, detect_med = 1440, report_med = 96, decay_h = 300, txn_lam = 6.5, channels = [4, 5, 7], cross_border = 0.30),
    'TECH_SUPPORT': dict(weight = 0.03, sigma = 1.00, detect_med = 48, report_med = 16, decay_h = 200, txn_lam = 2.2, channels = [1, 2, 5], cross_border = 0.28),
    'INSIDER': dict(weight = 0.01, sigma = 1.10, detect_med = 2880, report_med = 24, decay_h = 4000, txn_lam = 8.0, channels = [4, 7], cross_border = 0.08),
}

SUB_SCENARIOS = {
    'CNP_CARD': ['online retail', 'subscription abuse', 'digital wallet', 'card testing'],
    'SKIMMING': ['ATM skimmer', 'gas pump skimmer', 'POS shimmer'],
    'PHISHING': ['credential harvest', 'SMS link', 'fake login page', 'QR code'],
    'ATO': ['SIM swap', 'credential stuffing', 'password reset abuse', 'session hijack'],
    'ZELLE_SCAM': ['fake marketplace seller', 'rental deposit', 'ticket resale', 'utility impersonation'],
    'CHECK_FRAUD': ['check washing', 'counterfeit check', 'mail theft', 'altered payee'],
    'BEC_WIRE': ['vendor invoice redirect', 'CEO impersonation', 'closing wire redirect', 'payroll diversion'],
    'SYNTH_ID': ['synthetic identity', 'stolen SSN', 'new account fraud', 'bust-out'],
    'ELDER_EXP': ['romance scam', 'grandparent scam', 'caregiver exploitation', 'lottery scam'],
    'TECH_SUPPORT': ['fake antivirus', 'bank impersonation', 'refund overpayment'],
    'INSIDER': ['employee siphoning', 'unauthorized access', 'data exfiltration'],
}

DETECTION_METHODS = {
    'CNP_CARD': (['Rules Engine', 'ML Model', 'Merchant Alert', 'Customer Reported'], [0.34, 0.30, 0.20, 0.16]),
    'SKIMMING': (['ML Model', 'Rules Engine', 'Customer Reported'], [0.34, 0.28, 0.38]),
    'PHISHING': (['Customer Reported', 'ML Model', 'Rules Engine'], [0.48, 0.30, 0.22]),
    'ATO': (['ML Model', 'Rules Engine', 'Customer Reported'], [0.40, 0.26, 0.34]),
    'ZELLE_SCAM': (['Customer Reported', 'Rules Engine'], [0.86, 0.14]),
    'CHECK_FRAUD': (['Statement Review', 'Branch Teller', 'Customer Reported'], [0.36, 0.24, 0.40]),
    'BEC_WIRE': (['Customer Reported', 'Rules Engine', 'ML Model'], [0.62, 0.22, 0.16]),
    'SYNTH_ID': (['ML Model', 'Statement Review', 'Customer Reported'], [0.44, 0.30, 0.26]),
    'ELDER_EXP': (['Branch Teller', 'Customer Reported', 'ML Model'], [0.42, 0.36, 0.22]),
    'TECH_SUPPORT': (['Customer Reported', 'Rules Engine'], [0.78, 0.22]),
    'INSIDER': (['Statement Review', 'ML Model', 'Rules Engine'], [0.48, 0.32, 0.20]),
}

OWNER_TEAMS = {
    'CNP_CARD': 'Card Services',
    'SKIMMING': 'Card Services',
    'PHISHING': 'Fraud Ops',
    'ATO': 'Fraud Ops',
    'ZELLE_SCAM': 'Claims',
    'CHECK_FRAUD': 'Claims',
    'BEC_WIRE': 'Wire Recall',
    'SYNTH_ID': 'Fraud Ops',
    'ELDER_EXP': 'Escalations',
    'TECH_SUPPORT': 'Claims',
    'INSIDER': 'Escalations',
}

months = []
y = WINDOW_START.year
m = WINDOW_START.month
while (y, m) <= (WINDOW_END.year, WINDOW_END.month):
    months.append((y, m))
    m = m + 1
    if m > 12:
        m = 1
        y = y + 1

def month_weights(type_code):
    w = []
    for pair in months:
        mm = pair[1]
        f = 1.0
        if type_code in ('CNP_CARD', 'SKIMMING') and mm in (11, 12):
            f = 1.45
        if type_code == 'SYNTH_ID' and mm in (1, 2, 3, 4):
            f = 1.40
        if type_code == 'ZELLE_SCAM' and mm in (6, 7, 8):
            f = 1.20
        w.append(f)
    total = sum(w)
    return [x / total for x in w]

def gamma_hours(median, n, shape = 2.0):
    scale = median / 1.678
    return np.random.gamma(shape, scale, size = n)

def random_ts(y, m):
    if m == 12:
        days = (date(y + 1, 1, 1) - date(y, 12, 1)).days
    else:
        days = (date(y, m + 1, 1) - date(y, m, 1)).days
    d = int(np.random.randint(1, days + 1))
    hh = int(np.random.randint(0, 24))
    mi = int(np.random.randint(0, 60))
    ss = int(np.random.randint(0, 60))
    return datetime(y, m, d, hh, mi, ss)

case_rows = []
case_counter = 1

for code in TYPE_CONFIG:
    cfg = TYPE_CONFIG[code]
    params = type_params[code]
    n = int(round(N_CASES * cfg['weight']))
    if n == 0:
        continue

    picks = np.random.choice(len(months), size = n, p = month_weights(code))
    starts = [random_ts(months[i][0], months[i][1]) for i in picks]

    detect_lag = gamma_hours(cfg['detect_med'], n)
    report_lag = gamma_hours(cfg['report_med'], n, shape = 1.6)

    mu = math.log(params['median_loss'])
    attempted = np.random.lognormal(mu, cfg['sigma'], size = n)
    attempted = np.minimum(attempted, params['median_loss'] * 60)

    full_loss = np.random.rand(n) < 0.72
    loss_ratio = np.where(full_loss, 1.0, np.random.uniform(0.05, 0.95, size = n))
    lost = attempted * loss_ratio

    decay = np.exp(-report_lag / cfg['decay_h'])
    decay = decay / decay.mean()
    noise = np.random.uniform(0.75, 1.25, size = n)
    rec_frac = np.clip(params['baseline_recovery'] * decay * noise, 0.0, 1.0)

    no_fraud = np.random.rand(n) < 0.10

    channels = np.random.choice(cfg['channels'], size = n)
    subs = np.random.choice(SUB_SCENARIOS[code], size = n)
    dm_vals = DETECTION_METHODS[code][0]
    dm_p = DETECTION_METHODS[code][1]
    methods = np.random.choice(dm_vals, size = n, p = dm_p)
    txns = np.maximum(1, np.random.poisson(cfg['txn_lam'], size = n))
    cross = np.random.rand(n) < cfg['cross_border']
    accounts_hit = np.random.randint(1, accts + 1, size = n)

    is_authorized = params['category'] == 'Authorized'
    if is_authorized:
        reimb_p = 0.12
    else:
        reimb_p = 0.94
    reimb = np.random.rand(n) < reimb_p

    for i in range(n):
        start = starts[i]
        detect = start + timedelta(hours = float(detect_lag[i]))

        reported = None
        if methods[i] == 'Customer Reported' or np.random.rand() < 0.55:
            reported = detect + timedelta(hours = float(report_lag[i]))

        if no_fraud[i]:
            amt_attempted = round(float(attempted[i]), 2)
            amt_lost = 0.00
            amt_recovered = 0.00
            status = 'Closed-No Fraud'
            resolution = detect + timedelta(days = float(np.random.uniform(1, 21)))
            reimbursed = False
            provisional = False
        else:
            amt_attempted = round(float(attempted[i]), 2)
            amt_lost = round(float(lost[i]), 2)
            amt_recovered = round(min(amt_lost, amt_lost * float(rec_frac[i])), 2)

            roll = np.random.rand()
            if roll < 0.08:
                status = 'Open'
                resolution = None
            elif roll < 0.15:
                status = 'Under Review'
                resolution = None
            else:
                if reported is not None:
                    anchor = reported
                else:
                    anchor = detect
                resolution = anchor + timedelta(days = float(np.random.gamma(2.0, 9.0)))
                if amt_recovered == 0:
                    status = 'Written Off'
                else:
                    status = 'Closed-Confirmed'

            reimbursed = bool(reimb[i])
            provisional = False
            if not is_authorized and reported is not None:
                gap = (reported - detect).total_seconds() / 3600
                if gap < 240 and np.random.rand() < 0.65:
                    provisional = True

        case_rows.append((
            f'FRD{case_counter:09d}',
            int(accounts_hit[i]),
            params['id'],
            int(channels[i]),
            str(subs[i]),
            str(methods[i]),
            start,
            detect,
            reported,
            resolution,
            amt_attempted,
            amt_lost,
            amt_recovered,
            int(txns[i]),
            status,
            reimbursed,
            provisional,
            bool(cross[i]),
            OWNER_TEAMS[code]
        ))
        case_counter = case_counter + 1

np.random.shuffle(case_rows)

SQL_CASES = """INSERT INTO fraud_cases
(case_ref, account_id, fraud_type_id, channel_id, sub_scenario,
detection_method, fraud_start_ts, detection_ts, customer_report_ts,
resolution_ts, amount_attempted, amount_lost, amount_recovered,
transaction_count, case_status, reimbursed_flag,
provisional_credit_flag, cross_border_flag, case_owner_team)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

cursor.executemany(SQL_CASES, case_rows)
conn.commit()

print(len(case_rows))

cursor.close()
conn.close()