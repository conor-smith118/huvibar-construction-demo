# Databricks notebook source

# COMMAND ----------
%pip install faker --quiet

# COMMAND ----------

import uuid
import random
import pandas as pd
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

catalog = "css_genie"  # hardcoded for serverless compatibility

# COMMAND ----------

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

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.billables")

# COMMAND ----------

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def date_to_str(d):
    return d.isoformat() if d is not None else None

today = date(2026, 8, 11)

EMPLOYEE_NAMES = [fake.name() for _ in range(80)]

def rand_employee():
    return random.choice(EMPLOYEE_NAMES)

# ─────────────────────────────────────────────
# Invoice line item templates
# ─────────────────────────────────────────────

INVOICE_LINE_TEMPLATES = [
    ("03 30 00", "Cast-in-Place Concrete - Foundations", "CY", 320.0, 450.0),
    ("03 30 00", "Cast-in-Place Concrete - Slabs on Grade", "CY", 290.0, 380.0),
    ("05 10 00", "Structural Steel Erection", "TON", 2200.0, 3500.0),
    ("05 30 00", "Metal Deck Installation", "SF", 4.5, 8.0),
    ("06 10 00", "Rough Carpentry - Wall Framing", "SF", 12.0, 18.0),
    ("07 50 00", "TPO Membrane Roofing", "SF", 14.0, 22.0),
    ("07 20 00", "Rigid Board Insulation", "SF", 3.5, 6.5),
    ("08 10 00", "Hollow Metal Doors and Frames", "EA", 1200.0, 2200.0),
    ("08 40 00", "Aluminum Storefront System", "SF", 85.0, 145.0),
    ("09 20 00", "Gypsum Board Assemblies", "SF", 8.0, 14.0),
    ("09 60 00", "Polished Concrete Flooring", "SF", 6.0, 11.0),
    ("09 90 00", "Interior Painting", "SF", 1.5, 3.0),
    ("21 10 00", "Fire Sprinkler System", "SF", 4.5, 7.5),
    ("22 10 00", "Plumbing Rough-In and Fixtures", "SF", 12.0, 20.0),
    ("23 05 00", "HVAC System Installation", "SF", 18.0, 32.0),
    ("26 05 00", "Electrical Rough-In", "SF", 10.0, 18.0),
    ("26 50 00", "Lighting Fixtures and Controls", "SF", 6.0, 12.0),
    ("27 10 00", "Structured Cabling and Low Voltage", "SF", 4.0, 8.0),
    ("31 20 00", "Mass Excavation and Grading", "CY", 22.0, 38.0),
    ("32 10 00", "Asphalt Paving", "SF", 5.5, 9.0),
    ("32 90 00", "Landscaping and Irrigation", "LS", 1.0, 1.0),
    ("01 10 00", "General Conditions - Monthly", "LS", 1.0, 1.0),
    ("01 40 00", "Testing and Inspection Services", "LS", 1.0, 1.0),
    ("14 20 00", "Elevator Installation", "EA", 85000.0, 150000.0),
    ("04 20 00", "Masonry - CMU and Brick Veneer", "SF", 28.0, 48.0),
    ("28 10 00", "Access Control and Security Systems", "LS", 1.0, 1.0),
    ("31 60 00", "Drilled Piers and Caissons", "LF", 180.0, 320.0),
    ("33 10 00", "Site Utilities - Water and Sewer", "LF", 95.0, 175.0),
    ("02 41 00", "Selective Demolition", "SF", 4.0, 9.0),
    ("10 20 00", "Toilet Compartments and Accessories", "EA", 450.0, 850.0),
]

