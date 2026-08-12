# =============================================================================
# Huvibar Construction — Project Tracking & Field Management
# Dash application — connects to Databricks SQL for live project data
# =============================================================================

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date

# -----------------------------------------------------------------------------
# SEED DATA — replace each block with a live Databricks SQL query
# TODO: Connect to Databricks SQL warehouse
#   warehouse_id = os.environ.get("DATABRICKS_WAREHOUSE_ID", "f5a185ab7f9f1e9f")
# -----------------------------------------------------------------------------

# TODO: Query css_genie.project_tracking.projects WHERE status IN ('active','closeout')
PROJECTS = [
    {"name": "Colorado Convention Center Expansion", "value": 150, "pct": 94.9, "status": "active",   "type": "commercial",     "open_rfis": 11, "max_rfi_age": 1528, "pending_submittals": 18},
    {"name": "Broomfield Semiconductor Fab",          "value": 135, "pct": 76.3, "status": "active",   "type": "industrial",     "open_rfis": 10, "max_rfi_age":  703, "pending_submittals": 18},
    {"name": "Denver Airport Terminal Upgrade",       "value": 120, "pct": 94.9, "status": "active",   "type": "commercial",     "open_rfis": 15, "max_rfi_age":  833, "pending_submittals": 14},
    {"name": "Englewood Mixed-Use Development",       "value":  88, "pct": 94.9, "status": "active",   "type": "commercial",     "open_rfis": 11, "max_rfi_age":  996, "pending_submittals": 17},
    {"name": "Parker Senior Living Campus",           "value":  61, "pct": 94.9, "status": "active",   "type": "healthcare",     "open_rfis": 12, "max_rfi_age": 1174, "pending_submittals": 18},
    {"name": "Westminster High School",               "value":  52, "pct": 97.7, "status": "closeout", "type": "education",      "open_rfis":  0, "max_rfi_age":    0, "pending_submittals": 10},
    {"name": "Loveland Logistics Hub",                "value":  45, "pct": 94.9, "status": "active",   "type": "industrial",     "open_rfis": 15, "max_rfi_age": 1253, "pending_submittals": 23},
    {"name": "Aurora VA Medical Clinic",              "value":  42, "pct": 94.9, "status": "active",   "type": "healthcare",     "open_rfis": 10, "max_rfi_age":  839, "pending_submittals": 15},
    {"name": "Rocky Flats Remediation Facility",      "value":  38, "pct": 94.9, "status": "active",   "type": "industrial",     "open_rfis":  9, "max_rfi_age": 1294, "pending_submittals": 14},
    {"name": "Castle Rock Municipal Building",        "value":  24, "pct": 94.9, "status": "active",   "type": "government",     "open_rfis":  9, "max_rfi_age":  973, "pending_submittals": 20},
    {"name": "Centennial Airport Hangar",             "value":  19, "pct": 94.9, "status": "active",   "type": "infrastructure", "open_rfis":  5, "max_rfi_age":  748, "pending_submittals": 18},
    {"name": "Brighton Solar Farm O&M",               "value":  15, "pct": 97.5, "status": "closeout", "type": "industrial",     "open_rfis":  0, "max_rfi_age":    0, "pending_submittals":  8},
]

