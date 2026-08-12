# Databricks notebook source

# COMMAND ----------
%pip install faker --quiet

# COMMAND ----------

# COMMAND ----------
catalog = "css_genie"  # hardcoded for serverless compatibility
print(f"Using catalog: {catalog}")

# COMMAND ----------
import random
import pandas as pd
from datetime import date, timedelta, datetime
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

PROJECTS = [
    {"project_id": "P001", "project_name": "Centennial Tower Office Complex", "contract_value": 85_000_000, "start_date": "2020-03-01", "end_date": "2022-08-15", "status": "completed", "city": "Denver", "state": "CO", "project_type": "commercial"},
    {"project_id": "P002", "project_name": "Rocky Mountain Medical Center Expansion", "contract_value": 125_000_000, "start_date": "2020-06-15", "end_date": "2023-01-30", "status": "completed", "city": "Aurora", "state": "CO", "project_type": "healthcare"},
    {"project_id": "P003", "project_name": "Aurora Industrial Warehouse Phase I", "contract_value": 22_000_000, "start_date": "2020-09-01", "end_date": "2021-11-30", "status": "completed", "city": "Aurora", "state": "CO", "project_type": "industrial"},
    {"project_id": "P004", "project_name": "Lakewood Elementary School Modernization", "contract_value": 18_500_000, "start_date": "2020-11-01", "end_date": "2022-05-31", "status": "completed", "city": "Lakewood", "state": "CO", "project_type": "education"},
    {"project_id": "P005", "project_name": "Colorado Springs Data Center", "contract_value": 55_000_000, "start_date": "2021-01-15", "end_date": "2022-09-30", "status": "completed", "city": "Colorado Springs", "state": "CO", "project_type": "commercial"},
    {"project_id": "P006", "project_name": "Union Station Hotel Renovation", "contract_value": 32_000_000, "start_date": "2021-03-01", "end_date": "2022-12-15", "status": "completed", "city": "Denver", "state": "CO", "project_type": "commercial"},
    {"project_id": "P007", "project_name": "Fort Collins Civic Center", "contract_value": 48_000_000, "start_date": "2021-05-15", "end_date": "2023-07-31", "status": "completed", "city": "Fort Collins", "state": "CO", "project_type": "government"},
    {"project_id": "P008", "project_name": "Boulder Tech Campus Building A", "contract_value": 72_000_000, "start_date": "2021-07-01", "end_date": "2023-11-30", "status": "completed", "city": "Boulder", "state": "CO", "project_type": "commercial"},
    {"project_id": "P009", "project_name": "Pueblo Steel Mill Upgrade", "contract_value": 41_000_000, "start_date": "2021-09-01", "end_date": "2023-03-31", "status": "completed", "city": "Pueblo", "state": "CO", "project_type": "industrial"},
    {"project_id": "P010", "project_name": "Greeley Wastewater Treatment Plant", "contract_value": 67_000_000, "start_date": "2021-11-01", "end_date": "2024-02-28", "status": "completed", "city": "Greeley", "state": "CO", "project_type": "infrastructure"},
    {"project_id": "P011", "project_name": "DTC Multifamily Residential Tower", "contract_value": 95_000_000, "start_date": "2022-01-15", "end_date": "2024-08-31", "status": "completed", "city": "Greenwood Village", "state": "CO", "project_type": "residential"},
    {"project_id": "P012", "project_name": "Longmont Distribution Center", "contract_value": 28_000_000, "start_date": "2022-03-01", "end_date": "2023-09-30", "status": "completed", "city": "Longmont", "state": "CO", "project_type": "industrial"},
    {"project_id": "P013", "project_name": "Colorado Convention Center Expansion", "contract_value": 150_000_000, "start_date": "2022-05-01", "end_date": "2025-12-31", "status": "active", "city": "Denver", "state": "CO", "project_type": "government"},
    {"project_id": "P014", "project_name": "Thornton Community Recreation Center", "contract_value": 35_000_000, "start_date": "2022-07-15", "end_date": "2024-06-30", "status": "completed", "city": "Thornton", "state": "CO", "project_type": "government"},
    {"project_id": "P015", "project_name": "Westminster High School", "contract_value": 52_000_000, "start_date": "2022-09-01", "end_date": "2024-11-30", "status": "closeout", "city": "Westminster", "state": "CO", "project_type": "education"},
    {"project_id": "P016", "project_name": "Rocky Flats Remediation Facility", "contract_value": 38_000_000, "start_date": "2022-11-01", "end_date": "2025-04-30", "status": "active", "city": "Arvada", "state": "CO", "project_type": "industrial"},
    {"project_id": "P017", "project_name": "Loveland Logistics Hub", "contract_value": 45_000_000, "start_date": "2023-01-15", "end_date": "2025-03-31", "status": "active", "city": "Loveland", "state": "CO", "project_type": "industrial"},
    {"project_id": "P018", "project_name": "Parker Senior Living Campus", "contract_value": 61_000_000, "start_date": "2023-03-01", "end_date": "2025-09-30", "status": "active", "city": "Parker", "state": "CO", "project_type": "healthcare"},
    {"project_id": "P019", "project_name": "Castle Rock Municipal Building", "contract_value": 24_000_000, "start_date": "2023-05-15", "end_date": "2025-02-28", "status": "active", "city": "Castle Rock", "state": "CO", "project_type": "government"},
    {"project_id": "P020", "project_name": "Brighton Solar Farm O&M Facility", "contract_value": 15_000_000, "start_date": "2023-07-01", "end_date": "2024-10-31", "status": "closeout", "city": "Brighton", "state": "CO", "project_type": "industrial"},
    {"project_id": "P021", "project_name": "Englewood Mixed-Use Development", "contract_value": 88_000_000, "start_date": "2023-09-01", "end_date": "2026-03-31", "status": "active", "city": "Englewood", "state": "CO", "project_type": "commercial"},
    {"project_id": "P022", "project_name": "Denver International Airport Terminal Upgrade", "contract_value": 120_000_000, "start_date": "2023-11-01", "end_date": "2026-06-30", "status": "active", "city": "Denver", "state": "CO", "project_type": "infrastructure"},
    {"project_id": "P023", "project_name": "Aurora Veterans Affairs Medical Clinic", "contract_value": 42_000_000, "start_date": "2024-01-15", "end_date": "2026-01-31", "status": "active", "city": "Aurora", "state": "CO", "project_type": "healthcare"},
    {"project_id": "P024", "project_name": "Centennial Airport Hangar Expansion", "contract_value": 19_000_000, "start_date": "2024-03-01", "end_date": "2025-08-31", "status": "active", "city": "Englewood", "state": "CO", "project_type": "infrastructure"},
    {"project_id": "P025", "project_name": "Broomfield Semiconductor Fab Clean Room", "contract_value": 135_000_000, "start_date": "2024-06-01", "end_date": "2027-01-31", "status": "active", "city": "Broomfield", "state": "CO", "project_type": "industrial"},
]