LUMP_SUM_ITEMS = [
    ("01 10 00", "Mobilization and Site Setup", "LS"),
    ("01 10 00", "Project Management and Supervision", "LS"),
    ("01 40 00", "Quality Control and Testing", "LS"),
    ("01 10 00", "Safety Program and Site Security", "LS"),
    ("01 10 00", "Temporary Utilities and Facilities", "LS"),
    ("01 10 00", "Bonds and Insurance", "LS"),
    ("01 10 00", "Permits and Fees", "LS"),
    ("01 10 00", "Closeout Documentation", "LS"),
    ("01 10 00", "Commissioning Support", "LS"),
    ("01 10 00", "Owner Training", "LS"),
]

# ─────────────────────────────────────────────
# Generate invoices
# ─────────────────────────────────────────────

invoice_rows = []
# Track invoice_id -> project_id for line items
invoice_index = []  # list of dicts with invoice_id, project_id, billing_period_from, billing_period_to

for proj in PROJECTS:
    pid = proj["project_id"]
    contract_value = proj["contract_value"]
    start = parse_date(proj["start_date"])
    end = parse_date(proj["end_date"])
    status = proj["status"]

    billing_end = min(end, today)

    # Build monthly periods
    periods = []
    cur = date(start.year, start.month, 1)
    if cur.month == 12:
        cur = date(cur.year + 1, 1, 1)
    else:
        cur = date(cur.year, cur.month + 1, 1)

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

    # Generate ~20 invoices - use actual periods plus any extra as T&M invoices
    # If fewer than 20 periods, duplicate some as T&M invoices
    n_target = 20
    inv_counter = 1

    for i, (pf, pt) in enumerate(periods[:n_target]):
        inv_number = f"INV-{pid}-{inv_counter:03d}"
        invoice_date = pt + timedelta(days=random.randint(1, 5))
        due_date = invoice_date + timedelta(days=30)

        # Billing amounts: roughly proportional slice of contract
        period_fraction = (pt - pf).days / max((billing_end - start).days, 1)
        base_subtotal = round(contract_value * period_fraction * random.uniform(0.8, 1.2), 2)
        # Clamp to reasonable range
        base_subtotal = max(base_subtotal, 50000.0)
        base_subtotal = min(base_subtotal, contract_value * 0.15)

        # CO construction in CO is generally tax-exempt
        tax_amount = 0.0
        total_amount = round(base_subtotal + tax_amount, 2)

        is_last = (i == len(periods[:n_target]) - 1)
        is_second_last = (i == len(periods[:n_target]) - 2)

        if status == "completed":
            amount_paid = total_amount
            payment_date = due_date + timedelta(days=random.randint(-5, 10))
            inv_status = "paid"
            balance_due = 0.0
        elif status == "closeout":
            if is_last:
                amount_paid = round(total_amount * random.uniform(0.0, 0.0), 2)
                payment_date = None
                inv_status = "sent"
                balance_due = total_amount
            elif is_second_last:
                amount_paid = round(total_amount * random.uniform(0.5, 0.9), 2)
                payment_date = due_date - timedelta(days=random.randint(1, 15))
                inv_status = "partial"
                balance_due = round(total_amount - amount_paid, 2)
            else:
                amount_paid = total_amount
                payment_date = due_date + timedelta(days=random.randint(-5, 10))
                inv_status = "paid"
                balance_due = 0.0
        elif status == "active":
            if is_last:
                amount_paid = 0.0
                payment_date = None
                if invoice_date < today - timedelta(days=30):
                    inv_status = "overdue"
                else:
                    inv_status = "sent"
                balance_due = total_amount
            elif is_second_last:
                amount_paid = round(total_amount * random.uniform(0.0, 0.5), 2)
                payment_date = None if amount_paid == 0.0 else (due_date - timedelta(days=5))
                inv_status = "partial" if amount_paid > 0 else "sent"
                balance_due = round(total_amount - amount_paid, 2)
            else:
                amount_paid = total_amount
                payment_date = due_date + timedelta(days=random.randint(-5, 10))
                inv_status = "paid"
                balance_due = 0.0
        else:
            amount_paid = total_amount
            payment_date = due_date + timedelta(days=random.randint(-5, 10))
            inv_status = "paid"
            balance_due = 0.0

        if payment_date and payment_date > today:
            payment_date = today - timedelta(days=random.randint(1, 5))

        days_outstanding = (today - invoice_date).days if inv_status != "paid" else 0

        invoice_id = str(uuid.uuid4())
        invoice_rows.append({
            "invoice_id": invoice_id,
            "project_id": pid,
            "invoice_number": inv_number,
            "invoice_date": date_to_str(invoice_date),
            "due_date": date_to_str(due_date),
            "billing_period_from": date_to_str(pf),
            "billing_period_to": date_to_str(pt),
            "subtotal": base_subtotal,
            "tax_amount": tax_amount,
            "total_amount": total_amount,
            "amount_paid": amount_paid,
            "balance_due": balance_due,
            "payment_date": date_to_str(payment_date),
            "status": inv_status,
            "days_outstanding": days_outstanding,
        })
        invoice_index.append({
            "invoice_id": invoice_id,
            "project_id": pid,
            "billing_period_from": pf,
            "billing_period_to": pt,
            "total_amount": total_amount,
            "inv_number": inv_number,
        })
        inv_counter += 1