# TODO: Query css_genie.project_tracking.rfis WHERE status = 'open' ORDER BY days_open DESC
RFIS = [
    {"id": "RFI-0892", "project": "Denver Airport Terminal Upgrade",       "discipline": "Structural",   "subject": "Beam splice detail at column B-12 curtain wall interface",  "days_open": 47, "ball_in_court": "Structural Engineer"},
    {"id": "RFI-0856", "project": "Colorado Convention Center Expansion",  "discipline": "Architectural","subject": "Expansion joint cover assembly at concourse level",           "days_open": 38, "ball_in_court": "Architect"},
    {"id": "RFI-0871", "project": "Parker Senior Living Campus",           "discipline": "MEP",          "subject": "Medical gas outlet locations - Floor 3 nursing wing",         "days_open": 34, "ball_in_court": "MEP Engineer"},
    {"id": "RFI-0901", "project": "Loveland Logistics Hub",                "discipline": "Civil",        "subject": "Truck court drainage slope at dock 7-12",                     "days_open": 29, "ball_in_court": "Civil Engineer"},
    {"id": "RFI-0876", "project": "Broomfield Semiconductor Fab",          "discipline": "Structural",   "subject": "Overhead crane runway beam camber requirement",                "days_open": 22, "ball_in_court": "Structural Engineer"},
    {"id": "RFI-0915", "project": "Rocky Flats Remediation Facility",      "discipline": "Mechanical",   "subject": "Exhaust fan interlock sequence with fire dampers",             "days_open": 18, "ball_in_court": "MEP Engineer"},
    {"id": "RFI-0923", "project": "Aurora VA Medical Clinic",              "discipline": "Architectural","subject": "Accessible route at main entry - slope compliance",             "days_open": 14, "ball_in_court": "Architect"},
    {"id": "RFI-0934", "project": "Castle Rock Municipal Building",        "discipline": "Electrical",   "subject": "Emergency power transfer switch coordination",                 "days_open": 11, "ball_in_court": "Electrical Engineer"},
    {"id": "RFI-0941", "project": "Englewood Mixed-Use Development",       "discipline": "Architectural","subject": "Curtain wall head condition at Level 14",                      "days_open":  8, "ball_in_court": "Huvibar GC"},
    {"id": "RFI-0947", "project": "Centennial Airport Hangar",             "discipline": "Structural",   "subject": "Hangar door track anchorage detail",                           "days_open":  5, "ball_in_court": "Structural Engineer"},
]

# TODO: Query css_genie.project_tracking.schedules for start/end/health per project
SCHEDULE = [
    {"name": "Colorado Convention Center Expansion", "start": "2022-05-01", "end": "2025-12-15", "status": "active"},
    {"name": "Broomfield Semiconductor Fab",          "start": "2024-06-01", "end": "2027-01-31", "status": "active"},
    {"name": "Denver Airport Terminal Upgrade",       "start": "2023-11-01", "end": "2026-06-30", "status": "active"},
    {"name": "Englewood Mixed-Use Development",       "start": "2023-09-01", "end": "2026-03-31", "status": "active"},
    {"name": "Parker Senior Living Campus",           "start": "2023-03-01", "end": "2025-09-30", "status": "active"},
    {"name": "Westminster High School",               "start": "2022-09-01", "end": "2024-11-30", "status": "closeout"},
    {"name": "Loveland Logistics Hub",                "start": "2023-01-01", "end": "2025-03-31", "status": "active"},
    {"name": "Aurora VA Medical Clinic",              "start": "2024-01-01", "end": "2026-01-31", "status": "active"},
    {"name": "Rocky Flats Remediation Facility",      "start": "2022-11-01", "end": "2025-04-30", "status": "active"},
    {"name": "Castle Rock Municipal Building",        "start": "2023-05-01", "end": "2025-02-28", "status": "active"},
    {"name": "Centennial Airport Hangar",             "start": "2024-03-01", "end": "2025-08-31", "status": "active"},
    {"name": "Brighton Solar Farm O&M",               "start": "2023-07-01", "end": "2024-10-31", "status": "closeout"},
]

# -----------------------------------------------------------------------------
# Palette
# -----------------------------------------------------------------------------
C_BLUE     = "#2a78d6"
C_AQUA     = "#1baf7a"
C_YELLOW   = "#eda100"
C_RED      = "#e34948"
C_ORANGE   = "#eb6834"
C_VIOLET   = "#4a3aa7"
C_SURFACE  = "#fcfcfb"
C_INK      = "#0b0b0b"
C_SECONDARY= "#52514e"
C_GRID     = "#e1e0d9"
C_GOOD     = "#0ca30c"
C_WARN     = "#eda100"
C_CRIT     = "#e34948"

TODAY = "2026-08-11"

# -----------------------------------------------------------------------------
# Derived / computed constants
# -----------------------------------------------------------------------------
active_projects  = [p for p in PROJECTS if p["status"] == "active"]
total_value      = sum(p["value"] for p in active_projects)
total_open_rfis  = sum(p["open_rfis"] for p in PROJECTS)
total_submittals = sum(p["pending_submittals"] for p in PROJECTS)
avg_pct_complete = sum(p["pct"] for p in active_projects) / len(active_projects)

