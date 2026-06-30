# Data Sources

User input data = uploaded by users (PDFs, forms, text) — messy, needs heavy validation, needs fast processing because users want instant results

System-generated data = logs, model predictions, click behavior — cleaner, can be processed in batch (hourly/daily), use tools like Logstash to make sense of massive log volumes

Internal databases = company's own data — inventory, customers, transactions — ML models query this directly

First-party = your company collected it. Second-party = another company shares it (you pay). Third-party = collected on general public, being phased out due to privacy laws

AppZen version: Invoice data = user input (needs validation) + internal ERP database (clean, structured) + third-party vendor data (payment history, company info)

On User Data:

"We retain data according to compliance rules. SOC 2 ensures financial data is encrypted, access is logged and restricted, and we never use it without explicit permission. User-uploaded documents are processed for that specific workflow only and never used to train models without customer consent."

# ETL vs ELT — Key Points

ETL (Extract → Transform → Load)

Extract raw data from sources, validate and reject bad data early

Transform = clean, join, standardize, aggregate, derive features

Load = send processed, clean data to target (database/warehouse)

Best for = structured data, predefined schema, data warehouse

ELT (Extract → Load → Transform)

Extract raw data → dump everything into data lake FIRST

Transform later when needed

Best for = flexible schema, fast ingestion, massive unstructured data

Downside = searching through massive raw data lake is slow and inefficient

Simple Rule:

text
Know your schema upfront → ETL → Data Warehouse
Don't know schema yet → ELT → Data Lake first
Modern solution = both together (Databricks, Snowflake)

Store raw in data lake (flexible)

Process into structured warehouse (queryable)


# Modes of Data Flow — Key Points

3 Ways Data Passes Between Services:

1. Through Databases

Process A writes to DB → Process B reads from DB

Too slow for real-time apps

Both processes must access same DB — not feasible across companies

2. Through Services (REST/RPC)

Services talk directly to each other via API requests

REST = public APIs between different companies

RPC = internal calls within same organization

Gets complicated with many services — creates tight coupling

Good for simple request-response patterns

3. Through Real-Time Transport (Event-Driven)

Services don't talk to each other directly

Instead → publish events to a broker (Kafka)

Other services subscribe to what they need

Decoupled — services don't depend on each other

Fast — in-memory, not database reads

Scalable — works with hundreds of services

Pub/Sub vs Message Queue:

Pub/Sub (Kafka, Kinesis) = any subscriber can read the event — one event, many consumers

Message Queue (RabbitMQ, RocketMQ) = event has ONE specific consumer — delivered to right place

Event-Driven vs Request-Driven:

text
Request-driven = synchronous
"I ask you, you respond, I wait"
Good for = logic-heavy systems

Event-driven = asynchronous  
"I publish, whoever needs it takes it"
Good for = data-heavy systems


# Batch vs Stream Processing

Batch Processing:

Data sitting in storage (S3, Snowflake, DB) = historical data → processed in batch jobs

Jobs run on a schedule (hourly, daily) — not real-time

Tools: Spark, MapReduce

Use for features that don't change fast → e.g., driver rating (won't shift dramatically day to day)

These slow-changing features = Static Features

Stream Processing:

Data flowing live through Kafka/Kinesis = streaming data → processed as it arrives

Near-zero latency — no waiting, no writing to DB first

Tools: Apache Flink, KSQL, Kafka Streams

Use for features that change fast → e.g., how many drivers available RIGHT NOW, median price of last 10 rides

These fast-changing features = Dynamic Features

The Key Difference — One Table:

Batch	Stream
Data source	DB / S3 / Snowflake	Kafka / Kinesis
When it runs	Scheduled (daily/hourly)	Continuously / on event
Latency	High (minutes–hours)	Low (milliseconds)
Tools	Spark, MapReduce	Flink, KSQL
Feature type	Static	Dynamic
Example	Driver's avg rating last 30 days	Drivers available right now
Critical insight:

Most real ML systems need BOTH static + dynamic features together

Flink can do batch AND stream — batch is just a special case of stream

