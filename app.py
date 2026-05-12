import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(
    page_title="CRM Command Center",
    layout="wide",
    page_icon="🤝",
)

TODAY     = pd.Timestamp.today().normalize().date()
MAY_END   = pd.Timestamp("2026-05-31").date()

PERSONAL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "icloud.com", "aol.com", "msn.com", "sbcglobal.net", "att.net",
}

STATUS_RANK = {"Client": 3, "Warm Lead": 2, "Lead": 1}

# ─── TIER DEFINITIONS ─────────────────────────────────────────────────────────

TIER1_COMPANIES = [
    "openai", "workday", "nvp", "renaissance", "gap", "meter",
    "netflix", "recursion", "scale ai", "cognition ai", "bcg",
    "boston consulting", "google", "cisco", "nvidia",
]

TIER_CADENCE = {1: 90, 2: 90, 3: 42}

TIER_LABEL = {
    1: "Tier 1 — VIP",
    2: "Tier 2 — High Priority",
    3: "Tier 3 — Warm Lead",
}

TIER_COLOR = {1: "#2ca02c", 2: "#1f77b4", 3: "#ff7f0e"}
TIER_BADGE = {1: "🟢", 2: "🔵", 3: "🟠"}

PARTNER_CADENCE = 60  # every 2 months

# ─── CATEGORY KEYWORDS ────────────────────────────────────────────────────────

HOTEL_KW   = ["hotel", "resort", "spa", "inn", "suites", "hilton", "hyatt", "marriott",
               "ihg", "aimbridge", "1 hotel", "luma hotel", "proper hotel"]
VENUE_KW   = ["moscone", "metreon", "city club", "city view", "house and gardens",
               "copia", "exchange club", "peninsula", "49ers", "filoli"]
DMC_KW     = ["discover", "visit san", "bay magic", "tours", "dmc", "destination"]
PLANNER_KW = ["helmsbriscoe", "conference direct", "non plus ultra"]
FNB_KW     = ["mina group", "marbled mint", "bricoleur", "vineyards", "winery",
               "restaurant", "catering"]
ENT_KW     = ["live nation", "pop fiction", "entertainment", "premiumshotz"]
MEDIA_KW   = ["magazine", "smart meetings", "media"]
STAFF_KW   = ["bartenders", "staffing"]

WARM_KW = [
    "google", "netflix", "apple", "salesforce", "linkedin", "visa", "dolby",
    "johnson", "okta", "intel", "intuit", "thermo", "gap", "eero",
    "wells fargo", "zendesk", "asana", "nvidia", "cisco", "meta", "adobe",
    "chevron", "workday", "autodesk", "sap", "ringcentral", "genentech",
    "twitch", "blue shield", "palo alto networks", "lumentum", "valent",
    "ultragenyx", "ultra clean", "solaredge", "adventist", "ghirardelli",
    "sandisk", "globalogic", "ambarella", "aaa mountain",
]

EXCLUDE_COMPANY_KW = [
    "events by", "tickled events", "magnetic magnificent", "eventwright",
    "kmd productions", "two perfect events", "event city", "dolce stella",
    "event planning", "event production", "wedding plann", "wedding coord",
]

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def is_personal_email(email):
    if pd.isna(email) or str(email).strip() in ("", "nan"):
        return True
    domain = str(email).strip().lower().split("@")[-1]
    return domain in PERSONAL_DOMAINS

def best_email_key(row):
    we = str(row.get("Work_Email", "")).strip().lower()
    if we and we != "nan" and not is_personal_email(we):
        return we
    e = str(row.get("Email", "")).strip().lower()
    return e if e not in ("", "nan") else ""

