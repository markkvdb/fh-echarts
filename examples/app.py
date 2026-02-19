from fasthtml.common import *
from fh_echarts.core import echarts_header, EChart, EChartUpdate, EChartJS, EChartOOB, JSFunc

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

# --- 3. Line chart with custom click fields (multiple series) ---
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
    return EChart(options, chart_id="line1", height="350px",
                  hx_get_click="/line-clicked", hx_target_click="#line-click-result",
                  hx_click_vals=["name", "value", "seriesName", "seriesIndex", "dataIndex"])

# --- 3b. Scatter chart with custom JS click callback ---
def scatter_chart():
    options = {
        "title": {"text": "Scatter Plot — Custom Click Callback"},
        "tooltip": {"formatter": JSFunc("function(p) { return 'Point: (' + p.data[0] + ', ' + p.data[1] + ')'; }")},
        "xAxis": {},
        "yAxis": {},
        "series": [{
            "type": "scatter", "symbolSize": 12,
            "data": [[10, 8], [20, 14], [30, 26], [40, 35], [50, 48], [25, 20], [35, 30]]
        }]
    }
    return EChart(options, chart_id="scatter1", height="350px",
                  hx_get_click="/scatter-clicked", hx_target_click="#scatter-click-result",
                  hx_click_cb=JSFunc("function(params) { return {x: params.data[0], y: params.data[1], idx: params.dataIndex}; }"))

# --- 4. Dynamic update demo chart ---
def dynamic_chart():
    options = {
        "title": {"text": "Dynamic Data (click button to update)"},
        "xAxis": {"data": ["A", "B", "C", "D", "E"]},
        "yAxis": {},
        "series": [{"type": "bar", "data": [10, 20, 30, 40, 50]}]
    }
    return EChart(options, chart_id="dynamic1", theme="dark", height="350px")

# --- 5. Append mode demo (streaming time series) ---
_stream_counter = [0]

def stream_chart():
    options = {
        "title": {"text": "Live Sensor Data (append via EChartJS)"},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": ["0s", "1s", "2s", "3s", "4s"]},
        "yAxis": {"type": "value"},
        "series": [
            {"name": "Sensor A", "type": "line", "data": [22, 24, 21, 25, 23]},
            {"name": "Sensor B", "type": "line", "data": [15, 18, 14, 17, 16]}
        ]
    }
    _stream_counter[0] = 5
    return EChart(options, chart_id="stream1", height="350px")

# --- 6. EChartJS demo (blur/unblur) ---
def js_demo_chart():
    options = {
        "title": {"text": "EChartJS Demo — Blur/Unblur"},
        "xAxis": {"data": ["Q1", "Q2", "Q3", "Q4"]},
        "yAxis": {},
        "series": [{"type": "bar", "data": [80, 120, 95, 140], "name": "Sales"}]
    }
    return EChart(options, chart_id="jsdemo1", height="350px")

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

        H2("3. Line Chart — Custom Click Fields (hx_click_vals)"),
        P("Click any data point to see seriesName, seriesIndex, and dataIndex:"),
        line_chart(),
        Div(id="line-click-result",
            style="margin-top:10px; padding:10px; border:1px dashed gray; min-height:40px;"),
        Hr(),

        H2("3b. Scatter Plot — Custom JS Callback (hx_click_cb)"),
        P("Click any point to extract x/y coordinates via a custom JS callback:"),
        scatter_chart(),
        Div(id="scatter-click-result",
            style="margin-top:10px; padding:10px; border:1px dashed gray; min-height:40px;"),
        Hr(),

        H2("4. Dynamic Update via EChartUpdate"),
        dynamic_chart(),
        Button("Randomize Data", hx_get="/randomize", hx_target="#update-slot",
               hx_swap="innerHTML", style="margin-top:10px;"),
        Div(id="update-slot"),
        Hr(),

        H2("5. Streaming Time Series via EChartJS"),
        P("Click to append new data points using EChartJS:"),
        stream_chart(),
        Button("Add Data Point", hx_get="/append-point", hx_target="#script-sink",
               hx_swap="innerHTML", style="margin-top:10px;"),
        Hr(),

        H2("6. EChartJS — Run Arbitrary JS on Chart"),
        P("Use EChartJS to blur/unblur a chart, or stash data on the DOM element:"),
        js_demo_chart(),
        Div(
            Button("Blur", hx_get="/blur-chart", hx_target="#js-slot",
                   hx_swap="innerHTML", style="margin-right:8px;"),
            Button("Unblur", hx_get="/unblur-chart", hx_target="#js-slot",
                   hx_swap="innerHTML", style="margin-right:8px;"),
            Button("Stash & Log Data", hx_get="/stash-data", hx_target="#js-slot",
                   hx_swap="innerHTML"),
            style="margin-top:10px;"
        ),
        Div(id="js-slot"),
        Div(id="script-sink"),
    )

@rt('/bar-clicked')
def get(name: str, value: int, seriesName: str):
    return Div(
        P(Strong("Server received click!"),
          f" Bar: {name}, Series: {seriesName}, Value: ${value:,}"),
        style="background:#e8f5e9; padding:8px; border-radius:4px;"
    )

@rt('/line-clicked')
def get(name: str, value: str, seriesName: str, seriesIndex: int, dataIndex: int):
    return Div(
        P(Strong("Line click! "),
          f"Day: {name}, Value: {value}, Series: {seriesName} (index {seriesIndex}), Data index: {dataIndex}"),
        style="background:#e3f2fd; padding:8px; border-radius:4px;"
    )

@rt('/scatter-clicked')
def get(x: float, y: float, idx: int):
    return Div(
        P(Strong("Scatter click! "),
          f"Coordinates: ({x}, {y}), Point index: {idx}"),
        style="background:#fff3e0; padding:8px; border-radius:4px;"
    )

import random

@rt('/randomize')
def get():
    new_data = [random.randint(5, 100) for _ in range(5)]
    return EChartUpdate("dynamic1", {
        "series": [{"data": new_data}]
    })

@rt('/append-point')
def get():
    i = _stream_counter[0]
    _stream_counter[0] += 1
    a, b = random.randint(18, 30), random.randint(10, 22)
    return EChartOOB(
        EChartJS("stream1", f"""function(chart, el) {{
            var opt = chart.getOption();
            opt.xAxis[0].data.push('{i}s');
            opt.series[0].data.push({a});
            opt.series[1].data.push({b});
            chart.setOption(opt);
        }}""")
    )

@rt('/blur-chart')
def get():
    return EChartOOB(
        EChartJS("jsdemo1", "function(chart, el) { el.style.filter = 'blur(4px)'; }")
    )

@rt('/unblur-chart')
def get():
    return EChartOOB(
        EChartJS("jsdemo1", "function(chart, el) { el.style.filter = ''; }")
    )

@rt('/stash-data')
def get():
    return EChartOOB(
        EChartJS("jsdemo1", """function(chart, el) {
            el._stashedData = chart.getOption().series[0].data;
            console.log('Stashed data:', el._stashedData);
        }""")
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    serve(port=args.port)
