# Databricks notebook source
import random
import uuid
from datetime import date, datetime, timedelta
import pandas as pd
from faker import Faker

random.seed(42)
fake = Faker()
Faker.seed(42)

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

TODAY = date(2026, 8, 11)

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.scheduling")
print(f"Schema {catalog}.scheduling ready")

# COMMAND ----------

# ── TABLE: crew_schedules (~100,000 rows) ──────────────────────────────────────
# One row per employee-day per project. Crew size 5-12 per project per day,
# weekdays only, capped at TODAY. EMP-001 to EMP-200 pool.

FIELD_TASK_DESCRIPTIONS = [
    "Concrete formwork installation",
    "Electrical rough-in wiring",
    "Structural steel erection",
    "Plumbing rough-in below slab",
    "Drywall framing and studs",
    "Foundation excavation",
    "Slab on grade concrete pour",
    "MEP overhead coordination",
    "Masonry block wall construction",
    "Roofing installation - membrane",
    "Curtain wall installation",
    "HVAC ductwork installation",
    "Site grading and earthwork",
    "Reinforcing steel placement",
    "Concrete column pour",
    "Partition wall stud framing",
    "Underground utility installation",
    "Footing excavation and forming",
    "Structural steel bolt-up",
    "Exterior insulation and finish",
    "Tile installation - floor",
    "Overhead MEP rough-in",
    "Equipment pad concrete pour",
    "Concrete deck topping",
    "Overhead door installation",
    "Storefront glazing installation",
    "Elevator shaft forming",
    "Waterproofing application",
    "Suspended ceiling grid",
    "Fire sprinkler rough-in",
    "Painting - primer coat",
    "Insulation batt installation",
    "Metal deck welding",
    "Grading and paving sub-base",
    "Interior concrete stair pour",
    "Exterior masonry veneer",
    "Mechanical equipment setting",
    "Electrical switchgear installation",
    "Demolition - selective interior",
    "Steel stud exterior framing",
]

FIELD_TRADES = [
    "carpenter", "ironworker", "electrician", "plumber", "laborer",
    "foreman", "cement_mason", "operating_engineer", "pipefitter", "roofer",
]

FIELD_COST_CODES = [
    "03-100", "03-200", "03-300", "05-100", "05-300",
    "06-100", "06-200", "09-100", "15-200", "15-300",
    "16-100", "16-200", "02-040", "02-020",
]

ALL_EMP_IDS = [f"EMP-{i:03d}" for i in range(1, 201)]
FOREMAN_IDS = [f"EMP-{i:03d}" for i in range(131, 151)]  # foremen band

crew_schedules = []
for p in PROJECTS:
    start = datetime.strptime(p["start_date"], "%Y-%m-%d").date()
    end_raw = datetime.strptime(p["end_date"], "%Y-%m-%d").date()
    end = min(end_raw, TODAY)

    # Scale crew size by contract value: small projects fewer workers per day
    val = p["contract_value"]
    if val < 25000000:
        crew_min, crew_max = 3, 8
    elif val < 60000000:
        crew_min, crew_max = 5, 12
    elif val < 100000000:
        crew_min, crew_max = 6, 14
    else:
        crew_min, crew_max = 8, 16

    current = start
    while current <= end:
        if current.weekday() < 5:
            n_workers = random.randint(crew_min, crew_max)
            workers = random.sample(ALL_EMP_IDS, min(n_workers, len(ALL_EMP_IDS)))
            foreman_id = random.choice(FOREMAN_IDS)
            task = random.choice(FIELD_TASK_DESCRIPTIONS)
            cost_code = random.choice(FIELD_COST_CODES)

            for emp_id in workers:
                is_ot_day = random.random() < 0.25
                overtime_hours = round(random.uniform(1.0, 4.0), 1) if is_ot_day else 0.0
                hours_worked = round(8.0 + overtime_hours, 1)
                shift_end_hr = 15 if overtime_hours == 0 else 17
                shift_end_min = random.choice(["00", "30"])
                shift_end = f"{shift_end_hr:02d}:{shift_end_min}"

                crew_schedules.append({
                    "schedule_id": str(uuid.uuid4()),
                    "employee_id": emp_id,
                    "project_id": p["project_id"],
                    "work_date": str(current),
                    "shift_start": "07:00",
                    "shift_end": shift_end,
                    "hours_worked": hours_worked,
                    "trade": random.choice(FIELD_TRADES),
                    "task_description": task,
                    "foreman_id": foreman_id,
                    "overtime_hours": overtime_hours,
                    "cost_code": cost_code,
                })
        current += timedelta(days=1)

