# Databricks App: Huvibar Inventory & Materials Management
# Connects to css_genie.contracts.purchase_orders for materials tracking

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
BLUE     = "#2a78d6"
AQUA     = "#1baf7a"
YELLOW   = "#eda100"
RED      = "#e34948"
ORANGE   = "#eb6834"
MUTED    = "#898781"

SURFACE  = "#fcfcfb"
INK      = "#0b0b0b"
SECONDARY= "#52514e"
GRID     = "#e1e0d9"
CHARCOAL = "#1a1a19"

GOOD     = "#0ca30c"
WARNING  = "#eda100"
CRITICAL = "#e34948"

# ---------------------------------------------------------------------------
# Seed data  (TODO: Replace with live Databricks SQL query)
# ---------------------------------------------------------------------------

# TODO: Replace with live Databricks SQL query
# SELECT project_name, SUM(po_value) FROM css_genie.contracts.purchase_orders GROUP BY project_name
PROJECTS = [
    "Colorado Convention Center",
    "Broomfield Semiconductor Fab",
    "Denver Airport Terminal Upgrade",
    "Englewood Mixed-Use",
    "Parker Senior Living",
    "Westminster High School",
    "Loveland Logistics Hub",
    "Aurora VA Clinic",
    "Rocky Flats Facility",
    "Castle Rock Municipal",
    "Centennial Airport Hangar",
    "Brighton Solar Farm",
]

# TODO: Replace with live Databricks SQL query
# SELECT status, COUNT(*), SUM(po_value) FROM css_genie.contracts.purchase_orders GROUP BY status
PO_STATUS = {
    "open":      {"count": 96,  "value_m": 44.6},
    "invoiced":  {"count": 80,  "value_m": 32.2},
    "partial":   {"count": 76,  "value_m": 34.2},
    "received":  {"count": 40,  "value_m": 20.7},
    "paid":      {"count": 69,  "value_m": 27.3},
}

# TODO: Replace with live Databricks SQL query
# SELECT vendor, project, description, amount, status
# FROM css_genie.contracts.purchase_orders WHERE status IN ('overdue','partial')
# ORDER BY amount DESC LIMIT 50
OVERDUE_ITEMS = [
    {
        "project": "Colorado Convention Center",
        "description": "Structural Steel — wide-flange beams & columns",
        "vendor": "Commercial Metals Co",
        "amount": 3_700_000,
        "status": "OVERDUE",
    },
    {
        "project": "Colorado Convention Center",
        "description": "HVAC Controls & BAS Integration",
        "vendor": "Siemens Building Technologies",
        "amount": 807_000,
        "status": "OVERDUE",
    },
    {
        "project": "Englewood Mixed-Use",
        "description": "Luxury Vinyl Tile — Level 3 & 4 corridors",
        "vendor": "Armstrong Flooring",
        "amount": 564_000,
        "status": "PARTIAL",
    },
    {
        "project": "Denver Airport Terminal Upgrade",
        "description": "Commercial Flooring System — Gates B10-B22",
        "vendor": "Forbo Flooring",
        "amount": 744_000,
        "status": "PARTIAL",
    },
    {
        "project": "Broomfield Semiconductor Fab",
        "description": "Ready-Mix Concrete — fab slab pour",
        "vendor": "Colorado Ready Mix",
        "amount": 1_300_000,
        "status": "OVERDUE",
    },
    {
        "project": "Rocky Flats Facility",
        "description": "Heavy Lift Crane Rental — Phase 2 steel erection",
        "vendor": "Barnhart Crane & Rigging",
        "amount": 375_000,
        "status": "OVERDUE",
    },
    {
        "project": "Rocky Flats Facility",
        "description": "Roofing Membrane & Insulation System",
        "vendor": "Tremco Roofing",
        "amount": 126_000,
        "status": "PARTIAL",
    },
    {
        "project": "Rocky Flats Facility",
        "description": "Crushed Aggregate Base — access roads",
        "vendor": "Vulcan Materials",
        "amount": 213_000,
        "status": "OVERDUE",
    },
    {
        "project": "Parker Senior Living",
        "description": "Structural Engineering Peer Review",
        "vendor": "RMT Engineering",
        "amount": 124_000,
        "status": "PARTIAL",
    },
    {
        "project": "Parker Senior Living",
        "description": "Geotechnical Testing & Special Inspection",
        "vendor": "Terracon Consultants",
        "amount": 150_000,
        "status": "OVERDUE",
    },
]

