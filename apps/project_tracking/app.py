# =============================================================================
# Huvibar Construction — Project Tracking & Field Management
# Interactive Dash app: portfolio overview + per-project drill-down
# Click any project in the sidebar or Gantt → opens project detail
# Click "All Projects" breadcrumb → back to portfolio
# TODO: Replace PROJECTS / RFIS / SUBMITTALS data with live Databricks SQL queries
# =============================================================================

import json
import pandas as pd
from datetime import date
import dash
from dash import dcc, html, Input, Output, State, ALL, ctx
import plotly.express as px
import plotly.graph_objects as go

# ─── Palette ────────────────────────────────────────────────────────
C_BLUE    = "#2a78d6"
C_AQUA    = "#1baf7a"
C_YELLOW  = "#eda100"
C_RED     = "#e34948"
C_ORANGE  = "#eb6834"
C_VIOLET  = "#4a3aa7"
C_SURFACE = "#fcfcfb"
C_INK     = "#0b0b0b"
C_SEC     = "#52514e"
C_MUTED   = "#898781"
C_GRID    = "#e1e0d9"
C_GOOD    = "#0ca30c"
FONT      = "system-ui, -apple-system, 'Segoe UI', sans-serif"
TODAY     = date(2026, 8, 11)
TODAY_TS  = pd.Timestamp("2026-08-11")  # MUST be Timestamp for px.timeline vline

# ─── Seed data ──────────────────────────────────────────────────────
# TODO: Query css_genie.project_tracking.projects WHERE status IN ('active','closeout')
PROJECTS = [
    {"id":"P013","short":"Convention Center",  "name":"Colorado Convention Center Expansion","value":150,"pct":94.9,"status":"active",  "type":"commercial",   "open_rfis":11,"pending_subs":18,"pm":"Sarah Chen",       "super":"Tom Kowalski", "start":"2022-05-01","end":"2025-12-15"},
    {"id":"P025","short":"Broomfield Fab",      "name":"Broomfield Semiconductor Fab",        "value":135,"pct":76.3,"status":"active",  "type":"industrial",   "open_rfis":10,"pending_subs":18,"pm":"Marcus Williams",  "super":"Rick Sanchez", "start":"2024-06-01","end":"2027-01-31"},
    {"id":"P022","short":"DEN Terminal",        "name":"Denver Airport Terminal Upgrade",     "value":120,"pct":94.9,"status":"active",  "type":"commercial",   "open_rfis":15,"pending_subs":14,"pm":"Jennifer Rodriguez","super":"Bill Murphy",   "start":"2023-11-01","end":"2026-06-30"},
    {"id":"P021","short":"Englewood Mixed",     "name":"Englewood Mixed-Use Development",     "value": 88,"pct":94.9,"status":"active",  "type":"commercial",   "open_rfis":11,"pending_subs":17,"pm":"David Park",       "super":"Dave Nelson",  "start":"2023-09-01","end":"2026-03-31"},
    {"id":"P018","short":"Parker Senior",       "name":"Parker Senior Living Campus",         "value": 61,"pct":94.9,"status":"active",  "type":"healthcare",   "open_rfis":12,"pending_subs":18,"pm":"Ashley Thompson",  "super":"Chris Okonkwo","start":"2023-03-01","end":"2025-09-30"},
    {"id":"P015","short":"Westminster HS",      "name":"Westminster High School",             "value": 52,"pct":97.7,"status":"closeout","type":"education",    "open_rfis": 0,"pending_subs":10,"pm":"Robert Martinez",  "super":"Frank Delgado","start":"2022-09-01","end":"2024-11-30"},
    {"id":"P017","short":"Loveland Logistics",  "name":"Loveland Logistics Hub",              "value": 45,"pct":94.9,"status":"active",  "type":"industrial",   "open_rfis":15,"pending_subs":23,"pm":"Kimberly Johnson", "super":"Steve Yamamoto","start":"2023-01-01","end":"2025-03-31"},
    {"id":"P023","short":"Aurora VA Clinic",    "name":"Aurora VA Medical Clinic",            "value": 42,"pct":94.9,"status":"active",  "type":"healthcare",   "open_rfis":10,"pending_subs":15,"pm":"James Wilson",     "super":"Al Petersen",  "start":"2024-01-01","end":"2026-01-31"},
    {"id":"P016","short":"Rocky Flats",         "name":"Rocky Flats Remediation Facility",   "value": 38,"pct":94.9,"status":"active",  "type":"industrial",   "open_rfis": 9,"pending_subs":14,"pm":"Patricia Davis",   "super":"Joe Morales",  "start":"2022-11-01","end":"2025-04-30"},
    {"id":"P019","short":"Castle Rock Muni",    "name":"Castle Rock Municipal Building",      "value": 24,"pct":94.9,"status":"active",  "type":"government",   "open_rfis": 9,"pending_subs":20,"pm":"Michael Brown",    "super":"Ed Blackwell", "start":"2023-05-01","end":"2025-02-28"},
    {"id":"P024","short":"Centennial Hangar",   "name":"Centennial Airport Hangar",           "value": 19,"pct":94.9,"status":"active",  "type":"infrastructure","open_rfis": 5,"pending_subs":18,"pm":"Sarah Chen",       "super":"Tom Kowalski", "start":"2024-03-01","end":"2025-08-31"},
    {"id":"P020","short":"Brighton Solar",      "name":"Brighton Solar Farm O&M",             "value": 15,"pct":97.5,"status":"closeout","type":"industrial",   "open_rfis": 0,"pending_subs": 8,"pm":"Marcus Williams",  "super":"Rick Sanchez", "start":"2023-07-01","end":"2024-10-31"},
]
PROJ_BY_ID = {p["id"]: p for p in PROJECTS}

