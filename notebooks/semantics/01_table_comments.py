# Databricks notebook source

# COMMAND ----------
catalog = "css_genie"  # hardcoded for serverless compatibility if "catalog" in [w.name for w in dbutils.widgets.getAll()] else "css_genie"

# COMMAND ----------
# =============================================================================
# SCHEDULING SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.scheduling.crew_schedules IS
'Daily crew assignment records tracking which Huvibar Construction employees are assigned to each project, their shift hours, trade, and assigned tasks. Used for workforce planning, utilization analysis, and overtime tracking. Each row represents one employee-day assignment; multiple rows may exist per employee per day when split across projects.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.scheduling.equipment_schedules IS
'Daily equipment deployment records tracking which pieces of heavy equipment (cranes, excavators, lifts, compactors) are assigned to which projects. Used for equipment utilization reporting, rental cost allocation, and scheduling conflict detection. Includes both owned and rented equipment with associated cost rates.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.scheduling.subcontractor_schedules IS
'Scheduled and actual on-site dates for specialty subcontractors across all active Huvibar projects. Tracks mobilization dates, crew sizes, and trade disciplines (mechanical, electrical, plumbing, roofing, etc.). Used to coordinate multi-trade sequencing and identify schedule conflicts or delays.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.scheduling.daily_manpower_log IS
'Aggregated daily headcount and total hours worked per project, derived from foreman sign-in sheets and crew schedule confirmations. Used to calculate labor productivity metrics, verify payroll inputs, and compute TRIR denominators for safety rate calculations. Each row is one project per day.'""")

# COMMAND ----------
# =============================================================================
# PAYMENTS SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.payments.pay_applications IS
'Monthly pay application submissions from Huvibar to owners (GC billing) and from subcontractors to Huvibar (sub billing). Each pay app covers work completed during the billing period and cumulative-to-date values against the schedule of values. Tracks retainage held, amounts certified, and payment status through the AIA G702/G703 process.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.payments.schedule_of_values IS
'Line-item breakdown of contract value by cost code or work section, established at project start and updated through change orders. Forms the basis for monthly progress billing. Each row is one SOV line; the sum of all lines equals the current contract value including approved change orders.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.payments.lien_waivers IS
'Conditional and unconditional lien waiver records exchanged between Huvibar, owners, and subcontractors as a condition of payment. Tracks waiver type (conditional/unconditional), payment period covered, and execution date. Required for compliance with Colorado lien law and as a prerequisite for pay application certification.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.payments.payment_ledger IS
'Detailed payment transaction history recording every check, ACH transfer, and wire payment made to subcontractors and received from owners. Used for cash flow analysis, accounts payable/receivable aging, and audit trail. Links to pay applications and invoice records for full payment lifecycle tracing.'""")

