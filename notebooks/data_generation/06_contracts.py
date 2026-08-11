# Databricks notebook source

# COMMAND ----------

import uuid
import random
import math
from datetime import datetime, timedelta, date
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

catalog = spark.conf.get("catalog", "css_genie")

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

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.contracts")

# COMMAND ----------

# ============================================================
# TABLE: prime_contracts  (25 rows, one per project)
# ============================================================

def parse_date(d_str):
    return datetime.strptime(d_str, "%Y-%m-%d").date()

OWNER_NAMES = {
    "P001": "Centennial Partners LLC",
    "P002": "UCHealth System",
    "P003": "Aurora Industrial Properties LLC",
    "P004": "Jefferson County Public Schools",
    "P005": "Peak Technology Real Estate Partners",
    "P006": "Union Station Alliance LLC",
    "P007": "City of Fort Collins",
    "P008": "University of Colorado Research Foundation",
    "P009": "EVRAZ Rocky Mountain Steel Inc",
    "P010": "City of Greeley",
    "P011": "DTC Development Partners LLC",
    "P012": "Mountain West Logistics Properties LLC",
    "P013": "City and County of Denver - Denver Arts and Venues",
    "P014": "City of Thornton",
    "P015": "Adams 12 Five Star Schools",
    "P016": "US Department of Energy Rocky Flats Site Office",
    "P017": "Front Range Logistics LLC",
    "P018": "Covenant Senior Living Colorado",
    "P019": "Town of Castle Rock",
    "P020": "Xcel Energy Services Inc",
    "P021": "Englewood Development Group LLC",
    "P022": "Denver International Airport Authority",
    "P023": "US Department of Veterans Affairs Colorado",
    "P024": "Centennial Airport Authority",
    "P025": "Infineon Technologies Colorado LLC",
}

ARCHITECT_FIRMS = {
    "P001": "Gensler",
    "P002": "HKS Architects",
    "P003": "Ware Malcomb",
    "P004": "DLR Group",
    "P005": "HOK",
    "P006": "RB+B Architects",
    "P007": "Fentress Architects",
    "P008": "Gensler",
    "P009": "Jacobs Engineering Group",
    "P010": "AECOM",
    "P011": "OZ Architecture",
    "P012": "Ware Malcomb",
    "P013": "Fentress Architects",
    "P014": "Stantec",
    "P015": "DLR Group",
    "P016": "AECOM",
    "P017": "Ware Malcomb",
    "P018": "OZ Architecture",
    "P019": "RB+B Architects",
    "P020": "Burns and McDonnell",
    "P021": "Gensler",
    "P022": "HOK",
    "P023": "AECOM",
    "P024": "Jacobs Engineering Group",
    "P025": "HOK",
}

CONTRACT_TYPES = {
    "P001": "GMP",
    "P002": "GMP",
    "P003": "lump_sum",
    "P004": "lump_sum",
    "P005": "GMP",
    "P006": "cost_plus",
    "P007": "lump_sum",
    "P008": "GMP",
    "P009": "cost_plus",
    "P010": "lump_sum",
    "P011": "GMP",
    "P012": "lump_sum",
    "P013": "GMP",
    "P014": "lump_sum",
    "P015": "lump_sum",
    "P016": "cost_plus",
    "P017": "lump_sum",
    "P018": "GMP",
    "P019": "lump_sum",
    "P020": "lump_sum",
    "P021": "GMP",
    "P022": "GMP",
    "P023": "GMP",
    "P024": "lump_sum",
    "P025": "GMP",
}

random.seed(101)
prime_rows = []
prime_contract_ids = {}  # project_id -> contract_id

