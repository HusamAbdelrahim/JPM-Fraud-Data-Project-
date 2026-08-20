DROP DATABASE IF EXISTS fraud_sections;
CREATE SCHEMA fraud_sections DEFAULT CHARACTER SET utf8mb4;
USE fraud_sections;
SELECT COUNT(*) FROM fraud_cases;

CREATE TABLE fraud_types (
    fraud_type_id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    type_code VARCHAR(30) NOT NULL UNIQUE,
    type_name VARCHAR(60) NOT NULL,
    category VARCHAR(20),
    is_scam BOOLEAN NOT NULL,
    baseline_recovery_rate DECIMAL(4,3) CHECK (baseline_recovery_rate BETWEEN 0 AND 1),
    median_loss_target DECIMAL(12,2)
);

CREATE TABLE channels (
    channel_id TINYINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    channel_name VARCHAR(30) NOT NULL,
    is_digital BOOLEAN NOT NULL
);

CREATE TABLE agents (
    agent_id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    agent_ref CHAR(8) UNIQUE,
    team VARCHAR(40),
    hire_date DATE,
    site VARCHAR(30)
);

CREATE TABLE customers (
    customer_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_ref CHAR(10) UNIQUE,
    age_band VARCHAR(10),
    segment VARCHAR(30),
    state CHAR(2),
    city VARCHAR(60),
    tenure_years DECIMAL(4,1),
    digital_enrolled BOOLEAN,
    paperless_flag BOOLEAN,
    prior_fraud_claims TINYINT UNSIGNED DEFAULT 0
);

