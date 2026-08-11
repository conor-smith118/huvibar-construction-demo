# Databricks App: Huvibar Project Tracking
# Connects to css_genie.project_tracking for project health, milestones, and RFIs

import gradio as gr
import os

# TODO: Connect to Databricks SQL warehouse
# warehouse_id = os.environ.get("DATABRICKS_WAREHOUSE_ID", "f5a185ab7f9f1e9f")

def get_project_health():
    """Placeholder: query project_tracking.projects with open RFI and submittal counts"""
    return [
        ["P022 - DEN Airport Terminal", "active", "34%", 42, 12, 5, "ON TRACK"],
        ["P025 - Broomfield Manufacturing Facility", "active", "61%", 18, 3, 2, "ON TRACK"],
        ["P021 - Englewood Mixed-Use Tower", "active", "78%", 7, 8, 11, "AT RISK"],
        ["P019 - Aurora Medical Office Building", "active", "52%", 28, 6, 4, "ON TRACK"],
        ["P023 - Castle Rock Data Center", "active", "15%", 64, 21, 7, "AT RISK"],
        ["P017 - Lakewood Retail Center", "active", "88%", 4, 1, 14, "AT RISK"],
        ["P016 - Rocky Flats Environmental Facility", "active", "44%", 35, 14, 3, "ON TRACK"],
        ["P018 - Parker Senior Living", "active", "67%", 9, 4, 6, "ON TRACK"],
        ["P020 - Thornton Industrial Park", "active", "29%", 44, 18, 2, "AT RISK"],
        ["P024 - Highlands Ranch Office Campus", "active", "55%", 22, 7, 8, "ON TRACK"],
        ["P026 - Westminster Civic Center", "active", "71%", 12, 5, 9, "ON TRACK"],
        ["P027 - Commerce City Warehouse", "active", "83%", 6, 2, 3, "ON TRACK"],
        ["P028 - Arvada Senior Center", "closeout", "94%", 2, 0, 31, "ON TRACK"],
        ["P029 - Brighton Distribution", "active", "38%", 48, 12, 5, "AT RISK"],
        ["P030 - Longmont Tech Campus", "active", "22%", 71, 29, 1, "AT RISK"],
    ]

def get_milestone_tracker(project="All"):
    """Placeholder: query project_tracking.milestones with variance"""
    return [
        ["P022 - DEN Airport Terminal", "Structural Steel Complete", "2024-06-15", "2024-06-28", "+13 days", "DELAYED"],
        ["P022 - DEN Airport Terminal", "MEP Rough-In", "2024-09-01", None, "TBD", "PENDING"],
        ["P025 - Broomfield Fab", "Foundation Complete", "2024-01-20", "2024-01-18", "-2 days", "COMPLETE"],
        ["P025 - Broomfield Fab", "Steel Erection Complete", "2024-04-15", "2024-04-17", "+2 days", "COMPLETE"],
        ["P025 - Broomfield Fab", "Roof Complete", "2024-06-30", None, "TBD", "IN PROGRESS"],
        ["P021 - Englewood Mixed-Use", "Substantial Completion", "2024-05-01", None, "+14 days projected", "AT RISK"],
        ["P023 - Castle Rock Data Center", "Permit Received", "2024-02-01", "2024-03-15", "+43 days", "DELAYED"],
        ["P019 - Aurora Medical Office", "MEP Commissioning", "2024-07-01", None, "On track", "IN PROGRESS"],
        ["P017 - Lakewood Retail", "Punch List Complete", "2024-04-30", None, "+7 days projected", "AT RISK"],
        ["P028 - Arvada Senior Center", "Final Completion", "2024-05-15", None, "On track", "IN PROGRESS"],
    ]

