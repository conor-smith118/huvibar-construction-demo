# Databricks App: Huvibar Inventory Management
# Connects to css_genie.contracts.purchase_orders for materials tracking

import gradio as gr
import os

# TODO: Connect to Databricks SQL warehouse
# warehouse_id = os.environ.get("DATABRICKS_WAREHOUSE_ID", "f5a185ab7f9f1e9f")

def get_open_pos(project_filter="All"):
    """Placeholder: query css_genie.contracts.purchase_orders WHERE status = 'open'"""
    # TODO: implement with databricks-sdk
    return [
        ["P022 - DEN Airport Terminal", "Structural Steel", "Atlas Steel Supply", "$2,450,000", "2024-03-15", "Partial"],
        ["P025 - Broomfield Fab", "Mechanical Equipment", "Carrier HVAC", "$890,000", "2024-04-01", "On Order"],
        ["P021 - Englewood Mixed-Use", "Curtain Wall", "Kawneer Products", "$1,200,000", "2024-02-28", "Overdue"],
        ["P019 - Aurora Medical Office", "Roofing System", "Firestone Building Products", "$340,000", "2024-03-22", "On Order"],
        ["P017 - Lakewood Retail", "HVAC Units", "Trane Technologies", "$520,000", "2024-03-10", "Partial"],
        ["P023 - Castle Rock Data Center", "UPS Systems", "Eaton Corporation", "$1,750,000", "2024-04-15", "On Order"],
        ["P016 - Rocky Flats Facility", "Specialty Mechanical", "Custom Air Systems", "$980,000", "2024-05-01", "On Order"],
    ]

def get_material_alerts():
    """Placeholder: surface overdue POs and low inventory alerts"""
    return [
        ["P021 - Englewood Mixed-Use", "Curtain Wall System", "14 days overdue", "CRITICAL"],
        ["P018 - Parker Senior Living", "Roofing Materials", "Delivery confirmation pending", "WARNING"],
        ["P016 - Rocky Flats Facility", "Specialty Mechanical", "Lead time 16 weeks — order now", "INFO"],
        ["P022 - DEN Airport Terminal", "Structural Steel", "Partial delivery received, balance pending", "WARNING"],
        ["P023 - Castle Rock Data Center", "UPS Systems", "Long-lead item — monitor weekly", "INFO"],
    ]

def get_po_summary():
    """Placeholder: aggregate PO status summary"""
    return [
        ["On Order", 12, "$8,240,000"],
        ["Partial", 7, "$5,610,000"],
        ["Overdue", 3, "$2,890,000"],
        ["Received", 28, "$14,320,000"],
        ["Cancelled", 2, "$450,000"],
    ]

with gr.Blocks(title="Huvibar | Inventory Management", theme=gr.themes.Default()) as app:
    gr.Markdown("# Huvibar Construction - Inventory Management")
    gr.Markdown("*Powered by Databricks | css_genie catalog*")

    with gr.Row():
        gr.Markdown("### Purchase Order Status Summary")

    with gr.Row():
        po_summary_table = gr.Dataframe(
            headers=["Status", "Count", "Total Value"],
            value=get_po_summary(),
            interactive=False,
            scale=1
        )

    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### Open Purchase Orders")
            project_filter = gr.Dropdown(
                choices=["All", "P022 - DEN Airport Terminal", "P025 - Broomfield Fab",
                         "P021 - Englewood Mixed-Use", "P019 - Aurora Medical Office",
                         "P017 - Lakewood Retail", "P023 - Castle Rock Data Center",
                         "P016 - Rocky Flats Facility"],
                value="All",
                label="Filter by Project"
            )
            po_table = gr.Dataframe(
                headers=["Project", "Material", "Vendor", "Amount", "Expected Delivery", "Status"],
                value=get_open_pos(),
                interactive=False
            )

        with gr.Column(scale=1):
            gr.Markdown("### Alerts")
            alerts_table = gr.Dataframe(
                headers=["Project", "Item", "Issue", "Severity"],
                value=get_material_alerts(),
                interactive=False
            )

    refresh_btn = gr.Button("Refresh Data", variant="secondary")
    refresh_btn.click(fn=get_open_pos, inputs=project_filter, outputs=po_table)

    gr.Markdown("---")
    gr.Markdown("*Connect your Databricks SQL warehouse to enable live data. See README for setup instructions.*")

if __name__ == "__main__":
    app.launch()
