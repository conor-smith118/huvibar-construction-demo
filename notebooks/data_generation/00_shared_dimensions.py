# Databricks notebook source

# COMMAND ----------
%pip install faker --quiet

# COMMAND ----------
import random
import uuid
from datetime import date, datetime, timedelta
import pandas as pd
from faker import Faker

random.seed(42)
fake = Faker()
Faker.seed(42)

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

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.project_tracking")
print(f"Schema {catalog}.project_tracking ready")

# COMMAND ----------

# ── TABLE: projects (25 rows) ─────────────────────────────────────────────────

def _assign_project_type(name):
    n = name.lower()
    if any(w in n for w in ["medical", "health", "hospital", "clinic", "veterans affairs", "senior living"]):
        return "healthcare"
    if any(w in n for w in ["school", "elementary", "high school", "university", "campus"]):
        return "education"
    if any(w in n for w in ["warehouse", "industrial", "distribution", "logistics", "steel mill",
                             "semiconductor", "fab", "solar", "data center", "remediation",
                             "wastewater", "hangar", "o&m"]):
        return "industrial"
    return "commercial"

CLIENT_MAP = {
    "P001": "CBRE Group",
    "P002": "UCHealth",
    "P003": "Prologis",
    "P004": "Jefferson County Public Schools",
    "P005": "Xcel Energy",
    "P006": "Sage Hospitality Group",
    "P007": "City of Fort Collins",
    "P008": "Boulder Innovation Campus LLC",
    "P009": "EVRAZ Rocky Mountain Steel",
    "P010": "City of Greeley",
    "P011": "Shea Properties",
    "P012": "Amazon Logistics",
    "P013": "Colorado Convention Center Authority",
    "P014": "City of Thornton",
    "P015": "Westminster Public Schools",
    "P016": "U.S. Department of Energy",
    "P017": "ProLogis Industrial REIT",
    "P018": "Brookdale Senior Living",
    "P019": "Town of Castle Rock",
    "P020": "NextEra Energy Resources",
    "P021": "Continuum Partners",
    "P022": "Denver International Airport",
    "P023": "U.S. Department of Veterans Affairs",
    "P024": "Centennial Airport Authority",
    "P025": "Entegris Colorado",
}

CONTRACT_TYPE_MAP = {
    "P001": "GMP", "P002": "GMP", "P003": "lump_sum", "P004": "lump_sum",
    "P005": "GMP", "P006": "cost_plus", "P007": "GMP", "P008": "GMP",
    "P009": "lump_sum", "P010": "GMP", "P011": "GMP", "P012": "lump_sum",
    "P013": "GMP", "P014": "lump_sum", "P015": "lump_sum", "P016": "GMP",
    "P017": "lump_sum", "P018": "GMP", "P019": "lump_sum", "P020": "lump_sum",
    "P021": "GMP", "P022": "GMP", "P023": "GMP", "P024": "lump_sum", "P025": "GMP",
}

PM_NAMES = [
    "Sarah Chen", "Marcus Williams", "Jennifer Rodriguez", "David Park", "Ashley Thompson",
    "Robert Martinez", "Kimberly Johnson", "James Wilson", "Patricia Davis", "Michael Brown",
    "Lisa Nguyen", "Kevin O'Brien", "Stephanie Clark", "Daniel Lee", "Amanda Foster",
]

SUPERINTENDENT_NAMES = [
    "Tom Kowalski", "Rick Sanchez", "Bill Murphy", "Dave Nelson", "Chris Okonkwo",
    "Frank Delgado", "Steve Yamamoto", "Al Petersen", "Joe Morales", "Ed Blackwell",
    "Gary Hutchins", "Mike Trevino", "Bob Lindstrom", "Ray Castellano", "Dan Whitfield",
]

