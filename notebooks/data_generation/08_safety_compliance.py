# Databricks notebook source

# COMMAND ----------
dbutils.widgets.text("catalog", "css_genie")
catalog = dbutils.widgets.get("catalog")
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
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.safety_compliance")
print(f"Schema {catalog}.safety_compliance ready")

# COMMAND ----------
# Table: incidents (~200 rows across all projects)
INCIDENT_TYPES = ["struck_by", "fall", "caught_between", "overexertion", "electrical", "chemical", "near_miss", "property_damage"]
INCIDENT_TYPE_WEIGHTS = [20, 18, 12, 15, 8, 5, 15, 7]
SEVERITIES = ["first_aid", "recordable", "lost_time", "restricted_duty"]
SEVERITY_WEIGHTS = [60, 25, 10, 5]
BODY_PARTS = ["hand", "finger", "back", "knee", "eye", "shoulder", "foot", "ankle", "head", "wrist"]
INCIDENT_DESCRIPTIONS = {
    "struck_by": [
        "Worker struck by falling material from upper level",
        "Employee struck by swinging crane load",
        "Worker hit by forklift in travel aisle",
        "Struck by falling hand tool from scaffold above",
        "Employee struck by backing equipment",
    ],
    "fall": [
        "Worker fell from scaffolding at elevation",
        "Employee slipped on wet concrete surface",
        "Worker fell into floor opening - cover displaced",
        "Employee fell from ladder during descent",
        "Tripped over material on walking surface",
    ],
    "caught_between": [
        "Hand caught between steel connections during bolt-up",
        "Finger pinched between concrete formwork panels",
        "Employee caught between equipment and structure",
        "Hand caught in rotating equipment",
        "Foot caught in elevator pit landing",
    ],
    "overexertion": [
        "Lower back strain from lifting concrete block",
        "Shoulder strain during rebar placement",
        "Wrist sprain from repetitive hand tool use",
        "Back injury from awkward lifting position",
        "Knee strain from kneeling on concrete",
    ],
    "electrical": [
        "Contact with energized electrical panel",
        "Electric shock from improperly grounded tool",
        "Arc flash incident during panel work",
        "Contact with overhead power line (near miss)",
        "Shock from damaged extension cord",
    ],
    "chemical": [
        "Concrete burns from prolonged skin contact",
        "Eye irritation from epoxy fume exposure",
        "Skin irritation from sealant chemical contact",
        "Inhalation of silica dust - inadequate PPE",
        "Paint solvent exposure - skin contact",
    ],
    "near_miss": [
        "Unsecured load nearly fell from crane during pick",
        "Worker nearly struck by reversing dump truck",
        "Scaffold board nearly dislodged underfoot",
        "Flying debris from cut-off saw narrowly missed worker",
        "Trench wall showed signs of instability - evacuated",
    ],
    "property_damage": [
        "Crane boom contacted existing structure during swing",
        "Forklift damaged installed door frame",
        "Concrete truck damaged site fence during egress",
        "Excavator bucket contacted underground utility",
        "Flood damage to stored materials from rain event",
    ],
}
INJURED_BODY_PART_MAP = {
    "struck_by": ["head", "shoulder", "back", "knee", "foot"],
    "fall": ["back", "ankle", "knee", "wrist", "shoulder"],
    "caught_between": ["hand", "finger", "wrist"],
    "overexertion": ["back", "shoulder", "knee", "wrist"],
    "electrical": ["hand", "arm", "chest"],
    "chemical": ["eye", "hand", "skin"],
    "near_miss": [],
    "property_damage": [],
}

random.seed(42)
fake2 = Faker()
Faker.seed(42)
incidents = []
incident_id_counter = 1
emp_ids = [f"EMP-{str(j).zfill(4)}" for j in range(1, 151)]

