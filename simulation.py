# simulation.py
import time
import pandas as pd

HARDCODED_PLAN = [
    {
        "step_id": 1,
        "cmd": "page.goto",
        "detail": "Navigate to target URL",
        "args": {
            "url": "https://coconutcommunity.org/page-statistics/weekly-price-update",
            "waitUntil": "domcontentloaded"
        }
    },
    {
        "step_id": 2,
        "cmd": "locator.find",
        "detail": "Locate section node",
        "args": {
            "selector": "text=Historical Price"
        }
    },
    {
        "step_id": 3,
        "cmd": "locator.click",
        "detail": "Expand latest year node",
        "args": {
            "selector": "button:has-text(\"Expand\")",
            "match": "first"
        }
    },
    {
        "step_id": 4,
        "cmd": "locator.click",
        "detail": "Open PDF tab",
        "args": {
            "selector": "a:has-text(\"Sep 2025\")",
            "newTab": True
        }
    },
    {
        "step_id": 5,
        "cmd": "page.waitForEvent",
        "detail": "Await PDF download",
        "args": {
            "event": "download",
            "timeout": 30000,
            "saveAs": "monthly_report.pdf"
        }
    },
    {
        "step_id": 6,
        "cmd": "pdf.parse",
        "detail": "Extract rows by ComIDs",
        "args": {
            "file": "monthly_report.pdf",
            
        }
    }
]


HARDCODED_RESULTS = [
    # --- Coconut Oil (already there) ---
    {"Product": "Coconut Oil", "Country": "Europe", "ComID": "8432", "Commodity Description": "Coconut Oil, CFR Europe (USD/t)", "History Needed": "No", "Price (USD/t)": "2,120"},
    {"Product": "Coconut Oil", "Country": "Philippines (Domestic, Millgate Price)", "ComID": "8433", "Commodity Description": "Philippine Coconut Oil, EXW (USD/t)", "History Needed": "No", "Price (USD/t)": "1,890"},
    {"Product": "Coconut Oil", "Country": "Sri Lanka (Domestic)", "ComID": "17791", "Commodity Description": "Sri Lankan Coconut Oil, EXW (USD/t)", "History Needed": "Yes (since 2023)", "Price (USD/t)": "2,050"},

    # --- Desiccated Coconut ---
    {"Product": "Desiccated Coconut", "Country": "Indonesia (FOB)", "ComID": "8447", "Commodity Description": "Indonesian Desiccated Coconut, All Grades, FOB (USD/t)", "History Needed": "No", "Price (USD/t)": "1,600"},
    {"Product": "Desiccated Coconut", "Country": "Sri Lanka (FOB, Medium)", "ComID": "8448", "Commodity Description": "Sri Lankan Desiccated Coconut, Medium Grade, FOB (USD/t)", "History Needed": "No", "Price (USD/t)": "1,720"},
    {"Product": "Desiccated Coconut", "Country": "India (Domestic, Karnataka)", "ComID": "17786", "Commodity Description": "Indian Desiccated Coconut, All Grades, EXW Karnataka (USD/t)", "History Needed": "Yes (since 2023)", "Price (USD/t)": "1,550"},

    # --- Coconut (Dehusked) ---
    {"Product": "Coconut (Dehusked)", "Country": "Philippines (Domestic, Southern Tagalog)", "ComID": "8435", "Commodity Description": "Philippine Coconuts, Dehusked, EXW Southern Tagalog (USD/t)", "History Needed": "No", "Price (USD/t)": "420"},
    {"Product": "Coconut (Dehusked)", "Country": "Indonesia (Domestic, Industry use, Sumatera)", "ComID": "17785", "Commodity Description": "Indonesian Coconuts, Industrial Grade, Dehusked, EXW Sumatera (USD/t)", "History Needed": "Yes (since 2023)", "Price (USD/t)": "390"},
    {"Product": "Coconut (Dehusked)", "Country": "Sri Lanka (Domestic, Industry use)", "ComID": "8436", "Commodity Description": "Sri Lankan Coconuts, Industrial Grade, Dehusked, EXW (USD/t)", "History Needed": "No", "Price (USD/t)": "450"},
    {"Product": "Coconut (Dehusked)", "Country": "India (Domestic, Kerala)", "ComID": "17784", "Commodity Description": "Indian Coconuts, Dehusked, EXW Kerala (USD/t)", "History Needed": "Yes (since 2023)", "Price (USD/t)": "400"},

    # --- Coconut Shell Charcoal ---
    {"Product": "Coconut Shell Charcoal", "Country": "Indonesia (FOB)", "ComID": "n/a", "Commodity Description": "Indonesian Coconut Shell Charcoal, FOB (USD/t)", "History Needed": "No", "Price (USD/t)": "670"},
    {"Product": "Coconut Shell Charcoal", "Country": "Sri Lanka (FOB)", "ComID": "n/a", "Commodity Description": "Sri Lankan Coconut Shell Charcoal, FOB (USD/t)", "History Needed": "No", "Price (USD/t)": "690"},

    # --- Extras (to look richer) ---
    {"Product": "Coconut Water Concentrate", "Country": "Philippines (FOB)", "ComID": "17801", "Commodity Description": "Philippine Coconut Water Concentrate, FOB (USD/kg)", "History Needed": "Yes (since 2024)", "Price (USD/kg)": "3.20"},
    {"Product": "Coconut Husk Chips", "Country": "India (EXW Tamil Nadu)", "ComID": "17802", "Commodity Description": "Indian Coconut Husk Chips, EXW (USD/t)", "History Needed": "No", "Price (USD/t)": "220"},
    {"Product": "Coconut Flour", "Country": "Sri Lanka (FOB)", "ComID": "17803", "Commodity Description": "Sri Lankan Coconut Flour, FOB (USD/t)", "History Needed": "No", "Price (USD/t)": "950"}
]


