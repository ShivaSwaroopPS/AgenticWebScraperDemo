# Webscraper.py
import streamlit as st
import time
import os
import pandas as pd
from simulation import parse_vsop_text, simulate_mcp_handshake, simulate_execute_plan

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Web Agent", page_icon="🕸️", layout="wide")

# =========================
# CUSTOM CSS
# =========================
custom_css = """
<style>
footer, header, #MainMenu {visibility:hidden;}
.console-box {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: "Consolas", monospace;
    padding: 15px;
    border-radius: 8px;
    font-size: 13px;
    line-height: 1.5;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.6);
    white-space: pre-wrap;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# =========================
# HEADER with LOGO + TITLE
# =========================
# =========================
# HEADER with LOGO + TITLE
# =========================
BASE_DIR = os.path.dirname(__file__)
logo_path = os.path.join(BASE_DIR, "assets", "logos", "SP Logo.png")

# Side by side: logo and title same size
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)  # scale logo to match title height

with header_col2:
    st.markdown("""
        <div style="display:flex;align-items:center;height:100%;">
            <h1 style="margin:0; font-size:32px;">
                <span style="color:#D6001C;">Agentic</span>
                <span style="color:#111;">Web Scraper(MCP)</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)


# =========================
# MAIN LAYOUT: 2 PARTS
# =========================
left, right = st.columns([1, 2])

# --- LEFT: INPUT PANEL ---
with left:
    st.subheader("Instruction Input")
    uploaded = st.file_uploader("Upload VSOP / instruction doc", type=["txt", "docx"])
    manual_text = st.text_area("Paste instructions here", height=180)
    user_command = st.text_input("Agent command", "Follow the VSOP and extract Coconut Oil prices")
    run_btn = st.button("▶️ Run Agent")

# --- RIGHT: OUTPUT PANEL ---
with right:
    st.markdown("""
        <h3 style="margin-top:0;">
            <span style="color:#D6001C;">Agent</span> <span style="color:#111;">Console</span>
        </h3>
    """, unsafe_allow_html=True)
    console_area = st.empty()
    logs = []

    def append_log(line):
        logs.append(line)
        console_area.markdown("<div class='console-box'>" + "\n".join(logs[-30:]) + "</div>", unsafe_allow_html=True)

    st.markdown("""
        <h3>
            <span style="color:#D6001C;">Parsed</span> <span style="color:#111;">Plan</span>
        </h3>
    """, unsafe_allow_html=True)
    plan_area = st.empty()

    st.markdown("""
        <h3>
            <span style="color:#D6001C;">Extracted</span> <span style="color:#111;">Results</span>
        </h3>
    """, unsafe_allow_html=True)
    results_area = st.empty()


# =========================
# EXECUTION FLOW
# =========================
if run_btn:
    text = manual_text or user_command or "<empty>"
    append_log("SESSION: starting at " + time.strftime("%Y-%m-%d %H:%M:%S"))
    append_log("→ ingesting payload...")
    time.sleep(1.0)
    append_log("→ routing to instruction planner...")
    time.sleep(1.0)

    plan = parse_vsop_text(text)
    append_log("PARSER >> instruction plan generated")
    plan_md = "| Step ID | Command | Args |\n|---:|---|---|\n"
    for p in plan:
        args_str = ", ".join([f"{k}={v}" for k, v in p.get("args", {}).items()])
        plan_md += f"| {p['step_id']} | {p['cmd']} | {args_str} |\n"
    plan_area.markdown(plan_md, unsafe_allow_html=True)

    append_log("")
    append_log("→ establishing MCP channel...")
    simulate_mcp_handshake(append_log, pause=0.9)
    append_log("→ channel active. beginning execution")
    time.sleep(1.0)

    append_log("AGENT >> analyzing click paths, stabilizing selectors...")
    for i in range(2):
        append_log(f"⏳ reasoning{'.'*(i+1)}")
        time.sleep(1.0)
    append_log("AGENT >> execution plan locked in")

    final_df = simulate_execute_plan(plan, append_log, show_step_pause=1.1)

    append_log("→ normalizing extracted table...")
    time.sleep(1.0)
    append_log("RESULT >> 3 rows extracted")

    results_area.dataframe(final_df, use_container_width=True)
    csv_bytes = final_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv_bytes, "extracted_data.csv", "text/csv")
    append_log("SESSION: run complete. artifacts ready.")