for p in PROJECTS:
    start = parse_date(p["start_date"])
    end = min(parse_date(p["end_date"]), TODAY)
    total_days = max((end - start).days, 1)
    n_incidents = random.randint(6, 10)
    for i in range(n_incidents):
        incident_date = start + timedelta(days=random.randint(5, total_days))
        if incident_date > TODAY:
            incident_date = TODAY - timedelta(days=random.randint(1, 30))
        incident_type = random.choices(INCIDENT_TYPES, weights=INCIDENT_TYPE_WEIGHTS)[0]
        severity = random.choices(SEVERITIES, weights=SEVERITY_WEIGHTS)[0]
        osha_recordable = severity in ("recordable", "lost_time", "restricted_duty")
        if severity == "lost_time":
            days_away = random.randint(1, 30)
        else:
            days_away = 0
        if severity == "restricted_duty":
            days_restricted = random.randint(1, 14)
        else:
            days_restricted = 0
        body_parts = INJURED_BODY_PART_MAP.get(incident_type, [])
        injured_part = random.choice(body_parts) if body_parts else None
        description = random.choice(INCIDENT_DESCRIPTIONS.get(incident_type, ["Incident occurred on site"]))
        report_date = incident_date + timedelta(days=random.randint(0, 1))
        case_number = f"INC-{p['project_id']}-{str(i + 1).zfill(3)}"
        incidents.append({
            "incident_id": f"INC-{str(incident_id_counter).zfill(4)}",
            "project_id": p["project_id"],
            "case_number": case_number,
            "incident_date": incident_date,
            "incident_type": incident_type,
            "severity": severity,
            "description": description,
            "employee_id": random.choice(emp_ids),
            "employee_type": random.choice(["Huvibar", "Subcontractor"]),
            "body_part_injured": injured_part,
            "osha_recordable": osha_recordable,
            "days_away_from_work": days_away,
            "days_restricted": days_restricted,
            "report_date": report_date,
            "supervisor_employee_id": f"EMP-{str(random.randint(1, 20)).zfill(4)}",
            "investigation_complete": True if incident_date < TODAY - timedelta(days=14) else False,
            "corrective_action_taken": random.choice([
                "Toolbox talk conducted on topic", "Barricades and warning tape installed",
                "Employee retrained on PPE requirements", "Equipment inspected and repaired",
                "Housekeeping improved in affected area", "Procedure revised and re-communicated",
                "Additional supervision assigned to crew", "Near miss report filed and reviewed at safety meeting",
            ]),
        })
        incident_id_counter += 1

pdf_inc = pd.DataFrame(incidents)
for col in ["incident_date", "report_date"]:
    pdf_inc[col] = pd.to_datetime(pdf_inc[col])
spark.createDataFrame(pdf_inc).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.safety_compliance.incidents")
print(f"incidents: {len(incidents)} rows")

# COMMAND ----------
# Table: osha_300_log (~150 rows, recordable only)
INJURY_TYPES = ["injury", "illness"]
INJURY_WEIGHTS = [90, 10]

recordable_incidents = [inc for inc in incidents if inc["osha_recordable"]]
osha_300_log = []
log_id_counter = 1
for inc in recordable_incidents:
    inc_date = inc["incident_date"]
    if hasattr(inc_date, "date"):
        inc_date = inc_date.date()
    elif isinstance(inc_date, str):
        inc_date = datetime.strptime(inc_date, "%Y-%m-%d").date()
    year = inc_date.year
    osha_300_log.append({
        "log_id": f"O300-{str(log_id_counter).zfill(4)}",
        "project_id": inc["project_id"],
        "case_number": inc["case_number"],
        "employee_id": inc["employee_id"],
        "job_title": random.choice(["Carpenter", "Ironworker", "Laborer", "Electrician", "Plumber", "Cement Mason", "Operating Engineer", "Foreman"]),
        "incident_date": inc["incident_date"],
        "location_description": f"Project {inc['project_id']} - Active construction site",
        "incident_description": inc["description"],
        "injury_type": random.choices(INJURY_TYPES, weights=INJURY_WEIGHTS)[0],
        "days_away": inc["days_away_from_work"],
        "days_restricted": inc["days_restricted"],
        "outcome": "days_away" if inc["days_away_from_work"] > 0 else (
            "days_restricted" if inc["days_restricted"] > 0 else "recordable_no_days"
        ),
        "privacy_case": False,
        "year": year,
    })
    log_id_counter += 1