# COMMAND ----------
# =============================================================================
# BILLABLES SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.billables.invoices IS
'Invoice header records for all billings issued by Huvibar to project owners and clients. Covers both lump-sum progress billings and time-and-material invoices. Tracks invoice status through the approval-to-payment cycle including disputes, credits, and write-offs.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.billables.invoice_line_items IS
'Detailed line-item breakdown for every invoice, linking each billable item to a cost code, work description, quantity, unit rate, and extended amount. Provides the granular detail behind each invoice header for owner review, audit support, and revenue recognition.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.billables.time_and_material_tickets IS
'Field-generated T&M tickets documenting extra work performed on a time-and-material basis outside the lump-sum contract scope. Each ticket captures date, crew members, hours, equipment used, and materials incorporated. Must be signed by owner representative to be billable; unsigned tickets are flagged for follow-up.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.billables.change_order_billings IS
'Billing records specifically tied to approved change orders, tracking how much of each approved CO has been invoiced and collected. Separates change order revenue from base contract revenue for margin analysis. Links to change_orders in cost_reporting schema for cost-to-revenue matching.'""")

# COMMAND ----------
# =============================================================================
# COST REPORTING SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.cost_reporting.budget_line_items IS
'Original and current approved budget by cost code for every active and completed project. The original_budget reflects the initial estimate; current_budget includes all approved change orders. Used as the baseline for variance analysis and earned value calculations. One row per project-cost_code combination.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.cost_reporting.committed_costs IS
'Executed subcontracts and purchase orders representing firm financial commitments not yet fully invoiced. Committed cost = contract/PO value minus amounts already recognized as actual costs. Used for cash flow forecasting and to identify total project exposure before invoices arrive.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.cost_reporting.actual_costs IS
'All posted cost transactions against project cost codes including labor hours billed, subcontractor invoices paid, material purchases, equipment charges, and general conditions. The authoritative source for project cost-to-date. Feeds into cost forecast and earned value calculations.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.cost_reporting.cost_forecast IS
'Monthly project-level cost forecasts capturing estimate-at-completion (EAC), remaining cost-to-complete, and variance from budget. Generated by project managers each month and used for executive reporting, cash flow projection, and early identification of over-budget projects.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.cost_reporting.change_orders IS
'All change order records across all projects, tracking scope changes from initial identification through owner approval. Includes both owner-directed changes and contractor-initiated claims. Captures cost impact, schedule impact, and current status. Approved COs flow to budget_line_items to update the current budget.'""")

# COMMAND ----------
# =============================================================================
# PROJECT TRACKING SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.projects IS
'Master project registry for all Huvibar Construction projects including active, closeout, and recently completed work. Contains core project metadata: client, location, contract value, project team, key dates, and current status. The central linking table for all cross-domain analysis — every other schema joins back to this table via project_id.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.employees IS
'Huvibar Construction employee master data including project managers, superintendents, field engineers, and craft workers. Tracks trade classification, hire date, union affiliation, and current project assignment. Used for workforce planning, org chart reporting, and linking named staff to project roles.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.subcontractors IS
'Approved subcontractor registry covering all specialty trades used by Huvibar. Includes insurance expiration dates, bonding capacity, prequalification status, and performance ratings from prior projects. Insurance fields are critical — expired certificates trigger payment holds and compliance alerts.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.cost_codes IS
'Standardized cost code hierarchy used across all Huvibar projects for budget tracking and cost allocation. Based on CSI MasterFormat divisions. Enables consistent cross-project benchmarking and supports roll-up reporting by work type (e.g., total concrete costs across all projects).'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.milestones IS
'Contractual and internal milestone records tracking planned vs. actual completion dates for key project phases (mobilization, structural completion, substantial completion, final completion). Variance from planned dates drives schedule risk scoring and liquidated damages exposure calculations.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.rfis IS
'Requests for Information submitted by Huvibar to design teams (architects, engineers) seeking clarification on contract documents. Tracks submission date, responsible discipline, days open, ball-in-court status, and resolution. Aging open RFIs are a leading indicator of schedule risk and potential delay claims.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.submittals IS
'Shop drawing and submittal log tracking required submittals from subcontractors through Huvibar review to design team approval. Tracks planned and actual submission dates, review cycles, and approval status. Overdue submittals on the critical path are a primary driver of procurement delays.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.daily_reports IS
'Superintendent daily field reports capturing weather conditions, crew counts, work performed, visitors, delays, and safety observations for each project day. The legal record of daily site conditions used in delay claims and dispute resolution. Linked to daily_manpower_log for headcount verification.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.project_tracking.punch_list_items IS
'Deficiency items identified during owner walkthroughs and pre-closeout inspections that must be corrected before final payment. Tracks item description, responsible subcontractor, due date, and completion status. Open punch list items are the primary gating factor for certificate of substantial completion and final retainage release.'""")

# COMMAND ----------
# =============================================================================
# CONTRACTS SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.contracts.prime_contracts IS
'Prime contract records between Huvibar Construction and project owners (developers, government agencies, corporations). Captures contract type (lump-sum, GMP, CM-at-risk, design-build), executed value, retainage terms, liquidated damages provisions, and key dates. The financial backbone of each project.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.contracts.subcontracts IS
'Executed subcontract agreements between Huvibar and specialty subcontractors for all trade scopes. Tracks contract value, scope description, insurance requirements, payment terms, and retainage. The flow-down of prime contract terms to the subcontract tier is critical for risk management and back-charge rights.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.contracts.purchase_orders IS
'Material and equipment purchase orders issued by Huvibar to suppliers and vendors. Tracks PO value, delivery schedule, partial receipt status, and invoice matching. Used for material procurement tracking, committed cost reporting, and accounts payable management.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.contracts.contract_amendments IS
'Formal amendments and modifications to both prime contracts and subcontracts, excluding routine change orders. Captures scope modifications, schedule extensions, retainage reductions, and commercial term changes. Amendments require owner or subcontractor signature and update the base contract record.'""")