TODAY = date(2025, 8, 11)

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

# COMMAND ----------
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.payments")
print(f"Schema {catalog}.payments ready")

# COMMAND ----------
# Table: pay_applications (~300 rows)
CSI_LINES = [
    ("01 10 00", "General Requirements - Mobilization & Temporary Facilities"),
    ("01 40 00", "General Requirements - Quality Requirements"),
    ("02 41 00", "Demolition"),
    ("03 10 00", "Concrete Formwork"),
    ("03 20 00", "Concrete Reinforcing"),
    ("03 30 00", "Cast-in-Place Concrete"),
    ("04 20 00", "Unit Masonry"),
    ("05 10 00", "Structural Steel Framing"),
    ("05 30 00", "Steel Decking"),
    ("06 10 00", "Rough Carpentry"),
    ("07 50 00", "Membrane Roofing"),
    ("07 90 00", "Joint Protection - Sealants"),
    ("08 10 00", "Doors and Frames"),
    ("08 40 00", "Entrances and Storefronts"),
    ("09 20 00", "Plaster and Gypsum Board"),
    ("09 60 00", "Flooring"),
    ("09 90 00", "Paints and Coatings"),
    ("14 20 00", "Elevators"),
    ("21 10 00", "Fire Suppression - Sprinkler Systems"),
    ("22 10 00", "Plumbing Piping"),
    ("23 31 00", "HVAC Ductwork"),
    ("26 20 00", "Low-Voltage Electrical Distribution"),
    ("26 50 00", "Lighting"),
    ("27 10 00", "Structured Cabling"),
    ("31 20 00", "Earthwork - Grading"),
    ("31 60 00", "Special Foundations"),
    ("32 10 00", "Paving"),
    ("33 10 00", "Water Utilities"),
    ("00-LBR", "Self-Perform Labor"),
    ("00-GC1", "General Conditions - Supervision"),
    ("00-GC2", "General Conditions - Temporary Utilities"),
    ("00-INS", "Insurance and Bonds"),
    ("00-FEE", "Contractor Fee"),
]

random.seed(42)
pay_apps = []
sov_rows = []
pa_id_counter = 1
sov_id_counter = 1

