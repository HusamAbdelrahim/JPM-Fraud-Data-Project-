CREATE schema fraud_sections;
USE fraud_sections;

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