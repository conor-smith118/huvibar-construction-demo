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

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.safety_compliance")

# COMMAND ----------

# ============================================================
# TABLE: incidents  (~200 rows)
# ============================================================

def parse_date(d_str):
    return datetime.strptime(d_str, "%Y-%m-%d").date()

TODAY = date(2026, 8, 11)

INCIDENT_TIMES = [
    "06:15", "07:00", "07:30", "07:45", "08:00", "08:15", "08:30", "09:00",
    "09:30", "10:00", "10:30", "11:00", "11:30", "13:00", "13:30", "14:00",
    "14:30", "15:00", "15:30", "16:00",
]

INCIDENT_TYPES = [
    "near_miss", "near_miss", "near_miss", "near_miss", "near_miss",
    "near_miss", "near_miss", "near_miss",
    "struck_by", "struck_by",
    "fall", "fall",
    "overexertion", "overexertion",
    "caught_between",
    "electrical",
    "chemical",
    "property_damage", "property_damage",
]

SEVERITY_BY_TYPE = {
    "near_miss": ["near_miss"],
    "struck_by": ["first_aid", "first_aid", "first_aid", "recordable", "recordable", "lost_time", "restricted_duty"],
    "fall": ["first_aid", "first_aid", "recordable", "recordable", "lost_time", "lost_time", "restricted_duty"],
    "overexertion": ["first_aid", "first_aid", "first_aid", "recordable", "restricted_duty"],
    "caught_between": ["first_aid", "recordable", "lost_time", "restricted_duty"],
    "electrical": ["first_aid", "recordable", "recordable", "lost_time"],
    "chemical": ["first_aid", "first_aid", "recordable"],
    "property_damage": ["property_damage"],
}

BODY_PART_BY_TYPE = {
    "struck_by": ["head", "arm", "hand", "foot", "back", "eye"],
    "fall": ["back", "knee", "foot", "hand", "arm", "head"],
    "overexertion": ["back", "back", "back", "shoulder", "knee"],
    "caught_between": ["hand", "hand", "arm", "foot"],
    "electrical": ["hand", "arm", "eye"],
    "chemical": ["eye", "hand", "arm"],
    "near_miss": [None],
    "property_damage": [None],
}

INCIDENT_DESCRIPTIONS = {
    "struck_by": [
        "Employee was struck by falling wrench dropped by worker on upper level",
        "Worker was struck by swinging load during crane pick operation",
        "Employee contacted by steel reinforcing bar swung by adjacent worker",
        "Worker struck by door panel being carried by coworker on stairs",
        "Employee struck by forklift while in pedestrian zone",
        "Worker hit by concrete debris ejected from circular saw",
        "Employee struck on arm by dumpster lid during disposal operation",
    ],
    "fall": [
        "Employee slipped on wet concrete floor and fell to grade level",
        "Worker fell approximately 4 feet from scaffold platform",
        "Employee lost footing descending ladder and fell last two rungs",
        "Worker tripped over air hose and fell on concrete surface",
        "Employee fell into unprotected floor opening",
        "Worker lost balance on sloped roof and slid before self-arrest",
        "Employee stepped off elevated platform edge while backing up",
    ],
    "overexertion": [
        "Employee strained lower back while lifting concrete masonry unit",
        "Worker sustained shoulder strain while pulling wire through conduit",
        "Employee injured knee while carrying heavy toolbox up stairs",
        "Worker reported back pain after extended concrete screeding activity",
        "Employee strained wrist while using impact wrench in awkward position",
    ],
    "caught_between": [
        "Worker's fingers caught between steel beam and column flange during erection",
        "Employee's hand caught between concrete form and wall during stripping",
        "Worker's sleeve caught in drill bit causing arm contusion",
        "Employee's fingers pinched between precast panel and bearing pad",
    ],
    "electrical": [
        "Worker contacted energized 120V conductor while connecting temporary power",
        "Employee experienced minor shock from faulty power tool with damaged cord",
        "Worker contacted energized panel buss bar during installation",
        "Employee received minor shock from ungrounded equipment",
    ],
    "chemical": [
        "Employee splashed with concrete curing compound in eye area",
        "Worker exposed to epoxy resin fumes in enclosed space without adequate ventilation",
        "Employee contacted hydraulic fluid leak and sustained skin irritation",
    ],
    "near_miss": [
        "Scaffold plank fell from upper level, narrowly missed worker below",
        "Tool dropped from elevated work area, struck ground near worker",
        "Forklift backed toward worker who was outside operator's field of view",
        "Load on crane shifted unexpectedly during pick, workers in area cleared safely",
        "Worker nearly stepped into unprotected floor opening in low-light area",
        "Concrete truck reversed toward flagman before horn warning issued",
        "Electrical cord ran through puddle near workers; hazard identified before contact",
        "Unsecured material fell from elevated platform, cleared workers below",
        "Worker found operating power saw without blade guard installed",
        "Near-contact between crane swing radius and worker on adjacent scaffold",
        "Compressed air hose disconnect struck adjacent worker on glancing blow",
        "Worker nearly struck by steel decking sheet in high wind condition",
    ],
    "property_damage": [
        "Forklift struck and damaged finished drywall partition",
        "Concrete truck struck overhead door frame during site access",
        "Excavator bucket contacted and damaged underground utility",
        "Crane load contacted building facade during pick, causing minor spall",
        "Delivery truck damaged perimeter fence during off-hours delivery",
    ],
}