# TODO: Query css_genie.project_tracking.rfis WHERE status='open' ORDER BY days_open DESC
RFIS = [
    {"id":"RFI-0892","pid":"P022","disc":"Structural",   "subject":"Beam splice detail at column B-12 curtain wall interface",      "days":47,"bic":"Structural Engineer"},
    {"id":"RFI-0856","pid":"P013","disc":"Architectural","subject":"Expansion joint cover assembly at concourse level",               "days":38,"bic":"Architect"},
    {"id":"RFI-0871","pid":"P018","disc":"MEP",          "subject":"Medical gas outlet locations - Floor 3 nursing wing",            "days":34,"bic":"MEP Engineer"},
    {"id":"RFI-0901","pid":"P017","disc":"Civil",        "subject":"Truck court drainage slope at dock 7-12",                        "days":29,"bic":"Civil Engineer"},
    {"id":"RFI-0876","pid":"P025","disc":"Structural",   "subject":"Overhead crane runway beam camber requirement",                  "days":22,"bic":"Structural Engineer"},
    {"id":"RFI-0963","pid":"P013","disc":"Structural",   "subject":"Column base plate grout gap at grid B-7",                       "days":19,"bic":"Structural Engineer"},
    {"id":"RFI-0915","pid":"P016","disc":"Mechanical",   "subject":"Exhaust fan interlock sequence with fire dampers",               "days":18,"bic":"MEP Engineer"},
    {"id":"RFI-0923","pid":"P023","disc":"Architectural","subject":"Accessible route at main entry - slope compliance",               "days":14,"bic":"Architect"},
    {"id":"RFI-0971","pid":"P025","disc":"Mechanical",   "subject":"Clean room HVAC pressure differential setpoint",                 "days":12,"bic":"MEP Engineer"},
    {"id":"RFI-0934","pid":"P019","disc":"Electrical",   "subject":"Emergency power transfer switch coordination",                   "days":11,"bic":"Electrical Engineer"},
    {"id":"RFI-0941","pid":"P021","disc":"Architectural","subject":"Curtain wall head condition at Level 14",                        "days": 8,"bic":"Huvibar GC"},
    {"id":"RFI-0978","pid":"P021","disc":"Civil",        "subject":"Underground storm line invert elevation at MH-14",               "days": 6,"bic":"Civil Engineer"},
    {"id":"RFI-0947","pid":"P024","disc":"Structural",   "subject":"Hangar door track anchorage detail",                            "days": 5,"bic":"Structural Engineer"},
    {"id":"RFI-0952","pid":"P017","disc":"Mechanical",   "subject":"HVAC unit selection for dock doors 1-6",                        "days": 3,"bic":"MEP Engineer"},
    {"id":"RFI-0958","pid":"P022","disc":"Electrical",   "subject":"LED dimming control wiring at gate level",                      "days": 2,"bic":"Electrical Engineer"},
]