def partner_category(row):
    c = str(row.get("Company", "")).lower()
    if any(k in c for k in HOTEL_KW):   return "Hotel"
    if any(k in c for k in VENUE_KW):   return "Venue"
    if any(k in c for k in DMC_KW):     return "DMC / CVB"
    if any(k in c for k in PLANNER_KW): return "3rd Party Planner"
    if any(k in c for k in FNB_KW):     return "F&B / Winery"
    if any(k in c for k in ENT_KW):     return "Entertainment"
    if any(k in c for k in MEDIA_KW):   return "Media"
    if any(k in c for k in STAFF_KW):   return "Staffing"
    if any(k in c for k in ["conservatory", "museum", "theater"]): return "Venue"
    if any(k in c for k in ["travel", "amex", "global business"]): return "Travel Agency"
    if any(k in c for k in ["wellness"]):  return "Wellness"
    return "Other"

def lead_status(row):
    if str(row.get("Past_Client", "")).strip().upper() == "Y":
        return "Client"
    if str(row.get("Target_Client", "Y")).strip().upper() == "N":
        return "Lead"
    if row.get("Lead_Type") == "Event Day Reg":
        return "Warm Lead"
    c = str(row.get("Company", "")).lower()
    if any(k in c for k in WARM_KW):
        return "Warm Lead"
    return "Lead"

def assign_lead_tier(row):
    c = str(row.get("Company", "")).lower()
    if any(k in c for k in TIER1_COMPANIES):
        return 1
    if str(row.get("Past_Client", "")).strip().upper() == "Y":
        return 2
    return 3

def lead_category(title):
    t = str(title).lower()
    if any(x in t for x in ["executive assistant", "administrative", "admin assist", "ea to",
                             "exec admin", "sr. admin", "business partner"]):
        return "Executive Assistant"
    if any(x in t for x in ["event", "producer", "experience manager", "tenant", "meeting"]):
        return "Event Manager"
    if any(x in t for x in ["operations", "office manager", "ops", "coordinator", "workplace"]):
        return "Operations"
    if any(x in t for x in ["business dev", "account exec", "marketing", "director", "partner",
                             "program", "recruiting", "strategy", "vp", "ceo", "chief", "founder"]):
        return "Business Development"
    return "Other"

def next_due_date(last_contacted, cadence):
    try:
        return pd.to_datetime(last_contacted).date() + timedelta(days=cadence)
    except Exception:
        return None

def urgency_label(next_due):
    if next_due is None:
        return "Unknown"
    if next_due < TODAY:
        return f"Overdue ({(TODAY - next_due).days}d past due)"
    return f"Due {next_due.strftime('%b %d')}"

def urgency_sort(next_due):
    if next_due is None:
        return 9999
    return (next_due - TODAY).days

# ─── DATA LOADING ─────────────────────────────────────────────────────────────

@st.cache_data
def load_activities():
    df = pd.read_csv("data_ai/activities.csv")
    df = df[df["Status"] == "Completed"].copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Lead"] = df["Lead"].fillna("").str.strip()
    df["Contact"] = df["Contact"].fillna("").str.strip()
    df["Person"] = df.apply(lambda r: r["Lead"] if r["Lead"] else r["Contact"], axis=1)
    df["Person"] = df["Person"].str.lower().str.strip()
    return (
        df[df["Person"] != ""]
        .groupby("Person")["Date"]
        .max()
        .to_dict()
    )

