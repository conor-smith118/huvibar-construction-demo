# Huvibar Construction Demo

> A production-grade Databricks demo environment for the construction industry, purpose-built for demonstrating **Genie** to construction and engineering customers.

## Overview

This repository contains a complete, deployable Databricks demo for **Huvibar Construction**, a fictional mid-size general contractor based in Denver, CO with an active portfolio of 25 projects ranging from airport terminals to data centers. The demo includes:

- **35+ Delta tables** across 8 domains with ~500K rows of enterprise-quality synthetic data
- **8 Genie Spaces** with curated instructions and verified queries (one per domain)
- **3 Lakeview Dashboards** (Project Overview, Cost & Budget, Safety & Compliance)
- **2 Databricks Apps** (Inventory Management, Project Tracking)
- **Fully deployable via DABs** — one command to deploy all assets

## Architecture

```
GitHub Repository
       │
       ▼
  DABs Bundle Deploy
       │
       ▼
Databricks Workspace (adb-7405605962645785.5.azuredatabricks.net)
       │
       ├── Catalog: css_genie
       │       │
       │       ├── scheduling          (4 tables)
       │       ├── payments            (4 tables)
       │       ├── billables           (4 tables)
       │       ├── cost_reporting      (5 tables)
       │       ├── project_tracking    (9 tables)
       │       ├── contracts           (4 tables)
       │       ├── concrete_testing    (4 tables)
       │       └── safety_compliance   (5 tables)
       │
       ├── Genie Spaces (8 — one per schema)
       │
       ├── Lakeview Dashboards
       │       ├── Huvibar | Project Overview
       │       ├── Huvibar | Cost & Budget
       │       └── Huvibar | Safety & Compliance
       │
       └── Databricks Apps
               ├── Inventory Management
               └── Project Tracking
```

## Demo Domains

| Domain | Schema | Tables | Key Demo Questions |
|--------|--------|--------|--------------------|
| Scheduling & Workforce | scheduling | 4 | Who is on site today? What trades are running overtime? Which equipment is underutilized? |
| Payment Pipeline | payments | 4 | What pay apps are outstanding? How much retainage are we holding across all projects? |
| Billables & AR | billables | 4 | What's the total AR balance? Which invoices are 30+ days overdue? |
| Cost Reporting | cost_reporting | 5 | Which projects are over budget? What's the portfolio burn rate? |
| Project Tracking | project_tracking | 9 | Are milestones on track? How many RFIs are aging past 21 days? |
| Contract Management | contracts | 4 | Which subs have expiring insurance? What POs are overdue? |
| Concrete QA/QC | concrete_testing | 4 | What's our 28-day cylinder break pass rate? Any recent failures? |
| Safety & Compliance | safety_compliance | 5 | What's our TRIR? Which projects have the most open corrective actions? |

## Prerequisites

- Databricks CLI v0.200+: `brew install databricks` or `pip install databricks-cli`
- Access to workspace: `https://adb-7405605962645785.5.azuredatabricks.net`
- Unity Catalog: verify `css_genie` catalog exists: `SHOW SCHEMAS IN css_genie`
- SQL Warehouse available (default: `f5a185ab7f9f1e9f`)
- Personal access token with workspace admin or catalog owner privileges

## Quick Deploy

### 1. Clone and configure

```bash
git clone https://github.com/databricks-demos/huvibar-construction-demo
cd huvibar-construction-demo
```

### 2. Set up Databricks CLI authentication

```bash
databricks configure --host https://adb-7405605962645785.5.azuredatabricks.net
# Enter your personal access token when prompted
```

### 3. Deploy the bundle

```bash
# Deploy to dev target (default)
databricks bundle deploy --target dev

# Deploy to prod target
databricks bundle deploy --target prod
```

### 4. Run the setup job

```bash
# Trigger the data generation job
databricks bundle run huvibar_setup_job --target dev

# Monitor progress in the Databricks Jobs UI or via CLI
databricks jobs get-run <run_id>
```

### 5. Verify deployment

```sql
-- Run in Databricks SQL to verify tables
SHOW TABLES IN css_genie.scheduling;
SELECT COUNT(*) FROM css_genie.project_tracking.projects;
SELECT COUNT(*) FROM css_genie.cost_reporting.actual_costs;
```

### Estimated setup time

- Data generation job: ~20-30 minutes (parallel tasks)
- Table comments: ~5 minutes
- Total end-to-end: ~35 minutes

## Suggested Demo Script

### For each Genie Space, ask these 5 questions in order (they build on each other):

---

### 1. Scheduling & Workforce Genie

1. "How many workers do we have on site across all active projects today?"
2. "Which projects have the highest overtime hours this month, and what trades are driving it?"
3. "Show me equipment utilization by project — which pieces of equipment are sitting idle more than 3 days a week?"
4. "Compare labor hours for concrete work between our top 5 projects by contract value."
5. "Which superintendent has the most crew members reporting to them across all their projects?"

---

### 2. Payment Pipeline Genie

1. "What pay applications are currently outstanding and how long have they been waiting?"
2. "How much total retainage are we holding from subcontractors across all projects?"
3. "Which projects have the largest gap between work completed and amount certified by the owner?"
4. "Show me all lien waivers that haven't been executed yet for pay apps paid in the last 60 days."
5. "What's our average days-to-payment from pay app submission to receipt of funds, by project type?"

---

