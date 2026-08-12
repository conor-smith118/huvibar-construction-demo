# Databricks App: Huvibar Inventory & Materials Management
# Interactive procurement dashboard — sidebar navigation + PO drill-down

import json
from datetime import date

import dash
from dash import dcc, html, Input, Output, State, ALL, callback_context
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TODAY = date(2026, 8, 11)

C_BLUE    = "#2a78d6"
C_AQUA    = "#1baf7a"
C_YELLOW  = "#eda100"
C_RED     = "#e34948"
C_ORANGE  = "#eb6834"
C_VIOLET  = "#4a3aa7"
C_SURFACE = "#fcfcfb"
C_INK     = "#0b0b0b"
C_SECONDARY = "#52514e"
C_GRID    = "#e1e0d9"
C_GOOD    = "#0ca30c"
C_MUTED   = "#898781"
C_CHARCOAL = "#1a1a19"
C_BG      = "#f0f0ed"

FONT = "Inter, system-ui, sans-serif"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

PROJECTS = [
    {"id": "P013", "short": "Convention Center",   "name": "Colorado Convention Center Expansion"},
    {"id": "P025", "short": "Broomfield Fab",      "name": "Broomfield Semiconductor Fab"},
    {"id": "P022", "short": "DEN Terminal",        "name": "Denver Airport Terminal Upgrade"},
    {"id": "P021", "short": "Englewood Mixed-Use", "name": "Englewood Mixed-Use Development"},
    {"id": "P018", "short": "Parker Senior",       "name": "Parker Senior Living Campus"},
    {"id": "P015", "short": "Westminster HS",      "name": "Westminster High School"},
    {"id": "P017", "short": "Loveland Logistics",  "name": "Loveland Logistics Hub"},
    {"id": "P023", "short": "Aurora VA Clinic",    "name": "Aurora VA Medical Clinic"},
    {"id": "P016", "short": "Rocky Flats",         "name": "Rocky Flats Remediation Facility"},
    {"id": "P019", "short": "Castle Rock Muni",    "name": "Castle Rock Municipal Building"},
    {"id": "P024", "short": "Centennial Hangar",   "name": "Centennial Airport Hangar"},
    {"id": "P020", "short": "Brighton Solar",      "name": "Brighton Solar Farm O&M"},
]

