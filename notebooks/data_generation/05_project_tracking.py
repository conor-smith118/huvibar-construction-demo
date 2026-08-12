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

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.project_tracking")

# COMMAND ----------
# ==============================================================================
# TABLE 1: milestones (~200 rows — 8 per project)
# ==============================================================================

MILESTONE_NAMES = [
    "NTP/Mobilization",
    "Foundation_Complete",
    "Structural_Steel_Complete",
    "MEP_Rough-in_Complete",
    "Substantial_Completion",
    "Final_Completion",
    "Punch_List_Complete",
    "Certificate_of_Occupancy",
]

ARCHITECT_FIRMS = [
    "Gensler Denver", "HKS Architects", "Populous", "RNL Design",
    "Davis Partnership Architects", "Tryba Architects", "Anderson Mason Dale",
    "OZ Architecture", "Klipp Architecture",
]

milestone_rows = []
today = datetime.date(2026, 8, 11)

for proj in PROJECTS:
    pid = proj["project_id"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    is_complete = proj["status"] == "completed"
    is_closeout = proj["status"] == "closeout"
    duration_days = (end - start).days
    architect = random.choice(ARCHITECT_FIRMS)

    # Space milestones evenly across project duration
    milestone_offsets_pct = [0.0, 0.10, 0.25, 0.50, 0.80, 0.88, 0.94, 1.0]

    for i, (name, pct) in enumerate(zip(MILESTONE_NAMES, milestone_offsets_pct)):
        planned_date = start + datetime.timedelta(days=int(duration_days * pct))
        planned_date = planned_date if planned_date.weekday() < 5 else planned_date + datetime.timedelta(days=(7 - planned_date.weekday()))

        # Determine actual date and status
        variance_days = random.randint(-14, 21)
        effective_end = min(end, today)

        if is_complete:
            actual_date = planned_date + datetime.timedelta(days=variance_days)
            days_variance = variance_days
            status = "complete"
            responsible = "Huvibar Construction" if i % 2 == 0 else architect
        elif is_closeout:
            # Last 2 milestones may be pending
            if i < 6:
                actual_date = planned_date + datetime.timedelta(days=variance_days)
                days_variance = variance_days
                status = "complete"
            else:
                actual_date = None
                days_variance = None
                status = "pending"
            responsible = "Huvibar Construction" if i % 2 == 0 else architect
        else:
            # Active project: milestones before today may be complete
            if planned_date <= today and planned_date <= effective_end:
                actual_date = planned_date + datetime.timedelta(days=variance_days)
                days_variance = variance_days
                status = "complete" if actual_date <= today else "pending"
            elif planned_date > today:
                actual_date = None
                days_variance = None
                # Determine if at_risk
                if random.random() < 0.2:
                    status = "at_risk"
                else:
                    status = "pending"
            else:
                actual_date = None
                days_variance = None
                status = "pending"
            responsible = "Huvibar Construction" if i % 2 == 0 else architect

        milestone_rows.append({
            "milestone_id": str(uuid.uuid4()),
            "project_id": pid,
            "milestone_name": name,
            "planned_date": planned_date.isoformat(),
            "actual_date": actual_date.isoformat() if actual_date else None,
            "days_variance": days_variance,
            "status": status,
            "responsible_party": responsible,
        })

milestone_pdf = pd.DataFrame(milestone_rows)
milestone_sdf = spark.createDataFrame(milestone_pdf)
milestone_sdf.write.mode("overwrite").saveAsTable(f"{catalog}.project_tracking.milestones")
df = spark.table(f"{catalog}.project_tracking.milestones")
print(f"Created {catalog}.project_tracking.milestones with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 2: rfis (~1,500 rows — ~60 per project)
# ==============================================================================

RFI_TITLES = [
    "Clarification on concrete mix design for foundation walls",
    "Structural steel connection detail at column line 7",
    "MEP coordination conflict at level 4 ceiling plenum",
    "Waterproofing membrane specification clarification",
    "Door hardware schedule discrepancy - Series A",
    "Electrical panel location conflict with structural beam",
    "HVAC duct routing through shear wall opening",
    "Curtain wall attachment detail at floor slab",
    "Plumbing penetration sleeve requirements - slab on grade",
    "Fire suppression head placement in storage room",
    "Exterior insulation thickness at window head condition",
    "Rebar lap splice length at wall to footing",
    "Stair nosing material specification",
    "Roof drain overflow scupper location",
    "Elevator pit waterproofing detail",
    "Expansion joint location at building addition interface",
    "Concrete slab thickening requirement at loading dock",
    "Window flashing detail at masonry opening",
    "Toilet room floor slope to drain",
    "Mechanical room clearance requirement",
    "Exterior paving joint spacing at entry plaza",
    "Fire-rated assembly substitution request",
    "Embedded anchor plate location for canopy",
    "Ceiling grid suspension detail at high bay",
    "Generator exhaust routing clarification",
    "Standpipe hose cabinet location - stairwell B",
    "Tack welding requirement at metal deck",
    "Suspended ceiling height conflict - corridor level 2",
    "Site lighting photometrics clarification",
    "Underground conduit routing around existing utilities",
]

QUESTION_SUMMARIES = [
    "Drawings show conflicting information. Please clarify which detail governs.",
    "Specification section and drawing note are inconsistent. Requesting clarification.",
    "Coordination issue identified during BIM review. Multiple trades affected.",
    "Field condition differs from design assumption. Please advise on resolution.",
    "Missing detail on drawings. Requesting design team to provide.",
    "Material substitution proposed due to lead time. Awaiting approval.",
    "Contractor proposes alternate installation method. Please confirm acceptability.",
    "Code compliance question. Requesting interpretation from design team.",
]

ANSWER_SUMMARIES = [
    "See attached sketch SK-047. Proceed per updated detail.",
    "Specification governs. Disregard drawing note. Confirm with superintendent.",
    "Revised drawing issued via ASI-12. Coordinate with all affected trades.",
    "Field condition accepted. Proceed per contractor's proposed resolution.",
    "Detail provided via attached sketch. No cost impact.",
    "Substitution approved as noted. Update submittal log.",
    "Alternate method approved. Document in daily reports.",
    "Confirmed compliant per 2021 IBC Section 1004. Proceed as designed.",
]

DISCIPLINES = ["architectural", "structural", "mechanical", "electrical", "plumbing", "civil"]
BIC_OPTIONS = ["architect", "engineer", "owner", "GC"]

rfi_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    effective_end = min(end, today)
    duration_days = max((effective_end - start).days, 30)
    is_complete = proj["status"] in ("completed", "closeout")

    n_rfis = random.randint(50, 70)
    rfi_counter = 1

    for _ in range(n_rfis):
        submit_days = random.randint(14, duration_days - 5)
        submitted_date = start + datetime.timedelta(days=submit_days)
        due_days = random.randint(10, 14)
        due_date = submitted_date + datetime.timedelta(days=due_days)

        if is_complete:
            status = random.choices(["answered", "closed", "void"], weights=[10, 85, 5])[0]
        else:
            if submitted_date > today - datetime.timedelta(days=14):
                status = random.choices(["open", "answered"], weights=[70, 30])[0]
            else:
                status = random.choices(["open", "answered", "closed"], weights=[20, 30, 50])[0]

        answered_date = None
        answer_text = None
        if status in ("answered", "closed"):
            days_to_answer = random.randint(5, 21)
            answered_date = (submitted_date + datetime.timedelta(days=days_to_answer)).isoformat()
            answer_text = random.choice(ANSWER_SUMMARIES)

        days_open = (today - submitted_date).days if status == "open" else (
            (datetime.date.fromisoformat(answered_date) - submitted_date).days if answered_date else 0
        )

        emp_num = random.randint(1, 200)
        rfi_rows.append({
            "rfi_id": str(uuid.uuid4()),
            "project_id": pid,
            "rfi_number": f"RFI-{rfi_counter:03d}",
            "title": random.choice(RFI_TITLES),
            "submitted_by_employee_id": f"EMP-{emp_num:03d}",
            "submitted_date": submitted_date.isoformat(),
            "due_date": due_date.isoformat(),
            "answered_date": answered_date,
            "discipline": random.choice(DISCIPLINES),
            "question_summary": random.choice(QUESTION_SUMMARIES),
            "answer_summary": answer_text,
            "days_open": days_open,
            "status": status,
            "ball_in_court": "GC" if status == "open" else random.choice(BIC_OPTIONS),
        })
        rfi_counter += 1

rfi_pdf = pd.DataFrame(rfi_rows)
rfi_sdf = spark.createDataFrame(rfi_pdf)
rfi_sdf.write.mode("overwrite").saveAsTable(f"{catalog}.project_tracking.rfis")
df = spark.table(f"{catalog}.project_tracking.rfis")
print(f"Created {catalog}.project_tracking.rfis with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 3: submittals (~2,000 rows — ~80 per project)
# ==============================================================================

SPEC_SECTIONS = [
    "03300", "03410", "05120", "05210", "05310", "05400", "05500",
    "07110", "07210", "07411", "07533", "07900",
    "08111", "08311", "08411", "08520", "08711", "08810",
    "09250", "09310", "09511", "09651", "09900",
    "10155", "10440", "10810",
    "14210", "14420",
    "21130", "22110", "22300", "22400",
    "23050", "23100", "23200",
    "26110", "26200", "26510",
    "27100", "27500", "28100", "28200",
    "31100", "31200", "32110", "32310", "32900",
    "33100", "33300", "33400",
]

SUBMITTAL_DESCS = [
    "Concrete mix design - 4000 PSI structural",
    "Structural steel shop drawings - grid lines A-F",
    "Metal deck shop drawings - levels 2-6",
    "Cold-formed framing layout drawings",
    "Waterproofing system product data",
    "Roofing membrane system - TPO 60 mil",
    "Curtain wall shop drawings - west facade",
    "Storefront system product data and installation",
    "Hollow metal doors and frames schedule",
    "Hardware sets 1-24 product data",
    "Glazing system - IGU specifications",
    "Gypsum board assemblies - UL ratings",
    "Ceramic tile - floor and wall",
    "Suspended acoustical tile ceiling",
    "VCT flooring - colors and installation",
    "Paint system - interior and exterior",
    "Toilet accessories schedule",
    "Elevator cab design and equipment",
    "Automatic sprinkler head data",
    "Plumbing fixtures schedule",
    "HVAC equipment - air handling units",
    "Electrical distribution panel schedules",
    "LED lighting fixture schedule",
    "Fire alarm devices and system",
    "Access control hardware",
    "Structural steel anchor bolt layout",
    "Reinforcing steel bar bending schedule",
    "Precast panel shop drawings",
    "Seismic bracing calculations",
    "Site concrete paving mix design",
]

SUBMITTAL_TYPES = ["shop_drawing", "product_data", "sample", "closeout"]
STATUS_OPTIONS = ["pending", "approved", "approved_as_noted", "revise_resubmit", "rejected", "void"]

SUBCONTRACTOR_NAMES = [
    "Alpine Mechanical LLC", "Front Range Electrical Co", "Rocky Mountain Concrete Inc",
    "Centennial Steel Erectors", "High Plains Drywall", "Colorado Plumbing Group",
    "Summit Roofing Systems", "Pikes Peak Glazing", "Mile High Fire Protection",
    "Foothills Earthworks", "Gateway Masonry Inc", "Colorado Elevator Service",
    "Denver Tile & Stone", "Boulder Painting Co", "Northern Colorado HVAC",
]

ARCHITECT_FIRMS = [
    "Gensler Denver", "HKS Architects", "Populous", "RNL Design",
    "Davis Partnership Architects", "Tryba Architects", "Anderson Mason Dale",
    "OZ Architecture", "Klipp Architecture",
]

submittal_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    effective_end = min(end, today)
    duration_days = max((effective_end - start).days, 30)
    is_complete = proj["status"] in ("completed", "closeout")
    architect = random.choice(ARCHITECT_FIRMS)

    n_submittals = random.randint(70, 90)
    sub_counter = 1

    for _ in range(n_submittals):
        submit_days = random.randint(7, min(duration_days - 10, duration_days))
        submitted_date = start + datetime.timedelta(days=submit_days)
        required_date = submitted_date + datetime.timedelta(days=random.randint(14, 21))

        if is_complete:
            status = random.choices(
                ["approved", "approved_as_noted", "revise_resubmit", "void"],
                weights=[55, 30, 10, 5]
            )[0]
        else:
            if submitted_date > today - datetime.timedelta(days=21):
                status = random.choices(["pending", "approved", "approved_as_noted"], weights=[60, 25, 15])[0]
            else:
                status = random.choices(
                    ["approved", "approved_as_noted", "revise_resubmit", "pending", "void"],
                    weights=[45, 30, 15, 8, 2]
                )[0]

        returned_date = None
        if status in ("approved", "approved_as_noted", "revise_resubmit", "rejected"):
            review_days = random.randint(7, 21)
            returned_date = (submitted_date + datetime.timedelta(days=review_days)).isoformat()

        revision_num = 0
        if status == "revise_resubmit":
            revision_num = 1
        elif status == "approved_as_noted" and random.random() < 0.3:
            revision_num = 1

        spec = random.choice(SPEC_SECTIONS)
        sub_type = random.choices(
            SUBMITTAL_TYPES,
            weights=[40, 40, 10, 10]
        )[0]

        submittal_rows.append({
            "submittal_id": str(uuid.uuid4()),
            "project_id": pid,
            "submittal_number": f"SUB-{sub_counter:03d}",
            "spec_section": spec,
            "description": random.choice(SUBMITTAL_DESCS),
            "submittal_type": sub_type,
            "submitted_date": submitted_date.isoformat(),
            "required_date": required_date.isoformat(),
            "returned_date": returned_date,
            "revision_number": revision_num,
            "status": status,
            "submitted_by": random.choice(SUBCONTRACTOR_NAMES),
            "reviewed_by": architect,
        })
        sub_counter += 1

submittal_pdf = pd.DataFrame(submittal_rows)
submittal_sdf = spark.createDataFrame(submittal_pdf)
submittal_sdf.write.mode("overwrite").saveAsTable(f"{catalog}.project_tracking.submittals")
df = spark.table(f"{catalog}.project_tracking.submittals")
print(f"Created {catalog}.project_tracking.submittals with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 4: daily_reports (~15,000 rows)
# ==============================================================================

WEATHER_BY_MONTH = {
    1:  {"conditions": ["sunny", "cloudy", "snow", "windy"], "weights": [25, 30, 30, 15], "high_range": (28, 48), "low_range": (10, 28)},
    2:  {"conditions": ["sunny", "cloudy", "snow", "windy"], "weights": [30, 28, 28, 14], "high_range": (33, 52), "low_range": (14, 32)},
    3:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "snow", "rain"], "weights": [25, 25, 20, 15, 15], "high_range": (42, 60), "low_range": (22, 38)},
    4:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "rain", "snow"], "weights": [30, 28, 20, 15, 7], "high_range": (52, 68), "low_range": (32, 46)},
    5:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "rain"], "weights": [35, 30, 20, 15], "high_range": (62, 76), "low_range": (42, 54)},
    6:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "rain"], "weights": [45, 30, 15, 10], "high_range": (72, 90), "low_range": (50, 62)},
    7:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "rain"], "weights": [45, 28, 15, 12], "high_range": (80, 95), "low_range": (58, 68)},
    8:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "rain"], "weights": [45, 28, 15, 12], "high_range": (78, 93), "low_range": (56, 66)},
    9:  {"conditions": ["sunny", "partly_cloudy", "cloudy", "rain", "snow"], "weights": [38, 28, 18, 10, 6], "high_range": (66, 82), "low_range": (44, 56)},
    10: {"conditions": ["sunny", "partly_cloudy", "cloudy", "snow", "rain"], "weights": [38, 28, 18, 10, 6], "high_range": (52, 68), "low_range": (30, 44)},
    11: {"conditions": ["sunny", "cloudy", "snow", "windy"], "weights": [30, 30, 25, 15], "high_range": (38, 55), "low_range": (18, 34)},
    12: {"conditions": ["sunny", "cloudy", "snow", "windy"], "weights": [25, 30, 30, 15], "high_range": (30, 48), "low_range": (12, 28)},
}