for i, p in enumerate(PROJECTS):
    start = parse_date(p["start_date"])
    end = parse_date(p["end_date"])
    year = start.year

    contract_id = str(uuid.uuid4())
    prime_contract_ids[p["project_id"]] = contract_id

    contract_number = f"HC-{year}-{i + 1:03d}"
    contract_type = CONTRACT_TYPES[p["project_id"]]
    original_value = float(p["contract_value"])

    if p["status"] == "completed":
        co_pct = random.uniform(0.03, 0.08)
    elif p["status"] == "closeout":
        co_pct = random.uniform(0.03, 0.06)
    else:
        co_pct = random.uniform(0.01, 0.03)

    change_order_value = round(original_value * co_pct, 2)
    current_value = round(original_value + change_order_value, 2)

    exec_offset = random.randint(30, 60)
    execution_date = start - timedelta(days=exec_offset)
    substantial_completion = end - timedelta(days=30)

    if original_value < 20000000:
        ld = random.choice([1000, 1500, 2000, 2500])
    elif original_value < 50000000:
        ld = random.choice([2000, 2500, 3000, 4000, 5000])
    elif original_value < 100000000:
        ld = random.choice([5000, 6000, 7500])
    else:
        ld = random.choice([7500, 8000, 10000])

    prime_rows.append({
        "contract_id": contract_id,
        "project_id": p["project_id"],
        "contract_number": contract_number,
        "contract_type": contract_type,
        "original_value": original_value,
        "change_order_value": change_order_value,
        "current_value": current_value,
        "owner_name": OWNER_NAMES[p["project_id"]],
        "architect_firm": ARCHITECT_FIRMS[p["project_id"]],
        "execution_date": execution_date.strftime("%Y-%m-%d"),
        "notice_to_proceed_date": start.strftime("%Y-%m-%d"),
        "substantial_completion_date": substantial_completion.strftime("%Y-%m-%d"),
        "final_completion_date": end.strftime("%Y-%m-%d"),
        "liquidated_damages_per_day": ld,
        "retainage_pct": 10.0,
        "status": p["status"],
    })

prime_pdf = pd.DataFrame(prime_rows)
prime_df = spark.createDataFrame(prime_pdf)
prime_df.write.mode("overwrite").saveAsTable(f"{catalog}.contracts.prime_contracts")
df = spark.table(f"{catalog}.contracts.prime_contracts")
print(f"Created {catalog}.contracts.prime_contracts with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: subcontracts  (~150 rows, ~6 per project)
# ============================================================

TRADE_SUBCONTRACTORS = {
    "concrete":        ["Colorado Concrete Inc", "Front Range Concrete LLC", "Mountain States Concrete Co", "Rocky Mountain Ready Mix Contractors", "Peak Concrete Services LLC"],
    "steel":           ["Rocky Mountain Steel Fabricators Inc", "Colorado Structural Steel LLC", "Western Steel Erectors Inc", "Front Range Iron Works", "Summit Steel Services LLC"],
    "electrical":      ["Intermountain Electric Inc", "Colorado Power Systems LLC", "Encore Electric Inc", "Muth Electric Inc", "MDU Electric Construction"],
    "mechanical":      ["Apollo Mechanical Contractors LLC", "Comfort Systems USA Rocky Mountain", "Western Mechanical Inc", "Front Range Mechanical LLC", "Cannon Mechanical Services"],
    "plumbing":        ["Precision Plumbing and Heating", "Colorado Plumbing Contractors LLC", "High Country Plumbing Inc", "Rocky Mountain Plumbing Inc"],
    "drywall":         ["Front Range Drywall Inc", "Mountain West Drywall LLC", "Colorado Interiors Corp", "Western Drywall Systems Inc"],
    "roofing":         ["Colorado Roofing Company LLC", "Rocky Mountain Roofing Inc", "Peak Roofing Systems", "Front Range Roofing LLC"],
    "glazing":         ["Colorado Glass and Glazing LLC", "Summit Glazing Systems Inc", "Rocky Mountain Curtain Wall", "Western Architectural Products"],
    "fire_protection": ["Colorado Fire Protection Inc", "Rocky Mountain Fire Sprinkler LLC", "Western Fire Systems LLC"],
    "earthwork":       ["Front Range Excavating Inc", "Colorado Earthmovers LLC", "Rocky Mountain Grading Inc", "Western Site Development LLC"],
    "landscaping":     ["Western Landscape Services LLC", "Colorado Outdoor Environments Inc", "Front Range Landscaping"],
    "painting":        ["Colorado Commercial Painting LLC", "Summit Coatings Inc", "Front Range Finishes LLC"],
    "flooring":        ["Colorado Flooring Contractors LLC", "Western Floor Systems Inc", "Rocky Mountain Tile and Stone"],
}

CSI_DIVISIONS = {
    "earthwork":       ("Division 31 - Earthwork", 0.05),
    "concrete":        ("Division 03 - Concrete", 0.14),
    "steel":           ("Division 05 - Metals", 0.12),
    "electrical":      ("Division 26 - Electrical", 0.10),
    "mechanical":      ("Division 23 - HVAC", 0.12),
    "plumbing":        ("Division 22 - Plumbing", 0.06),
    "drywall":         ("Division 09 - Finishes", 0.07),
    "roofing":         ("Division 07 - Thermal and Moisture Protection", 0.04),
    "glazing":         ("Division 08 - Openings", 0.05),
    "fire_protection": ("Division 21 - Fire Suppression", 0.03),
    "landscaping":     ("Division 32 - Exterior Improvements", 0.02),
    "painting":        ("Division 09 - Finishes", 0.02),
    "flooring":        ("Division 09 - Finishes", 0.03),
}

# Trade mix per project type
PROJECT_TRADES = {
    "P001": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing"],
    "P002": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "roofing", "fire_protection"],
    "P003": ["earthwork", "concrete", "steel", "electrical", "mechanical", "roofing"],
    "P004": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "roofing"],
    "P005": ["earthwork", "concrete", "steel", "electrical", "mechanical", "drywall"],
    "P006": ["concrete", "electrical", "mechanical", "plumbing", "drywall", "flooring", "painting"],
    "P007": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing"],
    "P008": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing"],
    "P009": ["earthwork", "concrete", "steel", "electrical", "mechanical"],
    "P010": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing"],
    "P011": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing", "flooring"],
    "P012": ["earthwork", "concrete", "steel", "electrical", "mechanical", "roofing"],
    "P013": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing", "fire_protection"],
    "P014": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "roofing"],
    "P015": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "roofing"],
    "P016": ["earthwork", "concrete", "electrical", "mechanical", "plumbing"],
    "P017": ["earthwork", "concrete", "steel", "electrical", "mechanical", "roofing"],
    "P018": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "roofing"],
    "P019": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall"],
    "P020": ["earthwork", "concrete", "electrical", "mechanical"],
    "P021": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing", "flooring"],
    "P022": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing", "fire_protection"],
    "P023": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall"],
    "P024": ["earthwork", "concrete", "steel", "electrical", "mechanical"],
    "P025": ["earthwork", "concrete", "steel", "electrical", "mechanical", "plumbing", "drywall", "glazing", "fire_protection"],
}