for p in PROJECTS:
    start = parse_date(p["start_date"])
    billing_end = min(parse_date(p["end_date"]), TODAY)
    contract_val = float(p["contract_value"])

    # Build monthly billing periods
    cur = date(start.year, start.month, 1)
    if cur.month == 12:
        cur = date(cur.year + 1, 1, 1)
    else:
        cur = date(cur.year, cur.month + 1, 1)

    periods = []
    while cur <= billing_end:
        if cur.month == 12:
            last = date(cur.year + 1, 1, 1) - timedelta(days=1)
        else:
            last = date(cur.year, cur.month + 1, 1) - timedelta(days=1)
        periods.append((cur, min(last, billing_end)))
        if cur.month == 12:
            cur = date(cur.year + 1, 1, 1)
        else:
            cur = date(cur.year, cur.month + 1, 1)

    n_periods = len(periods)
    if n_periods == 0:
        continue

    # S-curve cumulative percentages
    def scurve_pcts(n, final_pct):
        raw = []
        for i in range(n):
            t = (i + 1) / n
            val = 1 / (1 + ((1 - t) / max(t, 0.0001)) ** 1.3)
            raw.append(val)
        if raw[-1] > 0:
            scaled = [v / raw[-1] * final_pct for v in raw]
        else:
            scaled = [final_pct / n * (i + 1) for i in range(n)]
        return scaled

    if p["status"] in ("completed", "closeout"):
        final_pct = random.uniform(0.97, 1.00)
    else:
        final_pct = random.uniform(0.55, 0.90)

    cum_pcts = scurve_pcts(n_periods, final_pct)

    # Select SOV lines
    n_lines = min(20, len(CSI_LINES))
    selected_lines = random.sample(CSI_LINES, n_lines)
    weights = [random.uniform(0.5, 10.0) for _ in range(n_lines)]
    total_w = sum(weights)
    line_svs = []
    running = 0.0
    for j, w in enumerate(weights):
        if j == n_lines - 1:
            sv = round(contract_val - running, 2)
        else:
            sv = round(contract_val * w / total_w, 2)
        line_svs.append(sv)
        running += sv
    line_cum_pcts = [0.0] * n_lines
    cumulative_billed = 0.0

    for i, (pf, pt) in enumerate(periods):
        pay_app_number = i + 1
        cum_pct = cum_pcts[i]
        work_to_date = round(contract_val * cum_pct, 2)
        prior_pct = cum_pcts[i - 1] if i > 0 else 0.0
        work_prior = round(contract_val * prior_pct, 2)
        work_this_period = round(work_to_date - work_prior, 2)
        stored_materials = round(random.uniform(0, contract_val * 0.005), 2)
        total_earned = round(work_to_date + stored_materials, 2)
        retainage_pct = 10.0 if cum_pct < 0.50 else 5.0
        retainage_amount = round(total_earned * retainage_pct / 100, 2)
        amount_due = round(total_earned - retainage_amount - cumulative_billed, 2)

        submitted_date = pt + timedelta(days=random.randint(3, 10))
        approved_date = submitted_date + timedelta(days=random.randint(7, 14))
        paid_date = approved_date + timedelta(days=random.randint(14, 30))

        is_last = (i == n_periods - 1)
        is_second_last = (i == n_periods - 2)

        if p["status"] == "completed":
            status = "paid"
        elif p["status"] == "closeout":
            if is_last:
                status = "submitted"
                paid_date = None
            elif is_second_last:
                status = "approved"
                paid_date = None
            else:
                status = "paid"
        else:
            if is_last:
                status = "draft"
                approved_date = None
                paid_date = None
            elif is_second_last:
                status = "submitted"
                paid_date = None
            elif i == n_periods - 3:
                status = "approved"
                paid_date = None
            else:
                status = "paid"

        if status == "paid":
            cumulative_billed += amount_due

        pa_id_str = f"PA-{str(pa_id_counter).zfill(4)}"
        pay_apps.append({
            "pay_app_id": pa_id_str,
            "project_id": p["project_id"],
            "pay_app_number": pay_app_number,
            "period_from": pf,
            "period_to": pt,
            "scheduled_value": contract_val,
            "work_completed_prior": work_prior,
            "work_completed_this_period": work_this_period,
            "work_completed_to_date": work_to_date,
            "stored_materials": stored_materials,
            "total_earned": total_earned,
            "retainage_pct": retainage_pct,
            "retainage_amount": retainage_amount,
            "amount_due": amount_due,
            "submitted_date": submitted_date,
            "approved_date": approved_date,
            "paid_date": paid_date,
            "status": status,
        })

        # SOV rows for this pay app
        overall_cum_pct = work_to_date / contract_val if contract_val > 0 else 0.0
        for ln_idx, (cost_code, description) in enumerate(selected_lines):
            sv = line_svs[ln_idx]
            line_factor = random.uniform(0.7, 1.3)
            target_cum = min(overall_cum_pct * line_factor, 1.0)
            target_cum = max(target_cum, line_cum_pcts[ln_idx])
            prior_p = line_cum_pcts[ln_idx]
            this_period_p = round(target_cum - prior_p, 4)
            stored_mat_val = round(sv * random.uniform(0, 0.02), 2)
            total_comp_pct = round(target_cum * 100, 2)
            ret_pct = 10.0 if overall_cum_pct < 0.50 else 5.0
            balance = round(sv * (1.0 - target_cum), 2)
            sov_rows.append({
                "sov_id": f"SOV-{str(sov_id_counter).zfill(6)}",
                "project_id": p["project_id"],
                "pay_app_number": pay_app_number,
                "line_number": ln_idx + 1,
                "cost_code": cost_code,
                "description": description,
                "scheduled_value": sv,
                "completed_prior_pct": round(prior_p * 100, 2),
                "completed_this_period_pct": round(this_period_p * 100, 2),
                "total_completed_pct": total_comp_pct,
                "stored_materials_value": stored_mat_val,
                "retainage_pct": ret_pct,
                "balance_to_finish_value": balance,
            })
            sov_id_counter += 1
            line_cum_pcts[ln_idx] = target_cum

        pa_id_counter += 1

