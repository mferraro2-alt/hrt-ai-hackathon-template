# Handoff — 2026-05-09

## Summary
- Appended three new contacts from a scanned business card PDF to `data_ai/contacts.csv`
  - **Jorge Romero** — Partner, Topa Architecture (jorge@topaarchitecture.com)
  - **Shawn Hawkins** — Wealth Advisor, Conversant Wealth Management (shawnh@conversantwealth.com)
  - **Sharon Fox** — Founder & President, Veterans Total Wellness (sharon@veteranstotalwellness.org)

## Current State
- Branch: `main` (up to date with origin/main, but changes are unstaged)
- `app.py`: modified (+177 lines vs last commit) — not yet committed
- `data_ai/contacts.csv`: untracked new file with 6 total contacts (3 original + 3 new)
- `.claude/settings.local.json`: untracked new file

## Next Steps
- Commit and push outstanding changes (`app.py`, `data_ai/contacts.csv`)
- Continue building out the Streamlit app features as needed
- Add more contacts from additional business cards if available

## Key Decisions
- Contacts are stored in `data_ai/contacts.csv` (AI-generated/managed data directory, not `data/`)
- CSV columns: First Name, Last Name, Title, Company, Email, Office Phone, Mobile Phone, Street Address, City, State, Zip, Website

## Watchouts
- Sharon Fox's street address was not on the business card — City field left as blank, State set to CA based on "San Jose & South Bay" reference
- Jorge Romero's office phone includes "ext. 500" in the field — may need normalization if used programmatically
- `app.py` has significant uncommitted changes; verify the app still runs correctly before committing