pdf_cs = pd.DataFrame(crew_schedules)
spark.createDataFrame(pdf_cs).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.scheduling.crew_schedules")
df = spark.table(f"{catalog}.scheduling.crew_schedules")
print(f"Created {catalog}.scheduling.crew_schedules with {df.count()} rows")

# COMMAND ----------

# ── TABLE: equipment_schedules (~30,000 rows) ──────────────────────────────────
# EQ-001 to EQ-150, 150 pieces. Logged on a subset of project working days.

EQUIPMENT_CATALOG = [
    # (equipment_type, name_options, fuel_gal_per_hr_min, fuel_gal_per_hr_max, rate_min, rate_max)
    ("excavator",      ["CAT 320 Excavator", "Komatsu PC290", "John Deere 350G"],          8.0, 14.0, 1200, 2200),
    ("crane",          ["Liebherr LTM 1100", "Grove GMK5150L", "Manitowoc 14000"],         9.0, 14.0, 1800, 2500),
    ("concrete_pump",  ["Schwing S43 Boom Pump", "Putzmeister BSF 42", "Alliance 47m"],    6.0, 12.0, 1500, 2200),
    ("forklift",       ["Toyota 8FGU25", "Caterpillar DP50N", "Crown FC 5200"],            2.0,  5.0,  200,  450),
    ("generator",      ["CAT XQ230", "Kohler 200REOZJF", "Cummins C200D6"],                3.5,  9.0,  250,  600),
    ("compactor",      ["Bomag BW 213", "Dynapac CA250D", "CAT CS56B"],                    4.0,  8.0,  400,  900),
    ("aerial_lift",    ["JLG 1250AJP Boom", "Genie Z-135/70", "Skyjack SJ45AJ"],          2.5,  6.0,  350,  800),
    ("bulldozer",      ["CAT D6T Dozer", "Komatsu D65EX", "John Deere 850K"],              9.0, 14.0,  900, 1600),
    ("grader",         ["CAT 140M3 Grader", "John Deere 772G", "Komatsu GD655"],           8.0, 13.0,  800, 1400),
    ("pump",           ["Godwin CD200M", "Tsurumi TE3-50HA", "Grundfos SP77-3"],           1.0,  3.0,  150,  400),
]

# Build equipment master list (150 pieces, cycling through types)
equipment_master = []
for i in range(150):
    eq_type_idx = i % len(EQUIPMENT_CATALOG)
    eq_type, name_opts, fuel_min, fuel_max, rate_min, rate_max = EQUIPMENT_CATALOG[eq_type_idx]
    equipment_master.append({
        "equipment_id": f"EQ-{i + 1:03d}",
        "equipment_name": name_opts[i % len(name_opts)],
        "equipment_type": eq_type,
        "fuel_rate_min": fuel_min,
        "fuel_rate_max": fuel_max,
        "rate_min": rate_min,
        "rate_max": rate_max,
    })

random.seed(42)