# TODO: Replace with live Databricks SQL query
# SELECT date_trunc('month', invoice_date) AS month, SUM(amount)
# FROM css_genie.contracts.purchase_orders WHERE invoice_date >= dateadd(month,-12,current_date())
MONTHLY_SPEND = {
    "months": [
        "Aug '25", "Sep '25", "Oct '25", "Nov '25", "Dec '25", "Jan '26",
        "Feb '26", "Mar '26", "Apr '26", "May '26", "Jun '26", "Jul '26",
    ],
    "values": [31.7, 50.7, 45.8, 39.9, 46.9, 38.2, 27.4, 30.4, 20.7, 19.4, 23.9, 11.3],
}

# ---------------------------------------------------------------------------
# Plotly figure helpers
# ---------------------------------------------------------------------------

def _base_layout(title: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(size=13, color=INK, family="Inter, system-ui, sans-serif"), x=0, xanchor="left"),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        margin=dict(l=16, r=16, t=48, b=16),
        font=dict(family="Inter, system-ui, sans-serif", color=INK, size=11),
        xaxis=dict(
            gridcolor=GRID,
            linecolor=GRID,
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=GRID,
            linecolor=GRID,
            showline=False,
            zeroline=False,
        ),
        showlegend=True,
    )


def build_po_status_figure() -> go.Figure:
    statuses = [
        ("Open",     PO_STATUS["open"]["value_m"],     BLUE),
        ("Invoiced", PO_STATUS["invoiced"]["value_m"], AQUA),
        ("Partial",  PO_STATUS["partial"]["value_m"],  YELLOW),
        ("Received", PO_STATUS["received"]["value_m"], GOOD),
        ("Paid",     PO_STATUS["paid"]["value_m"],     MUTED),
    ]

    fig = go.Figure()

    for label, value_m, color in statuses:
        text_label = f"${value_m:.1f}M" if value_m >= 5 else ""
        fig.add_trace(go.Bar(
            name=label,
            x=[value_m],
            y=["PO Pipeline"],
            orientation="h",
            marker=dict(color=color, line=dict(width=0)),
            text=[text_label],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11, color="white", family="Inter, system-ui, sans-serif"),
            hovertemplate=f"<b>{label}</b><br>${value_m:.1f}M<extra></extra>",
        ))

    layout = _base_layout("Purchase Order Pipeline — Active Projects")
    layout.update(
        barmode="stack",
        xaxis=dict(
            title=dict(text="Value ($ Millions)", font=dict(size=11)),
            tickprefix="$",
            ticksuffix="M",
            gridcolor=GRID,
            linecolor=GRID,
            showline=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            gridcolor=GRID,
            linecolor=GRID,
            showline=False,
            zeroline=False,
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
        height=220,
        margin=dict(l=16, r=16, t=72, b=32),
    )
    fig.update_layout(layout)
    return fig


def build_monthly_spend_figure() -> go.Figure:
    months = MONTHLY_SPEND["months"]
    values = MONTHLY_SPEND["values"]

    fig = go.Figure()

    # Filled area
    fig.add_trace(go.Scatter(
        x=months,
        y=values,
        fill="tozeroy",
        fillcolor="rgba(42, 120, 214, 0.10)",
        line=dict(color=BLUE, width=2.5),
        mode="lines+markers",
        marker=dict(size=6, color=BLUE, line=dict(width=1.5, color="white")),
        name="Monthly Spend",
        hovertemplate="<b>%{x}</b><br>$%{y:.1f}M<extra></extra>",
    ))

    layout = _base_layout("Monthly Materials Spend ($M) — Active Projects")
    layout.update(
        xaxis=dict(
            gridcolor=GRID,
            linecolor=GRID,
            showline=False,
            zeroline=False,
            tickangle=-30,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title=dict(text="$ Millions", font=dict(size=11)),
            tickprefix="$",
            ticksuffix="M",
            gridcolor=GRID,
            linecolor=GRID,
            showline=False,
            zeroline=False,
        ),
        showlegend=False,
        height=260,
        margin=dict(l=52, r=16, t=48, b=56),
    )
    fig.update_layout(layout)
    return fig


# ---------------------------------------------------------------------------
# Component builders
# ---------------------------------------------------------------------------

def _kpi_tile(label: str, value: str, subtext: str, accent_color: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody([
            html.Div(label, style={
                "fontSize": "11px",
                "fontWeight": "600",
                "letterSpacing": "0.06em",
                "textTransform": "uppercase",
                "color": SECONDARY,
                "marginBottom": "6px",
            }),
            html.Div(value, style={
                "fontSize": "36px",
                "fontWeight": "700",
                "color": accent_color,
                "lineHeight": "1",
                "marginBottom": "6px",
                "fontVariantNumeric": "tabular-nums",
            }),
            html.Div(subtext, style={
                "fontSize": "12px",
                "color": SECONDARY,
            }),
        ], style={"padding": "18px 20px"}),
        style={
            "backgroundColor": SURFACE,
            "border": f"1px solid {GRID}",
            "borderLeft": f"4px solid {accent_color}",
            "borderRadius": "6px",
            "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
        },
    )


def _format_amount(amount: int) -> str:
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    return f"${amount / 1_000:.0f}K"


def _overdue_card(item: dict) -> html.Div:
    badge_color = CRITICAL if item["status"] == "OVERDUE" else WARNING
    return html.Div([
        html.Div([
            html.Div([
                html.Span(item["project"], style={
                    "fontWeight": "600",
                    "fontSize": "13px",
                    "color": INK,
                    "display": "block",
                    "marginBottom": "2px",
                }),
                html.Span(item["description"], style={
                    "fontSize": "12px",
                    "color": SECONDARY,
                    "display": "block",
                    "marginBottom": "4px",
                }),
                html.Span(item["vendor"], style={
                    "fontSize": "11px",
                    "color": MUTED,
                    "fontStyle": "italic",
                }),
            ], style={"flex": "1", "minWidth": "0", "marginRight": "12px"}),
            html.Div([
                html.Div(_format_amount(item["amount"]), style={
                    "fontWeight": "700",
                    "fontSize": "14px",
                    "color": INK,
                    "textAlign": "right",
                    "fontVariantNumeric": "tabular-nums",
                    "marginBottom": "6px",
                }),
                html.Span(item["status"], style={
                    "backgroundColor": badge_color,
                    "color": "white",
                    "fontSize": "10px",
                    "fontWeight": "700",
                    "letterSpacing": "0.05em",
                    "padding": "2px 7px",
                    "borderRadius": "3px",
                    "display": "inline-block",
                }),
            ], style={"flexShrink": "0", "textAlign": "right"}),
        ], style={"display": "flex", "alignItems": "flex-start"}),
    ], style={
        "padding": "12px 14px",
        "borderBottom": f"1px solid {GRID}",
        "backgroundColor": SURFACE,
    })


# ---------------------------------------------------------------------------
# App layout
# ---------------------------------------------------------------------------

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Huvibar | Inventory & Materials Management",
)