POS = [
    # Convention Center (P013)
    {"id": "PO-13-001", "project_id": "P013", "vendor": "Commercial Metals Co",         "description": "Structural steel supply and fabrication",       "category": "material", "amount": 3676089, "received": 0,       "status": "open",    "order_date": "2023-03-21", "expected_delivery": "2023-05-07", "notes": "Partial delivery accepted; balance on hold pending RFI-0856 resolution"},
    {"id": "PO-13-002", "project_id": "P013", "vendor": "Siemens Building Technologies", "description": "HVAC controls and building automation system",    "category": "material", "amount":  807091, "received": 0,       "status": "open",    "order_date": "2023-03-25", "expected_delivery": "2023-05-18", "notes": "Long-lead controls package; submittals under review"},
    {"id": "PO-13-003", "project_id": "P013", "vendor": "Armstrong Flooring Inc",       "description": "Resilient flooring materials - Zone A",          "category": "material", "amount":  564251, "received": 0,       "status": "open",    "order_date": "2022-08-17", "expected_delivery": "2022-09-19", "notes": "Delivery window missed; vendor rescheduling"},
    {"id": "PO-13-004", "project_id": "P013", "vendor": "Forbo Flooring",               "description": "Resilient flooring materials - Zone B",          "category": "material", "amount":  743885, "received": 0,       "status": "open",    "order_date": "2022-09-25", "expected_delivery": "2022-10-08", "notes": "Awaiting color selection approval from owner"},
    {"id": "PO-13-005", "project_id": "P013", "vendor": "Colorado Ready Mix LLC",       "description": "Ready-mix concrete - elevated slabs Level 4-6",  "category": "material", "amount": 1341206, "received": 0,       "status": "open",    "order_date": "2022-10-12", "expected_delivery": "2022-11-27", "notes": "Placed on hold pending structural review"},
    # Rocky Flats (P016)
    {"id": "PO-16-001", "project_id": "P016", "vendor": "Barnhart Crane and Rigging",   "description": "Tower crane rental - foundation phase",          "category": "rental",   "amount":  375460, "received": 0,       "status": "open",    "order_date": "2022-11-19", "expected_delivery": "2022-12-05", "notes": "Crane availability delayed; remobilization scheduled"},
    {"id": "PO-16-002", "project_id": "P016", "vendor": "Tremco Roofing Materials",     "description": "Roofing membrane and insulation materials",       "category": "material", "amount":  126470, "received": 0,       "status": "open",    "order_date": "2022-11-29", "expected_delivery": "2022-12-31", "notes": "In transit from manufacturer"},
    {"id": "PO-16-003", "project_id": "P016", "vendor": "Vulcan Materials Co",          "description": "Aggregate base course and subbase materials",     "category": "material", "amount":  212549, "received": 0,       "status": "open",    "order_date": "2023-04-11", "expected_delivery": "2023-05-20", "notes": "Quarry supply disruption; alternative source identified"},
    # Parker Senior (P018)
    {"id": "PO-18-001", "project_id": "P018", "vendor": "RMT Engineering Inc",          "description": "Special inspections and materials testing",       "category": "service",  "amount":  124450, "received": 0,       "status": "open",    "order_date": "2023-03-26", "expected_delivery": "2023-04-06", "notes": "IBC required special inspection services"},
    {"id": "PO-18-002", "project_id": "P018", "vendor": "Terracon Consultants Inc",     "description": "Special inspections and materials testing",       "category": "service",  "amount":  149501, "received": 0,       "status": "open",    "order_date": "2023-05-14", "expected_delivery": "2023-05-19", "notes": "Concrete and steel inspection - ongoing through substantial completion"},
    {"id": "PO-18-003", "project_id": "P018", "vendor": "Mountain West Steel",          "description": "Miscellaneous metals and anchor bolts",           "category": "material", "amount":  255795, "received": 155210,  "status": "partial", "order_date": "2023-04-03", "expected_delivery": "2023-05-03", "notes": "Phase 1 delivered; Phase 2 anchors pending fabrication"},
    # Broomfield Fab (P025)
    {"id": "PO-25-001", "project_id": "P025", "vendor": "Kinetics Systems Inc",         "description": "Vibration isolation equipment for clean room",    "category": "material", "amount":  892000, "received": 0,       "status": "open",    "order_date": "2024-08-15", "expected_delivery": "2025-02-28", "notes": "24-week lead time; critical path item"},
    {"id": "PO-25-002", "project_id": "P025", "vendor": "M+W Group",                   "description": "Clean room air handling units",                   "category": "material", "amount": 1450000, "received": 0,       "status": "open",    "order_date": "2024-09-01", "expected_delivery": "2025-04-15", "notes": "Custom FAT required; delivery tied to electrical rough-in"},
    {"id": "PO-25-003", "project_id": "P025", "vendor": "Hilti Inc",                    "description": "Powder actuated fastening systems and anchors",   "category": "material", "amount":   78500, "received": 52000,   "status": "partial", "order_date": "2025-01-10", "expected_delivery": "2025-02-01", "notes": "Standard stock items; balance on will-call"},
    # Loveland (P017)
    {"id": "PO-17-001", "project_id": "P017", "vendor": "Nucor Building Systems",       "description": "Pre-engineered metal building system",            "category": "material", "amount": 2100000, "received": 1050000, "status": "partial", "order_date": "2023-02-15", "expected_delivery": "2023-06-30", "notes": "Phase 1 erected; Phase 2 panels delivery Q3"},
    {"id": "PO-17-002", "project_id": "P017", "vendor": "GrafTech International",       "description": "Dock leveler systems - 8 units",                  "category": "material", "amount":  184000, "received": 0,       "status": "open",    "order_date": "2023-05-01", "expected_delivery": "2023-08-15", "notes": "Awaiting dock pit dimensions confirmation"},
    # DEN Terminal (P022)
    {"id": "PO-22-001", "project_id": "P022", "vendor": "Kawneer Products",             "description": "Curtain wall and storefront systems",             "category": "material", "amount": 3200000, "received": 960000,  "status": "partial", "order_date": "2024-01-20", "expected_delivery": "2024-09-30", "notes": "Phase 1 fabricated; RFI-0892 must resolve before Phase 2 release"},
    {"id": "PO-22-002", "project_id": "P022", "vendor": "Otis Elevator Company",        "description": "Passenger elevator systems - 4 units",            "category": "material", "amount":  980000, "received": 0,       "status": "open",    "order_date": "2024-02-10", "expected_delivery": "2025-01-15", "notes": "Long-lead; factory witness test scheduled Oct 2024"},
]

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def _proj_by_id(project_id):
    return next((p for p in PROJECTS if p["id"] == project_id), None)