ARCHITECT_FIRMS = [
    "HOK", "Gensler", "AECOM", "Stantec", "Jacobs Engineering",
    "Anderson Mason Dale Architects", "Davis Partnership Architects",
    "OZ Architecture", "RNL Design", "Fentress Architects",
    "Murata Outland Architects", "Sink Combs Dethlefs",
    "Tryba Architects", "Semple Brown Design", "Cuningham Group",
]

TODAY = date(2026, 8, 11)

projects_rows = []
for i, p in enumerate(PROJECTS):
    pid = p["project_id"]
    ptype = _assign_project_type(p["project_name"])
    start = datetime.strptime(p["start_date"], "%Y-%m-%d").date()
    end = datetime.strptime(p["end_date"], "%Y-%m-%d").date()
    status = p["status"]
    duration_days = max((end - start).days, 1)

    if status == "completed":
        actual_end = end + timedelta(days=random.randint(-14, 45))
        pct = 100.0
    elif status == "closeout":
        actual_end = None
        pct = round(random.uniform(95.0, 99.5), 1)
    else:
        actual_end = None
        elapsed = max((TODAY - start).days, 0)
        raw = elapsed / duration_days * 100 * random.uniform(0.88, 1.05)
        pct = round(min(max(raw, 5.0), 94.9), 1)

    project_number = f"HUV-{pid[1:]}-{start.year}"

    projects_rows.append({
        "project_id": pid,
        "project_name": p["project_name"],
        "project_number": project_number,
        "client_name": CLIENT_MAP[pid],
        "location_city": p["city"],
        "location_state": p["state"],
        "project_type": ptype,
        "contract_type": CONTRACT_TYPE_MAP[pid],
        "contract_value": float(p["contract_value"]),
        "start_date": str(start),
        "projected_end_date": str(end),
        "actual_end_date": str(actual_end) if actual_end else None,
        "status": status,
        "project_manager": PM_NAMES[i % len(PM_NAMES)],
        "superintendent": SUPERINTENDENT_NAMES[i % len(SUPERINTENDENT_NAMES)],
        "architect": ARCHITECT_FIRMS[i % len(ARCHITECT_FIRMS)],
        "percent_complete": pct,
    })

pdf_projects = pd.DataFrame(projects_rows)
spark.createDataFrame(pdf_projects).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.project_tracking.projects")
df = spark.table(f"{catalog}.project_tracking.projects")
print(f"Created {catalog}.project_tracking.projects with {df.count()} rows")

# COMMAND ----------

# ── TABLE: employees (200 rows) ───────────────────────────────────────────────
# Trade breakdown:
#   30 carpenters, 20 ironworkers, 20 electricians, 15 plumbers,
#   40 laborers, 20 foremen, 15 superintendents, 15 PMs, 10 estimators,
#   15 other office/management staff  =>  total = 200

TRADE_SLOTS = [
    # (trade,            dept,         count,  is_hourly, rate_min, rate_max, sal_min,  sal_max)
    ("carpenter",        "field",       30,     True,  35.0,  55.0,   None,    None),
    ("ironworker",       "field",       20,     True,  40.0,  60.0,   None,    None),
    ("electrician",      "field",       20,     True,  38.0,  58.0,   None,    None),
    ("plumber",          "field",       15,     True,  36.0,  54.0,   None,    None),
    ("laborer",          "field",       40,     True,  22.0,  32.0,   None,    None),
    ("foreman",          "field",       20,     True,  45.0,  65.0,   None,    None),
    ("superintendent",   "management",  15,     False, None,  None,   95000,   140000),
    ("project_manager",  "management",  15,     False, None,  None,   90000,   135000),
    ("estimator",        "office",      10,     False, None,  None,   75000,   110000),
]