# COMMAND ----------
# =============================================================================
# CONCRETE TESTING SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.concrete_testing.mix_designs IS
'Approved concrete mix designs for each project, specifying design compressive strength (psi), water-cement ratio, aggregate size, admixtures, and ACI compliance class. Mix designs must be pre-approved by the engineer of record before placement. Serves as the reference standard for interpreting cylinder break results.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.concrete_testing.pour_logs IS
'Field records for each concrete pour event, capturing placement date, structural element poured (footing, slab, wall, column), volume placed (CY), mix design used, ambient temperature, and slump test results. Cylinders cast during each pour are linked to this record for traceability.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.concrete_testing.cylinder_breaks IS
'Compressive strength test results for concrete cylinders cast during pours and broken in a certified lab at 7, 14, and 28 days. Pass/fail is determined against the design strength requirement with ACI acceptance criteria. Failed cylinders trigger engineer notification and potential core sampling of in-place concrete.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.concrete_testing.concrete_inspections IS
'Third-party special inspection reports for reinforced concrete work, including rebar placement verification, formwork inspection, and pre-pour checklists. Required by the building department as a condition of the building permit. Failed inspections halt concrete placement until corrective action is documented.'""")

# COMMAND ----------
# =============================================================================
# SAFETY & COMPLIANCE SCHEMA
# =============================================================================

spark.sql(f"""COMMENT ON TABLE {catalog}.safety_compliance.incidents IS
'All safety incident records for Huvibar and subcontractor personnel on Huvibar-managed job sites, from near-misses through fatalities. OSHA-recordable incidents require entry on the OSHA 300 log. Each incident includes a corrective action plan with due dates and completion tracking. The primary table for TRIR and safety performance metrics.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.safety_compliance.osha_300_log IS
'OSHA Form 300 log entries required by 29 CFR 1904 for all recordable injuries and illnesses. Maintained separately from the incidents table to mirror the regulatory format. Posted annually at job sites per OSHA requirements. Used for regulatory compliance, EMR calculation, and insurance underwriting.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.safety_compliance.toolbox_talks IS
'Weekly safety meeting records documenting the topic covered, presenter, attendees, and sign-in roster for each project. OSHA requires documented weekly toolbox talks for construction sites. High attendance rates and topic variety are positive indicators of safety culture. Linked to incidents to track training-incident correlations.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.safety_compliance.safety_inspections IS
'Scheduled and unannounced safety inspection results conducted by Huvibar safety managers and third-party auditors. Each inspection generates an overall score (0-100), a list of observations, and required corrective actions. Trending scores by project and inspector identify systemic safety culture issues.'""")

# COMMAND ----------
spark.sql(f"""COMMENT ON TABLE {catalog}.safety_compliance.certifications IS
'Individual safety and trade certifications for Huvibar employees and subcontractor personnel working on Huvibar sites. Tracks OSHA 10/30, First Aid/CPR, forklift, crane operator, confined space, and trade-specific certs. Expiry date monitoring ensures only qualified personnel perform safety-sensitive work. Expired certs trigger access suspension.'""")

# COMMAND ----------
print("Table comments applied successfully — 35 tables across 8 schemas updated.")