equip_schedules = []
for p in PROJECTS:
    start = datetime.strptime(p["start_date"], "%Y-%m-%d").date()
    end_raw = datetime.strptime(p["end_date"], "%Y-%m-%d").date()
    end = min(end_raw, TODAY)

    # Scale equipment count by project size
    val = p["contract_value"]
    if val < 25000000:
        eq_per_day_min, eq_per_day_max = 1, 3
        active_day_prob = 0.60
    elif val < 60000000:
        eq_per_day_min, eq_per_day_max = 2, 5
        active_day_prob = 0.65
    elif val < 100000000:
        eq_per_day_min, eq_per_day_max = 3, 6
        active_day_prob = 0.70
    else:
        eq_per_day_min, eq_per_day_max = 4, 8
        active_day_prob = 0.75

    current = start
    while current <= end:
        if current.weekday() < 5 and random.random() < active_day_prob:
            n_eq = random.randint(eq_per_day_min, eq_per_day_max)
            selected_eq = random.sample(equipment_master, min(n_eq, len(equipment_master)))
            for eq in selected_eq:
                hours_op = round(random.uniform(2.0, 10.0), 1)
                fuel = round(hours_op * random.uniform(eq["fuel_rate_min"], eq["fuel_rate_max"]), 1)
                equip_schedules.append({
                    "schedule_id": str(uuid.uuid4()),
                    "equipment_id": eq["equipment_id"],
                    "equipment_name": eq["equipment_name"],
                    "equipment_type": eq["equipment_type"],
                    "project_id": p["project_id"],
                    "work_date": str(current),
                    "hours_operated": hours_op,
                    "operator_employee_id": f"EMP-{random.randint(1, 200):03d}",
                    "fuel_consumed_gallons": fuel,
                    "rental_rate_per_day": float(random.randint(eq["rate_min"], eq["rate_max"])),
                })
        current += timedelta(days=1)

pdf_eq = pd.DataFrame(equip_schedules)
spark.createDataFrame(pdf_eq).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.scheduling.equipment_schedules")
df = spark.table(f"{catalog}.scheduling.equipment_schedules")
print(f"Created {catalog}.scheduling.equipment_schedules with {df.count()} rows")

# COMMAND ----------

# ── TABLE: subcontractor_schedules (~500 rows) ─────────────────────────────────
# Each project gets 18-22 subcontractor schedule entries covering phases.
# Phases: mobilization, foundation, structure, MEP_rough, enclosure,
#         MEP_trim, finishes, punch_list

PHASES_ORDERED = [
    "mobilization", "foundation", "structure", "MEP_rough",
    "enclosure", "MEP_trim", "finishes", "punch_list",
]

# Duration (in days) for each phase
PHASE_DURATIONS = {
    "mobilization": (14, 30),
    "foundation":   (30, 75),
    "structure":    (45, 120),
    "MEP_rough":    (60, 120),
    "enclosure":    (45, 90),
    "MEP_trim":     (30, 75),
    "finishes":     (45, 90),
    "punch_list":   (14, 45),
}

# Typical crew sizes by trade
TRADE_CREW_SIZES = {
    "electrical":    (10, 60),
    "mechanical":    (8, 50),
    "steel_erection": (8, 40),
    "concrete":      (12, 70),
    "drywall":       (10, 50),
    "roofing":       (5, 30),
    "plumbing":      (6, 40),
    "glazing":       (5, 25),
    "fire_protection": (5, 25),
    "landscaping":   (5, 20),
    "elevators":     (4, 15),
    "HVAC":          (8, 45),
    "painting":      (6, 30),
    "flooring":      (6, 30),
    "masonry":       (8, 40),
}

SUB_ID_POOL = [f"SUB-{i:03d}" for i in range(1, 61)]

sub_schedules = []
random.seed(42)