pdf_invoices = pd.DataFrame(invoice_rows)
spark.createDataFrame(pdf_invoices).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.billables.invoices")
df = spark.table(f"{catalog}.billables.invoices")
print(f"Created {catalog}.billables.invoices with {df.count()} rows")

# COMMAND ----------

# ─────────────────────────────────────────────
# Generate invoice_line_items
# ─────────────────────────────────────────────

line_item_rows = []

for inv in invoice_index:
    invoice_id = inv["invoice_id"]
    pid = inv["project_id"]
    total_amount = inv["total_amount"]
    inv_number = inv["inv_number"]

    n_lines = 10
    # Pick a mix of unit-price and lump-sum items
    n_unit_price = random.randint(6, 8)
    n_lump_sum = n_lines - n_unit_price

    selected_unit = random.sample(INVOICE_LINE_TEMPLATES, min(n_unit_price, len(INVOICE_LINE_TEMPLATES)))
    selected_ls = random.sample(LUMP_SUM_ITEMS, min(n_lump_sum, len(LUMP_SUM_ITEMS)))

    line_amounts = []
    temp_lines = []

    for cost_code, description, unit, low_rate, high_rate in selected_unit:
        if unit == "LS":
            qty = 1.0
            unit_price = round(total_amount * random.uniform(0.03, 0.12), 2)
        elif unit == "SF":
            qty = round(random.uniform(500, 5000), 0)
            unit_price = round(random.uniform(low_rate, high_rate), 2)
        elif unit == "CY":
            qty = round(random.uniform(20, 300), 1)
            unit_price = round(random.uniform(low_rate, high_rate), 2)
        elif unit == "LF":
            qty = round(random.uniform(50, 800), 0)
            unit_price = round(random.uniform(low_rate, high_rate), 2)
        elif unit == "TON":
            qty = round(random.uniform(5, 80), 1)
            unit_price = round(random.uniform(low_rate, high_rate), 2)
        elif unit == "EA":
            qty = round(random.uniform(1, 20), 0)
            unit_price = round(random.uniform(low_rate, high_rate), 2)
        elif unit == "HR":
            qty = round(random.uniform(8, 120), 1)
            unit_price = round(random.uniform(low_rate, high_rate), 2)
        else:
            qty = 1.0
            unit_price = round(total_amount * random.uniform(0.05, 0.15), 2)

        amt = round(qty * unit_price, 2)
        temp_lines.append((cost_code, description, qty, unit, unit_price, amt))
        line_amounts.append(amt)

    for cost_code, description, unit in selected_ls:
        amt = round(total_amount * random.uniform(0.03, 0.10), 2)
        temp_lines.append((cost_code, description, 1.0, unit, amt, amt))
        line_amounts.append(amt)

    # Scale all amounts so they sum to total_amount
    raw_total = sum(line_amounts)
    scale = total_amount / raw_total if raw_total > 0 else 1.0

    for i, (cost_code, description, qty, unit, unit_price, amt) in enumerate(temp_lines):
        if i == len(temp_lines) - 1:
            scaled_amt = round(total_amount - sum(r["amount"] for r in line_item_rows[-i:] if r.get("_temp_inv") == invoice_id), 2)
        else:
            scaled_amt = round(amt * scale, 2)

        # pay_app_reference format: PA-PXXX-NN
        pa_ref = f"PA-{pid}-{random.randint(1, 20):02d}"

        line_item_rows.append({
            "line_id": str(uuid.uuid4()),
            "invoice_id": invoice_id,
            "project_id": pid,
            "cost_code": cost_code,
            "description": description,
            "quantity": float(qty),
            "unit": unit,
            "unit_price": float(unit_price),
            "amount": scaled_amt,
            "pay_app_reference": pa_ref,
        })