pdf_osha = pd.DataFrame(osha_300_log)
pdf_osha["incident_date"] = pd.to_datetime(pdf_osha["incident_date"])
spark.createDataFrame(pdf_osha).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.safety_compliance.osha_300_log")
print(f"osha_300_log: {len(osha_300_log)} rows")

# COMMAND ----------
# Table: toolbox_talks (~5K rows, ~200 per project)
TBT_TOPICS = [
    "Fall Protection - Proper Use of Harness and Lanyard",
    "Electrical Safety - Lockout/Tagout Procedures",
    "Struck-By Hazards - Maintaining Safe Distances from Equipment",
    "Heat Illness Prevention - Hydration and Rest Breaks",
    "Personal Protective Equipment - Proper Selection and Use",
    "Hazard Communication - Reading Safety Data Sheets (SDS)",
    "Excavation Safety - Trench Safety and Soil Classification",
    "Scaffolding Safety - Erection, Use, and Inspection",
    "Crane and Rigging Safety - Load Capacity and Signaling",
    "Emergency Procedures - Evacuation and First Aid Response",
    "Silica Dust Control - Wet Methods and Respiratory Protection",
    "Hand and Power Tool Safety - Guards and Proper Use",
    "Ladder Safety - Selection, Inspection, and 3-Point Contact",
    "Concrete Burns - Protective Clothing and Decontamination",
    "Fire Prevention - Housekeeping and Hot Work Permits",
    "Forklift Safety - Pedestrian Awareness and Load Handling",
    "Slips, Trips, and Falls - Housekeeping and Walking Surfaces",
    "Working at Heights - Hole Covers and Guardrails",
    "Back Injury Prevention - Proper Lifting Techniques",
    "Drug and Alcohol Free Workplace Policy",
]
PRESENTER_IDS = [f"EMP-{str(j).zfill(4)}" for j in range(1, 21)]  # Superintendents and foremen

random.seed(42)
toolbox_talks = []
tbt_id_counter = 1
for p in PROJECTS:
    start = parse_date(p["start_date"])
    end = min(parse_date(p["end_date"]), TODAY)
    n_talks = random.randint(180, 220)
    # Spread talks over weekdays within project duration
    total_days = max((end - start).days, 1)
    for i in range(n_talks):
        talk_date = start + timedelta(days=random.randint(0, total_days))
        if talk_date > TODAY:
            talk_date = TODAY
        # Ensure it's a weekday
        while talk_date.weekday() >= 5:
            talk_date -= timedelta(days=1)
        topic = TBT_TOPICS[i % len(TBT_TOPICS)]
        toolbox_talks.append({
            "talk_id": f"TBT-{str(tbt_id_counter).zfill(6)}",
            "project_id": p["project_id"],
            "talk_date": talk_date,
            "topic": topic,
            "presenter_employee_id": random.choice(PRESENTER_IDS),
            "attendee_count": random.randint(5, 40),
            "duration_minutes": random.randint(10, 20),
            "location_on_site": random.choice(["Job Site Office", "Lay Down Area", "Level 1 Work Area", "Parking Lot", "Gang Box Area"]),
            "notes": "" if random.random() < 0.8 else "Additional discussion on recent incident or near miss",
        })
        tbt_id_counter += 1

pdf_tbt = pd.DataFrame(toolbox_talks)
pdf_tbt["talk_date"] = pd.to_datetime(pdf_tbt["talk_date"])
spark.createDataFrame(pdf_tbt).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.safety_compliance.toolbox_talks")
print(f"toolbox_talks: {len(toolbox_talks)} rows")