SCOPE_DESCRIPTIONS = {
    "earthwork":       "Site preparation, mass excavation, grading, and utilities coordination",
    "concrete":        "Cast-in-place concrete including footings, foundations, slabs, and elevated decks",
    "steel":           "Structural steel fabrication, delivery, and erection including connections",
    "electrical":      "Complete electrical distribution, lighting, power, and low-voltage systems",
    "mechanical":      "HVAC systems, ductwork, air handling units, and controls integration",
    "plumbing":        "Domestic water, sanitary sewer, storm drainage, and specialty plumbing",
    "drywall":         "Metal framing, gypsum board, insulation, and interior partition systems",
    "roofing":         "Complete roofing system including membrane, insulation, flashings, and accessories",
    "glazing":         "Storefront, curtain wall, and glazed opening systems",
    "fire_protection": "Automatic fire sprinkler system including hydraulic calculations and inspection",
    "landscaping":     "Site landscaping, irrigation, hardscaping, and final site restoration",
    "painting":        "Interior and exterior painting, coatings, and wall coverings",
    "flooring":        "Resilient flooring, carpet, tile, and specialty flooring installations",
}

SC_STATUS_WEIGHTS = ["active", "active", "active", "completed", "completed", "completed", "completed", "terminated"]

random.seed(102)
subcontract_rows = []
subcontract_ids = []  # list of (subcontract_id, project_id) for amendments