OTHER_OFFICE = [
    ("accountant",         "office",     65000,  90000),
    ("scheduler",          "office",     70000, 100000),
    ("safety_manager",     "office",     72000, 105000),
    ("hr_coordinator",     "office",     60000,  80000),
    ("contract_admin",     "office",     65000,  90000),
    ("project_engineer",   "office",     70000,  95000),
    ("bim_coordinator",    "office",     72000,  98000),
    ("procurement_spec",   "office",     68000,  95000),
    ("cost_engineer",      "office",     72000, 100000),
    ("document_control",   "office",     55000,  72000),
    ("quality_manager",    "office",     75000, 105000),
    ("marketing_manager",  "office",     68000,  92000),
    ("it_specialist",      "office",     65000,  90000),
    ("assistant_pm",       "management", 65000,  88000),
    ("vp_operations",      "management",140000, 185000),
]

hire_floor = date(2012, 1, 1)
employees = []
emp_counter = 1

for trade, dept, count, is_hourly, rate_min, rate_max, sal_min, sal_max in TRADE_SLOTS:
    for _ in range(count):
        eid = f"EMP-{emp_counter:03d}"
        emp_counter += 1
        fn = fake.first_name()
        ln = fake.last_name()
        hire_date = hire_floor + timedelta(days=random.randint(0, 4200))
        if is_hourly:
            hourly_rate = round(random.uniform(rate_min, rate_max), 2)
            salary = None
            emp_type = "hourly"
        else:
            hourly_rate = None
            salary = float(round(random.randint(sal_min, sal_max) / 1000) * 1000)
            emp_type = "salary"
        employees.append({
            "employee_id": eid,
            "first_name": fn,
            "last_name": ln,
            "role": trade,
            "department": dept,
            "trade": trade if dept == "field" else None,
            "hire_date": str(hire_date),
            "hourly_rate": hourly_rate,
            "salary": salary,
            "employment_type": emp_type,
        })

# Fill remaining 15 slots with other office/management roles
for role, dept, sal_min, sal_max in OTHER_OFFICE:
    eid = f"EMP-{emp_counter:03d}"
    emp_counter += 1
    fn = fake.first_name()
    ln = fake.last_name()
    hire_date = hire_floor + timedelta(days=random.randint(0, 4200))
    salary = float(round(random.randint(sal_min, sal_max) / 1000) * 1000)
    employees.append({
        "employee_id": eid,
        "first_name": fn,
        "last_name": ln,
        "role": role,
        "department": dept,
        "trade": None,
        "hire_date": str(hire_date),
        "hourly_rate": None,
        "salary": salary,
        "employment_type": "salary",
    })

assert len(employees) == 200, f"Expected 200 employees, got {len(employees)}"

pdf_employees = pd.DataFrame(employees)
spark.createDataFrame(pdf_employees).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.project_tracking.employees")
df = spark.table(f"{catalog}.project_tracking.employees")
print(f"Created {catalog}.project_tracking.employees with {df.count()} rows")

# COMMAND ----------

# ── TABLE: subcontractors (60 rows) ───────────────────────────────────────────