# COMMAND ----------
# Table: safety_inspections (~500 rows, ~20 per project)
INSPECTION_CATEGORIES = [
    "General Site Conditions", "Fall Protection", "Electrical Safety", "Fire Prevention",
    "PPE Compliance", "Housekeeping", "Equipment Condition", "Hazard Communication",
    "Excavation/Trenching", "Scaffolding",
]
INSPECTORS_SAFETY = [
    "Huvibar Safety Manager", "Owner Safety Representative", "OSHA Compliance Officer",
    "Third-Party Safety Consultant", "Project Safety Officer",
]

random.seed(42)
safety_inspections = []
si_id_counter = 1
for p in PROJECTS:
    start = parse_date(p["start_date"])
    end = min(parse_date(p["end_date"]), TODAY)
    total_days = max((end - start).days, 1)
    n_inspections = random.randint(16, 24)
    for i in range(n_inspections):
        insp_date = start + timedelta(days=random.randint(7, total_days))
        if insp_date > TODAY:
            insp_date = TODAY - timedelta(days=random.randint(1, 60))
        overall_score = random.randint(70, 100)
        # Generate 8-10 category scores
        category_scores = {}
        for cat in random.sample(INSPECTION_CATEGORIES, 8):
            # Scores tend to cluster around overall_score
            cat_score = max(50, min(100, overall_score + random.randint(-15, 15)))
            category_scores[cat] = cat_score

        n_violations = 0 if overall_score >= 90 else random.randint(1, 4)
        n_observations = random.randint(0, 5)
        violations_list = []
        VIOLATION_DESCRIPTIONS = [
            "Unsecured floor opening without cover or guardrail",
            "Worker observed without hard hat in hard hat zone",
            "Extension cord damaged - outer jacket cut",
            "Fall protection not in use at leading edge",
            "Temporary electrical panel not properly guarded",
            "Combustibles stored within 10 feet of hot work area",
            "Scaffold not properly tagged or inspected",
            "Chemical container not labeled",
            "Ladder extends less than 3 feet above landing",
            "Concrete saw used without respiratory protection",
        ]
        for v in range(n_violations):
            violations_list.append(random.choice(VIOLATION_DESCRIPTIONS))

        safety_inspections.append({
            "inspection_id": f"SI-{str(si_id_counter).zfill(4)}",
            "project_id": p["project_id"],
            "inspection_date": insp_date,
            "inspector_name": random.choice(INSPECTORS_SAFETY),
            "inspection_type": random.choice(["routine", "scheduled", "follow-up", "pre-task"]),
            "overall_score": overall_score,
            "fall_protection_score": category_scores.get("Fall Protection", overall_score),
            "electrical_safety_score": category_scores.get("Electrical Safety", overall_score),
            "ppe_compliance_score": category_scores.get("PPE Compliance", overall_score),
            "housekeeping_score": category_scores.get("Housekeeping", overall_score),
            "equipment_condition_score": category_scores.get("Equipment Condition", overall_score),
            "num_violations": n_violations,
            "num_observations": n_observations,
            "violations_noted": "; ".join(violations_list) if violations_list else None,
            "follow_up_required": n_violations > 0,
            "follow_up_date": insp_date + timedelta(days=7) if n_violations > 0 else None,
            "follow_up_complete": True if n_violations > 0 and (insp_date + timedelta(days=7)) < TODAY else False,
        })
        si_id_counter += 1

pdf_si = pd.DataFrame(safety_inspections)
pdf_si["inspection_date"] = pd.to_datetime(pdf_si["inspection_date"])
pdf_si["follow_up_date"] = pd.to_datetime(pdf_si["follow_up_date"])
spark.createDataFrame(pdf_si).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.safety_compliance.safety_inspections")
print(f"safety_inspections: {len(safety_inspections)} rows")

