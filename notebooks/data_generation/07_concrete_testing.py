# Databricks notebook source

# COMMAND ----------
%pip install faker --quiet

# COMMAND ----------

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

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.concrete_testing")

# COMMAND ----------

# ============================================================
# TABLE: mix_designs  (~60 rows, 2-4 per project)
# ============================================================

def parse_date(d_str):
    return datetime.strptime(d_str, "%Y-%m-%d").date()

BATCH_PLANTS = [
    "Denver Concrete Inc",
    "Colorado Ready Mix LLC",
    "Front Range Concrete Materials",
    "Lafarge Denver",
]

ENGINEERS_OF_RECORD = [
    "Brian Kowalski, PE",
    "Carla Nguyen, PE, SE",
    "Douglas Hartley, PE",
    "Emily Strickland, PE, SE",
    "Frank Romero, PE",
    "Grace Kim, PE, SE",
    "Harold Bennett, PE",
    "Irene Castillo, PE",
]

ADMIXTURE_COMBOS = [
    "Water reducer (ASTM C494 Type A), Air entrainer (ASTM C260)",
    "Mid-range water reducer (ASTM C494 Type F), Air entrainer (ASTM C260)",
    "High-range water reducer (ASTM C494 Type F), Air entrainer (ASTM C260), Retarder (ASTM C494 Type B)",
    "Water reducer (ASTM C494 Type A), Air entrainer (ASTM C260), Accelerator (ASTM C494 Type C)",
    "Mid-range water reducer (ASTM C494 Type F), Air entrainer (ASTM C260), Fly ash 20% replacement",
    "Water reducer (ASTM C494 Type A), Air entrainer (ASTM C260), Silica fume 5% replacement",
    "High-range water reducer (ASTM C494 Type F), Air entrainer (ASTM C260), Slag cement 30% replacement",
    "Water reducer (ASTM C494 Type A), Air entrainer (ASTM C260), Shrinkage reducing admixture",
]

# Design strength by project type: larger/structural = higher strength
PROJECT_STRENGTH_PROFILES = {
    "P001": [4000, 5000, 3500],
    "P002": [4000, 5000, 6000, 3500],
    "P003": [3000, 4000],
    "P004": [3500, 4000, 3000],
    "P005": [4000, 5000, 3500],
    "P006": [3500, 3000, 4000],
    "P007": [4000, 4000, 3500, 3000],
    "P008": [4000, 5000, 3500],
    "P009": [4000, 5000, 3000],
    "P010": [4000, 4000, 3500, 5000],
    "P011": [4000, 5000, 3500, 3000],
    "P012": [3000, 3500, 4000],
    "P013": [4000, 5000, 6000, 3500],
    "P014": [3500, 4000, 3000],
    "P015": [4000, 3500, 3000],
    "P016": [3000, 4000, 3500],
    "P017": [3000, 3500, 4000],
    "P018": [3500, 4000, 3000],
    "P019": [3500, 4000, 3000],
    "P020": [3000, 3500],
    "P021": [4000, 5000, 3500, 3000],
    "P022": [4000, 5000, 6000, 3500],
    "P023": [4000, 3500, 3000],
    "P024": [3000, 3500, 4000],
    "P025": [4000, 5000, 6000, 5000],
}

W_C_RATIO_MAP = {3000: 0.53, 3500: 0.49, 4000: 0.45, 5000: 0.40, 6000: 0.36}

random.seed(201)
mix_design_rows = []
mix_design_map = {}  # project_id -> list of (mix_id, design_strength_psi)