def get_open_rfis():
    """Placeholder: query project_tracking.rfis WHERE status = 'open'"""
    return [
        ["RFI-0892", "P022 - DEN Airport Terminal", "Structural", "Beam splice detail at column B12", 47, "structural_engineer", "HIGH"],
        ["RFI-0901", "P023 - Castle Rock Data Center", "Electrical", "Generator paralleling switchgear spec", 38, "electrical_engineer", "HIGH"],
        ["RFI-0876", "P025 - Broomfield Fab", "Mechanical", "Crane runway beam camber requirement", 22, "architect", "MEDIUM"],
        ["RFI-0915", "P020 - Thornton Industrial", "Civil", "Storm detention sizing confirmation", 18, "civil_engineer", "MEDIUM"],
        ["RFI-0923", "P030 - Longmont Tech Campus", "Architectural", "Exterior cladding attachment at parapet", 14, "architect", "MEDIUM"],
        ["RFI-0888", "P029 - Brighton Distribution", "Structural", "Dock leveler pit reinforcement", 31, "structural_engineer", "HIGH"],
        ["RFI-0934", "P019 - Aurora Medical Office", "Plumbing", "Medical gas outlet locations Floor 3", 9, "mep_engineer", "MEDIUM"],
        ["RFI-0941", "P021 - Englewood Mixed-Use", "Architectural", "Curtain wall head condition at 14th floor", 6, "huvibar", "LOW"],
        ["RFI-0947", "P016 - Rocky Flats Facility", "Mechanical", "HVAC zone control sequence of operations", 4, "mep_engineer", "LOW"],
        ["RFI-0952", "P027 - Commerce City Warehouse", "Civil", "Paving joint layout at truck court", 2, "civil_engineer", "LOW"],
    ]

def highlight_aging_rfis(df_data):
    """Returns rows with days_open > 21 flagged"""
    return df_data

with gr.Blocks(title="Huvibar | Project Tracking", theme=gr.themes.Default()) as app:
    gr.Markdown("# Huvibar Construction - Project Tracking")
    gr.Markdown("*Powered by Databricks | css_genie catalog*")

    with gr.Tabs():
        with gr.Tab("Project Health"):
            gr.Markdown("### Project Health Summary")
            gr.Markdown("*Status key: AT RISK = open RFIs > 10, overdue submittals > 10, or milestone delayed. Numbers shown are days until deadline.*")
            health_table = gr.Dataframe(
                headers=["Project", "Status", "% Complete", "Days to Deadline", "Open RFIs", "Overdue Submittals", "Health"],
                value=get_project_health(),
                interactive=False
            )
            with gr.Row():
                gr.Markdown("**Legend:** Days to Deadline calculated from projected_end_date. Health = AT RISK if any metric is outside threshold.")

        with gr.Tab("Milestone Tracker"):
            gr.Markdown("### Milestone Tracker")
            project_select = gr.Dropdown(
                choices=["All", "P022 - DEN Airport Terminal", "P025 - Broomfield Manufacturing Facility",
                         "P021 - Englewood Mixed-Use Tower", "P019 - Aurora Medical Office Building",
                         "P023 - Castle Rock Data Center", "P017 - Lakewood Retail Center",
                         "P028 - Arvada Senior Center", "P029 - Brighton Distribution"],
                value="All",
                label="Filter by Project"
            )
            milestone_table = gr.Dataframe(
                headers=["Project", "Milestone", "Planned Date", "Actual Date", "Variance", "Status"],
                value=get_milestone_tracker(),
                interactive=False
            )
            project_select.change(fn=get_milestone_tracker, inputs=project_select, outputs=milestone_table)

        with gr.Tab("Open RFIs"):
            gr.Markdown("### Open Requests for Information")
            gr.Markdown("*RFIs open > 21 days are highlighted — these may impact schedule if on critical path.*")
            rfi_table = gr.Dataframe(
                headers=["RFI #", "Project", "Discipline", "Subject", "Days Open", "Ball in Court", "Priority"],
                value=get_open_rfis(),
                interactive=False
            )
            with gr.Row():
                refresh_rfis = gr.Button("Refresh RFIs", variant="secondary")
                refresh_rfis.click(fn=get_open_rfis, outputs=rfi_table)

    gr.Markdown("---")
    gr.Markdown("*Connect your Databricks SQL warehouse to enable live data. See README for setup instructions.*")

if __name__ == "__main__":
    app.launch()