# TODO: Query css_genie.project_tracking.submittals WHERE status IN ('pending','revise_resubmit')
SUBMITTALS = [
    {"id":"SUB-4201","pid":"P013","spec":"05-100","desc":"Structural Steel Shop Drawings",         "status":"revise_resubmit","submitted":"2026-06-15","required":"2026-07-01","days_late":41},
    {"id":"SUB-4290","pid":"P013","spec":"08-800","desc":"Curtain Wall Glazing Product Data",       "status":"pending",        "submitted":"2026-07-05","required":"2026-08-01","days_late":10},
    {"id":"SUB-4218","pid":"P017","spec":"23-100","desc":"HVAC Unit Product Data",                  "status":"pending",        "submitted":"2026-07-20","required":"2026-08-05","days_late": 6},
    {"id":"SUB-4301","pid":"P017","spec":"32-130","desc":"Rigid Paving Mix Design",                 "status":"revise_resubmit","submitted":"2026-06-01","required":"2026-06-20","days_late":52},
    {"id":"SUB-4229","pid":"P022","spec":"08-400","desc":"Storefront System Shop Drawings",         "status":"pending",        "submitted":"2026-07-28","required":"2026-08-15","days_late":-4},
    {"id":"SUB-4323","pid":"P022","spec":"14-200","desc":"Elevator Shop Drawings",                  "status":"revise_resubmit","submitted":"2026-05-20","required":"2026-06-05","days_late":67},
    {"id":"SUB-4235","pid":"P018","spec":"22-400","desc":"Plumbing Fixtures Product Data",          "status":"revise_resubmit","submitted":"2026-06-30","required":"2026-07-15","days_late":27},
    {"id":"SUB-4241","pid":"P025","spec":"11-000","desc":"Clean Room Equipment Data",               "status":"pending",        "submitted":"2026-08-01","required":"2026-08-20","days_late":-9},
    {"id":"SUB-4255","pid":"P021","spec":"09-200","desc":"Metal Framing Shop Drawings",             "status":"pending",        "submitted":"2026-07-15","required":"2026-08-01","days_late":10},
    {"id":"SUB-4267","pid":"P016","spec":"03-300","desc":"Concrete Mix Design Submittal",           "status":"revise_resubmit","submitted":"2026-05-10","required":"2026-05-25","days_late":77},
    {"id":"SUB-4278","pid":"P023","spec":"21-100","desc":"Fire Suppression Sprinkler Design",       "status":"pending",        "submitted":"2026-07-22","required":"2026-08-10","days_late": 1},
    {"id":"SUB-4312","pid":"P019","spec":"26-200","desc":"Electrical Distribution Shop Drawings",   "status":"pending",        "submitted":"2026-07-30","required":"2026-08-18","days_late":-7},
]

# ─── Color helpers ─────────────────────────────────────────────────
def rfi_color(days):
    if days > 21: return C_RED
    if days >= 14: return C_ORANGE
    if days >= 7: return C_YELLOW
    return C_BLUE

def rfi_label(days):
    if days > 21: return "Critical"
    if days >= 14: return "High"
    if days >= 7: return "Elevated"
    return "Watch"

TYPE_COLORS = {
    "commercial":     ("#e8f0fe", C_BLUE),
    "industrial":     ("#f3e8ff", C_VIOLET),
    "healthcare":     ("#e8f8f1", C_AQUA),
    "education":      ("#fff8e1", "#8d6e00"),
    "government":     ("#fce4ec", "#c62828"),
    "infrastructure": ("#e0f7fa", "#00838f"),
}

# ─── Charts ────────────────────────────────────────────────────────
def build_gantt():
    df = pd.DataFrame([{
        "short": p["short"], "start": p["start"], "end": p["end"], "status": p["status"]
    } for p in PROJECTS]).sort_values("start", ascending=False)

    fig = px.timeline(df, x_start="start", x_end="end", y="short", color="status",
                      color_discrete_map={"active": C_BLUE, "closeout": C_AQUA})
    # Add today line as a shape (add_vline broken on px.timeline in this plotly version)
    fig.add_shape(type="line",x0="2026-08-11",x1="2026-08-11",y0=0,y1=1,
                  yref="paper",line=dict(color=C_RED,width=2,dash="dash"))
    fig.add_annotation(x="2026-08-11",y=1.02,yref="paper",text="Today",
                       showarrow=False,font=dict(color=C_RED,size=9),xanchor="left")
    fig.update_traces(marker=dict(line=dict(width=0)), opacity=0.85,
                      hovertemplate="<b>%{y}</b><br>%{base|%b %Y} to %{x|%b %Y}<extra></extra>")
    fig.update_layout(
        paper_bgcolor=C_SURFACE, plot_bgcolor=C_SURFACE, height=400,
        margin=dict(l=0, r=16, t=8, b=32),
        xaxis=dict(gridcolor=C_GRID, tickfont=dict(color=C_SEC, size=10), showline=False, zeroline=False),
        yaxis=dict(tickfont=dict(color=C_INK, size=11), showline=False, title=None),
        legend=dict(orientation="h", y=-0.12, x=0, font=dict(color=C_SEC, size=11), bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def build_rfi_scatter(pid=None):
    rfis = sorted([r for r in RFIS if pid is None or r["pid"] == pid],
                  key=lambda r: r["days"], reverse=True)
    if not rfis:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor=C_SURFACE, plot_bgcolor=C_SURFACE, height=120,
                          annotations=[dict(text="No open RFIs", showarrow=False,
                                            font=dict(color=C_MUTED, size=13))])
        return fig

    y_labels = [PROJ_BY_ID.get(r["pid"], {}).get("short", r["pid"]) for r in rfis]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[r["days"] for r in rfis], y=y_labels,
        mode="markers+text",
        marker=dict(size=18, color=[rfi_color(r["days"]) for r in rfis],
                    opacity=0.9, line=dict(width=1.5, color="white")),
        text=[f"  {r['id']}" for r in rfis],
        textposition="middle right", textfont=dict(color=C_INK, size=10),
        customdata=[[r["id"], r["disc"], r["subject"], rfi_label(r["days"]), r["bic"]] for r in rfis],
        hovertemplate="<b>%{customdata[0]}</b> — %{customdata[3]}<br>%{y}<br><i>%{customdata[2]}</i><br><b>%{x} days open</b><br>BIC: %{customdata[4]}<extra></extra>",
    ))
    fig.add_vline(x=21, line=dict(color=C_RED, width=1.5, dash="dot"),
                  annotation_text="21d SLA", annotation_font=dict(color=C_RED, size=9),
                  annotation_position="top right")
    fig.update_layout(
        paper_bgcolor=C_SURFACE, plot_bgcolor=C_SURFACE,
        height=max(200, len(rfis) * 44),
        margin=dict(l=0, r=100, t=8, b=32),
        xaxis=dict(title="Days Open", gridcolor=C_GRID, tickfont=dict(color=C_SEC, size=10), zeroline=False, showline=False),
        yaxis=dict(tickfont=dict(color=C_INK, size=11), showline=False,
                   categoryorder="array", categoryarray=y_labels),
        showlegend=False,
    )
    return fig