# COMMAND ----------
# Table: certifications (~2K rows, ~10 per employee for a sample of 200 employees)
CERT_TYPES = [
    "OSHA_30_hour", "OSHA_10_hour", "First_Aid_CPR", "Competent_Person_Excavation",
    "Forklift_Operator", "Crane_Operator", "Silica_Awareness", "Fall_Protection_Competent_Person",
    "Scaffold_Competent_Person", "Rigging_Inspector",
]
CERT_ISSUERS = {
    "OSHA_30_hour": "OSHA Outreach Training Program",
    "OSHA_10_hour": "OSHA Outreach Training Program",
    "First_Aid_CPR": "American Red Cross",
    "Competent_Person_Excavation": "Associated Builders & Contractors",
    "Forklift_Operator": "Toyota Material Handling",
    "Crane_Operator": "National Commission for Certification of Crane Operators (NCCCO)",
    "Silica_Awareness": "Huvibar Construction Internal",
    "Fall_Protection_Competent_Person": "Capital Safety Training",
    "Scaffold_Competent_Person": "Scaffold & Access Industry Association",
    "Rigging_Inspector": "Crosby Group Certified Training",
}
CERT_VALIDITY_YEARS = {
    "OSHA_30_hour": 5, "OSHA_10_hour": 5, "First_Aid_CPR": 2,
    "Competent_Person_Excavation": 3, "Forklift_Operator": 3,
    "Crane_Operator": 5, "Silica_Awareness": 1,
    "Fall_Protection_Competent_Person": 3, "Scaffold_Competent_Person": 3,
    "Rigging_Inspector": 3,
}

random.seed(42)
certifications = []
cert_id_counter = 1

for emp_num in range(1, 201):
    emp_id = f"EMP-{str(emp_num).zfill(4)}"
    # Field employees (1-120) get more certifications; office (121-200) get fewer
    if emp_num <= 120:
        n_certs = random.randint(2, 5)
        eligible_certs = CERT_TYPES
    elif emp_num <= 170:
        n_certs = random.randint(1, 3)
        eligible_certs = ["OSHA_10_hour", "First_Aid_CPR", "OSHA_30_hour"]
    else:
        n_certs = random.randint(1, 2)
        eligible_certs = ["OSHA_30_hour", "First_Aid_CPR"]

    cert_types_for_emp = random.sample(eligible_certs, min(n_certs, len(eligible_certs)))
    for cert_type in cert_types_for_emp:
        validity_years = CERT_VALIDITY_YEARS[cert_type]
        # Issue date somewhere in past 1-10 years
        days_since_issue = random.randint(30, 3650)
        issue_date = TODAY - timedelta(days=days_since_issue)
        expiry_date = issue_date + timedelta(days=365 * validity_years)

        if expiry_date < TODAY - timedelta(days=30):
            status = "expired"
        elif expiry_date < TODAY + timedelta(days=60):
            status = "expiring_soon"
        else:
            status = "active"

        # 15% expired, 10% expiring soon - achieved naturally by random issue dates
        certifications.append({
            "cert_id": f"CERT-{str(cert_id_counter).zfill(5)}",
            "employee_id": emp_id,
            "cert_type": cert_type,
            "cert_number": f"{cert_type[:4].upper()}-{random.randint(100000, 999999)}",
            "issuing_organization": CERT_ISSUERS[cert_type],
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "status": status,
            "renewal_required": status in ("expired", "expiring_soon"),
        })
        cert_id_counter += 1

pdf_cert = pd.DataFrame(certifications)
pdf_cert["issue_date"] = pd.to_datetime(pdf_cert["issue_date"])
pdf_cert["expiry_date"] = pd.to_datetime(pdf_cert["expiry_date"])
spark.createDataFrame(pdf_cert).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.safety_compliance.certifications")
print(f"certifications: {len(certifications)} rows")

# COMMAND ----------
print("All safety_compliance tables created successfully!")
print(f"  - incidents: {len(incidents)} rows")
print(f"  - osha_300_log: {len(osha_300_log)} rows")
print(f"  - toolbox_talks: {len(toolbox_talks)} rows")
print(f"  - safety_inspections: {len(safety_inspections)} rows")
print(f"  - certifications: {len(certifications)} rows")