# Remove temp field if it leaked
for r in line_item_rows:
    r.pop("_temp_inv", None)

pdf_line_items = pd.DataFrame(line_item_rows)
spark.createDataFrame(pdf_line_items).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.billables.invoice_line_items")
df = spark.table(f"{catalog}.billables.invoice_line_items")
print(f"Created {catalog}.billables.invoice_line_items with {df.count()} rows")

# COMMAND ----------

# ─────────────────────────────────────────────
# Generate time_and_material_tickets
# ─────────────────────────────────────────────

EQUIPMENT_LIST = [
    ("Excavator CAT 336", 185.0),
    ("Tower Crane Liebherr 280 EC-H", 850.0),
    ("Concrete Pump Truck", 320.0),
    ("Skid Steer Loader", 95.0),
    ("Scissor Lift JLG 3246", 75.0),
    ("Boom Lift JLG 600S", 145.0),
    ("Forklift Toyota 5000lb", 85.0),
    ("Compactor Wacker BS60-4As", 45.0),
    ("Generator Generac 60kW", 95.0),
    ("Mini Excavator Kubota U55", 115.0),
    ("Concrete Mixer Truck", 145.0),
    ("Flatbed Truck 48ft", 125.0),
    ("Man Lift Genie Z-45", 135.0),
    ("Laser Level System", 35.0),
    ("Air Compressor 185CFM", 65.0),
]

MATERIAL_DESCRIPTIONS = [
    "Concrete mix 4000 PSI ready-mix",
    "Rebar #5 Grade 60",
    "Structural steel plate 1/2\"",
    "Lumber 2x6x16 SPF",
    "Plywood 3/4\" OSB sheathing",
    "Insulation batt R-30",
    "PVC conduit 2\" EMT",
    "Copper pipe 3/4\" Type L",
    "HVAC duct 18\" galvanized",
    "Electrical wire 12 AWG THHN",
    "Anchor bolts 1\" dia x 12\"",
    "Expansion joint filler",
    "Waterproofing membrane",
    "Grout non-shrink",
    "Epoxy adhesive cartridges",
    "Chain link fencing 8 ft",
    "Formwork ties and wedges",
    "Temporary power distribution panel",
    "Safety netting 10ft x 20ft",
    "Concrete curing compound",
]