def build_completion_chart():
    projs = sorted(PROJECTS, key=lambda p: p["pct"])
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[p["pct"] for p in projs], y=[p["short"] for p in projs],
        orientation="h",
        marker=dict(color=[C_AQUA if p["status"] == "closeout" else C_BLUE for p in projs],
                    line=dict(width=0)),
        text=[f'{p["pct"]}%' for p in projs], textposition="outside",
        textfont=dict(color=C_INK, size=11), cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{x:.1f}% complete<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor=C_SURFACE, plot_bgcolor=C_SURFACE,
        height=420, margin=dict(l=0, r=60, t=8, b=24),
        xaxis=dict(range=[0, 112], ticksuffix="%", gridcolor=C_GRID,
                   tickfont=dict(color=C_SEC, size=10), showline=False, zeroline=False),
        yaxis=dict(tickfont=dict(color=C_INK, size=11), showline=False),
        showlegend=False, bargap=0.32,
    )
    return fig

# ─── UI Components ─────────────────────────────────────────────────
def kpi_card(label, value, unit="", sub="", color=C_BLUE):
    return html.Div([
        html.Div(label, style={"fontSize":"10px","fontWeight":"600","letterSpacing":"0.07em",
                               "textTransform":"uppercase","color":C_SEC,"marginBottom":"6px"}),
        html.Div([
            html.Span(value, style={"fontSize":"30px","fontWeight":"700","color":color,"lineHeight":"1"}),
            html.Span(unit,  style={"fontSize":"13px","color":color,"marginLeft":"3px"}) if unit else None,
        ], style={"display":"flex","alignItems":"baseline"}),
        html.Div(sub, style={"fontSize":"11px","color":C_SEC,"marginTop":"4px"}),
    ], style={
        "background":"white","border":f"1px solid {C_GRID}","borderTop":f"3px solid {color}",
        "borderRadius":"6px","padding":"16px 18px","flex":"1","minWidth":"0",
    })


def rfi_card(r):
    col = rfi_color(r["days"])
    disc_bg, disc_fg = {
        "Structural": ("#e8f0fe", C_BLUE), "Architectural": ("#f3e8ff", C_VIOLET),
        "MEP": ("#e8f8f1", C_AQUA), "Mechanical": ("#e8f8f1", C_AQUA),
        "Civil": ("#fff8e1", "#8d6e00"), "Electrical": ("#fce4ec", "#b71c1c"),
    }.get(r["disc"], ("#f0f0f0", C_SEC))
    return html.Div([
        html.Div(style={"width":"4px","background":col,"borderRadius":"3px 0 0 3px","flexShrink":"0"}),
        html.Div([
            html.Div([
                html.Span(r["id"], style={"fontWeight":"700","fontSize":"13px","color":C_INK,"marginRight":"8px"}),
                html.Span(r["disc"], style={"background":disc_bg,"color":disc_fg,"fontSize":"10px","fontWeight":"600",
                                            "padding":"2px 7px","borderRadius":"10px","marginRight":"8px"}),
                html.Span(rfi_label(r["days"]), style={"background":col+"22","color":col,"fontSize":"10px","fontWeight":"700",
                                                        "padding":"2px 7px","borderRadius":"10px"}),
                html.Span(f'{r["days"]}d open', style={"marginLeft":"auto","fontSize":"12px","fontWeight":"700","color":col}),
            ], style={"display":"flex","alignItems":"center","marginBottom":"4px"}),
            html.Div(r["subject"], style={"fontSize":"13px","color":C_INK,"marginBottom":"4px"}),
            html.Div(f'Ball in court: {r["bic"]}', style={"fontSize":"11px","color":C_SEC}),
        ], style={"flex":"1","minWidth":"0","padding":"12px 14px"}),
    ], style={"display":"flex","background":"white","border":f"1px solid {C_GRID}",
              "borderRadius":"6px","overflow":"hidden","marginBottom":"8px"})