app.layout = html.Div([

    # ── Header bar ──────────────────────────────────────────────────────────
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    html.Span("🏗️ HUVIBAR CONSTRUCTION", style={
                        "fontWeight": "700",
                        "fontSize": "15px",
                        "letterSpacing": "0.04em",
                        "color": "white",
                        "fontFamily": "Inter, system-ui, sans-serif",
                    }),
                    width="auto",
                ),
                dbc.Col(
                    html.Span("Inventory & Materials Management", style={
                        "fontWeight": "400",
                        "fontSize": "14px",
                        "color": "rgba(255,255,255,0.70)",
                        "fontFamily": "Inter, system-ui, sans-serif",
                    }),
                    style={"textAlign": "center"},
                ),
                dbc.Col(
                    html.Div([
                        html.Span("●", style={"color": GOOD, "fontSize": "10px", "marginRight": "5px"}),
                        html.Span("Live · css_genie", style={
                            "fontSize": "12px",
                            "color": "rgba(255,255,255,0.60)",
                            "fontFamily": "Inter, system-ui, sans-serif",
                        }),
                    ], style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"}),
                    width="auto",
                ),
            ], align="center"),
        ], fluid=True, style={"maxWidth": "1400px"}),
    ], style={
        "backgroundColor": CHARCOAL,
        "padding": "14px 24px",
        "borderBottom": "1px solid rgba(255,255,255,0.08)",
        "position": "sticky",
        "top": "0",
        "zIndex": "1000",
    }),

    # ── Main content ────────────────────────────────────────────────────────
    dbc.Container([

        # ── KPI row ─────────────────────────────────────────────────────────
        dbc.Row([
            dbc.Col(_kpi_tile("Open POs",            "96",  "$44.6M value",      BLUE),     md=3),
            dbc.Col(_kpi_tile("Overdue Deliveries",  "96",  "Need attention",     CRITICAL), md=3),
            dbc.Col(_kpi_tile("Partial Deliveries",  "76",  "$34.2M in progress", WARNING),  md=3),
            dbc.Col(_kpi_tile("Active Projects",     "12",  "With open POs",      GOOD),     md=3),
        ], className="g-3", style={"marginTop": "24px"}),

        # ── Middle row: chart + overdue list ────────────────────────────────
        dbc.Row([

            # PO status chart
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            figure=build_po_status_figure(),
                            config={"displayModeBar": False},
                            style={"height": "220px"},
                        ),
                    ], style={"padding": "16px"}),
                ], style={
                    "backgroundColor": SURFACE,
                    "border": f"1px solid {GRID}",
                    "borderRadius": "6px",
                    "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
                    "height": "100%",
                }),
            ], md=7),

            # Overdue deliveries list
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.Div([
                            html.Span("Overdue Deliveries", style={
                                "fontWeight": "600",
                                "fontSize": "13px",
                                "color": INK,
                                "fontFamily": "Inter, system-ui, sans-serif",
                            }),
                            html.Span(f"{len(OVERDUE_ITEMS)} items", style={
                                "fontSize": "11px",
                                "color": SECONDARY,
                                "marginLeft": "8px",
                            }),
                        ]),
                        style={
                            "backgroundColor": SURFACE,
                            "borderBottom": f"1px solid {GRID}",
                            "padding": "12px 14px",
                        },
                    ),
                    html.Div(
                        [_overdue_card(item) for item in OVERDUE_ITEMS],
                        style={
                            "overflowY": "auto",
                            "maxHeight": "320px",
                            "backgroundColor": SURFACE,
                        },
                    ),
                ], style={
                    "backgroundColor": SURFACE,
                    "border": f"1px solid {GRID}",
                    "borderRadius": "6px",
                    "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
                    "height": "100%",
                }),
            ], md=5),

        ], className="g-3", style={"marginTop": "20px"}),

        # ── Bottom row: monthly spend trend ─────────────────────────────────
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            figure=build_monthly_spend_figure(),
                            config={"displayModeBar": False},
                            style={"height": "260px"},
                        ),
                    ], style={"padding": "16px"}),
                ], style={
                    "backgroundColor": SURFACE,
                    "border": f"1px solid {GRID}",
                    "borderRadius": "6px",
                    "boxShadow": "0 1px 4px rgba(0,0,0,0.06)",
                }),
            ]),
        ], className="g-3", style={"marginTop": "20px"}),

        # ── Footer ──────────────────────────────────────────────────────────
        html.Div(
            "Data sourced from css_genie.contracts.purchase_orders · Huvibar Construction · Read-only view",
            style={
                "textAlign": "center",
                "fontSize": "11px",
                "color": MUTED,
                "padding": "24px 0 16px",
                "fontFamily": "Inter, system-ui, sans-serif",
            },
        ),

    ], fluid=True, style={
        "maxWidth": "1400px",
        "padding": "0 24px",
        "fontFamily": "Inter, system-ui, sans-serif",
        "backgroundColor": "#f4f4f2",
        "minHeight": "calc(100vh - 53px)",
    }),

], style={"backgroundColor": "#f4f4f2", "minHeight": "100vh"})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