tm_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    start = parse_date(proj["start_date"])
    end = parse_date(proj["end_date"])
    status = proj["status"]

    work_end = min(end, today)
    project_days = (work_end - start).days

    # ~320 tickets per project average
    n_tickets = int(random.gauss(320, 40))
    n_tickets = max(n_tickets, 100)

    approvers = [rand_employee() for _ in range(5)]

    for _ in range(n_tickets):
        # Random date within project window
        day_offset = random.randint(0, project_days)
        ticket_date = start + timedelta(days=day_offset)

        employee_id = f"EMP-{random.randint(1, 200):03d}"
        hours_regular = round(random.uniform(0, 8), 1)
        hours_overtime = round(random.uniform(0, 4), 1) if random.random() < 0.30 else 0.0
        labor_rate = round(random.uniform(25, 65), 2)

        # Equipment (50% chance)
        has_equipment = random.random() < 0.50
        if has_equipment:
            eq_name, eq_rate = random.choice(EQUIPMENT_LIST)
            equipment_description = eq_name
            equipment_hours = round(random.uniform(1, 8), 1)
            equipment_rate = eq_rate
        else:
            equipment_description = None
            equipment_hours = None
            equipment_rate = None

        # Materials (40% chance)
        has_materials = random.random() < 0.40
        if has_materials:
            material_description = random.choice(MATERIAL_DESCRIPTIONS)
            material_cost = round(random.uniform(200, 8000), 2)
        else:
            material_description = None
            material_cost = None

        markup_pct = random.choice([15.0, 20.0])

        # Compute billable amount
        labor_cost = round((hours_regular + hours_overtime * 1.5) * labor_rate, 2)
        eq_cost = round((equipment_hours or 0.0) * (equipment_rate or 0.0), 2)
        mat_cost = material_cost or 0.0
        subtotal = labor_cost + eq_cost + mat_cost
        billable_amount = round(subtotal * (1 + markup_pct / 100), 2)

        # Status based on project status and ticket age
        ticket_age = (today - ticket_date).days
        if status == "completed":
            t_status = "billed"
        elif ticket_age > 60:
            t_status = random.choices(["billed", "approved"], weights=[0.80, 0.20])[0]
        elif ticket_age > 30:
            t_status = random.choices(["approved", "pending"], weights=[0.70, 0.30])[0]
        else:
            t_status = random.choices(["pending", "approved", "rejected"], weights=[0.60, 0.30, 0.10])[0]

        tm_rows.append({
            "ticket_id": str(uuid.uuid4()),
            "project_id": pid,
            "ticket_date": date_to_str(ticket_date),
            "employee_id": employee_id,
            "hours_regular": hours_regular,
            "hours_overtime": hours_overtime,
            "labor_rate": labor_rate,
            "equipment_description": equipment_description,
            "equipment_hours": equipment_hours,
            "equipment_rate": equipment_rate,
            "material_description": material_description,
            "material_cost": material_cost,
            "markup_pct": markup_pct,
            "billable_amount": billable_amount,
            "approved_by": random.choice(approvers),
            "status": t_status,
        })

pdf_tm = pd.DataFrame(tm_rows)
spark.createDataFrame(pdf_tm).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.billables.time_and_material_tickets")
df = spark.table(f"{catalog}.billables.time_and_material_tickets")
print(f"Created {catalog}.billables.time_and_material_tickets with {df.count()} rows")

# COMMAND ----------

# ─────────────────────────────────────────────
# Generate change_order_billings
# ─────────────────────────────────────────────

CO_DESCRIPTIONS = [
    "Owner-directed scope change - additional structural reinforcement",
    "Unforeseen subsurface conditions - additional excavation",
    "Design revision - mechanical system upgrade",
    "Added scope - security system expansion",
    "Differing site conditions - underground utilities relocation",
    "Owner change - upgraded finish specifications",
    "Code compliance revision - fire protection addition",
    "Value engineering credit - alternate roofing system",
    "Added scope - EV charging infrastructure",
    "Owner-directed acceleration premium",
    "Extended general conditions - owner-caused delay",
    "Structural change - foundation modification",
    "MEP coordination change - rerouted ductwork",
    "Added scope - exterior signage and wayfinding",
    "Utility company requirement - transformer relocation",
    "ADA compliance addition - elevator pit waterproofing",
    "Hazardous material abatement - discovered during demolition",
    "Owner added scope - rooftop solar conduit sleeves",
    "Added scope - enhanced landscaping package",
    "Design error correction - structural drawing revision",
    "Owner request - additional parking lot lights",
    "Code change during construction - sprinkler density upgrade",
    "Added scope - loading dock equipment",
    "Schedule acceleration - weekend overtime premium",
    "Owner change - lobby flooring upgrade to terrazzo",
    "Differing site conditions - rock excavation",
    "Added scope - generator and automatic transfer switch",
    "Owner change - upgraded glazing system",
    "MEP added scope - additional plumbing fixtures",
    "Added scope - exterior canopy structure",
]