for p in PROJECTS:
    trades = PROJECT_TRADES[p["project_id"]]
    contract_value = float(p["contract_value"])
    start = parse_date(p["start_date"])
    end = parse_date(p["end_date"])
    project_duration_days = (end - start).days

    # Total subcontract budget = 62-68% of contract value
    total_sub_budget = contract_value * random.uniform(0.62, 0.68)

    # Assign weights per trade and normalize
    trade_weights = [CSI_DIVISIONS[t][1] for t in trades]
    total_weight = sum(trade_weights)
    trade_values = [total_sub_budget * (w / total_weight) for w in trade_weights]

    proj_num = p["project_id"]  # e.g. "P001"

    for idx, trade in enumerate(trades):
        subcontract_id = str(uuid.uuid4())
        subcontract_ids.append((subcontract_id, p["project_id"]))

        # Pick a subcontractor from the pool
        sub_list = TRADE_SUBCONTRACTORS[trade]
        sub_company = random.choice(sub_list)

        # Assign a stable sub_id from the pool
        sub_id_num = (hash(sub_company) % 60) + 1
        sub_id = f"SUB-{sub_id_num:03d}"

        sc_number = f"SC-{proj_num}-{idx + 1:03d}"
        division_name = CSI_DIVISIONS[trade][0]

        original_value = round(trade_values[idx] * random.uniform(0.92, 1.08), 2)

        if p["status"] in ("completed", "closeout"):
            co_pct = random.uniform(0.02, 0.07)
        else:
            co_pct = random.uniform(0.00, 0.04)

        change_order_value = round(original_value * co_pct, 2)
        current_value = round(original_value + change_order_value, 2)

        # Execution date: 15-45 days after prime contract start
        exec_offset = random.randint(15, 45)
        exec_date = start + timedelta(days=exec_offset)

        # Sub start date: exec_date + 0-30 days
        sub_start_offset = random.randint(0, 30)
        sub_start = exec_date + timedelta(days=sub_start_offset)

        # Completion date: proportional to trade sequence, add some variance
        trade_completion_fraction = min(0.95, 0.5 + idx * 0.05 + random.uniform(-0.1, 0.1))
        completion_days = int(project_duration_days * trade_completion_fraction)
        sub_completion = start + timedelta(days=completion_days)

        # Insurance
        ins_cert_num = f"IC-{random.randint(100000, 999999)}"
        ins_verified_date = exec_date + timedelta(days=random.randint(0, 7))

        # Bond
        bond_required = original_value > 500000
        if bond_required:
            bond_amount = original_value
            perf_bond_num = f"PB-{random.randint(10000000, 99999999)}"
            pay_bond_num = f"PAY-{random.randint(10000000, 99999999)}"
        else:
            bond_amount = None
            perf_bond_num = None
            pay_bond_num = None

        # Status
        if p["status"] == "completed":
            sc_status = "completed"
        elif p["status"] == "closeout":
            sc_status = random.choice(["completed", "completed", "completed", "active"])
        else:
            sc_status = random.choice(["active", "active", "active", "active", "active", "completed", "suspended"])

        subcontract_rows.append({
            "subcontract_id": subcontract_id,
            "project_id": p["project_id"],
            "sub_id": sub_id,
            "subcontract_number": sc_number,
            "scope_description": SCOPE_DESCRIPTIONS[trade],
            "division": division_name,
            "original_value": original_value,
            "change_order_value": change_order_value,
            "current_value": current_value,
            "execution_date": exec_date.strftime("%Y-%m-%d"),
            "start_date": sub_start.strftime("%Y-%m-%d"),
            "completion_date": sub_completion.strftime("%Y-%m-%d"),
            "insurance_certificate_number": ins_cert_num,
            "insurance_verified_date": ins_verified_date.strftime("%Y-%m-%d"),
            "bond_required": bond_required,
            "bond_amount": float(bond_amount) if bond_amount is not None else None,
            "performance_bond_number": perf_bond_num,
            "payment_bond_number": pay_bond_num,
            "status": sc_status,
        })

