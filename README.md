# JPM Fraud Data Project

## Tools that I used:

**SQL**
**Python**
**Tableau**

## Data Analysis JP Morgan Fraud 

This project has some accurate deception of <ins> of fraud that occurs </ins>.
However, majority of the project is also a made up statistics. This is to protect **customer confidental information**
This project is mostly a side project of how we use tools analyze fraud and from my experience in the past working with client.
How does fraud actually occurs, if it was authorized, logged, and if the funds were returned


## Analysis of the project:

### SQL

Using **MySQL**, I have created a <ins> Schema </ins>

This **Schema** will contain six different tables:

- Fraud Types
- Channesls
- Agents
- Customers
- Accounts
- Fraud Cases

What each table contain critical information that we will be caregorizing & Inserting the values into.

### Python's Role:

Python role is pretty simple, basically I decided to make a syntehic data generator, so the data that is being provided here isn't an actual deception of real customer's information, but a presentation of the work that is being provided.

Each of the section will return a different set of rows in this project: 

For example.

**Agents (50)**
**Customers (3,000)**
**Accounts (3,000)**
**Fraud Cases (10,000)**

Once the data has been processed in Python and we run SQL

The result will be a data table that I would export in <ins> CSV </ins>

### Tableau Role:

Tableau is a powerful data visualization tools that let's you analyze and view your data.

By using a different range of visualizations, we will be using this tool to have a better understanding of our data!

## What this project tells us? 

First let's review some of that data starting off with **Net Loss**

How does this eventually occur? Well Netloss we can see that it somewhat goes down, but eventaully goes up but let's take a closer look of the Recovery rate and basically we are also seeing a much more steady rate for the recovery rate which is good.

But looking at the **Reimbursement Gap**

You can see many of the transaction are not authorized which means if we look at the fraud type many of the fraud were business, phishing tactis, and identity theft as well.

Many of the transactions that occurs basically shows an idea of the recovery rate and those that authorized means a higher amount was taken and those that was not authorized amount was still removed but not as much, this means it the bank could possibly detect an authorized and be able to investigate the problem sooner.

Loss by State is an interesting one, big states/cities like California, New York, Florida, and Texas is where the majority of the fraud has occured.

Overall, building a system and continue countering tactics like email compromise, identity theft, and account take over should be the main focus and have a better understanding of what transaction authorized and unauthorized. 
