# Data Sources (5 Bullets Only)
User input data = uploaded by users (PDFs, forms, text) — messy, needs heavy validation, needs fast processing because users want instant results

System-generated data = logs, model predictions, click behavior — cleaner, can be processed in batch (hourly/daily), use tools like Logstash to make sense of massive log volumes

Internal databases = company's own data — inventory, customers, transactions — ML models query this directly (like Amazon checking product availability before ranking results)

First-party = your company collected it. Second-party = another company shares it with you (you pay). Third-party = collected on general public, being phased out due to privacy laws

AppZen version: Invoice data = user input (needs validation) + internal ERP database (clean, structured) + third-party vendor data (payment history, company info)

ON USER DATA: "We retain data according to compliance rules. One of them is SOC 2, it ensures financial data is encrypted, we don't use it without explicit permission, and access is logged and restricted. We follow multiple compliance rules when dealing with financial data."