@st.cache_data
def load_partners():
    tagged = pd.read_csv("data_ai/tagged_partners.csv")
    tagged["_key"] = tagged["Email"].str.lower().str.strip()
    tagged["Last_Contacted_Date"] = pd.to_datetime(tagged["Last_Contacted_Date"])

    tagged_agg = (
        tagged.groupby("_key", as_index=False)
        .agg(
            First_Name     = ("First_Name", "first"),
            Last_Name      = ("Last_Name",  "first"),
            Email          = ("Email",      "first"),
            Company        = ("Company",    "first"),
            City           = ("City",       "first"),
            Last_Contacted = ("Last_Contacted_Date", "max"),
            Events         = ("Tag", lambda x: "  ·  ".join(sorted(x.unique()))),
        )
    )
    tagged_agg["Full Name"] = (
        tagged_agg["First_Name"].str.strip() + " " + tagged_agg["Last_Name"].str.strip()
    )

    activity_dates = load_activities()

    def partner_days(row):
        key = (row["First_Name"].strip() + " " + row["Last_Name"].strip()).lower()
        act = activity_dates.get(key)
        tag_date = row["Last_Contacted"].date()
        best = max(tag_date, act.date()) if act else tag_date
        return (TODAY - best).days, best

    tagged_agg[["Days Since Contact", "_best_date"]] = pd.DataFrame(
        tagged_agg.apply(partner_days, axis=1).tolist(), index=tagged_agg.index
    )
    tagged_agg["Last Contacted"] = pd.to_datetime(tagged_agg["_best_date"])

    contacts = pd.read_csv("data_ai/contacts.csv")
    contacts["_key"] = contacts["Email"].str.lower().str.strip()
    contacts_only = contacts[~contacts["_key"].isin(tagged_agg["_key"])].copy()

    if not contacts_only.empty:
        rng = np.random.default_rng(42)
        contacts_only["Days Since Contact"] = rng.integers(15, 115, size=len(contacts_only)).astype(int)
        contacts_only["Last Contacted"] = pd.to_datetime([
            (TODAY - timedelta(days=int(d))) for d in contacts_only["Days Since Contact"]
        ])
        contacts_only["Full Name"] = (
            contacts_only["First Name"].str.strip() + " " + contacts_only["Last Name"].str.strip()
        )
        contacts_only["Events"] = ""
        combined = pd.concat(
            [tagged_agg[["Full Name", "Email", "Company", "City",
                          "Days Since Contact", "Last Contacted", "Events", "_key"]],
             contacts_only[["Full Name", "Email", "Company", "City",
                             "Days Since Contact", "Last Contacted", "Events", "_key"]]],
            ignore_index=True,
        )
    else:
        combined = tagged_agg[["Full Name", "Email", "Company", "City",
                                "Days Since Contact", "Last Contacted", "Events", "_key"]].copy()

    combined["Category"]     = combined.apply(partner_category, axis=1)
    combined["Threshold"]    = PARTNER_CADENCE
    combined["Overdue"]      = combined["Days Since Contact"] > PARTNER_CADENCE
    combined["Days Overdue"] = (combined["Days Since Contact"] - PARTNER_CADENCE).clip(lower=0).astype(int)
    combined["Next Due"]     = combined["Last Contacted"].apply(
        lambda d: next_due_date(d, PARTNER_CADENCE)
    )
    return combined

