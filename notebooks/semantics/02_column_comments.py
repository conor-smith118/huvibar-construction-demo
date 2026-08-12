# Databricks notebook source

# COMMAND ----------
catalog = "css_genie"  # hardcoded for serverless compatibility if "catalog" in [w.name for w in dbutils.widgets.getAll()] else "css_genie"

# COMMAND ----------
# =============================================================================
# css_genie.payments.pay_applications
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.payments.pay_applications
  ALTER COLUMN pay_app_number COMMENT
  'Sequential number for this pay application on the project, starting at 1. Combined with project_id forms the unique identifier for owner billing. Pay app numbers must be sequential with no gaps; missing numbers indicate voided submissions.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.payments.pay_applications
  ALTER COLUMN scheduled_value COMMENT
  'Total current contract value as established in the Schedule of Values, including all approved change orders at the time of this pay application. Should equal the sum of all SOV line items. Used as the denominator for percent-complete calculations.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.payments.pay_applications
  ALTER COLUMN work_completed_to_date COMMENT
  'Cumulative dollar value of work completed from contract start through the end of this billing period, per the Schedule of Values. This is a running total — it should equal the prior pay app cumulative amount plus the current period work completed. Certified by the owner or their authorized representative.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.payments.pay_applications
  ALTER COLUMN retainage_pct COMMENT
  'Percentage of each progress payment withheld by the owner as retainage security until project completion and acceptance. Typically 10% for the first 50% of project completion, then reduced to 5% per AIA contract terms. Released upon final completion and owner acceptance, or per contract milestones.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.payments.pay_applications
  ALTER COLUMN amount_due COMMENT
  'Net amount due to Huvibar for this pay application period: work_completed_this_period minus retainage withheld this period, plus stored materials, minus previously released retainage adjustments. This is the check amount the owner should issue within the contract payment window (typically 30 days).'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.payments.pay_applications
  ALTER COLUMN status COMMENT
  'Current processing status of the pay application. Values: draft (being assembled), submitted (sent to owner), under_review (owner reviewing), certified (owner approved amount, pending payment), paid (payment received and matched), disputed (owner challenging amounts), void (cancelled and resubmitted).'""")

# COMMAND ----------
# =============================================================================
# css_genie.cost_reporting.actual_costs
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.actual_costs
  ALTER COLUMN cost_type COMMENT
  'Category classification for the cost transaction. Values: labor (Huvibar direct workforce payroll), subcontractor (payments to specialty subs), material (owner-supplied or direct-purchase materials), equipment (owned or rented equipment charges), general_conditions (job trailer, temp utilities, superintendent time), other (miscellaneous reimbursable costs).'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.actual_costs
  ALTER COLUMN amount COMMENT
  'Dollar amount of the cost transaction, always positive for costs. Labor amounts are derived from payroll: hours × fully-burdened rate including benefits, taxes, and insurance. Subcontractor amounts are from approved invoices. All amounts are posted in USD and represent the Huvibar cost basis, not the billed-to-owner value.'""")