SUB_COMPANY_TRADE = [
    ("Front Range Electrical",             "electrical"),
    ("Mile High Mechanical",               "mechanical"),
    ("Colorado Steel Erectors",            "steel_erection"),
    ("Rocky Mountain Concrete",            "concrete"),
    ("Summit Drywall Systems",             "drywall"),
    ("Peak Performance Roofing",           "roofing"),
    ("Alpine Plumbing & Heating",          "plumbing"),
    ("Denver Glass & Glazing",             "glazing"),
    ("Mountain States Fire Protection",    "fire_protection"),
    ("Foothills Landscaping",              "landscaping"),
    ("Colorado Elevator Services",         "elevators"),
    ("High Plains HVAC",                   "HVAC"),
    ("Centennial Painting Co",             "painting"),
    ("Flatiron Flooring",                  "flooring"),
    ("Boulder Masonry Works",              "masonry"),
    ("Pikes Peak Electrical",              "electrical"),
    ("Continental Mechanical",             "mechanical"),
    ("Western States Steel",               "steel_erection"),
    ("Concrete Innovations Colorado",      "concrete"),
    ("Front Range Drywall",                "drywall"),
    ("Colorado Roofing Specialists",       "roofing"),
    ("Metro Plumbing Solutions",           "plumbing"),
    ("Rocky Mountain Glazing",             "glazing"),
    ("Colorado Fire Systems",              "fire_protection"),
    ("Green Valley Landscaping",           "landscaping"),
    ("Mountain Elevator Group",            "elevators"),
    ("Denver Metro HVAC",                  "HVAC"),
    ("Precision Painting Inc",             "painting"),
    ("Colorado Commercial Flooring",       "flooring"),
    ("Pueblo Masonry & Stone",             "masonry"),
    ("Tri-State Electric Co",              "electrical"),
    ("Highline Mechanical Contractors",    "mechanical"),
    ("Ironworks of Colorado",              "steel_erection"),
    ("Aggregate Industries Concrete",      "concrete"),
    ("Interiors West Drywall",             "drywall"),
    ("American Roof Systems",              "roofing"),
    ("Summit Plumbing Group",              "plumbing"),
    ("Colorado Curtain Wall Systems",      "glazing"),
    ("Patriot Fire Protection",            "fire_protection"),
    ("Rocky Mountain Horticulture",        "landscaping"),
    ("Intermountain Elevator",             "elevators"),
    ("Superior HVAC Services",             "HVAC"),
    ("Alliance Painting Group",            "painting"),
    ("National Floor Covering",            "flooring"),
    ("Colorado Heritage Masonry",          "masonry"),
    ("Apex Electrical Contractors",        "electrical"),
    ("Cascade Mechanical Inc",             "mechanical"),
    ("Colorado Structural Steel",          "steel_erection"),
    ("Denver Concrete Specialists",        "concrete"),
    ("Altitude Drywall Inc",               "drywall"),
    ("Consolidated Roofing Denver",        "roofing"),
    ("Foothills Plumbing Inc",             "plumbing"),
    ("Continental Glass Systems",          "glazing"),
    ("Colorado Suppression Systems",       "fire_protection"),
    ("Prairie Landscape Group",            "landscaping"),
    ("Rocky Mountain Elevator Inc",        "elevators"),
    ("Front Range HVAC Solutions",         "HVAC"),
    ("Mountain West Coatings",             "painting"),
    ("Centennial Commercial Floors",       "flooring"),
    ("Colorado Stone & Brick",             "masonry"),
]

CO_CITIES = [
    "Denver", "Aurora", "Lakewood", "Thornton", "Arvada", "Westminster",
    "Pueblo", "Fort Collins", "Boulder", "Greeley", "Longmont", "Loveland",
    "Broomfield", "Castle Rock", "Commerce City", "Parker", "Brighton", "Littleton", "Englewood",
]

subs = []
for i, (company, trade) in enumerate(SUB_COMPANY_TRADE):
    sid = f"SUB-{i + 1:03d}"
    city = CO_CITIES[i % len(CO_CITIES)]
    lic_num = f"CO-{random.randint(100000, 999999)}"
    ins_exp = date(2025, 6, 1) + timedelta(days=random.randint(-180, 730))
    bond_cap = random.choice([500000, 1000000, 2500000, 5000000, 10000000, 25000000])
    tier = 1 if bond_cap >= 10000000 else (2 if bond_cap >= 2500000 else 3)
    preferred = random.random() < 0.45
    status = "active" if ins_exp >= date(2026, 1, 1) else "inactive"
    subs.append({
        "sub_id": sid,
        "company_name": company,
        "trade": trade,
        "contact_name": fake.name(),
        "phone": fake.phone_number(),
        "city": city,
        "state": "CO",
        "license_number": lic_num,
        "insurance_expiry": str(ins_exp),
        "bond_capacity": float(bond_cap),
        "tier": tier,
        "preferred": preferred,
        "status": status,
    })

assert len(subs) == 60, f"Expected 60 subs, got {len(subs)}"

pdf_subs = pd.DataFrame(subs)
spark.createDataFrame(pdf_subs).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.project_tracking.subcontractors")
df = spark.table(f"{catalog}.project_tracking.subcontractors")
print(f"Created {catalog}.project_tracking.subcontractors with {df.count()} rows")