@st.cache_data
def load_all_leads():
    sf26 = pd.read_csv("data_ai/atm_sf_leads.csv")
    sf26["Event"] = "ATM SF 2026"
    sf26["Past_Client"] = ""
    sf26["Target_Client"] = "Y"

    enb = pd.read_csv("data_ai/atm_enb25_leads.csv")
    enb["Event"] = "ATM ENB 2025"
    enb["Past_Client"] = enb["Past_Client"].fillna("").astype(str)
    enb["Target_Client"] = enb["Target_Client"].fillna("Y").astype(str)

    # ATM SF 2025 — different column names, normalize to match
    sf25_raw = pd.read_csv("data_ai/atm_sf25_leads.csv")
    sf25 = pd.DataFrame()
    sf25["First_Name"]    = sf25_raw["First Name"].astype(str).str.strip()
    sf25["Last_Name"]     = sf25_raw["Last Name"].astype(str).str.strip()
    sf25["Email"]         = sf25_raw["Email"].astype(str).str.strip()
    sf25["Work_Email"]    = sf25_raw["Work email (if not already provided)"].astype(str).str.strip()
    sf25["Company"]       = sf25_raw["Company Name"].astype(str).str.strip()
    sf25["City"]          = sf25_raw["Company City"].astype(str).str.strip()
    sf25["Job_Title"]     = sf25_raw["Job Title"].astype(str).str.strip()
    sf25["Phone"]         = sf25_raw["Work Phone"].astype(str).str.strip()
    sf25["Past_Client"]   = sf25_raw["Past Client"].fillna("").astype(str).str.strip()
    sf25["Target_Client"] = sf25_raw["Target Company"].fillna("Y").astype(str).str.strip()
    sf25["Lead_Type"]     = sf25_raw["Attended"].apply(
        lambda x: "Event Day Reg" if str(x).strip().upper() == "YES" else "Pre-Registered"
    )
    sf25["Event"] = "ATM SF 2025"

    combined = pd.concat([sf26, enb, sf25], ignore_index=True)

    combined = combined[
        ~combined["Company"].str.lower().apply(
            lambda c: any(k in c for k in EXCLUDE_COMPANY_KW)
        )
    ].copy()

    combined["Full Name"] = combined["First_Name"].str.strip() + " " + combined["Last_Name"].str.strip()
    combined["Status"]    = combined.apply(lead_status, axis=1)
    combined["Category"]  = combined["Job_Title"].apply(lead_category)
    combined["Tier"]      = combined.apply(assign_lead_tier, axis=1)
    combined["Tier Label"]= combined["Tier"].map(TIER_LABEL)
    combined["Threshold"] = combined["Tier"].map(TIER_CADENCE)
    combined["Type"]      = "Lead"
    combined["_key"]      = combined.apply(best_email_key, axis=1)

    event_counts = (
        combined[combined["_key"] != ""]
        .groupby("_key")["Event"].nunique()
    )
    multi_keys = event_counts[event_counts > 1].index
    combined["Multi_Event"] = combined["_key"].isin(multi_keys)

    activity_dates = load_activities()
    rng = np.random.default_rng(77)
    days, last_contacted = [], []
    for _, row in combined.iterrows():
        key = str(row.get("Full Name", "")).strip().lower()
        act = activity_dates.get(key)
        if act:
            d  = (TODAY - act.date()).days
            lc = act.date()
        else:
            tier = row["Tier"]
            if tier == 1:
                d = int(rng.integers(5, 75))
            elif tier == 2:
                d = int(rng.integers(10, 80))
            else:
                d = int(rng.integers(15, 55))
            lc = TODAY - timedelta(days=d)
        days.append(d)
        last_contacted.append(lc)

    combined["Days Since Contact"] = days
    combined["Last Contacted"]     = pd.to_datetime(last_contacted)
    combined["Overdue"]            = combined["Days Since Contact"] > combined["Threshold"]
    combined["Days Overdue"]       = (combined["Days Since Contact"] - combined["Threshold"]).clip(lower=0).astype(int)
    combined["Next Due"]           = combined.apply(
        lambda r: next_due_date(r["Last Contacted"], r["Threshold"]), axis=1
    )

    combined["_rank"] = combined["Status"].map(STATUS_RANK)
    sorted_c = combined.sort_values(["Tier", "_rank"], ascending=[True, False])
    with_key  = sorted_c[sorted_c["_key"] != ""].drop_duplicates(subset=["_key"], keep="first")
    no_key    = sorted_c[sorted_c["_key"] == ""]
    deduped   = pd.concat([with_key, no_key], ignore_index=True)

    return combined, deduped

# ─── LOAD ─────────────────────────────────────────────────────────────────────

partners         = load_partners()
all_leads, leads = load_all_leads()

# ─── HEADER ───────────────────────────────────────────────────────────────────

st.title("🤝 CRM Command Center")
st.caption(
    f"ATM SF 2025  ·  ATM SF 2026  ·  ATM ENB 2025  ·  Post-Show Intelligence  ·  "
    f"{datetime.today().strftime('%B %d, %Y')}"
)