def _pos_for_project(project_id):
    return [po for po in POS if po["project_id"] == project_id]

def _is_overdue(po):
    try:
        d = date.fromisoformat(po["expected_delivery"])
        return d < TODAY
    except Exception:
        return False

def _days_delta(po):
    """Positive = overdue by N days. Negative = due in N days."""
    try:
        d = date.fromisoformat(po["expected_delivery"])
        return (TODAY - d).days
    except Exception:
        return 0

def _fmt_amt(amount, received=None):
    """Format dollar amount. If received provided, show both."""
    def _f(v):
        if v >= 1_000_000:
            return f"${v / 1_000_000:.2f}M"
        return f"${v / 1_000:.0f}K"
    if received is not None:
        return f"{_f(received)} / {_f(amount)}"
    return _f(amount)

def _project_stats():
    """Per-project open/partial PO counts and value, for sidebar dots and chart."""
    stats = {}
    for proj in PROJECTS:
        pid = proj["id"]
        pos = _pos_for_project(pid)
        open_pos  = [po for po in pos if po["status"] == "open"]
        part_pos  = [po for po in pos if po["status"] == "partial"]
        has_overdue = any(_is_overdue(po) for po in open_pos + part_pos)
        stats[pid] = {
            "open_count":  len(open_pos),
            "partial_count": len(part_pos),
            "open_value":  sum(po["amount"] for po in open_pos),
            "partial_value": sum(po["amount"] - po["received"] for po in part_pos),
            "has_overdue": has_overdue,
        }
    return stats

# ---------------------------------------------------------------------------
# Style helpers
# ---------------------------------------------------------------------------

def _badge(text, bg, color="white", extra=None):
    style = {
        "backgroundColor": bg,
        "color": color,
        "fontSize": "10px",
        "fontWeight": "700",
        "letterSpacing": "0.05em",
        "padding": "2px 8px",
        "borderRadius": "3px",
        "display": "inline-block",
        "marginRight": "6px",
        **(extra or {}),
    }
    return html.Span(text, style=style)

CATEGORY_COLORS = {
    "material": C_BLUE,
    "rental":   C_ORANGE,
    "service":  C_VIOLET,
}

# ---------------------------------------------------------------------------
# Sidebar builder (called from callback to re-render highlights)
# ---------------------------------------------------------------------------

def build_sidebar_project_list(selected_project, stats):
    items = []
    for proj in PROJECTS:
        pid = proj["id"]
        s = stats[pid]
        total_open = s["open_count"] + s["partial_count"]

        # Dot color
        if s["has_overdue"]:
            dot_color = C_RED
        elif total_open > 0:
            dot_color = C_YELLOW
        else:
            dot_color = C_GOOD

        is_selected = selected_project == pid

        row = html.Button(
            [
                html.Span("●", style={
                    "color": dot_color,
                    "fontSize": "10px",
                    "marginRight": "8px",
                    "flexShrink": "0",
                }),
                html.Span(proj["short"], style={
                    "flex": "1",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "whiteSpace": "nowrap",
                    "fontSize": "13px",
                }),
                html.Span(str(total_open), style={
                    "backgroundColor": C_BLUE if is_selected else C_GRID,
                    "color": "white" if is_selected else C_SECONDARY,
                    "fontSize": "10px",
                    "fontWeight": "700",
                    "padding": "1px 6px",
                    "borderRadius": "10px",
                    "flexShrink": "0",
                    "marginLeft": "6px",
                }) if total_open > 0 else html.Span(),
            ],
            id={"type": "proj-btn", "index": pid},
            n_clicks=0,
            style={
                "display": "flex",
                "alignItems": "center",
                "width": "100%",
                "padding": "7px 12px",
                "border": "none",
                "borderRadius": "5px",
                "cursor": "pointer",
                "backgroundColor": C_BLUE if is_selected else "transparent",
                "color": "white" if is_selected else C_INK,
                "fontWeight": "600" if is_selected else "400",
                "fontFamily": FONT,
                "textAlign": "left",
                "marginBottom": "2px",
            },
        )
        items.append(row)
    return items