# Short names for charts (≤30 chars)
def short_name(name):
    mapping = {
        "Colorado Convention Center Expansion": "Convention Center Exp.",
        "Broomfield Semiconductor Fab":          "Broomfield Semi Fab",
        "Denver Airport Terminal Upgrade":       "Denver Airport Terminal",
        "Englewood Mixed-Use Development":       "Englewood Mixed-Use",
        "Parker Senior Living Campus":           "Parker Senior Living",
        "Westminster High School":               "Westminster High School",
        "Loveland Logistics Hub":                "Loveland Logistics Hub",
        "Aurora VA Medical Clinic":              "Aurora VA Clinic",
        "Rocky Flats Remediation Facility":      "Rocky Flats Remediation",
        "Castle Rock Municipal Building":        "Castle Rock Municipal",
        "Centennial Airport Hangar":             "Centennial Hangar",
        "Brighton Solar Farm O&M":               "Brighton Solar O&M",
    }
    return mapping.get(name, name[:28])

def rfi_color(days):
    if days > 21:   return C_RED
    if days >= 14:  return C_ORANGE
    if days >= 7:   return C_YELLOW
    return C_BLUE

def rfi_urgency_label(days):
    if days > 21:   return "Critical"
    if days >= 14:  return "High"
    if days >= 7:   return "Elevated"
    return "Watch"

# -----------------------------------------------------------------------------
# Chart builders
# -----------------------------------------------------------------------------

def build_project_health_chart():
    projects_sorted = sorted(PROJECTS, key=lambda p: p["pct"])
    names   = [short_name(p["name"]) for p in projects_sorted]
    pcts    = [p["pct"] for p in projects_sorted]
    colors  = [C_AQUA if p["status"] == "closeout" else C_BLUE for p in projects_sorted]
    labels  = [f"{p['pct']}%" for p in projects_sorted]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=pcts,
        y=names,
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=labels,
        textposition="outside",
        textfont=dict(color=C_INK, size=11, family="Inter, system-ui, sans-serif"),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}% complete<extra></extra>",
        cliponaxis=False,
    ))

    fig.update_layout(
        paper_bgcolor=C_SURFACE,
        plot_bgcolor=C_SURFACE,
        height=420,
        margin=dict(l=0, r=60, t=16, b=32),
        xaxis=dict(
            range=[0, 110],
            ticksuffix="%",
            gridcolor=C_GRID,
            tickfont=dict(color=C_SECONDARY, size=10),
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(color=C_INK, size=11, family="Inter, system-ui, sans-serif"),
            showline=False,
            ticklabelposition="outside left",
        ),
        showlegend=False,
        bargap=0.35,
    )
    return fig


def build_rfi_scatter():
    rfis_sorted = sorted(RFIS, key=lambda r: r["days_open"], reverse=True)

    x_vals     = [r["days_open"] for r in rfis_sorted]
    y_vals     = [short_name(r["project"]) for r in rfis_sorted]
    colors     = [rfi_color(r["days_open"]) for r in rfis_sorted]
    urgencies  = [rfi_urgency_label(r["days_open"]) for r in rfis_sorted]
    rfi_ids    = [r["id"] for r in rfis_sorted]
    subjects   = [r["subject"] for r in rfis_sorted]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="markers+text",
        marker=dict(
            size=20,
            color=colors,
            opacity=0.9,
            line=dict(width=1.5, color="white"),
        ),
        text=[f"  {r['id']}" for r in rfis_sorted],
        textposition="middle right",
        textfont=dict(color=C_INK, size=10, family="Inter, system-ui, sans-serif"),
        customdata=list(zip(rfi_ids, subjects, urgencies)),
        hovertemplate=(
            "<b>%{customdata[0]}</b> — %{customdata[2]}<br>"
            "%{y}<br>"
            "<i>%{customdata[1]}</i><br>"
            "<b>%{x} days open</b><extra></extra>"
        ),
    ))

    # Reference line at 21 days
    fig.add_vline(
        x=21,
        line=dict(color=C_RED, width=1.5, dash="dot"),
        annotation_text="21-day threshold",
        annotation_font=dict(color=C_RED, size=10),
        annotation_position="top right",
    )

    fig.update_layout(
        paper_bgcolor=C_SURFACE,
        plot_bgcolor=C_SURFACE,
        height=340,
        margin=dict(l=0, r=80, t=16, b=32),
        xaxis=dict(
            title=dict(text="Days Open", font=dict(color=C_SECONDARY, size=11)),
            gridcolor=C_GRID,
            tickfont=dict(color=C_SECONDARY, size=10),
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            tickfont=dict(color=C_INK, size=11, family="Inter, system-ui, sans-serif"),
            showline=False,
            categoryorder="array",
            categoryarray=y_vals,
        ),
        showlegend=False,
    )
    return fig