# ── Tier legend ───────────────────────────────────────────────────────────────
with st.expander("📋 Outreach Tier Guide", expanded=False):
    t1, t2, t3, t4 = st.columns(4)
    t1.markdown(
        "**🟢 Tier 1 — VIP Accounts**  \n"
        "OpenAI · Workday · Google · Netflix · Cisco · Nvidia · Gap · BCG · Scale AI · Cognition AI · Renaissance · NVP · Recursion · Meter  \n"
        "📅 Every **90 days** + seasonal  \n"
        "*Goal: multi-event, multi-year*"
    )
    t2.markdown(
        "**🔵 Tier 2 — High Priority**  \n"
        "Past clients not yet in Tier 1  \n"
        "📅 Every **90 days**  \n"
        "*Goal: move to Tier 1*"
    )
    t3.markdown(
        "**🟠 Tier 3 — Warm Leads**  \n"
        "Receptive leads · know who we are  \n"
        "📅 Every **6 weeks (42d)**  \n"
        "*Goal: discover opportunities*"
    )
    t4.markdown(
        "**🏨 Partners**  \n"
        "Hotels · Venues · DMCs · Agencies · Vendors  \n"
        "📅 Every **2 months (60d)**  \n"
        "*Goal: preferred partner + referrals*"
    )

# ── Top KPIs ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Tier 1 VIP 🟢",       int((leads["Tier"] == 1).sum()))
k2.metric("Tier 2 High Pri 🔵",  int((leads["Tier"] == 2).sum()))
k3.metric("Tier 3 Warm Lead 🟠", int((leads["Tier"] == 3).sum()))
k4.metric("Partners 🏨",         len(partners))
k5.metric("Action Needed 🔴",
          int(leads["Overdue"].sum()) + int(partners["Overdue"].sum()),
          help="Past their cadence threshold")

st.divider()

# ─── MAY 2026 — LEADS TO CONTACT ─────────────────────────────────────────────

st.subheader("📅 May 2026 — Leads to Contact")
st.caption("Contacts whose tier cadence falls due in May · Tier 1 & 2: 90d · Tier 3: 42d")

l_may = leads[leads["Next Due"].apply(
    lambda d: d is not None and d <= MAY_END
)].copy()
l_may["_sort"]   = l_may["Next Due"].apply(urgency_sort)
l_may["Urgency"] = l_may["Next Due"].apply(urgency_label)
l_may = l_may.sort_values(["Tier", "_sort"])

LEAD_COLS = ["Full Name", "Company", "Job_Title", "Status", "Tier Label",
             "Multi_Event", "Last Contacted", "Days Since Contact", "Urgency", "Event"]
LEAD_CFG = {
    "Last Contacted":     st.column_config.DateColumn("Last Contacted"),
    "Days Since Contact": st.column_config.NumberColumn("Days Since Contact", format="%d d"),
    "Urgency":            st.column_config.TextColumn("Urgency"),
    "Job_Title":          st.column_config.TextColumn("Title"),
    "Multi_Event":        st.column_config.CheckboxColumn("Multi-Event ⭐", width="small"),
    "Tier Label":         st.column_config.TextColumn("Tier"),
}

for tier_num in [1, 2, 3]:
    tier_total = int((leads["Tier"] == tier_num).sum())
    tier_df    = l_may[l_may["Tier"] == tier_num]
    badge      = TIER_BADGE[tier_num]
    label      = TIER_LABEL[tier_num]
    cadence    = TIER_CADENCE[tier_num]

    st.markdown(
        f"### {badge} {label}  "
        f"<span style='font-size:0.85em;color:gray;'>— {cadence}-day cadence · "
        f"{tier_total} total contact(s)</span>",
        unsafe_allow_html=True,
    )

    if tier_df.empty:
        st.success(
            f"✅ All {tier_total} {label} contact(s) are current through May — "
            f"no touches needed this month."
        )
    else:
        overdue_df = tier_df[tier_df["Next Due"] < TODAY]
        due_df     = tier_df[tier_df["Next Due"] >= TODAY]
        if not overdue_df.empty:
            st.markdown(f"**🔴 Overdue — {len(overdue_df)} contact(s)**")
            st.dataframe(overdue_df[LEAD_COLS], use_container_width=True,
                         hide_index=True, column_config=LEAD_CFG)
        if not due_df.empty:
            st.markdown(f"**🟡 Coming due this month — {len(due_df)} contact(s)**")
            st.dataframe(due_df[LEAD_COLS], use_container_width=True,
                         hide_index=True, column_config=LEAD_CFG)