for p in PROJECTS:
    start = parse_date(p["start_date"])
    strengths = PROJECT_STRENGTH_PROFILES[p["project_id"]]
    project_num = p["project_id"]

    mix_design_map[p["project_id"]] = []

    for idx, strength in enumerate(strengths):
        mix_id = str(uuid.uuid4())
        mix_design_number = f"MD-{project_num}-{idx + 1:02d}"

        # Cement type
        if strength >= 5000:
            cement_type = "Type_III"
        elif project_num in ("P002", "P010", "P016"):  # sulfate exposure environments
            cement_type = "Type_II"
        else:
            cement_type = "Type_II"

        base_wc = W_C_RATIO_MAP[strength]
        w_c_ratio = round(base_wc + random.uniform(-0.01, 0.01), 2)

        slump_min = 3.0
        slump_max = random.choice([5.0, 6.0, 7.0])

        air_min = 4.0
        air_max = random.choice([7.0, 7.5, 8.0])

        agg_size = random.choice([0.75, 1.0, 1.0, 1.5]) if strength < 5000 else random.choice([0.75, 0.75, 1.0])

        admixtures = random.choice(ADMIXTURE_COMBOS)
        batch_plant = random.choice(BATCH_PLANTS)

        # Approved date: before project start
        approved_days_before = random.randint(30, 90)
        approved_date = start - timedelta(days=approved_days_before)

        engineer = random.choice(ENGINEERS_OF_RECORD)

        mix_design_rows.append({
            "mix_id": mix_id,
            "project_id": p["project_id"],
            "mix_design_number": mix_design_number,
            "design_strength_psi": strength,
            "cement_type": cement_type,
            "w_c_ratio": w_c_ratio,
            "slump_min_inches": slump_min,
            "slump_max_inches": slump_max,
            "air_content_min_pct": air_min,
            "air_content_max_pct": air_max,
            "max_aggregate_size_inches": agg_size,
            "admixtures": admixtures,
            "batch_plant": batch_plant,
            "approved_date": approved_date.strftime("%Y-%m-%d"),
            "engineer_of_record": engineer,
        })

        mix_design_map[p["project_id"]].append((mix_id, strength, batch_plant))

