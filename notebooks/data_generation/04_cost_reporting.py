# Databricks notebook source

# COMMAND ----------
%pip install faker --quiet

# COMMAND ----------

import uuid
import random
import datetime
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

catalog = "css_genie"  # hardcoded for serverless compatibility

PROJECTS = [
    {"project_id": "P001", "project_name": "Centennial Tower Office Complex", "contract_value": 85000000, "start_date": "2020-03-01", "end_date": "2022-08-15", "status": "completed", "city": "Denver", "state": "CO"},
    {"project_id": "P002", "project_name": "Rocky Mountain Medical Center Expansion", "contract_value": 125000000, "start_date": "2020-06-15", "end_date": "2023-01-30", "status": "completed", "city": "Aurora", "state": "CO"},
    {"project_id": "P003", "project_name": "Aurora Industrial Warehouse Phase I", "contract_value": 22000000, "start_date": "2020-09-01", "end_date": "2021-11-30", "status": "completed", "city": "Aurora", "state": "CO"},
    {"project_id": "P004", "project_name": "Lakewood Elementary School Modernization", "contract_value": 18500000, "start_date": "2020-11-01", "end_date": "2022-05-31", "status": "completed", "city": "Lakewood", "state": "CO"},
    {"project_id": "P005", "project_name": "Colorado Springs Data Center", "contract_value": 55000000, "start_date": "2021-01-15", "end_date": "2022-09-30", "status": "completed", "city": "Colorado Springs", "state": "CO"},
    {"project_id": "P006", "project_name": "Union Station Hotel Renovation", "contract_value": 32000000, "start_date": "2021-03-01", "end_date": "2022-12-15", "status": "completed", "city": "Denver", "state": "CO"},
    {"project_id": "P007", "project_name": "Fort Collins Civic Center", "contract_value": 48000000, "start_date": "2021-05-15", "end_date": "2023-07-31", "status": "completed", "city": "Fort Collins", "state": "CO"},
    {"project_id": "P008", "project_name": "Boulder Tech Campus Building A", "contract_value": 72000000, "start_date": "2021-07-01", "end_date": "2023-11-30", "status": "completed", "city": "Boulder", "state": "CO"},
    {"project_id": "P009", "project_name": "Pueblo Steel Mill Upgrade", "contract_value": 41000000, "start_date": "2021-09-01", "end_date": "2023-03-31", "status": "completed", "city": "Pueblo", "state": "CO"},
    {"project_id": "P010", "project_name": "Greeley Wastewater Treatment Plant", "contract_value": 67000000, "start_date": "2021-11-01", "end_date": "2024-02-28", "status": "completed", "city": "Greeley", "state": "CO"},
    {"project_id": "P011", "project_name": "DTC Multifamily Residential Tower", "contract_value": 95000000, "start_date": "2022-01-15", "end_date": "2024-08-31", "status": "completed", "city": "Greenwood Village", "state": "CO"},
    {"project_id": "P012", "project_name": "Longmont Distribution Center", "contract_value": 28000000, "start_date": "2022-03-01", "end_date": "2023-09-30", "status": "completed", "city": "Longmont", "state": "CO"},
    {"project_id": "P013", "project_name": "Colorado Convention Center Expansion", "contract_value": 150000000, "start_date": "2022-05-01", "end_date": "2025-12-31", "status": "active", "city": "Denver", "state": "CO"},
    {"project_id": "P014", "project_name": "Thornton Community Recreation Center", "contract_value": 35000000, "start_date": "2022-07-15", "end_date": "2024-06-30", "status": "completed", "city": "Thornton", "state": "CO"},
    {"project_id": "P015", "project_name": "Westminster High School New Construction", "contract_value": 52000000, "start_date": "2022-09-01", "end_date": "2024-11-30", "status": "closeout", "city": "Westminster", "state": "CO"},
    {"project_id": "P016", "project_name": "Rocky Flats Remediation Facility", "contract_value": 38000000, "start_date": "2022-11-01", "end_date": "2025-04-30", "status": "active", "city": "Arvada", "state": "CO"},
    {"project_id": "P017", "project_name": "Loveland Logistics Hub", "contract_value": 45000000, "start_date": "2023-01-15", "end_date": "2025-03-31", "status": "active", "city": "Loveland", "state": "CO"},
    {"project_id": "P018", "project_name": "Parker Senior Living Campus", "contract_value": 61000000, "start_date": "2023-03-01", "end_date": "2025-09-30", "status": "active", "city": "Parker", "state": "CO"},
    {"project_id": "P019", "project_name": "Castle Rock Municipal Building", "contract_value": 24000000, "start_date": "2023-05-15", "end_date": "2025-02-28", "status": "active", "city": "Castle Rock", "state": "CO"},
    {"project_id": "P020", "project_name": "Brighton Solar Farm O&M Facility", "contract_value": 15000000, "start_date": "2023-07-01", "end_date": "2024-10-31", "status": "closeout", "city": "Brighton", "state": "CO"},
    {"project_id": "P021", "project_name": "Englewood Mixed-Use Development", "contract_value": 88000000, "start_date": "2023-09-01", "end_date": "2026-03-31", "status": "active", "city": "Englewood", "state": "CO"},
    {"project_id": "P022", "project_name": "Denver International Airport Terminal Upgrade", "contract_value": 120000000, "start_date": "2023-11-01", "end_date": "2026-06-30", "status": "active", "city": "Denver", "state": "CO"},
    {"project_id": "P023", "project_name": "Aurora Veterans Affairs Medical Clinic", "contract_value": 42000000, "start_date": "2024-01-15", "end_date": "2026-01-31", "status": "active", "city": "Aurora", "state": "CO"},
    {"project_id": "P024", "project_name": "Centennial Airport Hangar Expansion", "contract_value": 19000000, "start_date": "2024-03-01", "end_date": "2025-08-31", "status": "active", "city": "Englewood", "state": "CO"},
    {"project_id": "P025", "project_name": "Broomfield Semiconductor Fab Clean Room", "contract_value": 135000000, "start_date": "2024-06-01", "end_date": "2027-01-31", "status": "active", "city": "Broomfield", "state": "CO"},
]

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.cost_reporting")