# ---------------------------------------------------------------------------
# Main content builders
# ---------------------------------------------------------------------------

def _kpi_card(label, value, subtext, color):
    return html.Div([
        html.Div(label, style={
            "fontSize": "10px",
            "fontWeight": "700",
            "letterSpacing": "0.07em",
            "textTransform": "uppercase",
            "color": C_SECONDARY,
            "marginBottom": "6px",
        }),
        html.Div(value, style={
            "fontSize": "30px",
            "fontWeight": "800",
            "color": color,
            "lineHeight": "1",
            "marginBottom": "4px",
            "fontVariantNumeric": "tabular-nums",
        }),
        html.Div(subtext, style={
            "fontSize": "12px",
            "color": C_SECONDARY,
        }),
    ], style={
        "backgroundColor": C_SURFACE,
        "border": f"1px solid {C_GRID}",
        "borderLeft": f"4px solid {color}",
        "borderRadius": "6px",
        "padding": "16px 18px",
        "flex": "1",
        "minWidth": "0",
    })


def build_all_projects_view(status_filter, stats):
    # KPI calculations
    all_open  = [po for po in POS if po["status"] == "open"]
    all_part  = [po for po in POS if po["status"] == "partial"]
    all_inv   = [po for po in POS if po["status"] == "invoiced"]

    shown = []
    if "open"     in (status_filter or []):
        shown += all_open
    if "partial"  in (status_filter or []):
        shown += all_part
    if "invoiced" in (status_filter or []):
        shown += all_inv

    total_open_count = len(all_open)
    total_open_value = sum(po["amount"] for po in all_open)
    overdue_count    = len([po for po in all_open if _is_overdue(po)])
    projects_affected = len({po["project_id"] for po in all_open + all_part})

    # Bar chart
    chart_projs = [p for p in PROJECTS if stats[p["id"]]["open_count"] + stats[p["id"]]["partial_count"] > 0]
    chart_projs_sorted = sorted(chart_projs, key=lambda p: stats[p["id"]]["open_value"] + stats[p["id"]]["partial_value"])

    labels   = [p["short"] for p in chart_projs_sorted]
    open_vals   = [stats[p["id"]]["open_value"]    / 1e6 for p in chart_projs_sorted]
    partial_vals = [stats[p["id"]]["partial_value"] / 1e6 for p in chart_projs_sorted]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Open",
        y=labels,
        x=open_vals,
        orientation="h",
        marker=dict(color=C_BLUE),
        hovertemplate="<b>%{y}</b><br>Open: $%{x:.2f}M<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Partial",
        y=labels,
        x=partial_vals,
        orientation="h",
        marker=dict(color=C_YELLOW),
        hovertemplate="<b>%{y}</b><br>Partial remaining: $%{x:.2f}M<extra></extra>",
    ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor=C_SURFACE,
        plot_bgcolor=C_SURFACE,
        margin=dict(l=8, r=24, t=16, b=32),
        font=dict(family=FONT, color=C_INK, size=11),
        xaxis=dict(
            tickprefix="$",
            ticksuffix="M",
            gridcolor=C_GRID,
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            gridcolor=C_GRID,
            zeroline=False,
            showline=False,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=max(180, len(chart_projs_sorted) * 36 + 60),
        clickmode="event",
    )

    # Overdue POs table
    overdue_pos = sorted(
        [po for po in POS if po["status"] == "open" and _is_overdue(po)],
        key=lambda po: po["amount"],
        reverse=True,
    )

    overdue_rows = []
    for po in overdue_pos:
        proj = _proj_by_id(po["project_id"])
        days_ov = _days_delta(po)
        overdue_rows.append(html.Div([
            html.Div([
                html.Div([
                    html.Span(po["id"], style={"fontWeight": "700", "fontSize": "12px", "color": C_INK, "marginRight": "8px"}),
                    html.Span(proj["short"] if proj else po["project_id"], style={"fontSize": "11px", "color": C_SECONDARY}),
                ], style={"marginBottom": "2px"}),
                html.Div(po["vendor"], style={"fontSize": "12px", "color": C_SECONDARY}),
                html.Div(po["description"], style={"fontSize": "11px", "color": C_MUTED, "marginTop": "2px"}),
            ], style={"flex": "1", "minWidth": "0", "marginRight": "12px"}),
            html.Div([
                html.Div(_fmt_amt(po["amount"]), style={
                    "fontWeight": "700", "fontSize": "13px", "color": C_INK,
                    "textAlign": "right", "fontVariantNumeric": "tabular-nums",
                }),
                html.Div(f"{days_ov}d overdue", style={
                    "fontSize": "11px", "color": C_RED, "fontWeight": "600",
                    "textAlign": "right", "marginTop": "2px",
                }),
            ], style={"flexShrink": "0", "textAlign": "right"}),
        ], style={
            "display": "flex",
            "alignItems": "flex-start",
            "padding": "10px 14px",
            "borderBottom": f"1px solid {C_GRID}",
            "backgroundColor": C_SURFACE,
        }))

    return html.Div([
        # KPI row
        html.Div([
            _kpi_card("Total Open POs",    str(total_open_count),  f"${total_open_value/1e6:.1f}M value",     C_BLUE),
            _kpi_card("Total Open Value",  f"${total_open_value/1e6:.1f}M", f"{total_open_count} purchase orders", C_AQUA),
            _kpi_card("Overdue POs",       str(overdue_count),     "Past expected delivery", C_RED),
            _kpi_card("Projects Affected", str(projects_affected), "With open / partial POs", C_VIOLET),
        ], style={"display": "flex", "gap": "14px", "marginBottom": "20px"}),

        # Bar chart card
        html.Div([
            html.Div("PO Value by Project", style={
                "fontWeight": "600", "fontSize": "13px", "color": C_INK,
                "padding": "14px 16px 0", "marginBottom": "4px",
            }),
            html.Div("Click a bar to drill into that project", style={
                "fontSize": "11px", "color": C_MUTED,
                "padding": "0 16px 8px",
            }),
            dcc.Graph(
                id="po-bar-chart",
                figure=fig,
                config={"displayModeBar": False},
                style={"height": f"{max(180, len(chart_projs_sorted)*36+60)}px"},
            ),
        ], style={
            "backgroundColor": C_SURFACE,
            "border": f"1px solid {C_GRID}",
            "borderRadius": "6px",
            "marginBottom": "20px",
            "overflow": "hidden",
        }),

        # Overdue POs
        html.Div([
            html.Div([
                html.Span("Overdue Purchase Orders", style={
                    "fontWeight": "600", "fontSize": "13px", "color": C_INK,
                }),
                html.Span(f"{len(overdue_pos)} items", style={
                    "fontSize": "11px", "color": C_SECONDARY, "marginLeft": "8px",
                }),
            ], style={
                "padding": "12px 14px",
                "borderBottom": f"1px solid {C_GRID}",
                "backgroundColor": C_SURFACE,
            }),
            html.Div(overdue_rows if overdue_rows else [
                html.Div("No overdue purchase orders.", style={
                    "padding": "16px", "color": C_GOOD, "fontStyle": "italic",
                }),
            ]),
        ], style={
            "backgroundColor": C_SURFACE,
            "border": f"1px solid {C_GRID}",
            "borderRadius": "6px",
            "overflow": "hidden",
        }),
    ])


