# Data Sources

User input data = uploaded by users (PDFs, forms, text) — messy, needs heavy validation, needs fast processing because users want instant results

System-generated data = logs, model predictions, click behavior — cleaner, can be processed in batch (hourly/daily), use tools like Logstash to make sense of massive log volumes

Internal databases = company's own data — inventory, customers, transactions — ML models query this directly

First-party = your company collected it. Second-party = another company shares it (you pay). Third-party = collected on general public, being phased out due to privacy laws

AppZen version: Invoice data = user input (needs validation) + internal ERP database (clean, structured) + third-party vendor data (payment history, company info)

On User Data:

"We retain data according to compliance rules. SOC 2 ensures financial data is encrypted, access is logged and restricted, and we never use it without explicit permission. User-uploaded documents are processed for that specific workflow only and never used to train models without customer consent."