WORK_SUMMARIES = [
    "Concrete pour - mat foundation grid A-D",
    "Structural steel erection - levels 3-4",
    "Formwork installation - shear walls",
    "Rebar placement - elevated deck level 5",
    "MEP rough-in - levels 2-3 east wing",
    "Drywall installation - interior partitions level 6",
    "Roofing membrane installation - phase 2",
    "Site utilities - storm sewer installation",
    "Masonry work - exterior veneer north facade",
    "Window installation - levels 7-9",
    "Concrete deck pour - level 8",
    "Steel decking installation - level 9",
    "HVAC equipment installation - penthouse",
    "Electrical rough-in - levels 4-5",
    "Plumbing rough-in - core area levels 3-6",
    "Elevator installation - core shaft",
    "Interior finishes - painting levels 3-4",
    "Exterior glazing - south curtain wall",
    "Site grading and compaction - parking area",
    "Concrete topping slab - parking structure",
    "Insulation installation - exterior walls",
    "Fire suppression piping - levels 7-8",
    "Electrical switchgear installation",
    "Flooring installation - carpet and VCT levels 3-5",
    "Final grading and landscaping - site perimeter",
]

ISSUES_SUMMARIES = [
    None, None, None, None, None, None, None, None, None,
    "Material delivery delayed - concrete pump required rescheduling.",
    "Weather hold - high winds suspended crane operations.",
    "Subcontractor headcount low - productivity impacted.",
    "Inspection hold - awaiting city inspector for concrete pour.",
    "RFI field hold - awaiting design team response on structural detail.",
    "Equipment breakdown - compressor requiring repair.",
    "Coordination conflict identified - MEP and structural interference.",
    "Safety near-miss reported - corrective action taken.",
    "Material quality non-conformance - batch rejected.",
]