pdf_pa = pd.DataFrame(pay_apps)
for col in ["period_from", "period_to", "submitted_date", "approved_date", "paid_date"]:
    pdf_pa[col] = pd.to_datetime(pdf_pa[col])
spark.createDataFrame(pdf_pa).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.payments.pay_applications")
print(f"pay_applications: {len(pay_apps)} rows")

# COMMAND ----------
# Table: schedule_of_values
pdf_sov = pd.DataFrame(sov_rows)
spark.createDataFrame(pdf_sov).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.payments.schedule_of_values")
print(f"schedule_of_values: {len(sov_rows)} rows")

# COMMAND ----------
# Table: lien_waivers (~2K rows)
fake2 = Faker()
Faker.seed(42)
random.seed(42)

SUBCONTRACTOR_NAMES = [
    "Alpine Mechanical LLC", "Front Range Electrical Services", "Rocky Mountain Concrete Co.",
    "Mile High Steel Fabricators", "Colorado Plumbing Solutions", "Summit Roofing & Waterproofing",
    "Denver Drywall Systems", "Peak Elevation HVAC", "Foothills Fire Protection",
    "Continental Divide Masonry", "Pikes Peak Earthworks", "Gold Hill Glazing & Curtainwall",
    "Flatirons Flooring Group", "Arapahoe Painting & Coatings", "High Country Landscaping",
    "Mesa Verde Concrete Pumping", "Centennial Elevator Group", "Lariat Steel Erectors",
    "Prairie Wind Insulation", "Blue River Utilities Contractors",
]
SUPPLIER_NAMES = [
    "Western States Steel Supply", "Mountain West Lumber", "Colorado Ready Mix",
    "Front Range Glass & Glazing Supply", "Rocky Mountain Electrical Supply",
]

proj_lookup = {p["project_id"]: p for p in PROJECTS}
lien_waivers = []
lw_id_counter = 1