sub_pdf = pd.DataFrame(subcontract_rows)
sub_df = spark.createDataFrame(sub_pdf)
sub_df.write.mode("overwrite").saveAsTable(f"{catalog}.contracts.subcontracts")
df = spark.table(f"{catalog}.contracts.subcontracts")
print(f"Created {catalog}.contracts.subcontracts with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: purchase_orders  (~800 rows, ~32 per project)
# ============================================================

PO_TEMPLATES = [
    # (cost_code, description, category, vendor_pool, amount_range_factor)
    ("03-1000", "Ready-mix concrete supply - foundations", "material", ["Denver Concrete Inc", "Colorado Ready Mix LLC", "Continental Cement Co", "Front Range Concrete Materials"], (0.008, 0.015)),
    ("03-1000", "Ready-mix concrete supply - elevated slabs", "material", ["Denver Concrete Inc", "Colorado Ready Mix LLC", "Lafarge Denver", "Front Range Concrete Materials"], (0.006, 0.012)),
    ("03-2000", "Concrete formwork and shoring materials", "material", ["ABC Supply Co", "Doka USA Ltd", "EFCO Corp"], (0.003, 0.008)),
    ("03-2100", "Reinforcing steel (rebar) supply", "material", ["Nucor Steel Colorado", "Harris Rebar", "Commercial Metals Co"], (0.010, 0.018)),
    ("05-1200", "Structural steel supply and fabrication", "material", ["Nucor Steel Colorado", "Commercial Metals Co", "Olympic Steel"], (0.015, 0.025)),
    ("05-5000", "Miscellaneous metals and anchor bolts", "material", ["Fastenal Company", "RS Means Metals LLC", "Mountain West Steel"], (0.002, 0.005)),
    ("06-1000", "Dimensional lumber and engineered wood products", "material", ["ABC Supply Co", "US LBM Holdings", "Builders FirstSource"], (0.002, 0.006)),
    ("07-2100", "Rigid board insulation", "material", ["ABC Supply Co", "Owens Corning Distributor", "Johns Manville"], (0.002, 0.004)),
    ("07-5100", "Roofing membrane and insulation materials", "material", ["ABC Supply Co", "Tremco Roofing Materials", "GAF Commercial"], (0.003, 0.007)),
    ("07-9200", "Joint sealants and waterproofing materials", "material", ["Sika Corporation", "Tremco Inc", "W.R. Meadows"], (0.001, 0.003)),
    ("08-1100", "Steel doors and frames - standard", "material", ["ASSA ABLOY Commercial", "Ceco Door Products", "Steelcraft"], (0.002, 0.004)),
    ("08-8000", "Glass and glazing materials", "material", ["PPG Industries", "Guardian Glass", "Oldcastle BuildingEnvelope"], (0.003, 0.008)),
    ("09-2116", "Gypsum board and metal framing materials", "material", ["ABC Supply Co", "USG Corporation", "National Gypsum Co"], (0.004, 0.009)),
    ("09-6500", "Resilient flooring materials", "material", ["Tarkett Commercial", "Armstrong Flooring Inc", "Forbo Flooring"], (0.002, 0.005)),
    ("09-9000", "Paints and coatings materials", "material", ["Sherwin-Williams", "PPG Architectural Coatings", "Benjamin Moore Commercial"], (0.001, 0.003)),
    ("22-0500", "Plumbing piping and fittings", "material", ["Ferguson Enterprises", "Hajoca Corporation", "Winsupply Inc"], (0.003, 0.007)),
    ("22-1119", "Plumbing fixtures and trim", "material", ["Ferguson Enterprises", "American Standard Commercial", "Kohler Commercial"], (0.002, 0.005)),
    ("23-0900", "HVAC controls and building automation", "material", ["Johnson Controls", "Honeywell Building Solutions", "Siemens Building Technologies"], (0.003, 0.008)),
    ("23-7300", "Ductwork and HVAC distribution materials", "material", ["Ductmate Industries", "Sheet Metal Supplies LLC", "Elgin National Industries"], (0.004, 0.009)),
    ("26-0526", "Electrical conduit, wire, and grounding", "material", ["Graybar Electric", "WESCO International", "Anixter Inc"], (0.005, 0.010)),
    ("26-2717", "Switchgear and electrical distribution equipment", "material", ["Graybar Electric", "Eaton Corporation", "Square D by Schneider Electric"], (0.004, 0.010)),
    ("31-2200", "Grading and compaction equipment rental", "rental", ["United Rentals Inc", "Sunbelt Rentals LLC", "BlueLine Rental"], (0.003, 0.006)),
    ("31-2313", "Aggregate base course and subbase materials", "material", ["Colorado Aggregates Inc", "Martin Marietta Materials", "Vulcan Materials Co"], (0.003, 0.007)),
    ("32-1313", "Concrete paving and flatwork materials", "material", ["Denver Concrete Inc", "Colorado Ready Mix LLC", "Front Range Concrete Materials"], (0.002, 0.005)),
    ("01-5400", "Crane rental - tower crane or mobile crane", "rental", ["United Rentals Inc", "Maxim Crane Works LP", "Barnhart Crane and Rigging"], (0.004, 0.010)),
    ("01-5400", "Aerial work platform and scissor lift rental", "rental", ["United Rentals Inc", "Sunbelt Rentals LLC", "BlueLine Rental"], (0.002, 0.005)),
    ("01-5400", "Temporary fencing and site security", "rental", ["United Rentals Inc", "Fence Factory Colorado", "Sunbelt Rentals LLC"], (0.001, 0.002)),
    ("01-4500", "Special inspections and materials testing services", "service", ["CTL Thompson Inc", "RMT Engineering Inc", "Terracon Consultants Inc"], (0.002, 0.004)),
    ("01-4200", "Survey and layout services", "service", ["GPS Surveying LLC", "Colorado Land Surveying Inc", "KPFF Consulting Engineers"], (0.001, 0.003)),
    ("01-3100", "Project management software and field technology", "service", ["Procore Technologies", "Viewpoint Construction Software", "Oracle Construction"], (0.001, 0.002)),
    ("33-4200", "Stormwater management and erosion control", "service", ["Colorado Environmental Services", "Terracon Consultants Inc", "SWCA Environmental"], (0.001, 0.003)),
    ("01-9100", "Final cleaning and project closeout services", "service", ["Colorado Commercial Cleaning Inc", "Front Range Janitorial Services", "Coverall Holdings Inc"], (0.001, 0.002)),
    ("11-1300", "Loading dock equipment and specialty hardware", "material", ["Assa Abloy Entrance Systems", "Serco Inc", "Rytec Corporation"], (0.001, 0.003)),
    ("10-1400", "Signage and wayfinding systems", "material", ["Federal Heath Sign Co", "AGRetail Inc", "ColoradoSign Works LLC"], (0.001, 0.002)),
    ("26-5600", "Lighting fixtures and controls", "material", ["Acuity Brands Lighting", "Lithonia Lighting", "Cree Lighting"], (0.002, 0.005)),
]

PO_STATUSES = ["open", "partial", "partial", "received", "invoiced", "invoiced", "paid", "paid", "paid", "cancelled"]

random.seed(103)
po_rows = []
target_po_count = 800

pos_per_project = {p["project_id"]: 0 for p in PROJECTS}

for p in PROJECTS:
    contract_value = float(p["contract_value"])
    start = parse_date(p["start_date"])
    end = parse_date(p["end_date"])
    project_duration_days = max(1, (end - start).days)

    # Scale number of POs by project size
    if contract_value >= 100000000:
        num_pos = random.randint(38, 48)
    elif contract_value >= 50000000:
        num_pos = random.randint(28, 38)
    elif contract_value >= 25000000:
        num_pos = random.randint(20, 28)
    else:
        num_pos = random.randint(14, 22)

    pos_per_project[p["project_id"]] = num_pos

    # Sample PO templates (allow repeats with different vendors)
    templates_for_project = random.choices(PO_TEMPLATES, k=num_pos)

    for seq, tmpl in enumerate(templates_for_project):
        cost_code, desc_base, category, vendors, amount_range_factor = tmpl

        po_id = str(uuid.uuid4())
        vendor_name = random.choice(vendors)

        original_amount = round(contract_value * random.uniform(*amount_range_factor), 2)
        original_amount = max(original_amount, 5000.0)

        # Change order (occasional)
        if random.random() < 0.15:
            co_pct = random.uniform(0.05, 0.15)
            change_order_amount = round(original_amount * co_pct, 2)
        else:
            change_order_amount = 0.0

        current_amount = round(original_amount + change_order_amount, 2)

        # Order date within first 60% of project
        order_offset = int(project_duration_days * random.uniform(0.01, 0.50))
        order_date = start + timedelta(days=order_offset)

        lead_days = random.randint(7, 60) if category == "material" else random.randint(3, 21)
        expected_delivery_date = order_date + timedelta(days=lead_days)

        # Status and amounts
        status = random.choice(PO_STATUSES)
        if p["status"] == "completed":
            status = random.choice(["received", "invoiced", "invoiced", "paid", "paid", "paid"])
        elif p["status"] == "closeout":
            status = random.choice(["invoiced", "invoiced", "paid", "paid"])
        elif p["status"] == "active":
            status = random.choice(["open", "open", "partial", "partial", "received", "invoiced", "paid"])

        if status == "open":
            received_amount = 0.0
            invoiced_amount = 0.0
            paid_amount = 0.0
            actual_delivery_date = None
        elif status == "partial":
            received_pct = random.uniform(0.25, 0.75)
            received_amount = round(current_amount * received_pct, 2)
            invoiced_amount = round(received_amount * random.uniform(0.70, 1.00), 2)
            paid_amount = round(invoiced_amount * random.uniform(0.50, 0.90), 2)
            delivery_offset = random.randint(0, lead_days + 14)
            actual_delivery_date = (order_date + timedelta(days=delivery_offset)).strftime("%Y-%m-%d")
        elif status == "received":
            received_amount = current_amount
            invoiced_amount = round(current_amount * random.uniform(0.80, 1.00), 2)
            paid_amount = round(invoiced_amount * random.uniform(0.70, 0.95), 2)
            delivery_offset = random.randint(0, lead_days + 14)
            actual_delivery_date = (order_date + timedelta(days=delivery_offset)).strftime("%Y-%m-%d")
        elif status == "invoiced":
            received_amount = current_amount
            invoiced_amount = current_amount
            paid_amount = round(current_amount * random.uniform(0.75, 0.95), 2)
            delivery_offset = random.randint(0, lead_days + 7)
            actual_delivery_date = (order_date + timedelta(days=delivery_offset)).strftime("%Y-%m-%d")
        elif status == "paid":
            received_amount = current_amount
            invoiced_amount = current_amount
            paid_amount = current_amount
            delivery_offset = random.randint(0, lead_days + 7)
            actual_delivery_date = (order_date + timedelta(days=delivery_offset)).strftime("%Y-%m-%d")
        elif status == "cancelled":
            received_amount = 0.0
            invoiced_amount = 0.0
            paid_amount = 0.0
            actual_delivery_date = None
        else:
            received_amount = 0.0
            invoiced_amount = 0.0
            paid_amount = 0.0
            actual_delivery_date = None

        po_rows.append({
            "po_id": po_id,
            "project_id": p["project_id"],
            "vendor_name": vendor_name,
            "cost_code": cost_code,
            "description": desc_base,
            "category": category,
            "original_amount": original_amount,
            "change_order_amount": change_order_amount,
            "current_amount": current_amount,
            "received_amount": received_amount,
            "invoiced_amount": invoiced_amount,
            "paid_amount": paid_amount,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "expected_delivery_date": expected_delivery_date.strftime("%Y-%m-%d"),
            "actual_delivery_date": actual_delivery_date,
            "status": status,
        })

po_pdf = pd.DataFrame(po_rows)
po_df = spark.createDataFrame(po_pdf)
po_df.write.mode("overwrite").saveAsTable(f"{catalog}.contracts.purchase_orders")
df = spark.table(f"{catalog}.contracts.purchase_orders")
print(f"Created {catalog}.contracts.purchase_orders with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: contract_amendments  (~600 rows)
# ============================================================

PM_NAMES = [
    "Sarah Mitchell", "James Thornton", "Karen Okafor", "David Reyes",
    "Michael Chen", "Patricia Walshe", "Robert Vandenberg", "Lisa Nakamura",
    "Thomas Beaumont", "Angela Ferreira",
]

AMENDMENT_TYPES = ["change_order", "change_order", "change_order", "supplemental_agreement", "field_order"]

REASON_CODES = [
    "owner_directed", "owner_directed", "differing_conditions",
    "design_error", "weather", "scope_gap", "scope_gap",
]

CO_DESCRIPTIONS = [
    "Owner-directed addition of Level 4 mezzanine storage area",
    "Additional electrical capacity for owner-furnished equipment",
    "Unforeseen subsurface rock encountered during excavation",
    "Design coordination RFI resolution - structural beam size increase",
    "Weather delay - extended winter shutdown affecting schedule",
    "Scope gap in mechanical specification - add unit heaters",
    "Owner-directed upgrade to high-efficiency glazing system",
    "Add fire suppression to previously unsprinklered storage rooms",
    "Credit for deletion of specified flooring in mechanical rooms",
    "Additional concrete testing per structural engineer directive",
    "Owner-directed acceleration to maintain milestone date",
    "Hazardous material abatement - unforeseen lead paint in existing walls",
    "Additional grounding and bonding per electrical inspector directive",
    "Differing site conditions - higher groundwater than geotech report indicated",
    "Design error correction - insufficient rebar in transfer beam",
    "Owner-directed finish upgrade - LVT flooring in lieu of VCT",
    "Add temporary HVAC for occupied adjacent space during construction",
    "Extended general conditions - owner-directed scope additions",
    "Add access control and security system scope",
    "Credit - deletion of specified landscape berms by owner",
    "Additional waterproofing at below-grade walls per architect",
    "Field order - re-route fire protection main to avoid structural conflict",
    "Structural reinforcement at roof opening per RFI response",
    "Add generator and automatic transfer switch scope",
    "Owner-directed change to curtain wall system for improved performance",
    "Add EV charging infrastructure in parking garage",
    "Unforeseen utility conflict requiring horizontal directional drilling",
    "Additional cleanroom finishes - upgraded wall panel system",
    "Credit for value engineering - precast in lieu of cast-in-place stairs",
    "Additional seismic anchorage per engineer of record directive",
]

random.seed(104)
amendment_rows = []
amendment_counter_by_project = {p["project_id"]: 0 for p in PROJECTS}

for p in PROJECTS:
    start = parse_date(p["start_date"])
    end = parse_date(p["end_date"])
    project_duration_days = max(1, (end - start).days)
    contract_value = float(p["contract_value"])

    # Generate amendments to prime contract
    prime_contract_id = prime_contract_ids[p["project_id"]]
    num_prime_amendments = random.randint(10, 18)

    for seq in range(1, num_prime_amendments + 1):
        amendment_id = str(uuid.uuid4())
        amendment_number = seq
        amendment_type = random.choice(AMENDMENT_TYPES)
        description = random.choice(CO_DESCRIPTIONS)
        reason_code = random.choice(REASON_CODES)

        # Amount: most positive, some negative (credits)
        if random.random() < 0.15:
            amount = round(-contract_value * random.uniform(0.001, 0.005), 2)
        else:
            amount = round(contract_value * random.uniform(0.001, 0.015), 2)

        # Executed date within project window
        exec_offset = int(project_duration_days * random.uniform(0.05, 0.90))
        executed_date = start + timedelta(days=exec_offset)

        if amount > 100000 or reason_code in ("differing_conditions", "weather"):
            schedule_impact = random.choice([0, 0, 7, 14, 21, 30, 45, 60])
        else:
            schedule_impact = 0

        approved_by = random.choice(PM_NAMES)

        amendment_rows.append({
            "amendment_id": amendment_id,
            "parent_contract_id": prime_contract_id,
            "parent_contract_type": "prime",
            "project_id": p["project_id"],
            "amendment_number": amendment_number,
            "amendment_type": amendment_type,
            "description": description,
            "amount": amount,
            "executed_date": executed_date.strftime("%Y-%m-%d"),
            "reason_code": reason_code,
            "approved_by": approved_by,
            "schedule_impact_days": schedule_impact,
        })

    # Generate amendments to subcontracts
    project_subs = [(sid, pid) for sid, pid in subcontract_ids if pid == p["project_id"]]
    num_sub_amendments = random.randint(6, 12)

    for seq in range(num_sub_amendments):
        if not project_subs:
            break
        sub_id_chosen, _ = random.choice(project_subs)
        amendment_id = str(uuid.uuid4())
        amendment_type = random.choice(AMENDMENT_TYPES)
        description = random.choice(CO_DESCRIPTIONS)
        reason_code = random.choice(REASON_CODES)

        # Subcontract amendment amounts smaller
        if random.random() < 0.12:
            amount = round(-contract_value * random.uniform(0.0005, 0.002), 2)
        else:
            amount = round(contract_value * random.uniform(0.0003, 0.008), 2)

        exec_offset = int(project_duration_days * random.uniform(0.05, 0.90))
        executed_date = start + timedelta(days=exec_offset)

        schedule_impact = random.choice([0, 0, 0, 7, 14]) if amount > 50000 else 0
        approved_by = random.choice(PM_NAMES)

        amendment_rows.append({
            "amendment_id": amendment_id,
            "parent_contract_id": sub_id_chosen,
            "parent_contract_type": "subcontract",
            "project_id": p["project_id"],
            "amendment_number": seq + 1,
            "amendment_type": amendment_type,
            "description": description,
            "amount": amount,
            "executed_date": executed_date.strftime("%Y-%m-%d"),
            "reason_code": reason_code,
            "approved_by": approved_by,
            "schedule_impact_days": schedule_impact,
        })

    # A few PO amendments (field orders)
    num_po_amendments = random.randint(3, 7)
    for seq in range(num_po_amendments):
        amendment_id = str(uuid.uuid4())
        fake_po_id = str(uuid.uuid4())  # reference a PO by stub UUID
        description = random.choice(CO_DESCRIPTIONS)
        amount = round(contract_value * random.uniform(0.0001, 0.002), 2)
        if random.random() < 0.08:
            amount = -amount

        exec_offset = int(project_duration_days * random.uniform(0.05, 0.85))
        executed_date = start + timedelta(days=exec_offset)
        approved_by = random.choice(PM_NAMES)

        amendment_rows.append({
            "amendment_id": amendment_id,
            "parent_contract_id": fake_po_id,
            "parent_contract_type": "PO",
            "project_id": p["project_id"],
            "amendment_number": seq + 1,
            "amendment_type": "field_order",
            "description": description,
            "amount": amount,
            "executed_date": executed_date.strftime("%Y-%m-%d"),
            "reason_code": random.choice(REASON_CODES),
            "approved_by": approved_by,
            "schedule_impact_days": 0,
        })

amend_pdf = pd.DataFrame(amendment_rows)
amend_df = spark.createDataFrame(amend_pdf)
amend_df.write.mode("overwrite").saveAsTable(f"{catalog}.contracts.contract_amendments")
df = spark.table(f"{catalog}.contracts.contract_amendments")
print(f"Created {catalog}.contracts.contract_amendments with {df.count()} rows")