IMMEDIATE_CAUSES = [
    "Failure to maintain three points of contact on ladder",
    "Working within swing radius without spotter",
    "Inadequate housekeeping - debris in walkway",
    "Failure to use required PPE - safety glasses",
    "Improper manual lifting technique",
    "Inadequate barricading of floor opening",
    "Working near energized equipment without LOTO",
    "Tool not inspected before use",
    "Standing in load path of crane pick",
    "Working at height without fall protection attached",
    "Operating equipment without required spotter",
    "Entering confined space without atmospheric testing",
]

ROOT_CAUSES = [
    "Insufficient pre-task hazard analysis",
    "Inadequate supervisor oversight during critical operation",
    "Employee not trained on site-specific procedure",
    "Complacency after extended period without incident",
    "Time pressure leading to shortcut behavior",
    "Inadequate new employee orientation on site hazards",
    "PPE available but not enforced by crew leader",
    "Procedure exists but not consistently followed",
    "Environmental condition (wet surface, low light) not recognized",
    "Fatigue during late-shift work contributing to inattention",
]

CORRECTIVE_ACTIONS_SAFETY = [
    "Mandatory fall protection refresher training for all crew members",
    "Pre-task safety analysis required for all crane picks going forward",
    "Housekeeping inspection added to daily morning safety walkthrough",
    "PPE enforcement policy communicated to all subcontractors",
    "Manual lifting technique training conducted at next toolbox talk",
    "All floor openings to be barricaded and covered per OSHA 1926.502",
    "LOTO procedure updated and re-trained with affected crew",
    "Tool inspection checklist implemented for all power tools",
    "Exclusion zone established and marked for all crane operations",
    "100% tie-off enforcement initiated for all work above 6 feet",
    "Spotter requirement added to equipment operating procedures",
    "Confined space entry permit process reviewed and reinforced",
]

JOB_TITLES = [
    "Journeyman Carpenter", "Journeyman Ironworker", "Journeyman Electrician",
    "Journeyman Plumber", "Operating Engineer", "Laborer", "Laborer",
    "Concrete Finisher", "Ironworker Apprentice", "Carpenter Apprentice",
    "Foreman", "General Foreman", "Project Superintendent",
]