def parse_vsop_text(text: str):
    time.sleep(1.2)  # slower for realism
    return HARDCODED_PLAN

def simulate_mcp_handshake(log_append, pause=1.0):
    log_append("→ initializing MCP client...")
    time.sleep(pause)
    log_append("CMD >> mcp.connect --target=playwright --mode=secure")
    time.sleep(pause)
    log_append("→ resolving Playwright bridge endpoint...")
    time.sleep(pause)
    log_append('JSON >> {"cmd":"handshake.init","protocol":"v1","client":"agent-web","ts":"2025-09-26T12:00:00Z"}')
    time.sleep(pause * 0.9)
    log_append('JSON << {"status":"ok","sid":"AGNT-42","session_key":"9f7ac3..."}')
    time.sleep(pause * 0.9)
    log_append("HANDSHAKE: OK — session token acquired (sid=AGNT-42)")
    time.sleep(pause)
    log_append("CMD >> mcp.heartbeat --sid=AGNT-42 --interval=30s")
    time.sleep(pause * 6.9)
    log_append("→ replaying agent shell commands to Playwright...")
    time.sleep(pause)


def simulate_execute_plan(plan, log_append, show_step_pause=1.2):
    for step in plan:
        sid = step["step_id"]
        cmd = step["cmd"]          # use "cmd" now
        args = step.get("args", {})  # args dict

        # Show step header
        log_append(f"STEP {sid:02d} | {cmd.upper():12} | {args}")
        time.sleep(show_step_pause)

        # Simulated behavior based on cmd
        if cmd == "page.goto":
            log_append(f'JSON >> {{"cmd":"page.goto","url":"{args.get("url")}","waitUntil":"{args.get("waitUntil")}"}}')
            time.sleep(1.0)
            log_append('JSON << {"status":"ok","httpStatus":200,"title":"Weekly Price Update"}')

        elif cmd == "locator.find":
            log_append(f'JSON >> {{"cmd":"locator.find","selector":"{args.get("selector")}"}}')
            time.sleep(1.0)
            log_append('JSON << {"status":"ok","matches":1,"coordinates":{"x":225,"y":820}}')

        elif cmd == "locator.click":
            log_append(f'JSON >> {{"cmd":"locator.click","selector":"{args.get("selector")}"}}')
            time.sleep(1.1)
            log_append('JSON << {"status":"ok","clicked":true}')

        elif cmd == "page.waitForEvent":
            log_append(f'JSON >> {{"cmd":"page.waitForEvent","event":"{args.get("event")}","timeout":{args.get("timeout")}}}')
            time.sleep(1.4)
            log_append(f'JSON << {{"status":"ok","filename":"{args.get("saveAs")}","size":1642KB}}')

        elif cmd == "pdf.parse":
            log_append(f'JSON >> {{"cmd":"pdf.parse","file":"{args.get("file")}","filters":{args.get("filters")}}}')
            time.sleep(1.4)
            log_append('JSON << {"status":"ok"}')

        else:
            log_append("STATUS >> step executed")

        time.sleep(0.6)

    # Return final hardcoded DataFrame
    df = pd.DataFrame(HARDCODED_RESULTS)
    return df