for p in PROJECTS:
    p_start = datetime.strptime(p["start_date"], "%Y-%m-%d").date()
    p_end = datetime.strptime(p["end_date"], "%Y-%m-%d").date()
    project_duration = (p_end - p_start).days
    status = p["status"]

    # Assign 18-22 subcontractor entries per project
    n_entries = random.randint(18, 22)

    # Pick n_entries (phase, sub_id) pairs, cycling through phases multiple times
    phase_assignments = []
    for j in range(n_entries):
        phase = PHASES_ORDERED[j % len(PHASES_ORDERED)]
        sub_id = random.choice(SUB_ID_POOL)
        phase_assignments.append((phase, sub_id))

    # Lay phases out along the project timeline with some overlap
    cumulative_offset = 0
    for j, (phase, sub_id) in enumerate(phase_assignments):
        phase_idx = PHASES_ORDERED.index(phase)
        # Base start offset: roughly proportional to phase order
        base_offset = int(project_duration * phase_idx / (len(PHASES_ORDERED) + 1))
        jitter = random.randint(-10, 20)
        offset_days = max(0, base_offset + jitter + j * random.randint(0, 5))

        phase_min_dur, phase_max_dur = PHASE_DURATIONS[phase]
        phase_dur = random.randint(phase_min_dur, phase_max_dur)

        planned_start = p_start + timedelta(days=offset_days)
        planned_end = planned_start + timedelta(days=phase_dur)

        # Derive trade from SUB_ID index (use modulo against trades list)
        trade_list = list(TRADE_CREW_SIZES.keys())
        sub_idx = int(sub_id.split("-")[1]) - 1
        trade = trade_list[sub_idx % len(trade_list)]
        crew_min, crew_max = TRADE_CREW_SIZES[trade]
        crew_size = random.randint(crew_min, crew_max)

        # Determine actual dates and status
        if status == "completed":
            actual_start = planned_start + timedelta(days=random.randint(-3, 10))
            actual_end = planned_end + timedelta(days=random.randint(-7, 20))
            sched_status = "completed"
        elif status == "closeout":
            actual_start = planned_start + timedelta(days=random.randint(-3, 10))
            if planned_end <= TODAY:
                actual_end = planned_end + timedelta(days=random.randint(-7, 15))
                sched_status = "completed"
            else:
                actual_end = None
                sched_status = "active"
        else:
            # active project
            if planned_start > TODAY:
                actual_start = None
                actual_end = None
                sched_status = "scheduled"
            elif planned_end <= TODAY:
                actual_start = planned_start + timedelta(days=random.randint(-3, 10))
                actual_end = planned_end + timedelta(days=random.randint(-7, 20))
                sched_status = "completed"
            else:
                actual_start = planned_start + timedelta(days=random.randint(-3, 10))
                actual_end = None
                sched_status = random.choices(
                    ["active", "active", "delayed"],
                    weights=[65, 25, 10],
                )[0]

        sub_schedules.append({
            "schedule_id": str(uuid.uuid4()),
            "sub_id": sub_id,
            "project_id": p["project_id"],
            "phase": phase,
            "planned_start_date": str(planned_start),
            "planned_end_date": str(planned_end),
            "actual_start_date": str(actual_start) if actual_start else None,
            "actual_end_date": str(actual_end) if actual_end else None,
            "crew_size": crew_size,
            "status": sched_status,
        })

pdf_ss = pd.DataFrame(sub_schedules)
spark.createDataFrame(pdf_ss).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.scheduling.subcontractor_schedules")
df = spark.table(f"{catalog}.scheduling.subcontractor_schedules")
print(f"Created {catalog}.scheduling.subcontractor_schedules with {df.count()} rows")

# COMMAND ----------

# ── TABLE: daily_manpower_log (~15,000 rows) ────────────────────────────────────
# One log per project per working day (Mon-Fri), plus Saturday work.
# Uses the full projected project duration (not capped at TODAY) so future-dated
# active projects have forecasted log entries representing planned staffing.
# Saturday work logs are generated at realistic probabilities based on project size.
# Notes text is generated for ~15% of entries.
# Row count is naturally constrained by the 25-project universe: 25 projects
# averaging ~600 working days each yields ~15,000 project-day rows.