REPORTER_NAMES = [
    "Mark Simmons", "Susan Torres", "James Reilly", "Patricia Nguyen",
    "Kevin O'Brien", "Angela Washington", "David Kramer", "Brenda Silva",
    "Thomas Estes", "Rachel Chen",
]

random.seed(301)
incident_rows = []
incident_case_numbers = []  # list of dicts for OSHA recordables

# Distribute ~200 incidents across projects weighted by project size/duration
incident_counts = {}
for p in PROJECTS:
    start = parse_date(p["start_date"])
    end_effective = min(parse_date(p["end_date"]), TODAY)
    duration_years = max(0.1, (end_effective - start).days / 365)
    cv = float(p["contract_value"])
    base = int(cv / 5000000 * duration_years * 0.4)
    base = max(2, min(20, base))
    incident_counts[p["project_id"]] = base

total_base = sum(incident_counts.values())
scale = 200 / total_base
for pid in incident_counts:
    incident_counts[pid] = max(2, round(incident_counts[pid] * scale))

year_counters = {}

for p in PROJECTS:
    start = parse_date(p["start_date"])
    end_effective = min(parse_date(p["end_date"]), TODAY)
    project_duration_days = max(1, (end_effective - start).days)

    num_incidents = incident_counts[p["project_id"]]

    for i in range(num_incidents):
        incident_id = str(uuid.uuid4())

        offset = random.randint(0, project_duration_days)
        incident_date = start + timedelta(days=offset)
        if incident_date > TODAY:
            incident_date = TODAY - timedelta(days=random.randint(1, 30))

        incident_year = incident_date.year
        if incident_year not in year_counters:
            year_counters[incident_year] = 0
        year_counters[incident_year] += 1
        case_number = f"INC-{incident_year}-{year_counters[incident_year]:03d}"

        incident_time = random.choice(INCIDENT_TIMES)
        employee_id = f"EMP-{random.randint(1, 200):03d}"
        incident_type = random.choice(INCIDENT_TYPES)
        severity = random.choice(SEVERITY_BY_TYPE[incident_type])

        body_part = random.choice(BODY_PART_BY_TYPE[incident_type])

        description = random.choice(INCIDENT_DESCRIPTIONS[incident_type])
        immediate_cause = random.choice(IMMEDIATE_CAUSES)
        root_cause = random.choice(ROOT_CAUSES)
        corrective_action = random.choice(CORRECTIVE_ACTIONS_SAFETY)

        ca_due_days = random.randint(7, 30)
        ca_due_date = incident_date + timedelta(days=ca_due_days)

        if ca_due_date <= TODAY and random.random() < 0.85:
            ca_completed_date = ca_due_date - timedelta(days=random.randint(0, 5))
            ca_completed_date_str = ca_completed_date.strftime("%Y-%m-%d")
        else:
            ca_completed_date_str = None

        osha_recordable = severity in ("recordable", "lost_time", "restricted_duty")

        if severity == "lost_time":
            days_away = random.randint(1, 30)
            days_restricted = 0
        elif severity == "restricted_duty":
            days_away = 0
            days_restricted = random.randint(1, 20)
        else:
            days_away = 0
            days_restricted = 0

        reported_by = random.choice(REPORTER_NAMES)
        report_date = incident_date + timedelta(days=random.randint(0, 1))
        job_title = random.choice(JOB_TITLES)

        incident_rows.append({
            "incident_id": incident_id,
            "project_id": p["project_id"],
            "incident_date": incident_date.strftime("%Y-%m-%d"),
            "incident_time": incident_time,
            "employee_id": employee_id,
            "incident_type": incident_type,
            "severity": severity,
            "body_part_affected": body_part,
            "description": description,
            "immediate_cause": immediate_cause,
            "root_cause": root_cause,
            "corrective_action": corrective_action,
            "corrective_action_due_date": ca_due_date.strftime("%Y-%m-%d"),
            "corrective_action_completed_date": ca_completed_date_str,
            "osha_recordable": osha_recordable,
            "days_away_from_work": days_away,
            "days_on_restricted_duty": days_restricted,
            "reported_by": reported_by,
            "report_date": report_date.strftime("%Y-%m-%d"),
            "case_number": case_number,
        })

        if osha_recordable:
            incident_case_numbers.append({
                "case_number": case_number,
                "project_id": p["project_id"],
                "employee_id": employee_id,
                "incident_date": incident_date.strftime("%Y-%m-%d"),
                "incident_type": incident_type,
                "severity": severity,
                "job_title": job_title,
                "description": description,
                "days_away": days_away,
                "days_restricted": days_restricted,
                "incident_year": incident_year,
            })

