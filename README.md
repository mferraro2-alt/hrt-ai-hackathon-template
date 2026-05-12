# CRM Command Center

A post-show relationship management dashboard that turns tradeshow leads and partner contacts into a prioritized, cadence-driven outreach plan for business development.

## What It Does

- **Tiered Lead Management** — Classifies event contacts into three outreach tiers (VIP, High Priority, Warm Lead) with customized follow-up cadences, and surfaces who is overdue or coming due for a touch this month.
- **Partner Tracking** — Maintains a separate pipeline for hotels, venues, DMCs, and vendors with a 60-day outreach cadence, overdue alerts, and a category breakdown by partner type.
- **Pipeline Intelligence** — Deduplicates contacts across three ATM events (ATM SF 2025, ATM SF 2026, ATM ENB 2025), highlights multi-event attendees, and visualizes the full lead and partner mix at a glance.
- **CSV Upload** — Add new leads or contacts directly from the dashboard by uploading a CSV file; the app normalizes column names automatically and prevents duplicate uploads.

## How to Use

1. Open the app link in your browser
2. Review the **Outreach Tier Guide** to understand follow-up expectations by account quality
3. Check **May 2026 — Leads to Contact** for contacts that are overdue or coming due this month, broken out by tier
4. Review the **Partners to Contact** section for vendor and venue relationships that need a touch
5. Use the **Pipeline by Tier** and **Partner Mix** charts to see the full breakdown at a glance
6. To add new contacts, open **Upload a File**, choose the file type, select your CSV, and click **Add to Dashboard**

## Data

| File | Description |
|---|---|
| `data_ai/atm_sf_leads.csv` | Leads captured at ATM San Francisco 2026 |
| `data_ai/atm_sf25_leads.csv` | Leads captured at ATM San Francisco 2025 |
| `data_ai/atm_enb25_leads.csv` | Leads captured at ATM East/North Bay 2025 |
| `data_ai/contacts.csv` | Existing partner contact list |
| `data_ai/tagged_partners.csv` | Partners with event tags and last-contacted dates |
| `data_ai/activities.csv` | Completed outreach activity log used to calculate contact recency |

## Built With

- [Streamlit](https://streamlit.io)
- [Pandas](https://pandas.pydata.org)
- [Plotly](https://plotly.com/python/)
- [NumPy](https://numpy.org)