def sub_card(s):
    overdue = s["days_late"] > 0
    status_col  = C_RED if s["status"] == "revise_resubmit" else C_YELLOW
    status_lbl  = "REVISE & RESUBMIT" if s["status"] == "revise_resubmit" else "PENDING REVIEW"
    return html.Div([
        html.Div([
            html.Span(s["id"], style={"fontWeight":"700","fontSize":"12px","color":C_INK,"marginRight":"8px"}),
            html.Span(s["spec"], style={"background":"#f0f0f0","color":C_SEC,"fontSize":"10px","fontWeight":"600",
                                        "padding":"2px 7px","borderRadius":"10px","marginRight":"8px"}),
            html.Span(status_lbl, style={"background":status_col+"22","color":status_col,"fontSize":"10px",
                                          "fontWeight":"700","padding":"2px 7px","borderRadius":"10px"}),
            html.Span(
                f'{s["days_late"]}d overdue' if overdue else f'Due in {-s["days_late"]}d',
                style={"marginLeft":"auto","fontSize":"11px","fontWeight":"700",
                       "color":C_RED if overdue else C_BLUE}
            ),
        ], style={"display":"flex","alignItems":"center","marginBottom":"5px"}),
        html.Div(s["desc"], style={"fontSize":"13px","color":C_INK}),
    ], style={"background":"white","border":f"1px solid {C_GRID}","borderRadius":"6px",
              "padding":"12px 14px","marginBottom":"8px"})


def project_card(p):
    pct = p["pct"]
    bar_col = C_AQUA if pct >= 95 else (C_BLUE if pct >= 70 else C_YELLOW)
    tb, tf = TYPE_COLORS.get(p["type"], ("#f0f0f0", C_SEC))
    return html.Button(
        [
            html.Div([
                html.Span(p["name"], style={"fontWeight":"700","fontSize":"12px","color":C_INK,
                                            "whiteSpace":"nowrap","overflow":"hidden","textOverflow":"ellipsis","flex":"1","minWidth":"0"}),
                html.Span(f'${p["value"]}M', style={"fontSize":"11px","fontWeight":"600","color":C_SEC,
                                                     "marginLeft":"6px","whiteSpace":"nowrap"}),
            ], style={"display":"flex","alignItems":"center","marginBottom":"7px"}),
            html.Div([
                html.Div(html.Div(style={"width":f"{pct}%","height":"100%","background":bar_col,"borderRadius":"3px"}),
                         style={"flex":"1","height":"6px","background":C_GRID,"borderRadius":"3px","overflow":"hidden"}),
                html.Span(f"{pct}%", style={"fontSize":"10px","fontWeight":"600","color":bar_col,"marginLeft":"6px"}),
            ], style={"display":"flex","alignItems":"center","marginBottom":"7px"}),
            html.Div([
                html.Span(f'{p["open_rfis"]} RFIs',
                          style={"background":"#fff3e0" if p["open_rfis"]>5 else "#f0f0f0",
                                 "color":C_ORANGE if p["open_rfis"]>5 else C_SEC,
                                 "fontSize":"10px","fontWeight":"600","padding":"2px 7px","borderRadius":"10px","marginRight":"5px"}),
                html.Span(f'{p["pending_subs"]} Subs',
                          style={"background":"#fffde7" if p["pending_subs"]>10 else "#f0f0f0",
                                 "color":C_YELLOW if p["pending_subs"]>10 else C_SEC,
                                 "fontSize":"10px","fontWeight":"600","padding":"2px 7px","borderRadius":"10px","marginRight":"5px"}),
                html.Span(p["type"].capitalize(),
                          style={"background":tb,"color":tf,"fontSize":"10px","fontWeight":"600",
                                 "padding":"2px 7px","borderRadius":"10px"}),
            ], style={"display":"flex","flexWrap":"wrap","gap":"3px"}),
        ],
        id={"type":"proj-card-btn","index":p["id"]},
        n_clicks=0,
        style={"width":"calc(50% - 8px)","display":"inline-block","background":"white",
               "border":f"1px solid {C_GRID}","borderRadius":"6px","padding":"12px 14px",
               "cursor":"pointer","textAlign":"left","marginRight":"8px","marginBottom":"12px",
               "verticalAlign":"top"},
    )


def section_hd(text):
    return html.Div(text, style={"fontSize":"11px","fontWeight":"700","letterSpacing":"0.08em",
                                  "textTransform":"uppercase","color":C_SEC,
                                  "marginBottom":"12px","marginTop":"4px"})