### 3. Billables & Accounts Receivable Genie

1. "What's our total outstanding AR balance right now?"
2. "Which invoices are more than 30 days past due, and who's the owner contact on each project?"
3. "Show me all T&M tickets that haven't been signed off yet — what's the total value at risk?"
4. "How much revenue have we billed against change orders this quarter versus the prior quarter?"
5. "Which projects have invoices in disputed status, and what's the average time to resolve disputes?"

---

### 4. Cost Reporting Genie

1. "Which active projects are currently forecast over budget?"
2. "What's our total portfolio burn rate over the last 3 months, broken down by cost type?"
3. "Show me change order volume by reason code — what's driving the most cost growth?"
4. "For projects over $10M, how does estimate-at-completion compare to original contract value?"
5. "Which cost codes are most consistently over budget across our project portfolio?"

---

### 5. Project Tracking Genie

1. "How many RFIs have been open for more than 21 days, and which discipline is holding the most?"
2. "Which projects have milestones that are more than 2 weeks behind schedule?"
3. "Show me all submittals on the critical path that are still in 'revise and resubmit' status."
4. "Which project manager has the highest percentage of their projects on schedule?"
5. "How many open punch list items do we have per project, and which projects are in closeout?"

---

### 6. Contract Management Genie

1. "Which subcontractors have insurance certificates expiring in the next 90 days?"
2. "What purchase orders are more than 2 weeks past their expected delivery date?"
3. "Show me all subcontracts where the sub has billed more than 90% of their contract value."
4. "Which prime contracts have liquidated damages clauses, and what's the total daily LD exposure?"
5. "How many contract amendments have we executed this year, and what's the average value per amendment?"

---

### 7. Concrete QA/QC Genie

1. "What's our 28-day cylinder break pass rate across all active projects?"
2. "Are there any recent cylinder break failures, and have the engineers been notified?"
3. "Which mix designs have the highest variance between designed and actual strength?"
4. "Show me all concrete pours from this month with the associated test results."
5. "Which project has had the most concrete inspection failures this year?"

---

### 8. Safety & Compliance Genie

1. "What's our current TRIR and how does it compare to the ENR industry benchmark of 2.4?"
2. "Which projects have the most open corrective actions from safety incidents?"
3. "Show me all employees and subcontractor personnel with expired safety certifications."
4. "What were our top 3 incident types this year, and are they trending up or down?"
5. "Which projects have the lowest average safety inspection scores in the last 90 days?"

---

## Customization

### Override catalog

```bash
# Deploy with a different catalog
databricks bundle deploy --target dev --var catalog=my_catalog
```

### Override warehouse

```bash
databricks bundle deploy --target dev --var warehouse_id=my_warehouse_id
```

### Add more projects

Edit `notebooks/data_generation/00_shared_dimensions.py` to add projects to the master project list. All downstream notebooks read from the shared project dimension, so new projects will automatically flow into all domain tables on the next job run.

### Change data volumes

Each data generation notebook accepts a `num_rows` parameter to scale up or down. For a 15-minute demo, the default volumes are appropriate. For a persistent demo environment, consider increasing to 1M+ rows for more realistic query performance characteristics.

### Add a Genie Space

1. Create a new Space in the Databricks UI pointing to the relevant schema
2. Add the suggested questions from this README as verified queries
3. Add business context in the Space instructions (see existing spaces for examples)

## File Structure

```
huvibar-construction-demo/
├── databricks.yml                          # DABs bundle root
├── README.md
├── .gitignore
├── .github/
│   └── workflows/
│       └── deploy.yml                      # CI/CD pipeline
├── resources/
│   ├── jobs/
│   │   └── setup_job.yml                   # Data generation + semantics job
│   └── dashboards/
│       ├── project_overview.yml
│       ├── project_overview.lvdash.json
│       ├── cost_reporting.yml
│       ├── cost_reporting.lvdash.json
│       ├── safety.yml
│       └── safety.lvdash.json
├── notebooks/
│   ├── data_generation/
│   │   ├── 00_shared_dimensions.py
│   │   ├── 01_scheduling.py
│   │   ├── 02_payments.py
│   │   ├── 03_billables.py
│   │   ├── 04_cost_reporting.py
│   │   ├── 05_project_tracking.py
│   │   ├── 06_contracts.py
│   │   ├── 07_concrete_testing.py
│   │   └── 08_safety_compliance.py
│   └── semantics/
│       ├── 01_table_comments.py
│       └── 02_column_comments.py
└── apps/
    ├── inventory_management/
    │   ├── app.py
    │   ├── app.yml
    │   └── requirements.txt
    └── project_tracking/
        ├── app.py
        ├── app.yml
        └── requirements.txt
```

## About Huvibar Construction

Huvibar Construction is a fictional general contractor used exclusively for Databricks demo purposes. Any resemblance to real companies is coincidental. The company narrative:

- **Founded**: 1987, Denver, CO
- **Specialties**: Commercial, industrial, healthcare, government, and data center construction
- **Annual revenue**: ~$850M
- **Active projects**: 25 concurrent projects across the Front Range
- **Workforce**: ~1,200 employees + 3,000+ subcontractor personnel
- **Notable current projects**: Denver International Airport Terminal Expansion, Rocky Flats Environmental Remediation Facility, Castle Rock Data Center Campus

## Support

For questions about this demo, contact `conor.smith@databricks.com`.