def build_gantt():
    df = pd.DataFrame(SCHEDULE)
    df["Color"] = df["status"].map({"active": C_BLUE, "closeout": C_AQUA})
    df["Short"]  = df["name"].apply(short_name)
    df = df.sort_values("start", ascending=False)

    fig = px.timeline(
        df,
        x_start="start",
        x_end="end",
        y="Short",
        color="status",
        color_discrete_map={"active": C_BLUE, "closeout": C_AQUA},
    )

    # Today line
    fig.add_vline(
        x=TODAY,
        line=dict(color=C_RED, width=2, dash="dash"),
        annotation_text=f"Today ({TODAY})",
        annotation_font=dict(color=C_RED, size=10),
        annotation_position="top left",
    )

    fig.update_traces(
        marker=dict(line=dict(width=0)),
        opacity=0.88,
        hovertemplate="<b>%{y}</b><br>%{x|%b %Y} → %{base|%b %Y}<extra></extra>",
    )

    fig.update_layout(
        paper_bgcolor=C_SURFACE,
        plot_bgcolor=C_SURFACE,
        height=440,
        margin=dict(l=0, r=16, t=16, b=40),
        xaxis=dict(
            gridcolor=C_GRID,
            tickfont=dict(color=C_SECONDARY, size=10),
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(color=C_INK, size=11, family="Inter, system-ui, sans-serif"),
            showline=False,
            title=None,
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="left",
            x=0,
            font=dict(color=C_SECONDARY, size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    return fig


# -----------------------------------------------------------------------------
# Component builders
# -----------------------------------------------------------------------------

def kpi_tile(label, value, unit, subtext, accent):
    return dbc.Col(
        html.Div(
            [
                html.Div(label, style={
                    "fontSize": "10px",
                    "fontWeight": "600",
                    "letterSpacing": "0.08em",
                    "textTransform": "uppercase",
                    "color": C_SECONDARY,
                    "marginBottom": "6px",
                }),
                html.Div(
                    [
                        html.Span(value, style={
                            "fontSize": "32px",
                            "fontWeight": "700",
                            "color": accent,
                            "lineHeight": "1",
                        }),
                        html.Span(unit, style={
                            "fontSize": "14px",
                            "fontWeight": "500",
                            "color": accent,
                            "marginLeft": "3px",
                        }) if unit else None,
                    ],
                    style={"display": "flex", "alignItems": "baseline"},
                ),
                html.Div(subtext, style={
                    "fontSize": "11px",
                    "color": C_SECONDARY,
                    "marginTop": "4px",
                }),
            ],
            style={
                "background": "white",
                "border": f"1px solid {C_GRID}",
                "borderTop": f"3px solid {accent}",
                "borderRadius": "6px",
                "padding": "16px 20px",
            }
        ),
        md=3, sm=6, xs=12,
        class_name="mb-3",
    )


def project_card(p):
    pct = p["pct"]
    bar_color = C_AQUA if pct >= 95 else (C_BLUE if pct >= 70 else C_YELLOW)
    rfi_color_badge  = "#fff3e0" if p["open_rfis"] > 5  else "#f0f0f0"
    rfi_text_color   = C_ORANGE  if p["open_rfis"] > 5  else C_SECONDARY
    sub_color_badge  = "#fffde7" if p["pending_submittals"] > 10 else "#f0f0f0"
    sub_text_color   = C_YELLOW  if p["pending_submittals"] > 10 else C_SECONDARY
    type_colors = {
        "commercial":     ("#e8f0fe", C_BLUE),
        "industrial":     ("#f3e8ff", C_VIOLET),
        "healthcare":     ("#e8f8f1", C_AQUA),
        "education":      ("#fff8e1", C_YELLOW),
        "government":     ("#fce4ec", "#c62828"),
        "infrastructure": ("#e0f7fa", "#00838f"),
    }
    type_bg, type_fg = type_colors.get(p["type"], ("#f0f0f0", C_SECONDARY))

    return dbc.Col(
        html.Div(
            [
                html.Div(
                    [
                        html.Div(p["name"], style={
                            "fontWeight": "700",
                            "fontSize": "13px",
                            "color": C_INK,
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "flex": "1",
                            "minWidth": "0",
                        }),
                        html.Div(f"${p['value']}M", style={
                            "fontSize": "12px",
                            "fontWeight": "600",
                            "color": C_SECONDARY,
                            "whiteSpace": "nowrap",
                            "marginLeft": "8px",
                        }),
                    ],
                    style={"display": "flex", "alignItems": "center", "marginBottom": "8px"},
                ),
                # Progress bar
                html.Div(
                    [
                        html.Div(
                            html.Div(style={
                                "width": f"{pct}%",
                                "height": "100%",
                                "background": bar_color,
                                "borderRadius": "3px",
                                "transition": "width 0.3s ease",
                            }),
                            style={
                                "flex": "1",
                                "height": "7px",
                                "background": C_GRID,
                                "borderRadius": "3px",
                                "overflow": "hidden",
                            }
                        ),
                        html.Span(f"{pct}%", style={
                            "fontSize": "11px",
                            "fontWeight": "600",
                            "color": bar_color,
                            "marginLeft": "8px",
                            "whiteSpace": "nowrap",
                        }),
                    ],
                    style={"display": "flex", "alignItems": "center", "marginBottom": "8px"},
                ),
                # Badges
                html.Div(
                    [
                        html.Span(f"{p['open_rfis']} RFIs", style={
                            "background": rfi_color_badge,
                            "color": rfi_text_color,
                            "fontSize": "10px",
                            "fontWeight": "600",
                            "padding": "2px 7px",
                            "borderRadius": "10px",
                            "marginRight": "5px",
                        }),
                        html.Span(f"{p['pending_submittals']} Submittals", style={
                            "background": sub_color_badge,
                            "color": sub_text_color,
                            "fontSize": "10px",
                            "fontWeight": "600",
                            "padding": "2px 7px",
                            "borderRadius": "10px",
                            "marginRight": "5px",
                        }),
                        html.Span(p["type"].capitalize(), style={
                            "background": type_bg,
                            "color": type_fg,
                            "fontSize": "10px",
                            "fontWeight": "600",
                            "padding": "2px 7px",
                            "borderRadius": "10px",
                        }),
                    ],
                    style={"display": "flex", "flexWrap": "wrap", "gap": "3px"},
                ),
            ],
            style={
                "background": "white",
                "border": f"1px solid {C_GRID}",
                "borderRadius": "6px",
                "padding": "14px 16px",
                "height": "100%",
            }
        ),
        md=6, xs=12,
        class_name="mb-3",
    )


def rfi_card(rfi):
    color = rfi_color(rfi["days_open"])
    urgency = rfi_urgency_label(rfi["days_open"])
    disc_colors = {
        "Structural":    ("#e8f0fe", C_BLUE),
        "Architectural": ("#f3e8ff", C_VIOLET),
        "MEP":           ("#e8f8f1", C_AQUA),
        "Mechanical":    ("#e8f8f1", C_AQUA),
        "Civil":         ("#fff8e1", "#8d6e00"),
        "Electrical":    ("#fce4ec", "#b71c1c"),
    }
    disc_bg, disc_fg = disc_colors.get(rfi["discipline"], ("#f0f0f0", C_SECONDARY))

    return html.Div(
        [
            # Left color strip
            html.Div(style={
                "width": "4px",
                "background": color,
                "borderRadius": "3px 0 0 3px",
                "flexShrink": "0",
            }),
            # Content
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(rfi["id"], style={
                                "fontWeight": "700",
                                "fontSize": "13px",
                                "color": C_INK,
                                "marginRight": "8px",
                            }),
                            html.Span(rfi["discipline"], style={
                                "background": disc_bg,
                                "color": disc_fg,
                                "fontSize": "10px",
                                "fontWeight": "600",
                                "padding": "2px 7px",
                                "borderRadius": "10px",
                                "marginRight": "8px",
                            }),
                            html.Span(urgency, style={
                                "background": color + "22",
                                "color": color,
                                "fontSize": "10px",
                                "fontWeight": "700",
                                "padding": "2px 7px",
                                "borderRadius": "10px",
                            }),
                            html.Span(
                                f"{rfi['days_open']}d open",
                                style={
                                    "marginLeft": "auto",
                                    "fontSize": "12px",
                                    "fontWeight": "700",
                                    "color": color,
                                    "whiteSpace": "nowrap",
                                }
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center", "marginBottom": "4px"},
                    ),
                    html.Div(short_name(rfi["project"]), style={
                        "fontSize": "11px",
                        "color": C_SECONDARY,
                        "marginBottom": "3px",
                        "fontWeight": "500",
                    }),
                    html.Div(rfi["subject"], style={
                        "fontSize": "13px",
                        "color": C_INK,
                        "marginBottom": "5px",
                    }),
                    html.Div(f"Ball in court: {rfi['ball_in_court']}", style={
                        "fontSize": "11px",
                        "color": C_SECONDARY,
                    }),
                ],
                style={"flex": "1", "minWidth": "0"},
            ),
        ],
        style={
            "display": "flex",
            "background": "white",
            "border": f"1px solid {C_GRID}",
            "borderRadius": "6px",
            "overflow": "hidden",
            "marginBottom": "8px",
            "padding": "12px 16px 12px 0",
            "gap": "12px",
        }
    )


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    title="Huvibar | Project Tracking",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

# Precompute figures (static — replace with callbacks for live filtering)
fig_health = build_project_health_chart()
fig_rfi    = build_rfi_scatter()
fig_gantt  = build_gantt()

rfis_sorted = sorted(RFIS, key=lambda r: r["days_open"], reverse=True)
projects_by_value = sorted(PROJECTS, key=lambda p: p["value"], reverse=True)

app.layout = html.Div(
    [
        # ── Header ───────────────────────────────────────────────────────────
        html.Div(
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Span("🏗️", style={"marginRight": "10px", "fontSize": "22px"}),
                                    html.Span("HUVIBAR CONSTRUCTION", style={
                                        "fontSize": "18px",
                                        "fontWeight": "800",
                                        "letterSpacing": "0.05em",
                                        "color": "white",
                                        "marginRight": "14px",
                                    }),
                                    html.Span("Project Tracking & Field Management", style={
                                        "fontSize": "13px",
                                        "fontWeight": "400",
                                        "color": "rgba(255,255,255,0.65)",
                                    }),
                                ],
                                style={"display": "flex", "alignItems": "center"},
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div(style={
                                        "width": "8px",
                                        "height": "8px",
                                        "borderRadius": "50%",
                                        "background": C_GOOD,
                                        "marginRight": "6px",
                                        "boxShadow": f"0 0 6px {C_GOOD}",
                                    }),
                                    html.Span("LIVE", style={
                                        "fontSize": "10px",
                                        "fontWeight": "700",
                                        "letterSpacing": "0.1em",
                                        "color": C_GOOD,
                                    }),
                                ],
                                style={"display": "flex", "alignItems": "center"},
                            ),
                            width="auto",
                            style={"marginLeft": "auto"},
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                fluid=True,
                style={"padding": "0 24px"},
            ),
            style={
                "background": "#111111",
                "borderBottom": "2px solid #2a78d6",
                "padding": "14px 0",
            }
        ),

        # ── Body ─────────────────────────────────────────────────────────────
        dbc.Container(
            [
                # ── Portfolio KPIs ───────────────────────────────────────────
                dbc.Row(
                    [
                        kpi_tile("Active Projects",    "10",   "",  f"${total_value}M total value",      C_BLUE),
                        kpi_tile("Total Open RFIs",    str(total_open_rfis), "", "Across all projects", C_ORANGE),
                        kpi_tile("Pending Submittals", str(total_submittals), "", "Awaiting review",    C_YELLOW),
                        kpi_tile("Avg % Complete",     f"{avg_pct_complete:.1f}", "%", "Active portfolio", C_GOOD),
                    ],
                    className="mt-4 mb-2",
                ),

                # ── Tabs ─────────────────────────────────────────────────────
                dcc.Tabs(
                    id="main-tabs",
                    value="tab-health",
                    children=[
                        dcc.Tab(label="Project Health",   value="tab-health"),
                        dcc.Tab(label="RFI Tracker",      value="tab-rfi"),
                        dcc.Tab(label="Schedule Health",  value="tab-schedule"),
                    ],
                    style={"borderBottom": f"1px solid {C_GRID}"},
                    colors={"border": C_GRID, "primary": C_BLUE, "background": C_SURFACE},
                ),
                html.Div(id="tab-content", style={"paddingTop": "24px", "paddingBottom": "48px"}),
            ],
            fluid=True,
            style={"padding": "0 24px", "background": C_SURFACE, "minHeight": "calc(100vh - 60px)"},
        ),
    ],
    style={
        "fontFamily": "Inter, system-ui, -apple-system, sans-serif",
        "background": C_SURFACE,
        "minHeight": "100vh",
    }
)


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