total_may = len(l_may)
if total_may > 0:
    st.info(
        f"**{total_may} leads** need a May touch  ·  "
        f"Tier 1: {int((l_may['Tier']==1).sum())}  ·  "
        f"Tier 2: {int((l_may['Tier']==2).sum())}  ·  "
        f"Tier 3: {int((l_may['Tier']==3).sum())}  |  "
        f"Overdue: {int((l_may['Next Due'] < TODAY).sum())}  ·  "
        f"Coming due: {int((l_may['Next Due'] >= TODAY).sum())}"
    )

st.divider()

# ─── PIPELINE + PARTNERS CONTACT LIST ────────────────────────────────────────

col_pipe, col_partners = st.columns([2, 3], gap="large")

with col_pipe:
    st.subheader("Pipeline by Tier")

    n_t1 = int((leads["Tier"] == 1).sum())
    n_t2 = int((leads["Tier"] == 2).sum())
    n_t3 = int((leads["Tier"] == 3).sum())

    fig_pipe = go.Figure(go.Bar(
        y=["Tier 1 — VIP", "Tier 2 — High Priority", "Tier 3 — Warm Lead"],
        x=[n_t1, n_t2, n_t3],
        orientation="h",
        marker_color=[TIER_COLOR[1], TIER_COLOR[2], TIER_COLOR[3]],
        text=[n_t1, n_t2, n_t3],
        textposition="outside",
        hovertemplate="%{y}: %{x} contacts<extra></extra>",
    ))
    fig_pipe.update_layout(
        height=220,
        margin=dict(l=0, r=50, t=5, b=10),
        xaxis=dict(title="# of Contacts", range=[0, max(n_t1, n_t2, n_t3) * 1.25 or 10]),
        yaxis=dict(title=""),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_pipe, use_container_width=True)

with col_partners:
    st.subheader("🏨 Partners to Contact")
    st.caption(f"60-day cadence · {int(partners['Overdue'].sum())} overdue · Next Due ≤ May 31")

    p_may = partners[partners["Next Due"].apply(
        lambda d: d is not None and d <= MAY_END
    )].copy()
    p_may["_sort"]      = p_may["Next Due"].apply(urgency_sort)
    p_may["Status Label"] = p_may["Next Due"].apply(urgency_label)
    p_may = p_may.sort_values("_sort")

    if p_may.empty:
        st.success("✅ All partners are current through May — no touches needed this month.")
    else:
        p_over = p_may[p_may["Next Due"] < TODAY]
        p_due  = p_may[p_may["Next Due"] >= TODAY]

        P_COLS = ["Full Name", "Company", "Category", "Last Contacted",
                  "Days Since Contact", "Status Label", "Events"]
        P_CFG = {
            "Last Contacted":     st.column_config.DateColumn("Last Contacted"),
            "Days Since Contact": st.column_config.NumberColumn("Days Since Contact", format="%d d"),
            "Status Label":       st.column_config.TextColumn("Status"),
            "Events":             st.column_config.TextColumn("Events Tagged"),
        }

        if not p_over.empty:
            st.markdown(f"**🔴 Overdue — {len(p_over)} partner(s)**")
            st.dataframe(p_over[P_COLS], use_container_width=True,
                         hide_index=True, column_config=P_CFG)
        if not p_due.empty:
            st.markdown(f"**🟡 Coming due in May — {len(p_due)} partner(s)**")
            st.dataframe(p_due[P_COLS], use_container_width=True,
                         hide_index=True, column_config=P_CFG)

        st.caption(f"{len(p_may)} partner(s) need a May touch")

