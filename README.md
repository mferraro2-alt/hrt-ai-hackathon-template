# CRM Command Center

A post-show relationship management dashboard that turns business cards, tradeshow lists, and leads into a prioritized, cadence-driven outreach plan for business development purposes.

## What It Does

1. **Tiered Lead Management** — Classifies event contacts into three outreach tiers (VIP, High Priority, Warm Lead) with customized follow-up cadences, and surfaces who is overdue or coming due for a touch this month.
2. **Partner Tracking** — Maintains a separate pipeline for hotels, venues, DMCs, and vendors with a 60-day outreach cadence, overdue alerts, and a category breakdown by partner type.
3. **Pipeline Intelligence** — Deduplicates contacts across three ATM events (ATM SF 2025, ATM SF 2026, ATM ENB 2025), highlights multi-event attendees, and visualizes the full lead and partner mix at a glance.

## How To Use

1. Open the app link in your browser
2. Review the outreach guide based on account quality, labeled by tier
3. Review lead contacts due for outreach broken out by tier, past due and coming this month
4. Gain insights on lead count by tiers
5. Review partner contacts due for outreach
6. Gain insights on partner count by type

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