@app.callback(Output("tab-content", "children"), Input("main-tabs", "value"))
def render_tab(tab):

    # ── Tab 1: Project Health ─────────────────────────────────────────────────
    if tab == "tab-health":
        return html.Div([
            # Section header
            html.Div("% Complete by Project", style={
                "fontSize": "14px",
                "fontWeight": "600",
                "color": C_SECONDARY,
                "letterSpacing": "0.04em",
                "textTransform": "uppercase",
                "marginBottom": "12px",
            }),

            # Legend
            html.Div(
                [
                    html.Span(style={
                        "display": "inline-block",
                        "width": "12px",
                        "height": "12px",
                        "borderRadius": "2px",
                        "background": C_BLUE,
                        "marginRight": "5px",
                    }),
                    html.Span("Active", style={"fontSize": "11px", "color": C_SECONDARY, "marginRight": "16px"}),
                    html.Span(style={
                        "display": "inline-block",
                        "width": "12px",
                        "height": "12px",
                        "borderRadius": "2px",
                        "background": C_AQUA,
                        "marginRight": "5px",
                    }),
                    html.Span("Closeout", style={"fontSize": "11px", "color": C_SECONDARY}),
                ],
                style={"display": "flex", "alignItems": "center", "marginBottom": "8px"},
            ),

            dcc.Graph(
                figure=fig_health,
                config={"displayModeBar": False},
                style={"marginBottom": "32px"},
            ),

            # Section header
            html.Div("Project Portfolio", style={
                "fontSize": "14px",
                "fontWeight": "600",
                "color": C_SECONDARY,
                "letterSpacing": "0.04em",
                "textTransform": "uppercase",
                "marginBottom": "16px",
            }),

            dbc.Row(
                [project_card(p) for p in projects_by_value],
                className="g-3",
            ),
        ])

    # ── Tab 2: RFI Tracker ────────────────────────────────────────────────────
    elif tab == "tab-rfi":
        return html.Div([
            # Urgency legend
            html.Div(
                [
                    html.Span("Urgency: ", style={"fontSize": "11px", "color": C_SECONDARY, "marginRight": "10px", "fontWeight": "600"}),
                    *[
                        html.Span(
                            [
                                html.Span(style={
                                    "display": "inline-block",
                                    "width": "10px",
                                    "height": "10px",
                                    "borderRadius": "50%",
                                    "background": color,
                                    "marginRight": "4px",
                                    "verticalAlign": "middle",
                                }),
                                html.Span(label, style={"fontSize": "11px", "color": C_SECONDARY, "marginRight": "14px"}),
                            ]
                        )
                        for label, color in [
                            ("Critical (>21d)", C_RED),
                            ("High (14–21d)",   C_ORANGE),
                            ("Elevated (7–13d)",C_YELLOW),
                            ("Watch (<7d)",     C_BLUE),
                        ]
                    ],
                ],
                style={"display": "flex", "alignItems": "center", "marginBottom": "12px"},
            ),

            dcc.Graph(
                figure=fig_rfi,
                config={"displayModeBar": False},
                style={"marginBottom": "32px"},
            ),

            html.Div("Open RFIs — Sorted by Age", style={
                "fontSize": "14px",
                "fontWeight": "600",
                "color": C_SECONDARY,
                "letterSpacing": "0.04em",
                "textTransform": "uppercase",
                "marginBottom": "16px",
            }),

            html.Div([rfi_card(r) for r in rfis_sorted]),
        ])

    # ── Tab 3: Schedule Health ────────────────────────────────────────────────
    elif tab == "tab-schedule":
        active_count   = sum(1 for s in SCHEDULE if s["status"] == "active")
        closeout_count = sum(1 for s in SCHEDULE if s["status"] == "closeout")

        return html.Div([
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(str(active_count), style={
                                "fontSize": "26px", "fontWeight": "700", "color": C_BLUE, "lineHeight": "1",
                            }),
                            html.Div("Active", style={
                                "fontSize": "10px", "fontWeight": "600", "color": C_SECONDARY,
                                "textTransform": "uppercase", "letterSpacing": "0.06em",
                            }),
                        ],
                        style={
                            "background": "white", "border": f"1px solid {C_GRID}",
                            "borderTop": f"3px solid {C_BLUE}", "borderRadius": "6px",
                            "padding": "12px 20px", "marginRight": "12px", "textAlign": "center",
                        }
                    ),
                    html.Div(
                        [
                            html.Div(str(closeout_count), style={
                                "fontSize": "26px", "fontWeight": "700", "color": C_AQUA, "lineHeight": "1",
                            }),
                            html.Div("Closeout", style={
                                "fontSize": "10px", "fontWeight": "600", "color": C_SECONDARY,
                                "textTransform": "uppercase", "letterSpacing": "0.06em",
                            }),
                        ],
                        style={
                            "background": "white", "border": f"1px solid {C_GRID}",
                            "borderTop": f"3px solid {C_AQUA}", "borderRadius": "6px",
                            "padding": "12px 20px", "textAlign": "center",
                        }
                    ),
                    html.Div(
                        [
                            html.Div(style={
                                "width": "10px", "height": "10px", "borderRadius": "50%",
                                "background": C_RED, "marginRight": "6px", "flexShrink": "0",
                            }),
                            html.Span("Dashed red line = today (2026-08-11)", style={
                                "fontSize": "11px", "color": C_SECONDARY,
                            }),
                        ],
                        style={
                            "display": "flex", "alignItems": "center", "marginLeft": "auto",
                            "background": "white", "border": f"1px solid {C_GRID}",
                            "borderRadius": "6px", "padding": "10px 16px",
                        }
                    ),
                ],
                style={"display": "flex", "alignItems": "center", "marginBottom": "20px"},
            ),

            dcc.Graph(
                figure=fig_gantt,
                config={"displayModeBar": False},
            ),

            html.Div(
                [
                    html.Div("Schedule Notes", style={
                        "fontSize": "12px", "fontWeight": "700", "color": C_INK, "marginBottom": "8px",
                    }),
                    *[
                        html.Div(
                            [
                                html.Span(style={
                                    "display": "inline-block",
                                    "width": "8px", "height": "8px", "borderRadius": "50%",
                                    "background": C_AQUA if s["status"] == "closeout" else C_BLUE,
                                    "marginRight": "8px", "flexShrink": "0",
                                }),
                                html.Span(short_name(s["name"]), style={
                                    "fontSize": "12px", "color": C_INK, "fontWeight": "500",
                                    "minWidth": "220px", "display": "inline-block",
                                }),
                                html.Span(
                                    f"{s['start']} → {s['end']}",
                                    style={"fontSize": "11px", "color": C_SECONDARY, "marginLeft": "8px"},
                                ),
                                html.Span(
                                    "CLOSEOUT" if s["status"] == "closeout" else "ACTIVE",
                                    style={
                                        "fontSize": "10px", "fontWeight": "700",
                                        "padding": "1px 6px", "borderRadius": "8px",
                                        "marginLeft": "10px",
                                        "background": C_AQUA + "22" if s["status"] == "closeout" else C_BLUE + "22",
                                        "color": C_AQUA if s["status"] == "closeout" else C_BLUE,
                                    }
                                ),
                            ],
                            style={
                                "display": "flex", "alignItems": "center",
                                "padding": "6px 0",
                                "borderBottom": f"1px solid {C_GRID}",
                            }
                        )
                        for s in sorted(SCHEDULE, key=lambda x: x["start"], reverse=True)
                    ],
                ],
                style={
                    "background": "white", "border": f"1px solid {C_GRID}",
                    "borderRadius": "6px", "padding": "16px 20px", "marginTop": "24px",
                }
            ),
        ])

    return html.Div("Select a tab.")


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