inc_pdf = pd.DataFrame(incident_rows)
inc_df = spark.createDataFrame(inc_pdf)
inc_df.write.mode("overwrite").saveAsTable(f"{catalog}.safety_compliance.incidents")
df = spark.table(f"{catalog}.safety_compliance.incidents")
print(f"Created {catalog}.safety_compliance.incidents with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: osha_300_log  (~150 rows, only OSHA recordable incidents)
# ============================================================

INJURY_TYPES = {
    "struck_by": "injury",
    "fall": "injury",
    "overexertion": "injury",
    "caught_between": "injury",
    "electrical": "injury",
    "chemical": "illness",
}

OSHA_OUTCOMES = {
    "lost_time": "days_away",
    "restricted_duty": "restricted",
    "recordable": "other",
}

SENSITIVE_INJURY_TYPES = ["chemical", "electrical"]

random.seed(302)
osha_rows = []

for rec in incident_case_numbers:
    log_id = str(uuid.uuid4())
    incident_type = rec["incident_type"]
    severity = rec["severity"]

    injury_type = INJURY_TYPES.get(incident_type, "injury")
    outcome = OSHA_OUTCOMES.get(severity, "other")

    privacy_case = incident_type in SENSITIVE_INJURY_TYPES and random.random() < 0.4

    location_desc = f"Project {rec['project_id']} - active construction site"

    osha_rows.append({
        "log_id": log_id,
        "project_id": rec["project_id"],
        "case_number": rec["case_number"],
        "employee_id": rec["employee_id"],
        "job_title": rec["job_title"],
        "incident_date": rec["incident_date"],
        "location_description": location_desc,
        "incident_description": rec["description"],
        "injury_type": injury_type,
        "days_away": rec["days_away"],
        "days_restricted": rec["days_restricted"],
        "outcome": outcome,
        "privacy_case": privacy_case,
        "year": rec["incident_year"],
    })

osha_pdf = pd.DataFrame(osha_rows)
osha_df = spark.createDataFrame(osha_pdf)
osha_df.write.mode("overwrite").saveAsTable(f"{catalog}.safety_compliance.osha_300_log")
df = spark.table(f"{catalog}.safety_compliance.osha_300_log")
print(f"Created {catalog}.safety_compliance.osha_300_log with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: toolbox_talks  (~5,000 rows)
# ============================================================

TOOLBOX_TOPICS = [
    ("fall_protection", "Ladder Safety - Three Points of Contact"),
    ("fall_protection", "Scaffold Safety - Erection, Use, and Dismantling"),
    ("fall_protection", "Leading Edge Work and 100% Tie-Off Requirements"),
    ("fall_protection", "Personal Fall Arrest System Inspection and Use"),
    ("fall_protection", "Floor Opening and Hole Protection Requirements"),
    ("fall_protection", "Roof Work - Fall Hazards and Protection Methods"),
    ("electrical", "Lockout/Tagout Procedures for Electrical Hazards"),
    ("electrical", "Temporary Power and Ground Fault Circuit Interrupter Requirements"),
    ("electrical", "Arc Flash Hazards and PPE Selection"),
    ("electrical", "Working Near Overhead Power Lines - Safe Approach Distances"),
    ("electrical", "Extension Cord Inspection and Proper Use"),
    ("struck_by", "Crane and Rigging Safety - Exclusion Zones"),
    ("struck_by", "Flagging and Traffic Control Procedures"),
    ("struck_by", "Overhead Work - Tools and Materials Secured at Height"),
    ("struck_by", "Forklift Pedestrian Safety and Right of Way"),
    ("struck_by", "Hard Hat Requirements and Inspection"),
    ("heat_illness", "Heat Illness Prevention in Summer Months - Hydration and Rest"),
    ("heat_illness", "Recognizing Heat Exhaustion and Heat Stroke Symptoms"),
    ("heat_illness", "Shade and Water Requirements per Colorado Heat Standard"),
    ("PPE", "Eye and Face Protection - Selection and Use"),
    ("PPE", "Respiratory Protection - When Required and How to Use"),
    ("PPE", "Hand Protection - Glove Selection for Different Hazards"),
    ("PPE", "High-Visibility Clothing Requirements on Active Construction Sites"),
    ("PPE", "Foot Protection - Safety Boot Requirements and Inspection"),
    ("hazard_communication", "Understanding Safety Data Sheets and Chemical Labels"),
    ("hazard_communication", "Concrete Silica Dust - Engineering Controls and PPE"),
    ("hazard_communication", "Epoxy and Chemical Handling Safety Procedures"),
    ("hazard_communication", "Lead Paint Awareness in Renovation Work"),
    ("excavation", "Excavation and Trenching - Slope, Shore, and Shield Requirements"),
    ("excavation", "Competent Person Responsibilities for Excavation Work"),
    ("excavation", "Underground Utilities - Call 811 and Safe Digging Practices"),
    ("scaffolding", "Scaffold Inspection - Daily Checks Before Use"),
    ("scaffolding", "Plank Integrity and Guardrail Requirements"),
    ("scaffolding", "Suspended Scaffold Safety and Rigging Inspection"),
    ("crane_rigging", "Hand Signals for Crane Operations"),
    ("crane_rigging", "Sling Inspection and Load Rating Requirements"),
    ("crane_rigging", "Pre-Lift Meeting Requirements and Planning"),
    ("crane_rigging", "Rigging Hardware Inspection and Rejection Criteria"),
    ("emergency_procedures", "Site Emergency Action Plan and Muster Points"),
    ("emergency_procedures", "Fire Extinguisher Use - PASS Technique"),
    ("emergency_procedures", "First Aid Kit Locations and AED Availability"),
    ("emergency_procedures", "Severe Weather Procedures - Lightning and High Wind"),
    ("emergency_procedures", "Incident Reporting Requirements and Procedures"),
    ("fall_protection", "Stairway Safety During Construction - Handrails and Treads"),
    ("electrical", "Battery Storage Safety - Lithium Ion on Construction Sites"),
    ("struck_by", "Safe Backing Procedures and Spotters for Heavy Equipment"),
    ("heat_illness", "Cold Weather Safety - Frostbite and Hypothermia Prevention"),
    ("PPE", "Hearing Conservation - Noise Exposure and Hearing Protection"),
    ("hazard_communication", "Combustible Dust Hazards - Cutting and Grinding Control"),
    ("excavation", "Confined Space Awareness and Entry Permit Requirements"),
    ("crane_rigging", "Tagline Use and Load Control Procedures"),
]

PROJECT_SPECIFIC_HAZARDS_POOL = [
    "Active concrete pours in progress - slip hazard from wet concrete",
    "Steel erection in progress - overhead hazard zone in effect",
    "Crane operating on east side - exclusion zone posted",
    "Excavation open on north end of site - barricades in place",
    "Hot work permit required for welding operations today",
    "Roofing contractor active on Level 4 - no work below without hard hat area",
    "Temporary power installation underway - GFCI required for all tools",
    "Concrete cutting operations - silica controls in effect",
    "Scaffold inspection required before use on grid C elevations",
    "Delivery trucks expected between 7-9am - pedestrian caution at gate",
    "Manhole work in progress on south parking - confined space permits required",
    "Spray foam insulation crew working on floor 6 - ventilation required",
    "Curtain wall installation - glass handling zone on west elevation",
    "Electrical panel energization today - coordinate with superintendent",
    "Underground duct bank excavation - utility markings in place, hand dig required",
]

random.seed(303)
toolbox_rows = []

for p in PROJECTS:
    start = parse_date(p["start_date"])
    end_effective = min(parse_date(p["end_date"]), TODAY)
    project_duration_days = max(1, (end_effective - start).days)

    current_date = start
    while current_date <= end_effective:
        weekday = current_date.weekday()  # 0=Mon, 6=Sun

        talks_today = 0
        if weekday == 0:  # Monday - always have a talk
            talks_today = 1
        elif weekday in (2, 4):  # Wednesday, Friday - sometimes
            if random.random() < 0.60:
                talks_today = 1

        for _ in range(talks_today):
            talk_id = str(uuid.uuid4())
            topic_cat, topic_name = random.choice(TOOLBOX_TOPICS)

            presenter_id = f"EMP-{random.randint(1, 200):03d}"
            attendee_count = random.randint(5, 45)
            duration = random.choice([15, 15, 20, 20, 30])
            sign_in = random.random() < 0.95
            hazard = random.choice(PROJECT_SPECIFIC_HAZARDS_POOL)
            notes_options = [None, None, None,
                             "Translation provided in Spanish for non-English speakers",
                             "Written handout distributed to all attendees",
                             "Video demonstration used to supplement presentation",
                             "Inspector present and acknowledged safety briefing"]
            notes = random.choice(notes_options)

            toolbox_rows.append({
                "talk_id": talk_id,
                "project_id": p["project_id"],
                "talk_date": current_date.strftime("%Y-%m-%d"),
                "topic": topic_name,
                "topic_category": topic_cat,
                "presenter_employee_id": presenter_id,
                "attendee_count": attendee_count,
                "duration_minutes": duration,
                "sign_in_on_file": sign_in,
                "project_specific_hazards": hazard,
                "notes": notes,
            })

        current_date += timedelta(days=1)

tbt_pdf = pd.DataFrame(toolbox_rows)
tbt_df = spark.createDataFrame(tbt_pdf)
tbt_df.write.mode("overwrite").saveAsTable(f"{catalog}.safety_compliance.toolbox_talks")
df = spark.table(f"{catalog}.safety_compliance.toolbox_talks")
print(f"Created {catalog}.safety_compliance.toolbox_talks with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: safety_inspections  (~500 rows, ~20 per project)
# ============================================================

INSPECTOR_NAMES_SAFETY = [
    "Marcus Webb", "Diane Sullivan", "Carlos Ortega", "Jennifer Hayashi",
    "Robert Fitzpatrick", "Anita Kowalski", "Samuel Osei", "Laura Benning",
    "Gregory Chambers", "Yolanda Ruiz",
]

THIRD_PARTY_FIRMS = [
    "Triton Safety Consulting LLC",
    "Rocky Mountain Safety Group",
    "Front Range Risk Management Inc",
    "Colorado Safety Associates LLC",
]

random.seed(304)
safety_insp_rows = []

for p in PROJECTS:
    start = parse_date(p["start_date"])
    end_effective = min(parse_date(p["end_date"]), TODAY)
    project_duration_days = max(1, (end_effective - start).days)

    num_inspections = random.randint(16, 24)

    for i in range(num_inspections):
        insp_id = str(uuid.uuid4())

        frac = (i + random.uniform(0, 1)) / num_inspections
        offset_days = int(frac * project_duration_days)
        insp_date = start + timedelta(days=offset_days)
        if insp_date > TODAY:
            insp_date = TODAY - timedelta(days=random.randint(1, 14))

        inspector_type = random.choices(
            ["internal", "internal", "internal", "third_party", "owner"],
            weights=[40, 40, 40, 15, 5],
            k=1
        )[0]

        if inspector_type == "third_party":
            firm = random.choice(THIRD_PARTY_FIRMS)
            inspector_name = f"{random.choice(INSPECTOR_NAMES_SAFETY)} ({firm})"
        else:
            inspector_name = random.choice(INSPECTOR_NAMES_SAFETY)

        overall_score = max(60, min(100, int(random.gauss(85, 8))))
        fp_score = max(50, min(100, int(random.gauss(83, 10))))
        ppe_score = max(55, min(100, int(random.gauss(87, 8))))
        hk_score = max(55, min(100, int(random.gauss(82, 12))))
        equip_score = max(55, min(100, int(random.gauss(86, 9))))
        elec_score = max(55, min(100, int(random.gauss(85, 10))))

        total_obs = random.randint(10, 50)
        critical_count = 0 if overall_score > 75 else random.randint(0, 3)
        serious_count = 0 if overall_score > 70 else random.randint(0, 5)
        if overall_score < 80:
            serious_count = max(serious_count, random.randint(1, 3))
        minor_count = random.randint(0, min(15, total_obs // 2))

        follow_up_required = critical_count > 0 or serious_count > 0
        if follow_up_required:
            follow_up_days = random.randint(7, 14)
            follow_up_date = insp_date + timedelta(days=follow_up_days)
            if follow_up_date <= TODAY and random.random() < 0.80:
                closed_date = follow_up_date + timedelta(days=random.randint(0, 7))
                closed_date_str = closed_date.strftime("%Y-%m-%d") if closed_date <= TODAY else None
                status = "closed" if closed_date_str else "open"
            else:
                closed_date_str = None
                status = "open"
            follow_up_date_str = follow_up_date.strftime("%Y-%m-%d")
        else:
            follow_up_date_str = None
            closed_date_str = None
            status = "closed"

        safety_insp_rows.append({
            "inspection_id": insp_id,
            "project_id": p["project_id"],
            "inspection_date": insp_date.strftime("%Y-%m-%d"),
            "inspector_name": inspector_name,
            "inspector_type": inspector_type,
            "overall_score": overall_score,
            "fall_protection_score": fp_score,
            "ppe_compliance_score": ppe_score,
            "housekeeping_score": hk_score,
            "equipment_score": equip_score,
            "electrical_score": elec_score,
            "total_observations": total_obs,
            "critical_findings_count": critical_count,
            "serious_findings_count": serious_count,
            "minor_findings_count": minor_count,
            "follow_up_required": follow_up_required,
            "follow_up_date": follow_up_date_str,
            "closed_date": closed_date_str,
            "status": status,
        })

si_pdf = pd.DataFrame(safety_insp_rows)
si_df = spark.createDataFrame(si_pdf)
si_df.write.mode("overwrite").saveAsTable(f"{catalog}.safety_compliance.safety_inspections")
df = spark.table(f"{catalog}.safety_compliance.safety_inspections")
print(f"Created {catalog}.safety_compliance.safety_inspections with {df.count()} rows")

# COMMAND ----------

# ============================================================
# TABLE: certifications  (~2,000 rows)
# ============================================================

CERT_DEFINITIONS = [
    # (cert_type, issuing_org, validity_years, training_hours)
    ("OSHA_10_hour",                "OSHA",                            3,   10),
    ("OSHA_30_hour",                "OSHA",                            3,   30),
    ("First_Aid_CPR",               "American Red Cross",              2,   8),
    ("Competent_Person_Excavation", "OSHA",                            5,   16),
    ("Competent_Person_Scaffolding","OSHA",                            5,   16),
    ("Crane_Operator",              "NCCCO",                           5,   40),
    ("Forklift_Operator",           "Toyota Material Handling",        3,   8),
    ("Powder_Actuated_Tool",        "Hilti Inc",                       5,   8),
    ("Silica_Awareness",            "OSHA",                            3,   8),
    ("Lead_Awareness",              "EPA Lead Renovation Repair",      5,   8),
]

CERT_LOOKUP = {c[0]: c for c in CERT_DEFINITIONS}

ISSUE_YEAR_RANGE = list(range(2015, 2026))

random.seed(305)
cert_rows = []

all_cert_data = {}
for emp_num in range(1, 201):
    emp_id = f"EMP-{emp_num:03d}"
    all_cert_data[emp_id] = []

    # Everyone gets OSHA 10-hour
    all_cert_data[emp_id].append("OSHA_10_hour")

    # Foremen (1-60) get OSHA 30-hour + competencies + First Aid
    if emp_num <= 60:
        all_cert_data[emp_id].extend(["OSHA_30_hour", "First_Aid_CPR"])
        if random.random() < 0.60:
            all_cert_data[emp_id].append("Competent_Person_Excavation")
        if random.random() < 0.50:
            all_cert_data[emp_id].append("Competent_Person_Scaffolding")

    # Operators (61-100) get equipment certs
    if 61 <= emp_num <= 100:
        all_cert_data[emp_id].append("Crane_Operator")
        if random.random() < 0.70:
            all_cert_data[emp_id].append("Forklift_Operator")

    # Laborers and field (61-200) get silica + lead
    if emp_num >= 61:
        all_cert_data[emp_id].append("Silica_Awareness")
        if random.random() < 0.60:
            all_cert_data[emp_id].append("Lead_Awareness")

    # Random employees get powder actuated tool cert
    if random.random() < 0.40:
        all_cert_data[emp_id].append("Powder_Actuated_Tool")

    # Pad to ~10 certs per employee using additional safety certs
    # Use set difference to avoid infinite loop when pool is exhausted
    extra_cert_pool = ["OSHA_10_hour", "First_Aid_CPR", "Silica_Awareness",
                       "Lead_Awareness", "Forklift_Operator", "Powder_Actuated_Tool"]
    available = [c for c in extra_cert_pool if c not in all_cert_data[emp_id]]
    random.shuffle(available)
    for extra in available:
        if len(all_cert_data[emp_id]) >= 9:
            break
        all_cert_data[emp_id].append(extra)

for emp_num in range(1, 201):
    emp_id = f"EMP-{emp_num:03d}"
    certs = all_cert_data[emp_id]

    for cert_type in certs:
        cert_id = str(uuid.uuid4())

        cert_def = CERT_LOOKUP.get(cert_type)
        if cert_def is None:
            continue

        _, issuing_org, validity_years, training_hours = cert_def

        issue_year = random.choice(ISSUE_YEAR_RANGE)
        issue_month = random.randint(1, 12)
        issue_day = random.randint(1, 28)
        issued_date = date(issue_year, issue_month, issue_day)

        expiry_date = issued_date + timedelta(days=validity_years * 365)

        if expiry_date < TODAY:
            status = "expired"
        elif (expiry_date - TODAY).days < 90:
            status = "expiring_soon"
        else:
            status = "active"

        cert_number = f"CERT-{emp_num:04d}-{random.randint(100000, 999999)}"

        cert_rows.append({
            "cert_id": cert_id,
            "employee_id": emp_id,
            "cert_type": cert_type,
            "issuing_organization": issuing_org,
            "issued_date": issued_date.strftime("%Y-%m-%d"),
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "cert_number": cert_number,
            "status": status,
            "training_hours": training_hours,
        })

cert_pdf = pd.DataFrame(cert_rows)
cert_df = spark.createDataFrame(cert_pdf)
cert_df.write.mode("overwrite").saveAsTable(f"{catalog}.safety_compliance.certifications")
df = spark.table(f"{catalog}.safety_compliance.certifications")
print(f"Created {catalog}.safety_compliance.certifications with {df.count()} rows")