SUPERINTENDENT_IDS = [f"EMP-{random.randint(1, 50):03d}" for _ in range(25)]

daily_rows = []

for idx, proj in enumerate(PROJECTS):
    pid = proj["project_id"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    effective_end = min(end, today)
    super_id = SUPERINTENDENT_IDS[idx % len(SUPERINTENDENT_IDS)]

    # Walk weekdays
    d = start
    while d <= effective_end:
        if d.weekday() < 5:  # Mon-Fri only
            month = d.month
            weather_cfg = WEATHER_BY_MONTH[month]
            condition = random.choices(weather_cfg["conditions"], weights=weather_cfg["weights"])[0]
            high_f = random.randint(*weather_cfg["high_range"])
            low_f = random.randint(*weather_cfg["low_range"])

            precip = 0.0
            if condition in ("rain", "snow"):
                precip = round(random.uniform(0.1, 1.8), 2)
            elif condition == "partly_cloudy" and random.random() < 0.08:
                precip = round(random.uniform(0.05, 0.4), 2)

            huvibar_hc = random.randint(3, 15)
            sub_hc = random.randint(10, 80) if condition not in ("snow",) or precip < 0.5 else random.randint(0, 25)
            visitors = random.choices([0, 1, 2, 3, 4, 5], weights=[55, 25, 10, 6, 3, 1])[0]

            daily_rows.append({
                "report_id": str(uuid.uuid4()),
                "project_id": pid,
                "report_date": d.isoformat(),
                "weather_condition": condition,
                "temp_high_f": high_f,
                "temp_low_f": low_f,
                "precipitation_inches": precip,
                "work_performed_summary": random.choice(WORK_SUMMARIES),
                "issues_summary": random.choice(ISSUES_SUMMARIES),
                "visitors": visitors,
                "huvibar_headcount": huvibar_hc,
                "sub_headcount": sub_hc,
                "superintendent_employee_id": super_id,
                "created_date": d.isoformat(),
            })
        d += datetime.timedelta(days=1)

daily_pdf = pd.DataFrame(daily_rows)
daily_sdf = spark.createDataFrame(daily_pdf)
daily_sdf.write.mode("overwrite").saveAsTable(f"{catalog}.project_tracking.daily_reports")
df = spark.table(f"{catalog}.project_tracking.daily_reports")
print(f"Created {catalog}.project_tracking.daily_reports with {df.count()} rows")

# COMMAND ----------
# ==============================================================================
# TABLE 5: punch_list_items (~3,000 rows — ~120 per project)
# ==============================================================================

AREA_LOCATIONS = [
    "Level 1 - Lobby", "Level 1 - Corridor A", "Level 1 - Mechanical Room",
    "Level 2 - Suite 201", "Level 2 - Suite 215", "Level 2 - Restroom Core",
    "Level 3 - Suite 301", "Level 3 - Conference Room 3A", "Level 3 - Break Room",
    "Level 4 - Open Office", "Level 4 - Suite 410",
    "Level 5 - Penthouse Mech", "Roof - Main", "Roof - Equipment Screen",
    "Exterior - North Facade", "Exterior - South Entry", "Exterior - East Elevation",
    "Exterior - West Facade", "Exterior - Parking Lot", "Site - Landscaping",
    "Basement - Parking Level 1", "Basement - Electrical Room",
    "Stairwell A - All Levels", "Stairwell B - All Levels",
    "Elevator Lobby - Level 1", "Loading Dock", "Trash Room",
]

PUNCH_DESCRIPTIONS = [
    "Paint touch-up required at corner bead impact damage",
    "Door closer adjustment needed - not self-closing fully",
    "Carpet seam visible and lifting at suite entry",
    "Ceiling tile missing in corridor near IDF room",
    "Caulk joint at window frame incomplete - exterior",
    "Light fixture not functioning - lamp or driver replacement",
    "HVAC diffuser misaligned - not flush with ceiling",
    "Grout joint missing at tile transition - restroom",
    "Door hardware finish inconsistent - replace lever",
    "Wall scuff requiring repaint - high traffic corridor",
    "Baseboard not installed at mechanical room wall",
    "Floor drain cover missing - mechanical room",
    "Outlet cover plate missing - suite",
    "Condensation on window seal - IGU failure",
    "Exterior caulk shrinkage at curtain wall joint",
    "Stair nosing loose - safety concern",
    "Exit sign not illuminated - requires attention",
    "Plumbing fixture running continuously - requires adjustment",
    "Ceiling access panel not latching properly",
    "Parking lot line striping incomplete - handicap space",
    "Sidewalk joint filler missing - entrance plaza",
    "Landscaping mulch bed not complete - north side",
    "Roof drain strainer missing",
    "Exterior light fixture aimed incorrectly",
    "Smoke detector placement variance from RCP",
    "Fire extinguisher cabinet door misaligned",
    "Signage wrong suite number - suite 312",
    "Millwork drawer not aligned - break room",
    "VCT tile pop at seam - server room",
    "GFCI outlet not functioning - restroom",
]

PRIORITIES = ["critical", "high", "medium", "low"]
RESPONSIBLE_TYPES = ["GC", "sub"]
ITEM_STATUSES = ["open", "in_progress", "complete", "waived"]

SUPERINTENDENT_NAMES = [
    "Rick Delgado", "Pamela Voss", "Gary Hutchins", "Karen Stroud",
    "Dale Merchant", "Susan Falcone", "Fred Torrington", "Anita Breck",
]

punch_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    start = datetime.date.fromisoformat(proj["start_date"])
    end = datetime.date.fromisoformat(proj["end_date"])
    today = datetime.date(2026, 8, 11)
    is_complete = proj["status"] == "completed"
    is_closeout = proj["status"] == "closeout"

    # Punch lists are generated toward end of project
    effective_punch_start = end - datetime.timedelta(days=180)
    effective_punch_start = max(effective_punch_start, start)
    effective_punch_end = min(end + datetime.timedelta(days=30), today)

    n_items = random.randint(100, 140)
    item_counter = 1
    superintendent = random.choice(SUPERINTENDENT_NAMES)

    for _ in range(n_items):
        punch_duration = max((effective_punch_end - effective_punch_start).days, 10)
        id_offset = random.randint(0, punch_duration)
        identified_date = effective_punch_start + datetime.timedelta(days=id_offset)
        due_days = random.randint(7, 30)
        due_date = identified_date + datetime.timedelta(days=due_days)

        priority = random.choices(PRIORITIES, weights=[5, 20, 55, 20])[0]
        resp_type = random.choices(RESPONSIBLE_TYPES, weights=[30, 70])[0]
        sub_id = f"SUB-{random.randint(1, 60):03d}" if resp_type == "sub" else None
        emp_num = random.randint(1, 200)

        if is_complete:
            status = random.choices(["complete", "waived"], weights=[92, 8])[0]
        elif is_closeout:
            status = random.choices(["open", "in_progress", "complete", "waived"], weights=[20, 25, 48, 7])[0]
        else:
            status = random.choices(["open", "in_progress", "complete", "waived"], weights=[40, 30, 25, 5])[0]

        completed_date = None
        if status == "complete":
            comp_offset = random.randint(1, due_days + 5)
            completed_date = (identified_date + datetime.timedelta(days=comp_offset)).isoformat()

        punch_rows.append({
            "item_id": str(uuid.uuid4()),
            "project_id": pid,
            "item_number": f"PL-{item_counter:03d}",
            "area_location": random.choice(AREA_LOCATIONS),
            "description": random.choice(PUNCH_DESCRIPTIONS),
            "responsible_party_type": resp_type,
            "responsible_sub_id": sub_id,
            "assigned_to_employee_id": f"EMP-{emp_num:03d}",
            "priority": priority,
            "identified_date": identified_date.isoformat(),
            "due_date": due_date.isoformat(),
            "completed_date": completed_date,
            "status": status,
            "verified_by": superintendent,
        })
        item_counter += 1

punch_pdf = pd.DataFrame(punch_rows)
punch_sdf = spark.createDataFrame(punch_pdf)
punch_sdf.write.mode("overwrite").saveAsTable(f"{catalog}.project_tracking.punch_list_items")
df = spark.table(f"{catalog}.project_tracking.punch_list_items")
print(f"Created {catalog}.project_tracking.punch_list_items with {df.count()} rows")