NOTES_POOL = [
    "Full crew on site, weather favorable.",
    "Rain delay in morning, crew resumed at 10:00.",
    "Concrete pour completed for column grid B-C.",
    "Safety stand-down held for near-miss incident review.",
    "Steel erection crane on site for structural connections.",
    "Owner's rep conducted site walk.",
    "Inspector approved foundation pour.",
    "MEP coordination meeting held on site.",
    "Delayed start due to material delivery.",
    "Overtime authorized - schedule recovery.",
    "Sub crew demobilized early, returned following day.",
    "Site flooded by overnight rain, cleanup required.",
    "Productivity reduced by high winds at elevation.",
    "New subcontractor crew mobilized for framing work.",
    "QC punch list items addressed by trade crews.",
    "OSHA compliance inspection, no violations noted.",
    "Concrete delivery delayed 2 hours.",
    "All crew completed toolbox safety talk.",
    "Structural steel inspection passed.",
    "Major milestone: topping out ceremony.",
    "Reduced crew - Colorado holiday.",
    "Accelerated schedule - critical path activity.",
    "Electrical panel room forms stripped and set.",
    "Project manager on site for monthly owner meeting.",
    "Material staging reorganized per logistics plan.",
    "Formwork stripped for north shear wall.",
    "Roofing membrane installation continues, 60% complete.",
    "Elevator shaft forming reached floor 12.",
    "Fire marshal inspection scheduled for tomorrow.",
    "Crane pick list approved for structural connections.",
]

random.seed(42)
manpower_logs = []

for p in PROJECTS:
    start = datetime.strptime(p["start_date"], "%Y-%m-%d").date()
    # Use full projected end date — active projects generate forecasted entries
    end = datetime.strptime(p["end_date"], "%Y-%m-%d").date()

    val = p["contract_value"]
    # Approximate typical headcount scale by contract value
    if val < 20000000:
        base_huv, base_sub = 5, 20
    elif val < 40000000:
        base_huv, base_sub = 8, 30
    elif val < 70000000:
        base_huv, base_sub = 12, 45
    elif val < 100000000:
        base_huv, base_sub = 18, 60
    else:
        base_huv, base_sub = 25, 80

    # Saturday work probability — larger projects run more Saturdays
    if val >= 100000000:
        sat_work_prob = 0.55
    elif val >= 50000000:
        sat_work_prob = 0.40
    else:
        sat_work_prob = 0.25

    total_days = max((end - start).days, 1)

    current = start
    while current <= end:
        is_weekday = current.weekday() < 5
        is_saturday = current.weekday() == 5
        if not (is_weekday or (is_saturday and random.random() < sat_work_prob)):
            current += timedelta(days=1)
            continue

        # Bell-curve headcount over project timeline
        elapsed_frac = (current - start).days / total_days
        if 0.15 <= elapsed_frac <= 0.75:
            hc_scale = random.uniform(0.90, 1.10)
        elif elapsed_frac < 0.15:
            hc_scale = random.uniform(0.30, 0.70)
        else:
            hc_scale = random.uniform(0.40, 0.75)

        if is_saturday:
            hc_scale *= 0.55

        huv_hc = max(2, int(base_huv * hc_scale * random.uniform(0.85, 1.15)))
        sub_hc = max(4, int(base_sub * hc_scale * random.uniform(0.85, 1.15)))
        total_hc = huv_hc + sub_hc

        huv_hrs = round(huv_hc * 8.0 * random.uniform(0.92, 1.05), 1)
        sub_hrs = round(sub_hc * 8.0 * random.uniform(0.92, 1.05), 1)
        total_hrs = round(huv_hrs + sub_hrs, 1)

        notes = random.choice(NOTES_POOL) if random.random() < 0.15 else None

        manpower_logs.append({
            "log_id": str(uuid.uuid4()),
            "project_id": p["project_id"],
            "log_date": str(current),
            "huvibar_headcount": huv_hc,
            "sub_headcount": sub_hc,
            "total_headcount": total_hc,
            "huvibar_hours": huv_hrs,
            "sub_hours": sub_hrs,
            "total_hours": total_hrs,
            "notes": notes,
        })

        current += timedelta(days=1)

pdf_mpl = pd.DataFrame(manpower_logs)
spark.createDataFrame(pdf_mpl).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.scheduling.daily_manpower_log")
df = spark.table(f"{catalog}.scheduling.daily_manpower_log")
print(f"Created {catalog}.scheduling.daily_manpower_log with {df.count()} rows")

# COMMAND ----------

print("All scheduling tables created successfully!")
