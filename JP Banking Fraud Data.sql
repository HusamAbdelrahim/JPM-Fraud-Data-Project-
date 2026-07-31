-- Having to create a SCHEMA allows the user to make tables but having the USE case allows the user to actually select a data table that the user would like to work with
DROP TABLE IF exists fraud_sections;
CREATE schema fraud_sections;
USE fraud_sections;

-- Unsigned basically means that they a number can only go from 0 and positive, no negative numbers will be presented
-- Tinyint basically means that it can work with a small amount of number with at least 1 byte
-- PK is more so about working with one columns or can contribute to multiple as well so long as there is a value that is involved. Won't result in NULL

create TABLE fraud_types( 
	fraud_type_id tinyint unsigned auto_increment primary Key,
    type_code VARCHAR(30) NOT NULL unique, 
    type_name VARCHAR(60) NOT NULL,
    category VARCHAR(20),
    is_scam BOOLEAN NOT NULL,
    baseline_recovery_rate DECIMAL(4,3) CHECK (baseline_recovery_rate BETWEEN 0 and 1),
    median_loss_target DECIMAL(12,2)
    );
    
create TABLE channels(
	channel_id tinyint unsigned auto_increment Primary Key,
    channel_name VARCHAR(30) NOT NULL,
    is_digital BOOLEAN NOT NULL
);

create TABLE agents(
	agent_id smallint unsigned auto_increment Primary Key,
    agent_ref CHAR(8) UNIQUE,
    team VARCHAR(40),
    hire_date date,
    site VARCHAR(30)
);

create table customers(
	customer_id INT unsigned auto_increment primary key,
    customer_ref char(10) unique,
    age_band VARCHAR(10),
    segment VARCHAR(30),
    state CHAR(2),
    city VARCHAR(60),
    tenure_years DECIMAL(4,1),
    digital_enrolled BOOLEAN,
    paperless_flag BOOLEAN,
    prior_fraud_claims TINYINT unsigned DEFAULT 0
);

create table accounts(
		account_id INT unsigned auto_increment primary key,
        account_ref CHAR(12) Unique,
        customer_id INT UNSIGNED,
        Foreign Key (customer_id) references customers(customer_id),
        product_name VARCHAR(40),
        open_date DATE,
        balance_band VARCHAR(20),
        zelle_enabled BOOLEAN,
        card_present_capable BOOLEAN,
        account_status ENUM ('active','closed','restricted') NOT NULL DEFAULT 'active'
);

create table fraud_cases(
	case_id INT UNSIGNED primary key auto_increment,
    case_ref CHAR(12) unique,
    account_id int unsigned,
    fraud_type_id TINYINT unsigned not null,
    foreign key (fraud_type_id) references fraud_types(fraud_type_id),
    foreign key (account_id) references accounts(account_id),
    channel_id tinyint unsigned,
    foreign key (channel_id) references channels(channel_id),
    sub_scenario VARCHAR (60),
    detection_method VARCHAR(40),
    fraud_start_ts datetime not null,
    detection_ts datetime ,
    constraint chk_detect_after_start check (detection_ts >= fraud_start_ts),
    constraint chk_loss_range check (amount_lost >= 0 AND amount_lost <= amount_attempted),
    customer_report_ts datetime NULL,
    resolution_ts datetime NULL,
    amount_attempted decimal(12,2) not null,
    amount_lost decimal(12,2) not null,
    transaction_count smallint unsigned,
    case_status enum ('Open', 'Under Review','Closed-Confirmed','Closed-No Fraud','Written Off'),
    reimbursed_flag BOOLEAN,
    provisional_credit_flag BOOLEAN,
    cross_border_flag BOOLEAN,
    case_owner_team VARCHAR(40)
);

create table recovery_events(
	recovery_id INT unsigned auto_increment primary key,
    case_id int unsigned,
    foreign key (case_id) references fraud_cases(case_id),
    recovery_date date not null,
    amount decimal(12,2) not null check (amount > 0),
    method varchar(40)
);
create table call_logs(
	call_id int unsigned primary key auto_increment,
    call_ref char(12) unique,
    case_id int unsigned,
    foreign key (case_id) references fraud_cases(case_id),
    agent_id smallint unsigned null,
    foreign key (agent_id) references agents(agent_id),
    call_ts datetime not null,
    ivr_seconds smallint unsigned,
    queue_wait_seconds smallint unsigned,
    talk_seconds smallint unsigned,
    hold_seconds smallint unsigned,
    wrap_seconds smallint unsigned,
    aht_seconds smallint unsigned GENERATED ALWAYS AS (talk_seconds + hold_seconds + wrap_seconds) STORED,
    transfer_count tinyint unsigned,
    department VARCHAR(40),
    disposition VARCHAR(40),
    fcr_flag boolean,
    csat_score tinyint unsigned null check (csat_score BETWEEN 1 AND 5),
    abandoned_flag boolean,
    language varchar(20)
    );
    
    INSERT INTO channels (channel_id, channel_name, is_digital) VALUES
		(1, 'Online Banking', 1),
        (2, 'Mobile App', 1),
        (3, 'ATM', 0),
        (4, 'Branch', 0),
        (5, 'Phone', 0),
        (6, 'Card Terminal', 0),
        (7, 'Wire Room', 0);
        
	INSERT INTO fraud_types (fraud_type_id, type_code, type_name, category, is_scam, baseline_recovery_rate, median_loss_target) VALUES
		(1, 'CNP_CARD', 'Card-Not-Present', 'Unauthorized', '1', 0.900, 180.00),
        (2, 'SKIMMING', 'Card Skimming/ATM', 'Unauthorized', '1', 0.750, 600.00),
        (3, 'PHISHING', 'Phishing/Smishing', 'Unauthorized', '1', 0.550, 1900.00),
        (4, 'ATO', 'Account Takeover', 'Unauthorized','0', 0.450, 4200.00),
        (5, 'ZELLE_SCAM', 'Zelle/P2P Scam', 'Authorized','0', 0.120, 850.00),
        (6, 'CHECK_FRAUD', 'Check Fraud/Washing', 'Unauthorized', '0', 0.400, 3400.00),
        (7, 'BEC_WIRE', 'Business Email Compromise', 'Authorized','0', 0.350, 86000.00),
        (8, 'SYNTH_ID', 'Identity Theft/Synthetic', 'Unauthorized','0', 0.200, 9500.00),
        (9, 'ELDER_EXP', 'Elder Exploitation/Romance', 'Authorized','1', 0.080, 22000.00),
        (10, 'TECH_SUPPORT', 'Tech Support/Impersonation', 'Authorized','1', 0.250, 5100.00),
        (11, 'INSIDER', 'Insider/Employee','Unauthorized','0', 0.600, 140000.00);
        
SELECT category, COUNT(*), ROUND(AVG(baseline_recovery_rate),3)
FROM fraud_types GROUP BY category;

CREATE INDEX idx_cases_status ON fraud_cases (case_status);
CREATE INDEX idx_cases_type_status ON fraud_cases (fraud_type_id, case_status);
CREATE INDEX idx_calls_ts ON call_logs (call_ts);
CREATE INDEX idx_recovery_date ON recovery_events (recovery_date);

	
		
	