# COMMAND ----------
# =============================================================================
# css_genie.cost_reporting.cost_forecast
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.cost_forecast
  ALTER COLUMN estimate_at_completion COMMENT
  'Current best estimate by the project manager of the total cost to complete the project at the forecast date, including all costs incurred to date plus the estimated cost to finish. EAC = actual_costs_to_date + estimate_to_complete. When EAC exceeds current_budget, the project is forecast over budget and variance_amount will be positive.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.cost_forecast
  ALTER COLUMN variance_amount COMMENT
  'Dollar variance between estimate_at_completion and the current approved budget: variance = EAC - current_budget. Positive values indicate a cost overrun (over budget); negative values indicate the project is tracking under budget. Used to calculate the portfolio-level exposure for executive reporting.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.cost_forecast
  ALTER COLUMN variance_pct COMMENT
  'Percentage variance of EAC against current budget: (EAC - current_budget) / current_budget * 100. Positive means over budget; negative means under. Projects with variance_pct > 5% are flagged for executive review. Thresholds: green < 2%, yellow 2-5%, red > 5%.'""")

# COMMAND ----------
# =============================================================================
# css_genie.cost_reporting.change_orders
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.change_orders
  ALTER COLUMN co_type COMMENT
  'Classification of the change order by originating party and mechanism. Values: owner_directed (scope change instructed by owner), unforeseen_conditions (differing site conditions per contract clause), design_error (architect/engineer error or omission), rfi_clarification (work required by RFI response), value_engineering (scope reduction for savings), claim (disputed extra work, pending resolution).'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.change_orders
  ALTER COLUMN reason_code COMMENT
  'Standardized reason code for the change order, used for trend analysis across the portfolio. Common codes: DESIGN_INCOMPLETE, OWNER_SCOPE_ADD, OWNER_SCOPE_DELETE, DIFFERING_CONDITIONS, WEATHER_DELAY, MATERIAL_ESCALATION, CODE_CHANGE, COORDINATION_ERROR, ACCELERATION, EXTENDED_CONDITIONS. High frequency of DESIGN_INCOMPLETE indicates design quality issues worth raising with the design team.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.change_orders
  ALTER COLUMN amount COMMENT
  'Net dollar impact of the change order on the project contract value. Positive amounts increase the contract (additive changes); negative amounts decrease it (deductive changes or credits). Amount is zero for time-only changes. For pending/disputed COs, this is the amount claimed; for approved COs, it is the negotiated and executed value.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.cost_reporting.change_orders
  ALTER COLUMN affects_schedule COMMENT
  'Boolean flag indicating whether this change order includes a time extension claim affecting the project completion date. TRUE means a schedule extension is associated with this CO — see schedule_days_impact for the number of days requested or granted. Schedule-impacting COs are critical for liquidated damages exposure management.'""")

# COMMAND ----------
# =============================================================================
# css_genie.safety_compliance.incidents
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.safety_compliance.incidents
  ALTER COLUMN severity COMMENT
  'Huvibar internal severity classification for the incident. Values: near_miss (no injury, potential for harm identified), first_aid (minor injury treated on-site, not OSHA recordable), minor (recordable, no lost time), serious (lost time or restricted duty), critical (life-threatening or permanent impairment), fatality. Near-miss reporting is encouraged as a leading indicator of culture.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.safety_compliance.incidents
  ALTER COLUMN osha_recordable COMMENT
  'Boolean flag indicating whether the incident meets OSHA 29 CFR 1904 criteria for entry on the OSHA 300 log. Recordable incidents include: work-related injuries/illnesses resulting in days away from work, restricted work, job transfer, medical treatment beyond first aid, loss of consciousness, or diagnosis of a significant injury by a licensed healthcare professional. First aid cases are NOT recordable.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.safety_compliance.incidents
  ALTER COLUMN days_away_from_work COMMENT
  'Number of calendar days the injured worker was unable to perform any work due to the incident, per OSHA 300 log definition. Counts start the day after the injury. NULL or 0 for non-lost-time incidents. Days away from work directly impacts the DART rate (Days Away, Restricted, and Transfer rate) used in EMR insurance calculations.'""")

# COMMAND ----------
# =============================================================================
# css_genie.concrete_testing.cylinder_breaks
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.concrete_testing.cylinder_breaks
  ALTER COLUMN break_age_days COMMENT
  'Age of the concrete cylinder in days at the time of compressive strength testing. Standard break ages are 7 days (early strength indicator, typically 65-70% of 28-day strength), 14 days (intermediate check), and 28 days (specification strength, the acceptance break). Some projects specify additional breaks at 3 days or 56 days for high-performance mixes.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.concrete_testing.cylinder_breaks
  ALTER COLUMN design_strength_psi COMMENT
  'Specified minimum compressive strength in pounds per square inch (psi) that the concrete mix must achieve at 28 days, as defined in the project specifications and approved mix design. Typical values: 3000 psi (slabs on grade), 4000 psi (structural slabs and beams), 5000 psi (columns and high-stress elements), 6000+ psi (high-performance structural concrete).'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.concrete_testing.cylinder_breaks
  ALTER COLUMN actual_strength_psi COMMENT
  'Measured compressive strength of the test cylinder in psi as reported by the testing laboratory. ACI 318 acceptance criteria: a strength test (average of two cylinders) passes if (1) no individual test falls below fc-prime by more than 500 psi for fc-prime ≤ 5000 psi, AND (2) the average of any three consecutive tests exceeds fc-prime.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.concrete_testing.cylinder_breaks
  ALTER COLUMN pass_fail COMMENT
  'ACI 318 acceptance determination: PASS or FAIL. Failures at 28 days require immediate notification to the engineer of record and may trigger investigation including additional testing, core sampling of in-place concrete, or load testing. FAIL status does not always require removal — the engineer may accept based on in-place core results or structural analysis.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.concrete_testing.cylinder_breaks
  ALTER COLUMN percent_of_design COMMENT
  'Ratio of actual_strength_psi to design_strength_psi expressed as a percentage. Values below 100% at 28 days indicate a failing test. Values at 7 days typically range 60-80% — used to project 28-day strength and make early warning decisions. Values consistently above 110% may indicate over-design in the mix and opportunity for mix optimization to reduce cost.'""")