CREATE TABLE accounts (
    account_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_ref CHAR(12) UNIQUE,
    customer_id INT UNSIGNED,
    product_name VARCHAR(40),
    open_date DATE,
    balance_band VARCHAR(20),
    zelle_enabled BOOLEAN,
    card_present_capable BOOLEAN,
    account_status ENUM('active','closed','restricted') NOT NULL DEFAULT 'active',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE fraud_cases (
    case_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    case_ref CHAR(12) UNIQUE,
    account_id INT UNSIGNED,
    fraud_type_id TINYINT UNSIGNED NOT NULL,
    channel_id  TINYINT UNSIGNED,
    sub_scenario VARCHAR(60),
    detection_method VARCHAR(40),
    fraud_start_ts DATETIME NOT NULL,
    detection_ts DATETIME,
    customer_report_ts DATETIME NULL,
    resolution_ts DATETIME NULL,
    amount_attempted DECIMAL(12,2) NOT NULL,
    amount_lost DECIMAL(12,2) NOT NULL,
    amount_recovered DECIMAL(12,2) NOT NULL DEFAULT 0,
    transaction_count SMALLINT UNSIGNED,
    case_status ENUM('Open','Under Review','Closed-Confirmed','Closed-No Fraud','Written Off'),
    reimbursed_flag BOOLEAN,
    provisional_credit_flag BOOLEAN,
    cross_border_flag BOOLEAN,
    case_owner_team VARCHAR(40),

    FOREIGN KEY (fraud_type_id) REFERENCES fraud_types(fraud_type_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),

    CONSTRAINT chk_detect_after_start CHECK (detection_ts >= fraud_start_ts),
    CONSTRAINT chk_loss_range CHECK (amount_lost >= 0 AND amount_lost <= amount_attempted),
    CONSTRAINT chk_recovery_range CHECK (amount_recovered >= 0 AND amount_recovered <= amount_lost)
);

CREATE INDEX idx_cases_start_ts ON fraud_cases (fraud_start_ts);
CREATE INDEX idx_cases_status ON fraud_cases (case_status);
CREATE INDEX idx_cases_type_status ON fraud_cases (fraud_type_id, case_status);

INSERT INTO channels (channel_id, channel_name, is_digital) VALUES
    (1, 'Online Banking', 1),
    (2, 'Mobile App',1),
    (3, 'ATM', 0),
    (4, 'Branch', 0),
    (5, 'Phone', 0),
    (6, 'Card Terminal', 0),
    (7, 'Wire Room',0);

INSERT INTO fraud_types
    (fraud_type_id, type_code, type_name, category, is_scam,
     baseline_recovery_rate, median_loss_target)
VALUES
    (1,  'CNP_CARD','Card-Not-Present', 'Unauthorized', 0, 0.900,  180.00),
    (2,  'SKIMMING','Card Skimming/ATM','Unauthorized', 0, 0.750, 600.00),
    (3,  'PHISHING', 'Phishing/Smishing', 'Unauthorized', 1, 0.550, 1900.00),
    (4,  'ATO', 'Account Takeover', 'Unauthorized', 0, 0.450, 4200.00),
    (5,  'ZELLE_SCAM','Zelle/P2P Scam','Authorized',   1, 0.120, 850.00),
    (6,  'CHECK_FRAUD','Check Fraud/Washing', 'Unauthorized', 0, 0.400, 3400.00),
    (7,  'BEC_WIRE','Business Email Compromise', 'Authorized',   1, 0.350, 86000.00),
    (8,  'SYNTH_ID', 'Identity Theft/Synthetic', 'Unauthorized', 0, 0.200,9500.00),
    (9,  'ELDER_EXP','Elder Exploitation/Romance','Authorized',   1, 0.080,22000.00),
    (10, 'TECH_SUPPORT','Tech Support/Impersonation','Authorized',   1, 0.250, 5100.00),
    (11, 'INSIDER', 'Insider/Employee', 'Unauthorized', 0, 0.600, 140000.00);

SELECT
    fc.case_ref,
    ft.type_name AS fraud_type,
    ft.category,
    ft.is_scam,
    ch.channel_name,
    fc.sub_scenario,
    fc.detection_method,
    fc.case_owner_team,
    fc.case_status,
    fc.fraud_start_ts,
    DATE(fc.fraud_start_ts) AS fraud_date,
    fc.detection_ts,
    fc.customer_report_ts,
    fc.resolution_ts,
    fc.amount_attempted,
    fc.amount_lost,
    fc.amount_recovered,
    (fc.amount_lost - fc.amount_recovered) AS net_loss,
    ROUND(fc.amount_recovered / NULLIF(fc.amount_lost, 0), 4) AS recovery_rate,
    fc.transaction_count,
    fc.reimbursed_flag,
    fc.provisional_credit_flag,
    fc.cross_border_flag,
    TIMESTAMPDIFF(HOUR, fc.fraud_start_ts, fc.detection_ts) AS detect_lag_hours,
    TIMESTAMPDIFF(HOUR, fc.fraud_start_ts, fc.customer_report_ts) AS report_lag_hours,
    TIMESTAMPDIFF(DAY, fc.fraud_start_ts, fc.resolution_ts) AS resolution_days,
    CASE
        WHEN fc.customer_report_ts IS NULL THEN 'Never Reported'
        WHEN TIMESTAMPDIFF(HOUR, fc.fraud_start_ts, fc.customer_report_ts) < 24 THEN '1. <24h'
        WHEN TIMESTAMPDIFF(HOUR, fc.fraud_start_ts, fc.customer_report_ts) < 72 THEN '2. 24-72h'
        WHEN TIMESTAMPDIFF(HOUR, fc.fraud_start_ts, fc.customer_report_ts) < 168 THEN '3. 3-7d'
        ELSE '4. 7d+'
    END AS report_lag_band,
    a.product_name,
    a.balance_band,
    a.zelle_enabled,
    a.account_status,
    c.customer_ref,
    c.age_band,
    c.segment,
    c.state,
    c.city,
    c.tenure_years,
    c.digital_enrolled,
    c.prior_fraud_claims
FROM fraud_cases fc
JOIN fraud_types ft ON fc.fraud_type_id = ft.fraud_type_id
JOIN channels ch ON fc.channel_id = ch.channel_id
JOIN accounts a ON fc.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id;

		

	