# ─── Views ──────────────────────────────────────────────────────────
def portfolio_view():
    total_val  = sum(p["value"] for p in PROJECTS if p["status"]=="active")
    total_rfis = sum(p["open_rfis"] for p in PROJECTS)
    total_subs = sum(p["pending_subs"] for p in PROJECTS)
    active_pts = [p["pct"] for p in PROJECTS if p["status"]=="active"]
    avg_pct    = sum(active_pts) / len(active_pts)
    critical   = sum(1 for r in RFIS if r["days"]>21)

    return html.Div([
        # KPIs
        html.Div([
            kpi_card("Active Projects",    "10",            "",  f"${total_val}M total value",       C_BLUE),
            kpi_card("Open RFIs",          str(total_rfis), "",  f"{critical} critical (>21d)",       C_ORANGE),
            kpi_card("Pending Submittals", str(total_subs), "",  "Awaiting architect review",         C_YELLOW),
            kpi_card("Avg % Complete",     f"{avg_pct:.1f}","%" ,"Active portfolio",                 C_GOOD),
        ], style={"display":"flex","gap":"12px","marginBottom":"20px"}),

        # Gantt
        html.Div([
            section_hd("Project Schedule Timeline — click a bar to open project detail"),
            html.Div([
                html.Span(style={"display":"inline-block","width":"10px","height":"10px","borderRadius":"2px","background":C_BLUE,"marginRight":"5px","verticalAlign":"middle"}),
                html.Span("Active", style={"fontSize":"11px","color":C_SEC,"marginRight":"14px"}),
                html.Span(style={"display":"inline-block","width":"10px","height":"10px","borderRadius":"2px","background":C_AQUA,"marginRight":"5px","verticalAlign":"middle"}),
                html.Span("Closeout", style={"fontSize":"11px","color":C_SEC}),
            ], style={"marginBottom":"8px"}),
            dcc.Graph(id="gantt-chart", figure=build_gantt(), config={"displayModeBar":False}),
        ], style={"background":"white","border":f"1px solid {C_GRID}","borderRadius":"6px",
                  "padding":"16px 20px","marginBottom":"20px"}),

        # % Complete bar chart
        html.Div([
            section_hd("Portfolio Completion"),
            dcc.Graph(id="completion-chart", figure=build_completion_chart(), config={"displayModeBar":False}),
        ], style={"background":"white","border":f"1px solid {C_GRID}","borderRadius":"6px",
                  "padding":"16px 20px","marginBottom":"20px"}),

        # Project cards
        html.Div([
            section_hd("All Projects — click any card for details"),
            html.Div([project_card(p) for p in sorted(PROJECTS, key=lambda x: x["value"], reverse=True)]),
        ], style={"background":"white","border":f"1px solid {C_GRID}","borderRadius":"6px","padding":"16px 20px"}),
    ], style={"padding":"24px","overflowY":"auto","flex":"1"})