def build_po_card(po):
    delta = _days_delta(po)
    overdue = delta > 0

    # Delivery badge
    if overdue:
        delivery_badge = html.Span(f"{delta}d overdue", style={
            "backgroundColor": C_RED, "color": "white",
            "fontSize": "10px", "fontWeight": "700",
            "padding": "2px 8px", "borderRadius": "3px",
            "display": "inline-block", "marginLeft": "8px",
        })
    else:
        days_to = abs(delta)
        delivery_badge = html.Span(f"Due in {days_to}d", style={
            "backgroundColor": C_BLUE, "color": "white",
            "fontSize": "10px", "fontWeight": "700",
            "padding": "2px 8px", "borderRadius": "3px",
            "display": "inline-block", "marginLeft": "8px",
        })

    # Category badge
    cat_color = CATEGORY_COLORS.get(po["category"], C_MUTED)
    cat_badge = _badge(po["category"].upper(), cat_color)

    # Status badge
    stat_color = C_RED if po["status"] == "open" else C_YELLOW
    stat_badge = _badge(po["status"].upper(), stat_color)

    # Progress bar (partial only)
    progress = None
    if po["status"] == "partial" and po["amount"] > 0:
        pct = min(100, po["received"] / po["amount"] * 100)
        progress = html.Div([
            html.Div([
                html.Span("Received: ", style={"fontSize": "11px", "color": C_SECONDARY}),
                html.Span(_fmt_amt(po["received"]) + " / " + _fmt_amt(po["amount"]), style={
                    "fontSize": "11px", "color": C_INK, "fontWeight": "600",
                }),
                html.Span(f" ({pct:.0f}%)", style={"fontSize": "11px", "color": C_MUTED}),
            ], style={"marginBottom": "4px"}),
            html.Div([
                html.Div(style={
                    "height": "6px",
                    "width": f"{pct:.0f}%",
                    "backgroundColor": C_AQUA,
                    "borderRadius": "3px",
                }),
            ], style={
                "height": "6px",
                "backgroundColor": C_GRID,
                "borderRadius": "3px",
                "overflow": "hidden",
            }),
        ], style={"marginTop": "10px"})

    return html.Div([
        # Header row
        html.Div([
            html.Div([
                html.Span(po["id"], style={"fontWeight": "700", "fontSize": "14px", "color": C_INK, "marginRight": "10px"}),
                html.Span(po["vendor"], style={"fontSize": "13px", "color": C_SECONDARY}),
            ], style={"flex": "1", "minWidth": "0"}),
            html.Span(_fmt_amt(po["amount"]), style={
                "fontWeight": "800", "fontSize": "15px", "color": C_INK,
                "fontVariantNumeric": "tabular-nums", "flexShrink": "0",
            }),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),

        # Badges row
        html.Div([cat_badge, stat_badge], style={"marginBottom": "6px"}),

        # Description
        html.Div(po["description"], style={"fontSize": "13px", "color": C_INK, "marginBottom": "6px"}),

        # Delivery
        html.Div([
            html.Span(f"Expected: {po['expected_delivery']}", style={"fontSize": "12px", "color": C_SECONDARY}),
            delivery_badge,
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "6px"}),

        # Notes
        html.Div(po["notes"], style={
            "fontSize": "12px", "color": C_SECONDARY, "fontStyle": "italic",
            "borderLeft": f"3px solid {C_GRID}", "paddingLeft": "8px",
        }),

        # Progress bar
        progress,

    ], style={
        "backgroundColor": C_SURFACE,
        "border": f"1px solid {C_GRID}",
        "borderLeft": f"4px solid {C_RED if po['status'] == 'open' else C_YELLOW}",
        "borderRadius": "6px",
        "padding": "14px 16px",
        "marginBottom": "12px",
    })


def build_project_detail_view(project_id, status_filter):
    proj = _proj_by_id(project_id)
    if proj is None:
        return html.Div("Project not found.", style={"color": C_RED, "padding": "24px"})

    pos = _pos_for_project(project_id)

    # Filter by status
    sf = status_filter or ["open", "partial"]
    shown_pos = [po for po in pos if po["status"] in sf]

    open_pos  = [po for po in pos if po["status"] == "open"]
    part_pos  = [po for po in pos if po["status"] == "partial"]
    total_committed = sum(po["amount"] for po in pos)
    open_value = sum(po["amount"] for po in open_pos)

    # KPIs
    kpis = html.Div([
        _kpi_card("Open POs",        str(len(open_pos)),  f"${open_value/1e6:.2f}M value",    C_RED if any(_is_overdue(p) for p in open_pos) else C_BLUE),
        _kpi_card("Open Value",      f"${open_value/1e6:.2f}M",  f"{len(open_pos)} orders",      C_BLUE),
        _kpi_card("Partial POs",     str(len(part_pos)),  "In progress",                      C_YELLOW),
        _kpi_card("Total Committed", f"${total_committed/1e6:.2f}M", "All active POs",        C_VIOLET),
    ], style={"display": "flex", "gap": "14px", "marginBottom": "20px"})

    # PO cards
    if not shown_pos:
        po_section = html.Div("No open purchase orders for this project.", style={
            "color": C_GOOD, "fontStyle": "italic", "fontSize": "14px",
            "padding": "24px", "textAlign": "center",
            "backgroundColor": C_SURFACE,
            "border": f"1px solid {C_GRID}",
            "borderRadius": "6px",
        })
    else:
        po_section = html.Div([build_po_card(po) for po in shown_pos])

    return html.Div([
        # Breadcrumb
        html.Div([
            html.Button(
                "◀ All Projects",
                id="back-btn",
                n_clicks=0,
                style={
                    "background": "none",
                    "border": "none",
                    "color": C_BLUE,
                    "fontSize": "13px",
                    "fontWeight": "600",
                    "cursor": "pointer",
                    "padding": "0",
                    "fontFamily": FONT,
                },
            ),
        ], style={"marginBottom": "12px"}),

        # Project title
        html.H2(proj["name"], style={
            "fontSize": "22px",
            "fontWeight": "700",
            "color": C_INK,
            "margin": "0 0 4px",
        }),
        html.Div(f"Project ID: {project_id}", style={
            "fontSize": "12px", "color": C_MUTED, "marginBottom": "20px",
        }),

        kpis,

        html.Div("Open & Partial Purchase Orders", style={
            "fontSize": "14px", "fontWeight": "600", "color": C_INK,
            "marginBottom": "12px",
        }),

        po_section,
    ])

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    title="Huvibar | Procurement Dashboard",
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
    dcc.Store(id="selected-project", data=None),
    dcc.Store(id="status-filter",    data=["open", "partial"]),

    html.Div([
        # ── Sidebar ─────────────────────────────────────────────────────────
        html.Div([
            # Logo
            html.Div([
                html.Img(src="/assets/logo.png", style={"height": "44px", "width": "auto", "display": "block", "marginBottom": "6px"}),
                html.Div("Procurement Dashboard", style={
                    "fontSize": "10px",
                    "color": C_MUTED,
                    "letterSpacing": "0.04em",
                }),
            ], style={
                "padding": "16px 16px 14px",
                "borderBottom": f"1px solid {C_GRID}",
                "marginBottom": "10px",
            }),

            # All Projects button
            html.Button(
                "All Projects",
                n_clicks=0,
                style={
                    "display": "block",
                    "width": "calc(100% - 24px)",
                    "margin": "0 12px 10px",
                    "padding": "7px 12px",
                    "border": "none",
                    "borderRadius": "5px",
                    "cursor": "pointer",
                    "backgroundColor": "transparent",
                    "color": C_INK,
                    "fontWeight": "600",
                    "fontSize": "13px",
                    "fontFamily": FONT,
                    "textAlign": "left",
                },
                id="all-projects-btn-el",
            ),

            # Section label
            html.Div("PROJECTS", style={
                "fontSize": "10px",
                "fontWeight": "700",
                "letterSpacing": "0.1em",
                "color": C_MUTED,
                "padding": "0 16px 6px",
            }),

            # Project list — re-rendered by callback
            html.Div(id="sidebar-project-list", style={
                "padding": "0 12px",
                "overflowY": "auto",
                "flex": "1",
            }),

            # Legend
            html.Div([
                html.Div("Status Indicators", style={
                    "fontSize": "10px",
                    "fontWeight": "700",
                    "letterSpacing": "0.08em",
                    "color": C_MUTED,
                    "marginBottom": "6px",
                }),
                html.Div([html.Span("●", style={"color": C_RED,    "marginRight": "4px"}), html.Span("Has overdue",      style={"fontSize":"11px","color":C_SECONDARY})], style={"marginBottom": "3px"}),
                html.Div([html.Span("●", style={"color": C_YELLOW, "marginRight": "4px"}), html.Span("Has open POs",     style={"fontSize":"11px","color":C_SECONDARY})], style={"marginBottom": "3px"}),
                html.Div([html.Span("●", style={"color": C_GOOD,   "marginRight": "4px"}), html.Span("No open POs",      style={"fontSize":"11px","color":C_SECONDARY})]),
            ], style={
                "padding": "12px 16px",
                "borderTop": f"1px solid {C_GRID}",
                "marginTop": "auto",
            }),

            # Status filter
            html.Div([
                html.Div("STATUS FILTER", style={
                    "fontSize": "10px",
                    "fontWeight": "700",
                    "letterSpacing": "0.08em",
                    "color": C_MUTED,
                    "marginBottom": "8px",
                }),
                dcc.Checklist(
                    id="status-checklist",
                    options=[
                        {"label": "  Open",     "value": "open"},
                        {"label": "  Partial",  "value": "partial"},
                        {"label": "  Invoiced", "value": "invoiced"},
                    ],
                    value=["open", "partial"],
                    style={"fontSize": "13px", "color": C_INK, "fontFamily": FONT},
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"display": "block", "marginBottom": "4px", "cursor": "pointer"},
                ),
            ], style={
                "padding": "10px 16px 16px",
                "borderTop": f"1px solid {C_GRID}",
            }),
        ], style={
            "width": "260px",
            "flexShrink": "0",
            "backgroundColor": C_SURFACE,
            "borderRight": f"1px solid {C_GRID}",
            "display": "flex",
            "flexDirection": "column",
            "height": "100vh",
            "overflowY": "hidden",
            "position": "sticky",
            "top": "0",
        }),

        # ── Main content ────────────────────────────────────────────────────
        html.Div(
            id="main-content",
            style={
                "flex": "1",
                "overflowY": "auto",
                "padding": "24px 28px",
                "backgroundColor": C_BG,
                "minWidth": "0",
            },
        ),
    ], style={
        "display": "flex",
        "height": "100vh",
        "overflow": "hidden",
    }),

], style={
    "fontFamily": FONT,
    "backgroundColor": C_BG,
    "margin": "0",
    "padding": "0",
})

# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

# 1. Project sidebar button → set selected project
@app.callback(
    Output("selected-project", "data"),
    Input({"type": "proj-btn", "index": ALL}, "n_clicks"),
    State({"type": "proj-btn", "index": ALL}, "id"),
    prevent_initial_call=True,
)
def select_project(n_clicks_list, id_list):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    # Ignore synthetic triggers from sidebar re-renders (n_clicks == 0)
    if not ctx.triggered[0]["value"]:
        return dash.no_update
    triggered_prop = ctx.triggered[0]["prop_id"]
    try:
        idx = json.loads(triggered_prop.split(".")[0])["index"]
    except Exception:
        return dash.no_update
    return idx


# 2. "All Projects" button → clear selection
@app.callback(
    Output("selected-project", "data", allow_duplicate=True),
    Input("all-projects-btn-el", "n_clicks"),
    prevent_initial_call=True,
)
def go_all_projects(n_clicks):
    return None


# 3. Back breadcrumb → clear selection
@app.callback(
    Output("selected-project", "data", allow_duplicate=True),
    Input("back-btn", "n_clicks"),
    prevent_initial_call=True,
)
def back_to_all(n_clicks):
    return None


# 4. Bar chart click → drill into project
@app.callback(
    Output("selected-project", "data", allow_duplicate=True),
    Input("po-bar-chart", "clickData"),
    prevent_initial_call=True,
)
def chart_click(click_data):
    if not click_data:
        return dash.no_update
    label = click_data["points"][0]["y"]
    for p in PROJECTS:
        if p["short"] == label:
            return p["id"]
    return dash.no_update


# 5. Status checklist → update filter store
@app.callback(
    Output("status-filter", "data"),
    Input("status-checklist", "value"),
    prevent_initial_call=False,
)
def update_status_filter(values):
    return values or []


# 6. Main content render
@app.callback(
    Output("main-content", "children"),
    Input("selected-project", "data"),
    Input("status-filter", "data"),
)
def render_main(selected_project, status_filter):
    stats = _project_stats()
    if selected_project is None:
        return build_all_projects_view(status_filter, stats)
    return build_project_detail_view(selected_project, status_filter)


# 7. Sidebar project list (re-render to reflect selection highlight)
@app.callback(
    Output("sidebar-project-list", "children"),
    Input("selected-project", "data"),
)
def render_sidebar_list(selected_project):
    stats = _project_stats()
    return build_sidebar_project_list(selected_project, stats)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
