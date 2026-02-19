from fasthtml.common import *
from fh_echarts.core import echarts_header, EChart, EChartUpdate, JSFunc

app, rt = fast_app(hdrs=(echarts_header(),))

# --- 1. Bar chart with dark theme, JS tooltip formatter, and HTMX click ---
def bar_chart():
    options = {
        "title": {"text": "Monthly Revenue"},
        "tooltip": {
            "formatter": JSFunc("""function(params) {
                return '<b>' + params.name + '</b><br/>Revenue: $' + params.value.toLocaleString();
            }""")
        },
        "xAxis": {"data": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]},
        "yAxis": {"axisLabel": {
            "formatter": JSFunc("function(v) { return '$' + v/1000 + 'k'; }")
        }},
        "series": [{"name": "Revenue", "type": "bar",
                     "data": [12000, 18000, 15000, 25000, 22000, 30000]}]
    }
    return EChart(options, chart_id="bar1", theme="dark",
                  hx_get_click="/bar-clicked", hx_target_click="#click-result")

# --- 2. Pie chart with light theme ---
def pie_chart():
    options = {
        "title": {"text": "Market Share", "left": "center"},
        "tooltip": {
            "formatter": JSFunc("""function(params) {
                return params.name + ': ' + params.value + '%';
            }""")
        },
        "series": [{
            "type": "pie", "radius": "60%",
            "data": [
                {"value": 40, "name": "Product A"},
                {"value": 25, "name": "Product B"},
                {"value": 20, "name": "Product C"},
                {"value": 15, "name": "Product D"},
            ]
        }]
    }
    return EChart(options, chart_id="pie1", theme="light", height="350px")

# --- 3. Line chart (no theme = default) ---
def line_chart():
    options = {
        "title": {"text": "Temperature Forecast"},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["High", "Low"]},
        "xAxis": {"data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
        "yAxis": {"axisLabel": {
            "formatter": JSFunc("function(v) { return v + '°C'; }")
        }},
        "series": [
            {"name": "High", "type": "line", "data": [18, 20, 22, 25, 24, 21, 19]},
            {"name": "Low",  "type": "line", "data": [10, 11, 13, 15, 14, 12, 10]}
        ]
    }
    return EChart(options, chart_id="line1", height="350px")

# --- 4. Dynamic update demo chart ---
def dynamic_chart():
    options = {
        "title": {"text": "Dynamic Data (click button to update)"},
        "xAxis": {"data": ["A", "B", "C", "D", "E"]},
        "yAxis": {},
        "series": [{"type": "bar", "data": [10, 20, 30, 40, 50]}]
    }
    return EChart(options, chart_id="dynamic1", theme="dark", height="350px")

# --- Routes ---
@rt('/')
def get():
    return Titled("fh-echarts Showcase",
        H2("1. Bar Chart — Dark Theme + JS Formatters + HTMX Click"),
        P("Click any bar to trigger a server-side HTMX request:"),
        bar_chart(),
        Div(id="click-result",
            style="margin-top:10px; padding:10px; border:1px dashed gray; min-height:40px;"),
        Hr(),

        H2("2. Pie Chart — Light Theme + JS Tooltip"),
        pie_chart(),
        Hr(),

        H2("3. Line Chart — Default Theme + Axis Formatters"),
        line_chart(),
        Hr(),

        H2("4. Dynamic Update via EChartUpdate"),
        dynamic_chart(),
        Button("Randomize Data", hx_get="/randomize", hx_target="#update-slot",
               hx_swap="innerHTML", style="margin-top:10px;"),
        Div(id="update-slot"),
    )

@rt('/bar-clicked')
def get(name: str, value: int, seriesName: str):
    return Div(
        P(Strong("Server received click!"),
          f" Bar: {name}, Series: {seriesName}, Value: ${value:,}"),
        style="background:#e8f5e9; padding:8px; border-radius:4px;"
    )

import random

@rt('/randomize')
def get():
    new_data = [random.randint(5, 100) for _ in range(5)]
    return EChartUpdate("dynamic1", {
        "series": [{"data": new_data}]
    })

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    serve(port=args.port)