def detail_view(pid):
    p = PROJ_BY_ID.get(pid)
    if not p:
        return html.Div("Project not found.")

    proj_rfis = sorted([r for r in RFIS       if r["pid"]==pid], key=lambda x: x["days"], reverse=True)
    proj_subs = sorted([s for s in SUBMITTALS  if s["pid"]==pid], key=lambda x: x["days_late"], reverse=True)
    critical    = sum(1 for r in proj_rfis if r["days"]>21)
    overdue_sub = sum(1 for s in proj_subs if s["days_late"]>0)
    tb, tf = TYPE_COLORS.get(p["type"], ("#f0f0f0", C_SEC))
    status_col = C_AQUA if p["status"]=="closeout" else C_BLUE

    return html.Div([
        # Breadcrumb
        html.Div([
            html.Button("◀ All Projects", id="back-to-portfolio", n_clicks=0,
                        style={"background":"none","border":"none","color":C_BLUE,"fontSize":"13px",
                               "fontWeight":"600","cursor":"pointer","padding":"0","marginRight":"8px"}),
            html.Span("›", style={"color":C_MUTED,"marginRight":"8px"}),
            html.Span(p["short"], style={"color":C_INK,"fontSize":"13px","fontWeight":"600"}),
        ], style={"display":"flex","alignItems":"center","marginBottom":"16px"}),

        # Header
        html.Div([
            html.Div([
                html.Div([
                    html.Span(p["name"], style={"fontSize":"20px","fontWeight":"700","color":C_INK,"marginRight":"12px"}),
                    html.Span(p["type"].capitalize(), style={"background":tb,"color":tf,"fontSize":"10px","fontWeight":"700",
                                                             "padding":"3px 10px","borderRadius":"12px","marginRight":"8px"}),
                    html.Span(p["status"].upper(), style={"background":status_col+"22","color":status_col,"fontSize":"10px",
                                                          "fontWeight":"700","padding":"3px 10px","borderRadius":"12px"}),
                ], style={"display":"flex","alignItems":"center","flexWrap":"wrap","gap":"4px","marginBottom":"8px"}),
                html.Div([
                    html.Span(f'PM: {p["pm"]}', style={"fontSize":"12px","color":C_SEC,"marginRight":"20px"}),
                    html.Span(f'Supt: {p["super"]}', style={"fontSize":"12px","color":C_SEC,"marginRight":"20px"}),
                    html.Span(f'{p["start"]} to {p["end"]}', style={"fontSize":"12px","color":C_SEC}),
                ]),
            ], style={"flex":"1"}),
            html.Div([
                html.Div(f'${p["value"]}M', style={"fontSize":"26px","fontWeight":"700","color":C_BLUE,"lineHeight":"1"}),
                html.Div("Contract Value", style={"fontSize":"10px","color":C_SEC,"textTransform":"uppercase","letterSpacing":"0.06em"}),
            ], style={"textAlign":"right","marginLeft":"24px"}),
        ], style={"display":"flex","alignItems":"flex-start","background":"white",
                  "border":f"1px solid {C_GRID}","borderRadius":"6px","padding":"18px 20px","marginBottom":"16px"}),

        # KPIs
        html.Div([
            kpi_card("% Complete",        f'{p["pct"]}', "%", "Closeout" if p["status"]=="closeout" else "Active", C_AQUA if p["pct"]>=95 else C_BLUE),
            kpi_card("Open RFIs",         str(len(proj_rfis)), "", f'{critical} critical (>21d)', C_RED if critical else C_GOOD),
            kpi_card("Pending Submittals",str(len(proj_subs)), "", f'{overdue_sub} overdue', C_ORANGE if overdue_sub else C_GOOD),
            kpi_card("Oldest RFI",        str(proj_rfis[0]["days"]) if proj_rfis else "0", "d",
                     proj_rfis[0]["id"] if proj_rfis else "—",
                     C_RED if proj_rfis and proj_rfis[0]["days"]>21 else C_BLUE),
        ], style={"display":"flex","gap":"12px","marginBottom":"20px"}),

        # RFI scatter
        html.Div([
            section_hd(f'RFI Age Chart — {len(proj_rfis)} Open RFI{"s" if len(proj_rfis)!=1 else ""}'),
            dcc.Graph(figure=build_rfi_scatter(pid), config={"displayModeBar":False}),
        ], style={"background":"white","border":f"1px solid {C_GRID}","borderRadius":"6px",
                  "padding":"16px 20px","marginBottom":"20px"}),

        # RFIs + Submittals side by side
        html.Div([
            # RFIs column
            html.Div([
                section_hd(f'Open RFIs ({len(proj_rfis)})'),
                html.Div([rfi_card(r) for r in proj_rfis]) if proj_rfis else
                html.Div([
                    html.Span("✓ No open RFIs", style={"fontSize":"14px","color":C_GOOD,"fontWeight":"600"}),
                ], style={"background":C_GOOD+"11","border":f"1px solid {C_GOOD}44","borderRadius":"6px",
                          "padding":"16px","display":"flex","alignItems":"center"}),
            ], style={"flex":"1","minWidth":"0"}),

            html.Div(style={"width":"20px","flexShrink":"0"}),

            # Submittals column
            html.Div([
                section_hd(f'Pending Submittals ({len(proj_subs)})'),
                html.Div([sub_card(s) for s in proj_subs]) if proj_subs else
                html.Div([
                    html.Span("✓ All submittals current", style={"fontSize":"14px","color":C_GOOD,"fontWeight":"600"}),
                ], style={"background":C_GOOD+"11","border":f"1px solid {C_GOOD}44","borderRadius":"6px",
                          "padding":"16px","display":"flex","alignItems":"center"}),
            ], style={"flex":"1","minWidth":"0"}),
        ], style={"display":"flex","alignItems":"flex-start"}),
    ], style={"padding":"24px","overflowY":"auto","flex":"1"})


# ─── Sidebar ───────────────────────────────────────────────────────
def sidebar_content(selected_pid=None):
    rows = []
    for p in sorted(PROJECTS, key=lambda x: x["value"], reverse=True):
        active = selected_pid == p["id"]
        has_critical = any(r["days"]>21 for r in RFIS if r["pid"]==p["id"])
        dot_col = C_RED if has_critical else (C_YELLOW if p["open_rfis"]>0 else C_GOOD)
        rows.append(html.Button(
            [
                html.Div(style={"width":"7px","height":"7px","borderRadius":"50%","background":dot_col,
                                "marginRight":"9px","flexShrink":"0","marginTop":"3px"}),
                html.Div([
                    html.Div(p["short"], style={"fontSize":"12px","fontWeight":"700" if active else "500",
                                                "color":C_BLUE if active else C_INK,"lineHeight":"1.3"}),
                    html.Div(f'${p["value"]}M · {p["open_rfis"]} RFI{"s" if p["open_rfis"]!=1 else ""}',
                             style={"fontSize":"10px","color":C_SEC,"marginTop":"1px"}),
                ], style={"flex":"1","textAlign":"left"}),
            ],
            id={"type":"sidebar-proj-btn","index":p["id"]},
            n_clicks=0,
            style={"display":"flex","alignItems":"flex-start","width":"100%","border":"none",
                   "borderRadius":"5px","padding":"8px 10px","cursor":"pointer","marginBottom":"2px",
                   "background":C_BLUE+"11" if active else "transparent",
                   "borderLeft":f"3px solid {C_BLUE}" if active else "3px solid transparent"},
        ))
    return rows

# ─── App layout ────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    title="Huvibar | Project Tracking",
    suppress_callback_exceptions=True,
    meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1"}],
)