# COMMAND ----------
# =============================================================================
# css_genie.project_tracking.rfis
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.project_tracking.rfis
  ALTER COLUMN days_open COMMENT
  'Number of calendar days since the RFI was submitted, calculated from submission_date to current date (or response_date if resolved). Contract response time is typically 7-14 days depending on complexity. RFIs open beyond 21 days are flagged as aging. Unresolved RFIs may support delay claims if they are on the critical path and holding up field work.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.project_tracking.rfis
  ALTER COLUMN discipline COMMENT
  'Design discipline responsible for providing the RFI response. Values: architectural, structural, mechanical, electrical, plumbing, civil, geotech, specialty. Tracking response times and open counts by discipline identifies design team bottlenecks. High structural RFI counts often indicate incomplete or conflicting structural drawings.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.project_tracking.rfis
  ALTER COLUMN ball_in_court COMMENT
  'Party currently responsible for action on this RFI, indicating where the RFI sits in the review chain. Values: huvibar (we need to provide more information), architect (waiting on architect response), engineer (waiting on structural/MEP engineer), owner (owner decision required), sub (subcontractor to clarify scope). Used to distinguish Huvibar-caused delays from design team delays for schedule impact analysis.'""")

# COMMAND ----------
# =============================================================================
# css_genie.contracts.prime_contracts
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.contracts.prime_contracts
  ALTER COLUMN contract_type COMMENT
  'Delivery method and commercial structure of the prime contract. Values: lump_sum (fixed price for defined scope), guaranteed_maximum_price (GMP with shared savings provision), cost_plus_fee (reimbursable costs plus fixed or percentage fee), cm_at_risk (construction manager bears cost risk above GMP), design_build (single-entity responsibility for design and construction), unit_price (payment per measured unit of work).'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.contracts.prime_contracts
  ALTER COLUMN retainage_pct COMMENT
  'Percentage of each progress payment withheld by the owner as performance security, typically 10% until 50% project completion then reduced to 5% under standard AIA terms. Some public owners hold full 10% through final completion. Retainage represents a significant cash flow impact — on a $20M project with 10% retainage, up to $2M in earned revenue may be withheld at any time.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.contracts.prime_contracts
  ALTER COLUMN liquidated_damages_per_day COMMENT
  'Contractually stipulated daily penalty amount (in USD) assessed against Huvibar for each calendar day of unexcused delay beyond the substantial completion date. Values range from $500/day (small projects) to $50,000+/day (airports, hospitals, transit). Not a penalty but rather a pre-agreed estimate of owner damages. LD exposure is calculated as liquidated_damages_per_day × projected_delay_days.'""")

# COMMAND ----------
# =============================================================================
# css_genie.scheduling.crew_schedules
# =============================================================================

spark.sql(f"""ALTER TABLE {catalog}.scheduling.crew_schedules
  ALTER COLUMN hours_worked COMMENT
  'Actual hours worked by the employee on this schedule record, confirmed by foreman sign-off. Standard shift is 8 hours (7am-3:30pm) or 10 hours for four-day weeks. Hours worked plus overtime_hours should equal total hours for the day. Used for payroll verification, labor cost posting, and productivity analysis.'""")

# COMMAND ----------
spark.sql(f"""ALTER TABLE {catalog}.scheduling.crew_schedules
  ALTER COLUMN overtime_hours COMMENT
  'Hours worked beyond the standard 8-hour day (or 40-hour week for weekly OT calculations), subject to 1.5x pay rate per FLSA and union agreements. Carpenters, ironworkers, and operating engineers are governed by respective union CBA overtime provisions. High overtime rates signal understaffing or schedule acceleration — projects with >15% OT rate are flagged for staffing review.'""")

# COMMAND ----------
print("Column comments applied successfully — key columns across 9 tables updated.")