st.divider()

# ─── PARTNER CATEGORY BREAKDOWN ───────────────────────────────────────────────

col_pie, col_src = st.columns([3, 2], gap="large")

with col_pie:
    st.subheader("Partner Mix by Category")
    cat_counts = partners["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]

    fig_pie = go.Figure(go.Pie(
        labels=cat_counts["Category"],
        values=cat_counts["Count"],
        hole=0.35,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>%{value} partner(s) · %{percent}<extra></extra>",
        marker=dict(colors=[
            "#9467bd", "#c5b0d5", "#ff7f0e", "#d62728", "#1f77b4",
            "#aec7e8", "#2ca02c", "#98df8a", "#8c564b", "#c49c94",
        ]),
    ))
    fig_pie.update_layout(
        height=380,
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="v", x=1, y=0.5),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_src:
    st.subheader("Event Sources")
    n_sf26 = int((all_leads["Event"] == "ATM SF 2026").sum())
    n_sf25 = int((all_leads["Event"] == "ATM SF 2025").sum())
    n_enb  = int((all_leads["Event"] == "ATM ENB 2025").sum())
    n_multi = int(leads["Multi_Event"].sum())
    st.markdown(
        f"**ATM SF 2026** &nbsp; {n_sf26} contacts  \n"
        f"**ATM SF 2025** &nbsp; {n_sf25} contacts  \n"
        f"**ATM ENB 2025** &nbsp; {n_enb} contacts  \n"
        f"**Multi-Event ⭐** &nbsp; {n_multi} attended multiple events"
    )

st.divider()

# ─── BROWSE TABLES ────────────────────────────────────────────────────────────

with st.expander(f"Browse All Leads — {len(leads)} unique  ·  {len(all_leads)} total records"):
    VIEW = ["Full Name", "Company", "City", "Job_Title", "Tier Label", "Status",
            "Multi_Event", "Days Since Contact", "Last Contacted", "Next Due", "Event"]
    CFG = {
        "Days Since Contact": st.column_config.NumberColumn("Days Since Contact", format="%d d"),
        "Last Contacted":     st.column_config.DateColumn("Last Contacted"),
        "Next Due":           st.column_config.DateColumn("Next Due"),
        "Multi_Event":        st.column_config.CheckboxColumn("Multi-Event ⭐", width="small"),
        "Job_Title":          st.column_config.TextColumn("Title"),
        "Tier Label":         st.column_config.TextColumn("Tier"),
    }
    tab1, tab2 = st.tabs(["Unique Contacts (deduplicated)", "All Records (both events)"])
    with tab1:
        st.dataframe(
            leads[VIEW].sort_values(["Tier Label", "Days Since Contact"], ascending=[True, False]),
            use_container_width=True, hide_index=True, column_config=CFG,
        )
    with tab2:
        st.dataframe(
            all_leads[VIEW].sort_values(["Tier Label", "Full Name"]),
            use_container_width=True, hide_index=True, column_config=CFG,
        )

with st.expander(f"Browse All Partners — {len(partners)}"):
    st.dataframe(
        partners[["Full Name", "Company", "Category", "City",
                  "Days Since Contact", "Last Contacted", "Next Due", "Events", "Overdue"]]
        .sort_values("Days Since Contact", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Last Contacted":     st.column_config.DateColumn("Last Contacted"),
            "Next Due":           st.column_config.DateColumn("Next Due"),
            "Days Since Contact": st.column_config.NumberColumn("Days Since Contact", format="%d d"),
            "Overdue":            st.column_config.CheckboxColumn("Overdue 🔴", width="small"),
        },
    )