# COMMAND ----------

# ── TABLE: cost_codes (80 rows, CSI divisions 01-16) ─────────────────────────

CSI_DIVISIONS = {
    1:  "General Requirements",
    2:  "Existing Conditions",
    3:  "Concrete",
    4:  "Masonry",
    5:  "Metals",
    6:  "Wood, Plastics, and Composites",
    7:  "Thermal and Moisture Protection",
    8:  "Openings",
    9:  "Finishes",
    10: "Specialties",
    11: "Equipment",
    12: "Furnishings",
    13: "Special Construction",
    14: "Conveying Equipment",
    15: "Mechanical",
    16: "Electrical",
}

# (division_number, code, description, cost_type)  — exactly 80 entries
COST_CODE_DEFS = [
    # Division 01 - General Requirements (7)
    (1,  "01-010", "Project Management and Coordination",       "general"),
    (1,  "01-020", "Allowances",                                "general"),
    (1,  "01-030", "Alternates",                                "general"),
    (1,  "01-040", "Construction Schedule",                     "general"),
    (1,  "01-050", "Submittals",                                "general"),
    (1,  "01-060", "Quality Requirements",                      "general"),
    (1,  "01-070", "Temporary Facilities and Controls",         "general"),
    # Division 02 - Existing Conditions (6)
    (2,  "02-010", "Subsurface Investigation",                  "labor"),
    (2,  "02-020", "Demolition - Selective",                    "labor"),
    (2,  "02-030", "Site Clearing",                             "equipment"),
    (2,  "02-040", "Earthwork",                                 "equipment"),
    (2,  "02-050", "Excavation Support",                        "equipment"),
    (2,  "02-060", "Backfill and Compaction",                   "equipment"),
    # Division 03 - Concrete (5)
    (3,  "03-100", "Concrete Forming",                          "labor"),
    (3,  "03-200", "Concrete Reinforcing",                      "material"),
    (3,  "03-300", "Cast-in-Place Concrete",                    "material"),
    (3,  "03-400", "Precast Concrete",                          "sub"),
    (3,  "03-500", "Concrete Curing and Finishing",             "material"),
    # Division 04 - Masonry (3)
    (4,  "04-010", "Unit Masonry",                              "sub"),
    (4,  "04-020", "Masonry Anchorage and Reinforcing",         "material"),
    (4,  "04-030", "Stone Assemblies",                          "sub"),
    # Division 05 - Metals (5)
    (5,  "05-100", "Structural Metal Framing",                  "sub"),
    (5,  "05-200", "Metal Joists",                              "material"),
    (5,  "05-300", "Metal Decking",                             "material"),
    (5,  "05-400", "Cold-Formed Metal Framing",                 "labor"),
    (5,  "05-500", "Metal Fabrications",                        "material"),
    # Division 06 - Wood, Plastics, and Composites (3)
    (6,  "06-100", "Rough Carpentry",                           "labor"),
    (6,  "06-200", "Finish Carpentry",                          "labor"),
    (6,  "06-400", "Architectural Woodwork",                    "sub"),
    # Division 07 - Thermal and Moisture Protection (6)
    (7,  "07-100", "Dampproofing and Waterproofing",            "sub"),
    (7,  "07-200", "Thermal Insulation",                        "material"),
    (7,  "07-300", "Steep Slope Roofing",                       "sub"),
    (7,  "07-400", "Roofing and Siding Panels",                 "sub"),
    (7,  "07-500", "Membrane Roofing",                          "sub"),
    (7,  "07-700", "Roof and Wall Specialties",                 "material"),
    # Division 08 - Openings (5)
    (8,  "08-100", "Doors and Frames",                          "material"),
    (8,  "08-200", "Wood Doors",                                "material"),
    (8,  "08-400", "Entrances and Storefronts",                 "sub"),
    (8,  "08-500", "Windows",                                   "material"),
    (8,  "08-800", "Glazing",                                   "sub"),
    # Division 09 - Finishes (7)
    (9,  "09-100", "Metal Support Assemblies",                  "labor"),
    (9,  "09-200", "Plaster and Gypsum Board",                  "sub"),
    (9,  "09-300", "Tiling",                                    "sub"),
    (9,  "09-500", "Ceilings",                                  "sub"),
    (9,  "09-600", "Flooring",                                  "sub"),
    (9,  "09-700", "Wall Finishes",                             "sub"),
    (9,  "09-900", "Paints and Coatings",                       "sub"),
    # Division 10 - Specialties (3)
    (10, "10-100", "Visual Display Units",                      "material"),
    (10, "10-400", "Signage",                                   "material"),
    (10, "10-500", "Lockers",                                   "material"),
    # Division 11 - Equipment (2)
    (11, "11-100", "Vehicle and Pedestrian Equipment",          "equipment"),
    (11, "11-400", "Foodservice Equipment",                     "sub"),
    # Division 12 - Furnishings (2)
    (12, "12-200", "Window Treatments",                         "material"),
    (12, "12-500", "Furniture and Accessories",                 "material"),
    # Division 13 - Special Construction (4)
    (13, "13-010", "Special Purpose Rooms",                     "sub"),
    (13, "13-020", "Clean Rooms",                               "sub"),
    (13, "13-040", "Pre-Engineered Structures",                 "sub"),
    (13, "13-050", "Seismic Control",                           "sub"),
    # Division 14 - Conveying Equipment (4)
    (14, "14-100", "Dumbwaiters",                               "sub"),
    (14, "14-200", "Elevators",                                 "sub"),
    (14, "14-300", "Escalators and Moving Walks",               "sub"),
    (14, "14-400", "Lifts",                                     "sub"),
    # Division 15 - Mechanical (6)
    (15, "15-100", "HVAC Systems",                              "sub"),
    (15, "15-200", "Plumbing Systems",                          "sub"),
    (15, "15-300", "Fire Protection",                           "sub"),
    (15, "15-400", "Process Piping",                            "sub"),
    (15, "15-500", "HVAC Controls and Instrumentation",         "sub"),
    (15, "15-600", "Commissioning",                             "labor"),
    # Division 16 - Electrical (12)
    (16, "16-100", "Wiring Methods and Materials",              "sub"),
    (16, "16-200", "Electrical Service and Distribution",       "sub"),
    (16, "16-210", "Standby Power Systems",                     "sub"),
    (16, "16-300", "Transmission and Distribution",             "sub"),
    (16, "16-400", "Low-Voltage Distribution",                  "sub"),
    (16, "16-500", "Lighting",                                  "sub"),
    (16, "16-510", "Emergency Lighting",                        "sub"),
    (16, "16-600", "Special Systems",                           "sub"),
    (16, "16-700", "Communications",                            "sub"),
    (16, "16-750", "Structured Cabling",                        "sub"),
    (16, "16-800", "Sound and Video",                           "sub"),
    (16, "16-900", "Electrical Controls and Instrumentation",   "sub"),
]

assert len(COST_CODE_DEFS) == 80, f"Expected 80 cost codes, got {len(COST_CODE_DEFS)}"

cost_codes = []
for i, (div_num, code, description, cost_type) in enumerate(COST_CODE_DEFS):
    cost_codes.append({
        "code_id": f"CC-{i + 1:03d}",
        "division_number": div_num,
        "division_name": CSI_DIVISIONS[div_num],
        "code": code,
        "description": description,
        "cost_type": cost_type,
    })

pdf_cc = pd.DataFrame(cost_codes)
spark.createDataFrame(pdf_cc).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.project_tracking.cost_codes")
df = spark.table(f"{catalog}.project_tracking.cost_codes")
print(f"Created {catalog}.project_tracking.cost_codes with {df.count()} rows")

# COMMAND ----------

print("All shared dimensions created successfully!")