# COMMAND ----------
# ==============================================================================
# TABLE 1: budget_line_items (~2,000 rows)
# ==============================================================================

CSI_DIVISIONS = [
    ("01-100", "General Requirements - Temporary Facilities"),
    ("01-200", "General Requirements - Project Management"),
    ("01-300", "General Requirements - Submittals"),
    ("01-400", "General Requirements - Quality Requirements"),
    ("01-500", "General Requirements - Temporary Utilities"),
    ("02-100", "Existing Conditions - Demolition"),
    ("02-200", "Existing Conditions - Site Assessment"),
    ("03-100", "Concrete - Formwork"),
    ("03-200", "Concrete - Reinforcing"),
    ("03-300", "Concrete - Cast-in-Place"),
    ("03-400", "Concrete - Precast"),
    ("04-200", "Masonry - Unit Masonry"),
    ("04-400", "Masonry - Stone"),
    ("05-100", "Metals - Structural Steel"),
    ("05-200", "Metals - Metal Joists"),
    ("05-300", "Metals - Metal Decking"),
    ("05-400", "Metals - Cold-Formed Metal Framing"),
    ("05-500", "Metals - Metal Fabrications"),
    ("06-100", "Wood - Rough Carpentry"),
    ("06-200", "Wood - Finish Carpentry"),
    ("07-100", "Thermal - Waterproofing"),
    ("07-200", "Thermal - Insulation"),
    ("07-300", "Thermal - Roofing - Shingles"),
    ("07-400", "Thermal - Roofing - Membrane"),
    ("07-500", "Thermal - Roofing - Metal"),
    ("07-900", "Thermal - Joint Sealants"),
    ("08-100", "Openings - Metal Doors and Frames"),
    ("08-300", "Openings - Specialty Doors"),
    ("08-400", "Openings - Entrances and Storefronts"),
    ("08-500", "Openings - Windows"),
    ("08-700", "Openings - Hardware"),
    ("08-800", "Openings - Glazing"),
    ("09-200", "Finishes - Plaster and Gypsum Board"),
    ("09-300", "Finishes - Tiling"),
    ("09-500", "Finishes - Ceilings"),
    ("09-600", "Finishes - Flooring"),
    ("09-900", "Finishes - Painting"),
    ("10-100", "Specialties - Visual Display Units"),
    ("10-400", "Specialties - Signage"),
    ("10-800", "Specialties - Toilet Accessories"),
    ("11-000", "Equipment - General"),
    ("12-300", "Furnishings - Casework"),
    ("12-400", "Furnishings - Furnishings and Accessories"),
    ("13-000", "Special Construction - General"),
    ("14-200", "Conveying - Elevators"),
    ("14-400", "Conveying - Lifts"),
    ("21-100", "Fire Suppression - Sprinkler"),
    ("22-100", "Plumbing - Piping"),
    ("22-300", "Plumbing - Plumbing Equipment"),
    ("22-400", "Plumbing - Plumbing Fixtures"),
    ("23-100", "HVAC - Ductwork"),
    ("23-200", "HVAC - Equipment"),
    ("23-300", "HVAC - Controls"),
    ("26-100", "Electrical - Medium Voltage"),
    ("26-200", "Electrical - Low Voltage Distribution"),
    ("26-500", "Electrical - Lighting"),
    ("26-700", "Electrical - Electric Utilities"),
    ("27-100", "Communications - Structured Cabling"),
    ("27-500", "Communications - Distributed Communications"),
    ("28-100", "Electronic Safety - Fire Detection"),
    ("28-200", "Electronic Safety - Access Control"),
    ("31-100", "Earthwork - Site Clearing"),
    ("31-200", "Earthwork - Earthwork"),
    ("31-300", "Earthwork - Earthwork Methods"),
    ("32-100", "Exterior Improvements - Paving"),
    ("32-300", "Exterior Improvements - Fencing"),
    ("32-900", "Exterior Improvements - Landscaping"),
    ("33-100", "Utilities - Water Utilities"),
    ("33-300", "Utilities - Storm Utilities"),
    ("33-400", "Utilities - Sanitary Utilities"),
    ("33-700", "Utilities - Electrical Utilities"),
    ("00-001", "Overhead and Profit"),
    ("00-002", "General Liability Insurance"),
    ("00-003", "Builder's Risk Insurance"),
    ("00-004", "Performance Bond"),
    ("00-005", "Contingency"),
    ("00-006", "Owner Allowance"),
    ("00-007", "Design Contingency"),
    ("00-008", "Escalation Reserve"),
]