app.layout = html.Div([
    dcc.Store(id="selected-project", data=None),

    # Header
    html.Div([
        html.Span("🏗️", style={"marginRight":"10px","fontSize":"18px"}),
        html.Span("HUVIBAR CONSTRUCTION", style={"fontSize":"15px","fontWeight":"800",
                                                   "letterSpacing":"0.05em","color":"white","marginRight":"14px"}),
        html.Span("Project Tracking & Field Management", style={"fontSize":"12px","color":"rgba(255,255,255,0.6)"}),
        html.Div([
            html.Div(style={"width":"7px","height":"7px","borderRadius":"50%","background":C_GOOD,
                            "marginRight":"5px","boxShadow":f"0 0 5px {C_GOOD}"}),
            html.Span("LIVE", style={"fontSize":"9px","fontWeight":"700","letterSpacing":"0.1em","color":C_GOOD}),
        ], style={"display":"flex","alignItems":"center","marginLeft":"auto"}),
    ], style={"background":"#111111","borderBottom":f"2px solid {C_BLUE}","padding":"12px 20px",
              "display":"flex","alignItems":"center","flexShrink":"0"}),

    # Body: sidebar + main
    html.Div([
        # Sidebar
        html.Div([
            html.Div("PROJECTS", style={"fontSize":"9px","fontWeight":"700","letterSpacing":"0.12em",
                                         "color":C_MUTED,"padding":"12px 12px 6px","textTransform":"uppercase"}),
            html.Div([
                html.Div([html.Div(style={"width":"7px","height":"7px","borderRadius":"50%","background":C_RED,"marginRight":"6px"}),
                          html.Span("Critical RFI", style={"fontSize":"9px","color":C_MUTED})],
                         style={"display":"flex","alignItems":"center","marginBottom":"3px"}),
                html.Div([html.Div(style={"width":"7px","height":"7px","borderRadius":"50%","background":C_YELLOW,"marginRight":"6px"}),
                          html.Span("Open RFIs", style={"fontSize":"9px","color":C_MUTED})],
                         style={"display":"flex","alignItems":"center","marginBottom":"3px"}),
                html.Div([html.Div(style={"width":"7px","height":"7px","borderRadius":"50%","background":C_GOOD,"marginRight":"6px"}),
                          html.Span("On track", style={"fontSize":"9px","color":C_MUTED})],
                         style={"display":"flex","alignItems":"center"}),
            ], style={"padding":"0 12px 10px","borderBottom":f"1px solid {C_GRID}","marginBottom":"6px"}),
            html.Div(id="sidebar-list", children=sidebar_content(),
                     style={"overflowY":"auto","flex":"1","padding":"0 8px 16px"}),
        ], style={"width":"210px","flexShrink":"0","background":"white","borderRight":f"1px solid {C_GRID}",
                  "display":"flex","flexDirection":"column","overflowY":"hidden"}),

        # Main content
        html.Div(id="main-content", children=portfolio_view(),
                 style={"flex":"1","overflowY":"auto","background":C_SURFACE}),
    ], style={"display":"flex","flex":"1","overflow":"hidden"}),

], style={"fontFamily":FONT,"background":C_SURFACE,"height":"100vh","display":"flex",
          "flexDirection":"column","overflow":"hidden"})


# ─── Callbacks ─────────────────────────────────────────────────────

@app.callback(
    Output("selected-project","data"),
    Input({"type":"sidebar-proj-btn","index":ALL},"n_clicks"),
    State({"type":"sidebar-proj-btn","index":ALL},"id"),
    prevent_initial_call=True,
)
def sidebar_click(clicks, ids):
    triggered = ctx.triggered_id
    if triggered and isinstance(triggered, dict):
        return triggered["index"]
    return dash.no_update


@app.callback(
    Output("selected-project","data",allow_duplicate=True),
    Input({"type":"proj-card-btn","index":ALL},"n_clicks"),
    State({"type":"proj-card-btn","index":ALL},"id"),
    prevent_initial_call=True,
)
def card_click(clicks, ids):
    triggered = ctx.triggered_id
    if triggered and isinstance(triggered, dict):
        return triggered["index"]
    return dash.no_update


@app.callback(
    Output("selected-project","data",allow_duplicate=True),
    Input("gantt-chart","clickData"),
    prevent_initial_call=True,
)
def gantt_click(click_data):
    if not click_data:
        return dash.no_update
    try:
        label = click_data["points"][0]["y"]
        for p in PROJECTS:
            if p["short"] == label:
                return p["id"]
    except (KeyError, IndexError):
        pass
    return dash.no_update


@app.callback(
    Output("selected-project","data",allow_duplicate=True),
    Input("back-to-portfolio","n_clicks"),
    prevent_initial_call=True,
)
def go_back(n):
    if n:
        return None
    return dash.no_update


@app.callback(
    Output("main-content","children"),
    Input("selected-project","data"),
)
def render_main(pid):
    return detail_view(pid) if pid else portfolio_view()


@app.callback(
    Output("sidebar-list","children"),
    Input("selected-project","data"),
)
def update_sidebar(pid):
    return sidebar_content(pid)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