mix_pdf = pd.DataFrame(mix_design_rows)
mix_df = spark.createDataFrame(mix_pdf)
mix_df.write.mode("overwrite").saveAsTable(f"{catalog}.concrete_testing.mix_designs")
df = spark.table(f"{catalog}.concrete_testing.mix_designs")
print(f"Created {catalog}.concrete_testing.mix_designs with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: pour_logs  (~2,000 rows)
# ============================================================

STRUCTURAL_ELEMENTS = [
    ("footing", 30, 120, 0.15),
    ("pile_cap", 40, 200, 0.08),
    ("slab_on_grade", 50, 400, 0.25),
    ("elevated_slab", 40, 350, 0.25),
    ("column", 10, 60, 0.10),
    ("wall", 20, 150, 0.12),
    ("beam", 15, 80, 0.05),
)

LOCATION_TEMPLATES = [
    "Grid {col}-{row} Level {lvl} Slab",
    "Column Line {col} Footings {start} to {end}",
    "Shear Wall SW-{num} Level {lvl}",
    "Slab on Grade Zone {zone}",
    "Mat Foundation Grid {col1}{row1} to {col2}{row2}",
    "Pile Caps PC-{num1} through PC-{num2}",
    "Grade Beam GB-{num1} to GB-{num2}",
    "Elevator Core Walls Level {lvl}",
    "Transfer Beam TB-{num} at Level {lvl}",
    "Retaining Wall RW-{num} Station {sta1}+{sta2}",
]

CONCRETE_CONTRACTORS = {
    "P001": "Colorado Concrete Inc",
    "P002": "Front Range Concrete LLC",
    "P003": "Mountain States Concrete Co",
    "P004": "Colorado Concrete Inc",
    "P005": "Mountain States Concrete Co",
    "P006": "Front Range Concrete LLC",
    "P007": "Rocky Mountain Ready Mix Contractors",
    "P008": "Colorado Concrete Inc",
    "P009": "Peak Concrete Services LLC",
    "P010": "Rocky Mountain Ready Mix Contractors",
    "P011": "Colorado Concrete Inc",
    "P012": "Mountain States Concrete Co",
    "P013": "Front Range Concrete LLC",
    "P014": "Colorado Concrete Inc",
    "P015": "Rocky Mountain Ready Mix Contractors",
    "P016": "Peak Concrete Services LLC",
    "P017": "Mountain States Concrete Co",
    "P018": "Front Range Concrete LLC",
    "P019": "Colorado Concrete Inc",
    "P020": "Mountain States Concrete Co",
    "P021": "Front Range Concrete LLC",
    "P022": "Colorado Concrete Inc",
    "P023": "Peak Concrete Services LLC",
    "P024": "Mountain States Concrete Co",
    "P025": "Colorado Concrete Inc",
}

def denver_temp_f(pour_date):
    """Return a realistic ambient temperature for Denver by month."""
    month = pour_date.month
    # Monthly average highs in Denver (approximate)
    avg_temps = {1: 43, 2: 47, 3: 55, 4: 63, 5: 72, 6: 82,
                 7: 88, 8: 85, 9: 77, 10: 64, 11: 50, 12: 43}
    base = avg_temps[month]
    return base + random.randint(-10, 10)

def generate_location():
    cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
    rows = list(range(1, 12))
    lvls = list(range(1, 8))
    tmpl = random.choice(LOCATION_TEMPLATES)
    return tmpl.format(
        col=random.choice(cols),
        row=random.choice(rows),
        col1=random.choice(cols[:4]),
        col2=random.choice(cols[4:]),
        row1=random.choice(rows[:5]),
        row2=random.choice(rows[5:]),
        lvl=random.choice(lvls),
        start=random.randint(1, 10),
        end=random.randint(11, 20),
        num=random.randint(1, 50),
        num1=random.randint(1, 20),
        num2=random.randint(21, 50),
        zone=random.choice(["A", "B", "C", "D", "1", "2", "3"]),
        sta1=random.randint(0, 15),
        sta2=random.randint(10, 99),
    )

POUR_START_HOURS = ["06:00", "06:30", "07:00", "07:00", "07:00", "07:30", "08:00", "08:00", "08:00", "09:00", "10:00"]

random.seed(202)
pour_rows = []
pour_map = {}  # project_id -> list of (pour_id, pour_date, mix_id, design_strength_psi)

target_pour_count = 2000
pours_per_project = {}

for p in PROJECTS:
    cv = float(p["contract_value"])
    if cv >= 100000000:
        pours_per_project[p["project_id"]] = random.randint(110, 140)
    elif cv >= 50000000:
        pours_per_project[p["project_id"]] = random.randint(70, 100)
    elif cv >= 25000000:
        pours_per_project[p["project_id"]] = random.randint(45, 70)
    else:
        pours_per_project[p["project_id"]] = random.randint(25, 45)

for p in PROJECTS:
    start = parse_date(p["start_date"])
    end = parse_date(p["end_date"])
    project_duration_days = max(1, (end - start).days)
    cutoff = date(2026, 8, 11)  # today
    effective_end = min(end, cutoff)
    effective_duration = max(1, (effective_end - start).days)

    mixes = mix_design_map[p["project_id"]]
    concrete_contractor = CONCRETE_CONTRACTORS[p["project_id"]]

    pour_map[p["project_id"]] = []
    num_pours = pours_per_project[p["project_id"]]

    # Weight pours toward middle of project (bell curve-ish)
    for i in range(num_pours):
        # Use a beta distribution to cluster pours in middle
        frac = random.betavariate(2, 2)
        offset_days = int(frac * effective_duration)
        pour_date = start + timedelta(days=max(0, offset_days))

        # Pick a mix design - vary by structural element
        mix_id, design_strength, batch_plant = random.choice(mixes)

        # Pick structural element
        elem_choices = [(e[0], e[3]) for e in STRUCTURAL_ELEMENTS]
        elements, weights = zip(*elem_choices)
        structural_element = random.choices(elements, weights=weights, k=1)[0]

        # Yards by element type
        elem_idx = [e[0] for e in STRUCTURAL_ELEMENTS].index(structural_element)
        yds_min, yds_max = STRUCTURAL_ELEMENTS[elem_idx][1], STRUCTURAL_ELEMENTS[elem_idx][2]
        cubic_yards_ordered = random.randint(yds_min, yds_max)
        cubic_yards_placed = cubic_yards_ordered - random.randint(0, max(1, int(cubic_yards_ordered * 0.05)))

        truck_count = math.ceil(cubic_yards_ordered / 9)

        start_hour_str = random.choice(POUR_START_HOURS)
        start_hour, start_min = map(int, start_hour_str.split(":"))
        pour_duration_hours = random.randint(2, 8)
        end_hour = start_hour + pour_duration_hours
        end_min = start_min + random.randint(0, 59)
        if end_min >= 60:
            end_hour += 1
            end_min -= 60
        pour_end_time = f"{end_hour:02d}:{end_min:02d}"

        ambient_temp = denver_temp_f(pour_date)
        # Concrete temp adjusted for ambient
        concrete_temp = min(90, max(50, ambient_temp + random.randint(-5, 15)))

        slump = round(random.uniform(3.0, 7.0), 1)
        air_content = round(random.uniform(4.5, 7.5), 1)
        unit_weight = round(random.uniform(140.0, 150.0), 1)

        samples_taken = max(2, math.ceil(cubic_yards_placed / 50))
        special_inspector = structural_element not in ("slab_on_grade",) or random.random() < 0.85

        notes_options = [None, None, None, None,
                         "Hot weather concrete procedures in effect",
                         "Cold weather concrete procedures in effect",
                         "Rain delayed start by 1 hour",
                         "Pump truck used for placement",
                         "Night pour - temporary lighting required",
                         "High-early strength mix requested by structural engineer"]
        # Season-based notes
        if ambient_temp > 90:
            notes = "Hot weather concrete procedures in effect - ice added to mix water"
        elif ambient_temp < 35:
            notes = "Cold weather concrete procedures in effect - heated water and aggregates used"
        else:
            notes = random.choice(notes_options)

        pour_id = str(uuid.uuid4())
        pour_map[p["project_id"]].append((pour_id, pour_date, mix_id, design_strength))

        pour_rows.append({
            "pour_id": pour_id,
            "project_id": p["project_id"],
            "pour_date": pour_date.strftime("%Y-%m-%d"),
            "mix_design_id": mix_id,
            "location_description": generate_location(),
            "structural_element": structural_element,
            "cubic_yards_ordered": cubic_yards_ordered,
            "cubic_yards_placed": cubic_yards_placed,
            "concrete_contractor": concrete_contractor,
            "batch_plant": batch_plant,
            "truck_count": truck_count,
            "pour_start_time": start_hour_str,
            "pour_end_time": pour_end_time,
            "ambient_temp_f": ambient_temp,
            "concrete_temp_f": int(concrete_temp),
            "slump_measured_inches": slump,
            "air_content_measured_pct": air_content,
            "unit_weight_pcf": unit_weight,
            "samples_taken": samples_taken,
            "special_inspector_on_site": special_inspector,
            "notes": notes,
        })

pour_pdf = pd.DataFrame(pour_rows)
pour_df = spark.createDataFrame(pour_pdf)
pour_df.write.mode("overwrite").saveAsTable(f"{catalog}.concrete_testing.pour_logs")
df = spark.table(f"{catalog}.concrete_testing.pour_logs")
print(f"Created {catalog}.concrete_testing.pour_logs with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: cylinder_breaks  (~12,000 rows)
# ============================================================

LAB_NAMES = [
    "CTL Thompson Inc",
    "RMT Engineering Inc",
    "Terracon Consultants Inc",
    "AECOM Technical Services",
]

LAB_TECHNICIANS = [
    "Aaron Sandoval", "Brenda Park", "Carlos Mejia", "Diane Ohlsson",
    "Eduardo Ferraz", "Fiona McAllister", "George Tran", "Helen Buckley",
    "Ivan Korolev", "Janelle Watkins", "Kevin Oshiro", "Laura Stanton",
]

random.seed(203)
cylinder_rows = []

# 7-day strength as fraction of 28-day
# 28-day target = 110-120% of design
# 56-day target = 115-125% of design

for p in PROJECTS:
    pours = pour_map.get(p["project_id"], [])

    for (pour_id, pour_date, mix_id, design_strength) in pours:
        # Each pour gets samples_taken / 2 sets (minimum 1 set = pair of cylinders)
        # From pour_logs: samples_taken = max(2, ceil(cyd/50))
        # Number of sets: 1-4 depending on pour size
        num_sets = random.randint(1, 3)

        for set_num in range(1, num_sets + 1):
            # Break ages for this set
            break_ages = [7, 28]
            if random.random() < 0.30:
                break_ages.append(56)

            for break_age in break_ages:
                for sample_num in range(1, 3):  # 2 cylinders per break age per set
                    break_id = str(uuid.uuid4())

                    break_date = pour_date + timedelta(days=break_age)

                    # Design the actual strength based on break age
                    target_28_day = design_strength * random.uniform(1.10, 1.22)

                    # Low result probability
                    is_low = random.random() < 0.04  # 4% chance of low result

                    if break_age == 7:
                        fraction = random.uniform(0.63, 0.72)
                        actual_strength = int(target_28_day * fraction)
                        if is_low:
                            actual_strength = int(target_28_day * random.uniform(0.55, 0.63))
                    elif break_age == 14:
                        fraction = random.uniform(0.82, 0.90)
                        actual_strength = int(target_28_day * fraction)
                        if is_low:
                            actual_strength = int(target_28_day * random.uniform(0.72, 0.82))
                    elif break_age == 28:
                        actual_strength = int(target_28_day * random.uniform(0.97, 1.05))
                        if is_low:
                            actual_strength = int(design_strength * random.uniform(0.80, 0.89))
                    else:  # 56-day
                        fraction = random.uniform(1.10, 1.20)
                        actual_strength = int(target_28_day * fraction)
                        if is_low:
                            actual_strength = int(target_28_day * random.uniform(1.00, 1.08))

                    percent_of_design = round((actual_strength / design_strength) * 100, 1)

                    # Pass/fail: 28-day must be >= 85% of design
                    if break_age == 28:
                        pass_fail = "pass" if actual_strength >= design_strength * 0.85 else "fail"
                    elif break_age == 7:
                        # 7-day is informational, flag if very low
                        pass_fail = "pass" if actual_strength >= design_strength * 0.55 else "fail"
                    else:
                        pass_fail = "pass" if actual_strength >= design_strength * 0.85 else "fail"

                    tested_by = random.choice(LAB_TECHNICIANS)
                    lab_name = random.choice(LAB_NAMES)

                    # Remarks
                    if pass_fail == "fail":
                        remarks = f"Strength below minimum acceptance criterion. Field investigation required. Core samples may be warranted per ACI 318."
                    elif is_low and break_age == 7:
                        remarks = "Low 7-day result. Monitor 28-day break. Verify curing conditions."
                    elif break_date > date(2026, 8, 11):
                        remarks = "Break date in future - specimen in curing room"
                    else:
                        remarks = None

                    cylinder_rows.append({
                        "break_id": break_id,
                        "pour_id": pour_id,
                        "project_id": p["project_id"],
                        "mix_design_id": mix_id,
                        "set_number": set_num,
                        "sample_number": sample_num,
                        "break_age_days": break_age,
                        "break_date": break_date.strftime("%Y-%m-%d"),
                        "design_strength_psi": design_strength,
                        "actual_strength_psi": actual_strength,
                        "percent_of_design": percent_of_design,
                        "pass_fail": pass_fail,
                        "tested_by": tested_by,
                        "lab_name": lab_name,
                        "test_method": "ASTM_C39",
                        "remarks": remarks,
                    })

cyl_pdf = pd.DataFrame(cylinder_rows)
cyl_df = spark.createDataFrame(cyl_pdf)
cyl_df.write.mode("overwrite").saveAsTable(f"{catalog}.concrete_testing.cylinder_breaks")
df = spark.table(f"{catalog}.concrete_testing.cylinder_breaks")
print(f"Created {catalog}.concrete_testing.cylinder_breaks with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: concrete_inspections  (~2,000 rows, ~1 per pour)
# ============================================================

INSPECTOR_NAMES = [
    "Aaron Sandoval, ACI", "Brenda Park, ICC", "Carlos Mejia, ACI",
    "Diane Ohlsson, ICC", "Eduardo Ferraz, ACI", "Fiona McAllister, ICC",
    "George Tran, ACI", "Helen Buckley, ICC", "Ivan Korolev, ACI",
    "Janelle Watkins, ICC",
]

INSPECTOR_CERTIFICATIONS = [
    "ACI Field Testing Technician",
    "ICC Special Inspector",
    "ACI Field Testing Technician",
    "ICC Special Inspector",
    "ACI Field Testing Technician",
]

NC_DESCRIPTIONS = [
    "Rebar spacing outside specification tolerance",
    "Concrete placement exceeded maximum drop height per ACI 309",
    "Mix slump outside specified range",
    "Cover to reinforcement insufficient at formed edge",
    "Form alignment exceeds ACI 117 tolerance",
    "Consolidation inadequate at wall base",
    "Truck ticket not available for one load",
    "Water added to truck at site without engineer approval",
    "Cold weather protection not in place prior to pour",
    "Rebar lap splice length below specified minimum",
]

CORRECTIVE_ACTIONS = [
    "Contractor to reposition rebar within tolerance and re-inspect prior to placement",
    "Superintendent directed on proper placement methods per ACI 309",
    "Batch plant notified to adjust mix for slump compliance",
    "Additional concrete cover added; engineer of record notified",
    "Forms realigned and re-inspected; approved for placement",
    "Additional vibration applied; inspector monitored for adequacy",
    "Contractor to retain all truck tickets; engineer to review before final acceptance",
    "Structural engineer notified; additional core samples ordered to verify strength",
    "Cold weather protection blankets installed; temperature monitoring initiated",
    "Splice corrected prior to concrete placement",
]

random.seed(204)
inspection_rows = []
inspection_counter_by_project = {}

for p in PROJECTS:
    pours = pour_map.get(p["project_id"], [])
    inspection_counter_by_project[p["project_id"]] = 0

    for (pour_id, pour_date, mix_id, design_strength) in pours:
        inspection_id = str(uuid.uuid4())
        inspection_counter_by_project[p["project_id"]] += 1
        seq = inspection_counter_by_project[p["project_id"]]

        proj_num = p["project_id"]
        report_number = f"IR-{proj_num}-{pour_date.year}-{seq:03d}"

        inspector_full = random.choice(INSPECTOR_NAMES)
        inspector_name = inspector_full.split(",")[0]
        inspector_cert = random.choice(INSPECTOR_CERTIFICATIONS)

        # Results
        roll = random.random()
        if roll < 0.90:
            overall_result = "pass"
            nc_count = 0
        elif roll < 0.98:
            overall_result = "conditional"
            nc_count = random.randint(1, 3)
        else:
            overall_result = "fail"
            nc_count = random.randint(2, 4)

        pre_pour = random.random() < 0.95
        forms_ok = random.random() < 0.95
        rebar_ok = random.random() < 0.95 if pre_pour else False
        mix_verified = random.random() < 0.98
        tickets_reviewed = random.random() < 0.99

        if nc_count > 0:
            nc_descs = random.sample(NC_DESCRIPTIONS, min(nc_count, len(NC_DESCRIPTIONS)))
            nc_desc_text = "; ".join(nc_descs)
            ca_text = random.choice(CORRECTIVE_ACTIONS)
            corrective_action_required = True
        else:
            nc_desc_text = None
            ca_text = None
            corrective_action_required = False

        inspection_rows.append({
            "inspection_id": inspection_id,
            "project_id": p["project_id"],
            "pour_id": pour_id,
            "inspection_date": pour_date.strftime("%Y-%m-%d"),
            "inspector_name": inspector_name,
            "inspector_certification": inspector_cert,
            "pre_pour_approval": pre_pour,
            "forms_accepted": forms_ok,
            "rebar_accepted": rebar_ok,
            "mix_design_verified": mix_verified,
            "truck_tickets_reviewed": tickets_reviewed,
            "overall_result": overall_result,
            "nonconformance_count": nc_count,
            "nonconformance_descriptions": nc_desc_text,
            "corrective_action_required": corrective_action_required,
            "report_number": report_number,
        })

insp_pdf = pd.DataFrame(inspection_rows)
insp_df = spark.createDataFrame(insp_pdf)
insp_df.write.mode("overwrite").saveAsTable(f"{catalog}.concrete_testing.concrete_inspections")
df = spark.table(f"{catalog}.concrete_testing.concrete_inspections")
print(f"Created {catalog}.concrete_testing.concrete_inspections with {df.count()} rows")