budget_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    cv = proj["contract_value"]

    # Assign weights to divisions based on project type
    weights = []
    for code, desc in CSI_DIVISIONS:
        w = 1.0
        div = code.split("-")[0]
        if div in ("03", "05"):
            w = 3.0
        elif div in ("22", "23", "26"):
            w = 2.5
        elif div in ("09", "08"):
            w = 2.0
        elif div in ("00",):
            w = 1.5
        elif div in ("31", "32", "33"):
            w = 1.8
        weights.append(w)

    total_weight = sum(weights)
    norm_weights = [w / total_weight for w in weights]

    # Assign original budget portions
    division_budgets = []
    remaining = cv
    for i, (code, desc) in enumerate(CSI_DIVISIONS):
        if i < len(CSI_DIVISIONS) - 1:
            amt = round(cv * norm_weights[i] / 1000) * 1000
        else:
            amt = remaining
        division_budgets.append(amt)
        remaining -= amt

    # Distribute remainder to first item
    if remaining != 0:
        division_budgets[0] += remaining

    # Generate original budget rows
    for i, (code, desc) in enumerate(CSI_DIVISIONS):
        orig_budget = division_budgets[i]
        budget_rows.append({
            "budget_id": str(uuid.uuid4()),
            "project_id": pid,
            "cost_code": code,
            "description": desc,
            "original_budget": orig_budget,
            "approved_change_orders": 0,
            "current_budget": orig_budget,
            "budget_type": "original",
        })

    # Add some revised rows (change orders applied to specific line items)
    num_revised = random.randint(5, 12)
    revised_codes = random.sample(list(range(len(CSI_DIVISIONS))), num_revised)
    for idx in revised_codes:
        code, desc = CSI_DIVISIONS[idx]
        orig = division_budgets[idx]
        co_amount = round(random.uniform(0.02, 0.15) * orig / 1000) * 1000
        if random.random() < 0.15:
            co_amount = -co_amount
        budget_rows.append({
            "budget_id": str(uuid.uuid4()),
            "project_id": pid,
            "cost_code": code,
            "description": desc + " (Revised)",
            "original_budget": orig,
            "approved_change_orders": co_amount,
            "current_budget": orig + co_amount,
            "budget_type": "revised",
        })