for pa in pay_apps:
    if pa["status"] not in ("paid", "submitted", "approved"):
        continue
    proj_apps_for_p = [x for x in pay_apps if x["project_id"] == pa["project_id"]]
    max_pan = max(x["pay_app_number"] for x in proj_apps_for_p)
    is_final = (pa["pay_app_number"] == max_pan)
    proj_status = proj_lookup[pa["project_id"]]["status"]
    if is_final and proj_status == "completed":
        wtype = "unconditional_final"
    elif pa["status"] == "paid":
        wtype = "unconditional_partial"
    else:
        wtype = "conditional_partial"

    n_subs = random.randint(4, 7)
    subs_sel = random.sample(SUBCONTRACTOR_NAMES, min(n_subs - 1, len(SUBCONTRACTOR_NAMES)))
    sup_sel = random.sample(SUPPLIER_NAMES, 1)
    parties = [("GC", "Huvibar Construction Inc.", wtype)] + \
              [("sub", s, wtype) for s in subs_sel] + \
              [("supplier", sup_sel[0], wtype)]

    for party_type, party_name, w_type in parties:
        if party_type == "GC":
            amt = round(pa["amount_due"], 2)
        else:
            amt = round(pa["amount_due"] * random.uniform(0.03, 0.18), 2)

        if pa["status"] == "paid" and pa["paid_date"] is not None:
            paid_d = pa["paid_date"].date() if hasattr(pa["paid_date"], "date") else pa["paid_date"]
            signed_date = paid_d + timedelta(days=random.randint(1, 5))
            received_date = paid_d + timedelta(days=random.randint(3, 8))
            w_status = "received"
        else:
            signed_date = None
            received_date = None
            w_status = random.choice(["pending", "missing"])

        lien_waivers.append({
            "waiver_id": f"LW-{str(lw_id_counter).zfill(5)}",
            "project_id": pa["project_id"],
            "pay_app_id": pa["pay_app_id"],
            "party_type": party_type,
            "party_name": party_name,
            "waiver_type": w_type,
            "period_ending": pa["period_to"],
            "amount": amt,
            "signed_date": signed_date,
            "received_date": received_date,
            "status": w_status,
        })
        lw_id_counter += 1

pdf_lw = pd.DataFrame(lien_waivers)
for col in ["period_ending", "signed_date", "received_date"]:
    pdf_lw[col] = pd.to_datetime(pdf_lw[col])
spark.createDataFrame(pdf_lw).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.payments.lien_waivers")
print(f"lien_waivers: {len(lien_waivers)} rows")

# COMMAND ----------
# Table: payment_ledger (~1K rows)
random.seed(42)
PAYMENT_METHODS = ["wire", "check", "ACH"]

def rand_ref(method):
    if method == "check":
        return f"CHK-{random.randint(10000, 99999)}"
    elif method == "wire":
        return f"WIRE-{random.randint(100000, 999999)}"
    return f"ACH-{random.randint(100000, 999999)}"

ledger_rows = []
txn_id_counter = 1

for pa in pay_apps:
    if pa["status"] not in ("paid", "approved"):
        continue
    txn_date = pa["paid_date"] if pa["paid_date"] is not None else pa["approved_date"]
    if txn_date is None:
        continue
    method = random.choice(PAYMENT_METHODS)
    txn_date_d = txn_date.date() if hasattr(txn_date, "date") else txn_date
    ledger_rows.append({
        "transaction_id": f"TXN-{str(txn_id_counter).zfill(5)}",
        "project_id": pa["project_id"],
        "pay_app_id": pa["pay_app_id"],
        "transaction_date": txn_date_d,
        "transaction_type": "receipt",
        "from_party": proj_lookup[pa["project_id"]]["project_name"].split()[0] + " Owner LLC",
        "to_party": "Huvibar Construction Inc.",
        "amount": round(pa["amount_due"], 2),
        "payment_method": method,
        "reference_number": rand_ref(method),
        "memo": f"Pay App #{pa['pay_app_number']} - {pa['project_id']}",
    })
    txn_id_counter += 1
    # Disbursements to subs
    sub_names = random.sample(SUBCONTRACTOR_NAMES, random.randint(2, 3))
    for sub in sub_names:
        sub_amt = round(pa["amount_due"] * random.uniform(0.08, 0.20), 2)
        disburse_date = txn_date_d + timedelta(days=random.randint(3, 10))
        d_method = random.choice(PAYMENT_METHODS)
        ledger_rows.append({
            "transaction_id": f"TXN-{str(txn_id_counter).zfill(5)}",
            "project_id": pa["project_id"],
            "pay_app_id": pa["pay_app_id"],
            "transaction_date": disburse_date,
            "transaction_type": "disbursement",
            "from_party": "Huvibar Construction Inc.",
            "to_party": sub,
            "amount": sub_amt,
            "payment_method": d_method,
            "reference_number": rand_ref(d_method),
            "memo": f"Subcontract payment PA#{pa['pay_app_number']} - {sub}",
        })
        txn_id_counter += 1

pdf_ledger = pd.DataFrame(ledger_rows)
pdf_ledger["transaction_date"] = pd.to_datetime(pdf_ledger["transaction_date"])
spark.createDataFrame(pdf_ledger).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.payments.payment_ledger")
print(f"payment_ledger: {len(ledger_rows)} rows")

# COMMAND ----------
print("All payments tables created successfully!")
print(f"  - pay_applications: {len(pay_apps)} rows")
print(f"  - schedule_of_values: {len(sov_rows)} rows")
print(f"  - lien_waivers: {len(lien_waivers)} rows")
print(f"  - payment_ledger: {len(ledger_rows)} rows")