co_billing_rows = []

for proj in PROJECTS:
    pid = proj["project_id"]
    contract_value = proj["contract_value"]
    start = parse_date(proj["start_date"])
    end = parse_date(proj["end_date"])
    status = proj["status"]

    work_end = min(end, today)

    # ~16 COs per project, larger projects get more
    if contract_value >= 100000000:
        n_cos = random.randint(18, 25)
    elif contract_value >= 50000000:
        n_cos = random.randint(14, 20)
    else:
        n_cos = random.randint(8, 15)

    project_days = (work_end - start).days

    used_descriptions = random.sample(CO_DESCRIPTIONS, min(n_cos, len(CO_DESCRIPTIONS)))

    for i in range(n_cos):
        co_number = i + 1
        co_id = f"CO-{co_number:03d}"
        description = used_descriptions[i] if i < len(used_descriptions) else f"Change Order #{co_number} - Owner-directed scope change"

        # Approved amount: typically 0.5% to 3% of contract value
        approved_amount = round(contract_value * random.uniform(0.005, 0.030), 2)

        # Date of last billing
        day_offset = random.randint(30, project_days) if project_days > 30 else project_days
        last_billed_date = start + timedelta(days=day_offset)
        if last_billed_date > today:
            last_billed_date = today - timedelta(days=random.randint(1, 30))

        # Billing status
        co_age = (today - last_billed_date).days

        if status == "completed":
            billed_pct = random.uniform(0.95, 1.0)
            paid_pct = random.uniform(0.95, 1.0) * billed_pct
            co_status = "paid"
        elif status == "closeout":
            billed_pct = random.uniform(0.85, 1.0)
            paid_pct = random.uniform(0.70, 0.95) * billed_pct
            co_status = random.choice(["billed", "partial"])
        elif co_age > 90:
            billed_pct = random.uniform(0.70, 1.0)
            paid_pct = random.uniform(0.60, 0.95) * billed_pct
            co_status = random.choices(["paid", "partial", "billed"], weights=[0.40, 0.40, 0.20])[0]
        elif co_age > 30:
            billed_pct = random.uniform(0.40, 0.85)
            paid_pct = random.uniform(0.30, 0.80) * billed_pct
            co_status = random.choices(["partial", "billed", "pending"], weights=[0.50, 0.30, 0.20])[0]
        else:
            billed_pct = random.uniform(0.0, 0.50)
            paid_pct = 0.0
            co_status = "pending"

        billed_to_date = round(approved_amount * billed_pct, 2)
        paid_to_date = round(approved_amount * paid_pct, 2)
        remaining_balance = round(approved_amount - paid_to_date, 2)

        co_billing_rows.append({
            "billing_id": str(uuid.uuid4()),
            "project_id": pid,
            "co_id": co_id,
            "co_number": co_number,
            "description": description,
            "approved_amount": approved_amount,
            "billed_to_date": billed_to_date,
            "paid_to_date": paid_to_date,
            "remaining_balance": remaining_balance,
            "last_billed_date": date_to_str(last_billed_date),
            "status": co_status,
        })

pdf_co = pd.DataFrame(co_billing_rows)
spark.createDataFrame(pdf_co).write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.billables.change_order_billings")
df = spark.table(f"{catalog}.billables.change_order_billings")
print(f"Created {catalog}.billables.change_order_billings with {df.count()} rows")