budget_pdf = pd.DataFrame(budget_rows)
budget_sdf = spark.createDataFrame(budget_pdf)
budget_sdf.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.cost_reporting.budget_line_items")
df = spark.table(f"{catalog}.cost_reporting.budget_line_items")
print(f"Created {catalog}.cost_reporting.budget_line_items with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 2: committed_costs (~3,000 rows)
# ==============================================================================

SUBCONTRACTORS = [
    "Alpine Mechanical LLC", "Front Range Electrical Co", "Rocky Mountain Concrete Inc",
    "Centennial Steel Erectors", "High Plains Drywall", "Colorado Plumbing Group",
    "Summit Roofing Systems", "Pikes Peak Glazing", "Mile High Fire Protection",
    "Foothills Earthworks", "Gateway Masonry Inc", "Colorado Elevator Service",
    "Denver Tile & Stone", "Boulder Painting Co", "Northern Colorado HVAC",
    "Pueblo Rebar Inc", "Aurora Electrical Services", "Front Range Insulation",
    "Colorado Flooring Solutions", "Lakewood Landscaping LLC",
]

SUPPLIERS = [
    "Western States Lumber", "Colorado Ready Mix", "Mountain West Steel Supply",
    "Denver Electrical Supply", "Rocky Mountain Hardware", "Intermountain Pipe & Supply",
    "Colorado Roofing Supply", "Western Fasteners Inc", "Summit Building Products",
    "Colorado Paint & Coatings",
]

RENTAL_COMPANIES = [
    "United Rentals", "Sunbelt Rentals", "BlueLine Rental", "H&E Equipment Services",
    "BrandSafway",
]

committed_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    cv = proj["contract_value"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    proj_end_effective = min(end, today)
    duration_days = (proj_end_effective - start).days
    is_complete = proj["status"] in ("completed", "closeout")

    # ~120 commitments per project
    n_subs = random.randint(35, 50)
    n_suppliers = random.randint(45, 55)
    n_rentals = random.randint(20, 30)

    for i in range(n_subs):
        commit_date = start + datetime.timedelta(days=random.randint(0, min(90, duration_days)))
        committed = round(random.uniform(500000, min(10000000, cv * 0.12)) / 1000) * 1000
        pct_invoiced = random.uniform(0.6, 1.0) if is_complete else random.uniform(0.2, 0.85)
        invoiced = round(committed * pct_invoiced / 100) * 100
        pct_paid = random.uniform(0.9, 1.0) if is_complete else random.uniform(0.7, 0.95)
        paid = round(invoiced * pct_paid / 100) * 100
        code_idx = random.randint(0, len(CSI_DIVISIONS) - 1)
        status = "closed" if is_complete else "active"
        if random.random() < 0.03:
            status = "cancelled"
            invoiced = 0
            paid = 0
        committed_rows.append({
            "commitment_id": str(uuid.uuid4()),
            "project_id": pid,
            "vendor_name": random.choice(SUBCONTRACTORS),
            "vendor_type": "subcontractor",
            "cost_code": CSI_DIVISIONS[code_idx][0],
            "description": CSI_DIVISIONS[code_idx][1] + " Subcontract",
            "committed_amount": committed,
            "invoiced_to_date": invoiced,
            "paid_to_date": paid,
            "balance_remaining": committed - paid,
            "commitment_date": commit_date.isoformat(),
            "status": status,
        })

    for i in range(n_suppliers):
        commit_date = start + datetime.timedelta(days=random.randint(0, min(180, duration_days)))
        committed = round(random.uniform(50000, 500000) / 1000) * 1000
        pct_invoiced = random.uniform(0.7, 1.0) if is_complete else random.uniform(0.3, 0.9)
        invoiced = round(committed * pct_invoiced / 100) * 100
        pct_paid = random.uniform(0.95, 1.0) if is_complete else random.uniform(0.8, 0.98)
        paid = round(invoiced * pct_paid / 100) * 100
        code_idx = random.randint(0, len(CSI_DIVISIONS) - 1)
        status = "closed" if is_complete else "active"
        committed_rows.append({
            "commitment_id": str(uuid.uuid4()),
            "project_id": pid,
            "vendor_name": random.choice(SUPPLIERS),
            "vendor_type": "supplier",
            "cost_code": CSI_DIVISIONS[code_idx][0],
            "description": "Material Purchase Order - " + CSI_DIVISIONS[code_idx][1],
            "committed_amount": committed,
            "invoiced_to_date": invoiced,
            "paid_to_date": paid,
            "balance_remaining": committed - paid,
            "commitment_date": commit_date.isoformat(),
            "status": status,
        })

    for i in range(n_rentals):
        commit_date = start + datetime.timedelta(days=random.randint(0, min(60, duration_days)))
        committed = round(random.uniform(5000, 100000) / 500) * 500
        pct_invoiced = random.uniform(0.8, 1.0) if is_complete else random.uniform(0.4, 0.9)
        invoiced = round(committed * pct_invoiced / 100) * 100
        pct_paid = random.uniform(0.95, 1.0) if is_complete else random.uniform(0.85, 1.0)
        paid = round(invoiced * pct_paid / 100) * 100
        status = "closed" if is_complete else "active"
        committed_rows.append({
            "commitment_id": str(uuid.uuid4()),
            "project_id": pid,
            "vendor_name": random.choice(RENTAL_COMPANIES),
            "vendor_type": "rental",
            "cost_code": "01-500",
            "description": "Equipment Rental - " + random.choice(["Crane", "Lift", "Excavator", "Generator", "Scaffolding"]),
            "committed_amount": committed,
            "invoiced_to_date": invoiced,
            "paid_to_date": paid,
            "balance_remaining": committed - paid,
            "commitment_date": commit_date.isoformat(),
            "status": status,
        })

committed_pdf = pd.DataFrame(committed_rows)
committed_sdf = spark.createDataFrame(committed_pdf)
committed_sdf.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.cost_reporting.committed_costs")
df = spark.table(f"{catalog}.cost_reporting.committed_costs")
print(f"Created {catalog}.cost_reporting.committed_costs with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 3: actual_costs (~80,000 rows)
# ==============================================================================

EMPLOYEES = [
    "James Harrington", "Maria Santos", "David Chen", "Lisa Okonkwo", "Robert Paulson",
    "Angela Torres", "Michael Fitzgerald", "Sarah Kowalski", "Thomas Brennan", "Jennifer Marsh",
    "Carlos Rivera", "Heather MacAllister", "Kevin O'Brien", "Nicole Summers", "Patrick Walsh",
    "Amanda Foster", "Derek Whitfield", "Priya Nair", "Tyler Goodwin", "Shannon Holt",
]

LABOR_DESCS = [
    "Superintendent - Daily Field Labor", "Foreman Labor - Concrete Crew", "Field Engineer - Layout",
    "Project Manager - Site Time", "Safety Officer - Site Inspection", "Equipment Operator",
    "Ironworker Labor", "Carpenter Labor", "Laborer - General",
    "QC Inspector - Field", "Surveyor - Site", "MEP Coordinator",
]

MATERIAL_DESCS = [
    "Ready-mix concrete delivery", "Structural steel delivery", "Rebar delivery",
    "Lumber and sheeting delivery", "Drywall material", "Roofing membrane material",
    "Electrical conduit and wire", "Plumbing pipe and fittings", "HVAC ductwork material",
    "Glazing units delivery", "Insulation material", "Flooring material delivery",
    "Doors and hardware delivery", "Paint and coatings", "Masonry block delivery",
]

EQUIP_DESCS = [
    "Tower crane rental", "Man lift rental", "Concrete pump rental",
    "Generator rental", "Compressor rental", "Excavator rental",
    "Skid steer rental", "Welding equipment rental",
]

SUB_DESCS = [
    "Subcontractor progress billing", "Sub partial payment application",
    "Specialty contractor invoice", "Trade subcontract draw",
]

actual_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    cv = proj["contract_value"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    effective_end = min(end, today)
    duration_days = max((effective_end - start).days, 30)

    # Scale transactions to project size
    base_txns = int(cv / 1000000 * 30)
    n_txns = min(max(base_txns, 500), 8000)

    # Build list of working dates
    all_days = []
    d = start
    while d <= effective_end:
        if d.weekday() < 5:
            all_days.append(d)
        d += datetime.timedelta(days=1)
    if not all_days:
        all_days = [start]

    for _ in range(n_txns):
        txn_date = random.choice(all_days)
        cost_type = random.choices(
            ["labor", "material", "equipment", "sub", "other"],
            weights=[30, 25, 10, 30, 5]
        )[0]

        if cost_type == "labor":
            amount = round(random.uniform(500, 5000) / 50) * 50
            desc = random.choice(LABOR_DESCS)
            vendor = "Huvibar Construction"
            code_idx = random.randint(0, 7)
        elif cost_type == "material":
            amount = round(random.uniform(1000, 50000) / 100) * 100
            desc = random.choice(MATERIAL_DESCS)
            vendor = random.choice(SUPPLIERS)
            code_idx = random.randint(7, 40)
        elif cost_type == "equipment":
            amount = round(random.uniform(500, 25000) / 100) * 100
            desc = random.choice(EQUIP_DESCS)
            vendor = random.choice(RENTAL_COMPANIES)
            code_idx = 4
        elif cost_type == "sub":
            amount = round(random.uniform(10000, 500000) / 1000) * 1000
            desc = random.choice(SUB_DESCS)
            vendor = random.choice(SUBCONTRACTORS)
            code_idx = random.randint(5, len(CSI_DIVISIONS) - 9)
        else:
            amount = round(random.uniform(100, 5000) / 50) * 50
            desc = "Miscellaneous project cost"
            vendor = fake.company()
            code_idx = 0

        invoice_ref = f"INV-{random.randint(10000, 99999)}"
        posted_by = random.choice(EMPLOYEES)
        code = CSI_DIVISIONS[code_idx][0]

        actual_rows.append({
            "transaction_id": str(uuid.uuid4()),
            "project_id": pid,
            "cost_code": code,
            "transaction_date": txn_date.isoformat(),
            "vendor_name": vendor,
            "description": desc,
            "amount": amount,
            "cost_type": cost_type,
            "invoice_reference": invoice_ref,
            "posted_by": posted_by,
            "commitment_id": str(uuid.uuid4()) if cost_type in ("sub", "material") and random.random() < 0.7 else None,
        })

actual_pdf = pd.DataFrame(actual_rows)
actual_sdf = spark.createDataFrame(actual_pdf)
actual_sdf.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.cost_reporting.actual_costs")
df = spark.table(f"{catalog}.cost_reporting.actual_costs")
print(f"Created {catalog}.cost_reporting.actual_costs with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 4: cost_forecast (~3,000 rows)
# ==============================================================================

PM_NAMES = [
    "James Harrington", "Maria Santos", "David Chen", "Lisa Okonkwo", "Robert Paulson",
    "Angela Torres", "Michael Fitzgerald", "Sarah Kowalski", "Thomas Brennan",
]

FORECAST_NOTES = [
    None, None, None, None,
    "Tracking to budget. No significant variances identified.",
    "Labor productivity lower than anticipated; monitoring closely.",
    "Material escalation impacting concrete division.",
    "Change order P&P in negotiation; estimate subject to revision.",
    "On track. Owner requested scope addition pending pricing.",
    "Weather delays in Q2 pushed structural completion; recovery plan in place.",
    "Forecast updated following GMP reconciliation.",
    "Subcontractor buyout savings applied to contingency.",
]

forecast_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    cv = proj["contract_value"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    effective_end = min(end, today)
    duration_months = max(int((effective_end - start).days / 30), 4)
    n_snapshots = min(max(duration_months, 4), 24)

    pm = random.choice(PM_NAMES)
    running_actual = 0.0
    co_delta = round(random.uniform(-0.02, 0.08) * cv / 1000) * 1000

    for snap_idx in range(n_snapshots):
        months_offset = int(snap_idx * duration_months / n_snapshots)
        snap_date = (start + datetime.timedelta(days=months_offset * 30)).replace(day=1)
        progress_pct = (snap_idx + 1) / n_snapshots

        budget_orig = cv
        budget_current = cv + co_delta
        running_actual += round(cv * (1 / n_snapshots) * random.uniform(0.85, 1.15) / 100) * 100
        actual_to_date = min(running_actual, budget_current * 0.98)

        # ETC based on progress and any known issues
        productivity_factor = random.uniform(0.95, 1.08)
        etc = round((budget_current - actual_to_date) * productivity_factor / 100) * 100
        eac = actual_to_date + etc
        variance = budget_current - eac
        variance_pct = round(variance / budget_current * 100, 2) if budget_current else 0

        for code, desc in random.sample(CSI_DIVISIONS, min(5, len(CSI_DIVISIONS))):
            forecast_rows.append({
                "forecast_id": str(uuid.uuid4()),
                "project_id": pid,
                "cost_code": code,
                "forecast_month": snap_date.isoformat(),
                "budget_original": budget_orig,
                "budget_current": budget_current,
                "actual_to_date": round(actual_to_date * 0.2 / 100) * 100,
                "estimate_to_complete": round(etc * 0.2 / 100) * 100,
                "estimate_at_completion": round(eac * 0.2 / 100) * 100,
                "variance_amount": round(variance * 0.2 / 100) * 100,
                "variance_pct": variance_pct,
                "forecast_by": pm,
                "notes": random.choice(FORECAST_NOTES),
            })

forecast_pdf = pd.DataFrame(forecast_rows)
forecast_sdf = spark.createDataFrame(forecast_pdf)
forecast_sdf.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.cost_reporting.cost_forecast")
df = spark.table(f"{catalog}.cost_reporting.cost_forecast")
print(f"Created {catalog}.cost_reporting.cost_forecast with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 5: change_orders (~500 rows)
# ==============================================================================

CO_DESCRIPTIONS = [
    "Unforeseen underground utilities relocation",
    "Owner-directed scope addition - expanded lobby",
    "Design error correction - beam sizing revision",
    "Differing site conditions - soil bearing capacity",
    "Owner requested finish upgrade - lobby materials",
    "Weather delay compensation - extended winter conditions",
    "Scope gap - electrical panel capacity increase",
    "Owner-directed deletion - scope reduction",
    "Differing conditions - rock excavation encountered",
    "Design coordination issue - MEP clash resolution",
    "Owner change - added generator capacity",
    "Owner change - facade material substitution",
    "Design error - waterproofing detail revision",
    "Scope gap - fire suppression coverage extension",
    "Owner-directed acceleration premium",
    "Unforeseen hazardous material abatement",
    "Owner addition - rooftop terrace",
    "Value engineering credit - structural system",
    "Owner change - tenant improvement additions",
    "Code compliance revision - egress width",
]

REASON_CODES = ["owner_directed", "differing_conditions", "design_error", "weather", "scope_gap"]
CO_TYPES = ["owner_co", "sub_co", "internal"]

co_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    cv = proj["contract_value"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    is_complete = proj["status"] in ("completed", "closeout")
    today = datetime.date(2026, 8, 11)
    effective_end = min(end, today)
    duration_days = max((effective_end - start).days, 60)

    n_cos = random.randint(15, 25)
    co_counter = 1

    for _ in range(n_cos):
        submit_days = random.randint(30, duration_days - 10)
        submitted_date = start + datetime.timedelta(days=submit_days)

        co_type = random.choices(CO_TYPES, weights=[50, 35, 15])[0]
        reason = random.choice(REASON_CODES)
        desc = random.choice(CO_DESCRIPTIONS)

        # Amount
        if co_type == "internal":
            amount = round(random.uniform(5000, 100000) / 1000) * 1000
        else:
            amount = round(random.uniform(10000, cv * 0.04) / 1000) * 1000
        if random.random() < 0.1:
            amount = -amount

        # Status
        if is_complete:
            status = random.choices(["approved", "approved", "approved", "rejected", "void"], weights=[70, 10, 5, 10, 5])[0]
        else:
            status = random.choices(["pending", "approved", "rejected", "void"], weights=[30, 55, 10, 5])[0]

        approved_date = None
        if status == "approved":
            days_to_approve = random.randint(7, 45)
            approved_date = (submitted_date + datetime.timedelta(days=days_to_approve)).isoformat()

        affects_schedule = random.random() < 0.35
        schedule_days = 0
        if affects_schedule:
            schedule_days = random.randint(1, 30)

        co_rows.append({
            "co_id": str(uuid.uuid4()),
            "project_id": pid,
            "co_number": f"CO-{co_counter:03d}",
            "co_type": co_type,
            "description": desc,
            "reason_code": reason,
            "submitted_date": submitted_date.isoformat(),
            "approved_date": approved_date,
            "amount": amount,
            "status": status,
            "affects_schedule": affects_schedule,
            "schedule_days_impact": schedule_days,
        })
        co_counter += 1

co_pdf = pd.DataFrame(co_rows)
co_sdf = spark.createDataFrame(co_pdf)
co_sdf.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.cost_reporting.change_orders")
df = spark.table(f"{catalog}.cost_reporting.change_orders")
print(f"Created {catalog}.cost_reporting.change_orders with {df.count()} rows")
