#!/usr/bin/env python3
"""
Converts all canvas .tsx files to standalone HTML pages.
Run from: /Users/hdubey2/Personal/canvases/
"""

import os, re, shutil, sys

CANVAS_DIR = os.path.expanduser("~/.cursor/projects/Users-hdubey2-Personal/canvases")
# Output directory: first CLI arg wins, else the script's own directory.
# e.g.  python3 generate_html.py ~/MyGitPages
OUT_DIR    = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
# Base URL the landing page prints next to each canvas (GitHub Pages project site).
BASE_URL   = os.environ.get("PAGES_BASE_URL", "https://himanshu2405.github.io/MyGitPages/")

CSS = """
:root {
  --bg: #0f0f0f;
  --bg2: #1a1a1a;
  --bg3: #242424;
  --border: #2e2e2e;
  --text: #e8e8e8;
  --text2: #a0a0a0;
  --text3: #666;
  --accent: #4f8ef7;
  --success: #22c55e;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --neutral: #6b7280;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 14px; line-height: 1.6; }
.container { max-width: 1040px; margin: 0 auto; padding: 32px 24px; }
h1 { font-size: 24px; font-weight: 700; margin-bottom: 6px; }
h2 { font-size: 18px; font-weight: 600; margin: 24px 0 10px; }
h3 { font-size: 15px; font-weight: 600; margin: 16px 0 8px; }
p  { color: var(--text2); margin: 6px 0; }
.subtitle { color: var(--text2); margin-bottom: 20px; }

/* Tab nav */
.tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 20px 0 4px; }
.tab-btn { padding: 6px 14px; border: 1px solid var(--border); border-radius: 999px; background: transparent; color: var(--text2); cursor: pointer; font-size: 13px; transition: all .15s; }
.tab-btn:hover { border-color: var(--accent); color: var(--text); }
.tab-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
hr.divider { border: none; border-top: 1px solid var(--border); margin: 20px 0; }

/* Cards */
.card { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 12px; }
.card-header { padding: 12px 16px; font-weight: 600; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.card-body { padding: 14px 16px; }
.grid { display: grid; gap: 14px; }
.grid-2 { grid-template-columns: 1fr 1fr; }
.grid-3 { grid-template-columns: 1fr 1fr 1fr; }
.grid-4 { grid-template-columns: 1fr 1fr 1fr 1fr; }
@media(max-width:700px){ .grid-2,.grid-3,.grid-4 { grid-template-columns: 1fr; } }

/* Callouts */
.callout { border-left: 4px solid var(--neutral); background: var(--bg2); border-radius: 0 6px 6px 0; padding: 12px 14px; margin: 10px 0; }
.callout-title { font-weight: 600; font-size: 13px; margin-bottom: 4px; }
.callout.success { border-color: var(--success); }
.callout.warning { border-color: var(--warning); }
.callout.danger  { border-color: var(--danger);  }
.callout.info    { border-color: var(--info);    }
.callout.success .callout-title { color: var(--success); }
.callout.warning .callout-title { color: var(--warning); }
.callout.danger  .callout-title { color: var(--danger);  }
.callout.info    .callout-title { color: var(--info);    }

/* Pills */
.pill { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 500; }
.pill.success { background: rgba(34,197,94,.15); color: var(--success); }
.pill.warning { background: rgba(245,158,11,.15); color: var(--warning); }
.pill.danger  { background: rgba(239,68,68,.15);  color: var(--danger);  }
.pill.info    { background: rgba(59,130,246,.15); color: var(--info);    }
.pill.neutral { background: var(--bg3); color: var(--text2); }

/* Stats */
.stats { display: flex; flex-wrap: wrap; gap: 12px; margin: 16px 0; }
.stat-box { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; padding: 12px 18px; min-width: 130px; }
.stat-value { font-size: 20px; font-weight: 700; }
.stat-label { font-size: 12px; color: var(--text2); margin-top: 2px; }

/* Tables */
.tbl-wrap { overflow-x: auto; margin: 12px 0; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { background: var(--bg3); color: var(--text2); font-weight: 600; padding: 9px 12px; text-align: left; border-bottom: 1px solid var(--border); }
td { padding: 9px 12px; border-bottom: 1px solid var(--border); vertical-align: top; }
tr:last-child td { border-bottom: none; }
tr:nth-child(even) td { background: rgba(255,255,255,.02); }

/* Code */
pre, code { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 12px; }
pre { background: var(--bg3); border: 1px solid var(--border); border-radius: 6px; padding: 14px 16px; overflow-x: auto; line-height: 1.7; color: var(--text); white-space: pre; margin: 10px 0; }

/* Collapsible */
details { background: var(--bg2); border: 1px solid var(--border); border-radius: 8px; margin: 6px 0; }
summary { padding: 10px 14px; cursor: pointer; font-weight: 500; list-style: none; display: flex; justify-content: space-between; align-items: center; }
summary::after { content: "▸"; color: var(--text2); transition: transform .2s; }
details[open] summary::after { transform: rotate(90deg); }
details .details-body { padding: 12px 16px; border-top: 1px solid var(--border); }
.tag { font-size: 11px; color: var(--text3); }
ul.bullet { padding-left: 18px; }
ul.bullet li { color: var(--text2); margin: 4px 0; }
"""

JS = """
function initTabs(containerId) {
  var c = document.getElementById(containerId) || document;
  c.querySelectorAll('.tab-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var group = btn.dataset.group;
      c.querySelectorAll('.tab-btn[data-group="'+group+'"]').forEach(function(b){ b.classList.remove('active'); });
      c.querySelectorAll('.tab-panel[data-group="'+group+'"]').forEach(function(p){ p.classList.remove('active'); });
      btn.classList.add('active');
      var panel = c.querySelector('.tab-panel[data-group="'+group+'"][data-tab="'+btn.dataset.tab+'"]');
      if(panel) panel.classList.add('active');
    });
  });
}
document.addEventListener('DOMContentLoaded', function() { initTabs(); });
"""

def html_page(title, subtitle, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<p class="subtitle">{subtitle}</p>
<hr class="divider">
{body}
</div>
<script>{JS}</script>
</body>
</html>"""

def tabs(group, tab_list, panels):
    """tab_list = [(id,label)], panels = [(id, html)]"""
    btns = ""
    content = ""
    for i,(tid,label) in enumerate(tab_list):
        active = " active" if i==0 else ""
        btns += f'<button class="tab-btn{active}" data-group="{group}" data-tab="{tid}">{label}</button>\n'
    for i,(tid,panel_html) in enumerate(panels):
        active = " active" if i==0 else ""
        content += f'<div class="tab-panel{active}" data-group="{group}" data-tab="{tid}">{panel_html}</div>\n'
    return f'<div class="tabs">{btns}</div>\n<hr class="divider">\n{content}'

def card(header, body, pill=None):
    pill_html = f' <span class="pill neutral">{pill}</span>' if pill else ""
    return f'<div class="card"><div class="card-header">{header}{pill_html}</div><div class="card-body">{body}</div></div>'

def callout(tone, title, body):
    return f'<div class="callout {tone}"><div class="callout-title">{title}</div>{body}</div>'

def table(headers, rows):
    ths = "".join(f"<th>{h}</th>" for h in headers)
    trs = ""
    for row in rows:
        tds = "".join(f"<td>{c}</td>" for c in row)
        trs += f"<tr>{tds}</tr>"
    return f'<div class="tbl-wrap"><table><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>'

def stat_box(value, label):
    return f'<div class="stat-box"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'

def stats(*items):
    boxes = "".join(stat_box(v,l) for v,l in items)
    return f'<div class="stats">{boxes}</div>'

def collapsible(summary_text, body_html, tag=""):
    tag_html = f' <span class="tag">{tag}</span>' if tag else ""
    return f'<details><summary>{summary_text}{tag_html}</summary><div class="details-body">{body_html}</div></details>'

def grid2(*items):
    cells = "".join(f"<div>{i}</div>" for i in items)
    return f'<div class="grid grid-2">{cells}</div>'

def grid3(*items):
    cells = "".join(f"<div>{i}</div>" for i in items)
    return f'<div class="grid grid-3">{cells}</div>'

def ul(items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="bullet">{lis}</ul>'

def pill(text, tone="neutral"):
    return f'<span class="pill {tone}">{text}</span>'

def p(text, secondary=False):
    style = ' style="color:var(--text2)"' if secondary else ''
    return f'<p{style}>{text}</p>'

def h2(text): return f'<h2>{text}</h2>'
def h3(text): return f'<h3>{text}</h3>'
def pre(code): return f'<pre>{code}</pre>'

def b(text): return f'<strong>{text}</strong>'

def field(label, value):
    return (f'<div style="margin:8px 0">'
            f'<div style="font-size:11px;color:var(--text3);font-weight:600;letter-spacing:.04em;text-transform:uppercase">{label}</div>'
            f'<p style="margin-top:2px;color:var(--text2)">{value}</p></div>')

def caption(text):
    return f'<p style="color:var(--text3);font-size:12px;margin:6px 0 14px">{text}</p>'

def bars(items, prefix="", suffix=""):
    """items = [(label, value)] — simple horizontal bar chart."""
    maxv = max((v for _, v in items), default=1) or 1
    rows = ""
    for label, v in items:
        pct = max(2, round(v / maxv * 100))
        rows += (f'<div style="margin:9px 0">'
                 f'<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text2);margin-bottom:4px">'
                 f'<span>{label}</span><span style="color:var(--text)">{prefix}{v}{suffix}</span></div>'
                 f'<div style="background:var(--bg3);border-radius:4px;height:10px;overflow:hidden">'
                 f'<div style="width:{pct}%;height:100%;background:var(--accent)"></div></div></div>')
    return f'<div style="margin:12px 0">{rows}</div>'

def pill_row(items, tone="neutral"):
    inner = "".join(f'<span class="pill {tone}" style="margin:0">{i}</span>' for i in items)
    return f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0">{inner}</div>'

def chip_flow(items):
    """lifecycle chips separated by chevrons"""
    parts = []
    for i, s in enumerate(items):
        parts.append(f'<span class="pill neutral">{s}</span>')
        if i < len(items) - 1:
            parts.append('<span style="color:var(--text3)">&rsaquo;</span>')
    return f'<div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0">{"".join(parts)}</div>'

def steps_list(steps):
    """steps = [(n, title, body)]"""
    out = ""
    for n, title, body in steps:
        out += (f'<div style="display:flex;gap:12px;align-items:flex-start;margin:12px 0">'
                f'<div style="min-width:24px;height:24px;border-radius:999px;background:var(--bg3);'
                f'display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;flex-shrink:0">{n}</div>'
                f'<div><div style="font-weight:600">{title}</div><p style="margin-top:2px;color:var(--text2)">{body}</p></div></div>')
    return out

def mini_grid(items, cols=4):
    """items = [(title, body)] — small borderless cards in a grid"""
    cells = ""
    for title, body in items:
        cells += (f'<div style="background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:12px 14px">'
                  f'<div style="font-weight:600;font-size:13px">{title}</div>'
                  f'<p style="margin-top:3px;color:var(--text2);font-size:12px">{body}</p></div>')
    return f'<div class="grid grid-{cols}" style="margin:12px 0">{cells}</div>'

# ─────────────────────────────────────────────────────────────────────────────
# 1. ALPHASENSE DS ANALYSIS FRAMEWORK
# ─────────────────────────────────────────────────────────────────────────────

def make_alphasense_ds():
    body = ""

    # Overview
    overview = (
        h2("AlphaSense DS Interview — Role Analysis Framework") +
        callout("info", "What this covers",
            p("Strategic DS framework for AlphaSense: 7-tab analysis covering role framing, product context, "
              "metrics design, causal inference, experiment design, stakeholder communication, and 90-day plan.")) +
        stats(
            ("Senior DS", "Target Role"),
            ("GenAI/Retention", "Core Domain"),
            ("7 Tabs", "Sections"),
            ("B2B SaaS", "Context"),
        ) +
        grid2(
            card("Core Thesis",
                p("AlphaSense DS roles require blending product analytics (retention metrics, A/B testing) "
                  "with causal inference and ML modeling. The GenAI wave creates a specific analytical challenge: "
                  "separating novelty-driven spikes from true habit formation.")),
            card("Your Edge",
                p("Bayesian experimentation + PSM + AIPW experience from Mailchimp directly matches what "
                  "AlphaSense needs. The SMS cross-sell experiment ($2.3M, 96% Bayesian confidence) and the "
                  "integrations causal study (Canva +19pp) are direct proof points.")),
        )
    )

    # Product context
    product = (
        h2("AlphaSense Product Context") +
        table(
            ["Feature", "What It Does", "User Habit Signal", "DS Challenge"],
            [
                ["Generative Search", "Natural language research queries with cited answers", "Unprompted daily return to search bar", "Separate habit from novelty; thread depth as engagement proxy"],
                ["Deep Research", "30-min autonomous analyst-grade research", "Weekly Deep Research run per active project", "Low frequency, high ROI — hard to measure in short windows"],
                ["Smart Summaries", "60-second earnings catch-up on covered companies", "Earnings-day return rate vs non-earnings days", "Event-driven — retention cadence tied to earnings calendar"],
                ["Generative Grid", "Multi-document comparative analysis table", "Repeat grid creation within same research thread", "Requires workflow integration to become habitual"],
                ["Workflow Agents", "Scheduled recurring research delivery", "# scheduled agents per user", "Push-to-pull mindset shift — strongest retention anchor"],
                ["Due Diligence Workspace", "VDR upload + specialized DD agents", "Workspace sessions per active deal", "Deal lifecycle forces re-engagement — natural retention moat"],
                ["Monitoring & Alerts", "Push notifications on watchlist movements", "Notification-to-session conversion rate", "Alerts fire the cue — conversion measures cue effectiveness"],
            ]
        )
    )

    # Metrics
    metrics = (
        h2("Metrics Framework") +
        callout("success", "North Star Candidates",
            p("WAU/DAU ratio by GenAI cohort | D7/D30/D90 retention curves | Unprompted return rate | "
              "Feature adoption breadth | Seat expansion rate")) +
        h3("Primary Metrics") +
        table(
            ["Metric", "Type", "Why It Matters", "Implementation Note"],
            [
                ["WAU/DAU ratio by GenAI cohort", "Core retention health", "Is GenAI driving more frequent, consistent engagement?", "Track separately for each feature adoption tier"],
                ["D7 / D30 / D90 retention curves", "Lagging retention", "Does GenAI adoption shift the churn cliff forward?", "Plot GenAI adopters vs non-adopters, by feature depth"],
                ["Feature adoption breadth", "Engagement depth", "# GenAI features actively used per user per month", "Single-feature vs multi-feature users have different LTV"],
                ["Seat expansion rate", "Business outcome", "Do GenAI-habituated users trigger new license seats?", "Link to CRM expansion events within 90 days of activation"],
                ["Unprompted return rate", "Habit formation", "Sessions initiated without email/notification trigger", "Best single proxy for intrinsic habit; requires session attribution"],
            ]
        ) +
        h3("Leading Indicators") +
        table(
            ["Metric", "Signal Type", "Insight"],
            [
                ["Time-to-first-GenAI in session", "Habit cue strength", "Is GenAI becoming the default starting point?"],
                ["Follow-up query rate (Gen Search)", "Thread depth = value realization", "Users who ask 2+ follow-ups are 3x more likely to return next day"],
                ["Scheduled agent count per user", "Push-to-pull mindset shift", "Highest-conviction habit signal — user trusts platform to work for them"],
                ["Citation click-through rate", "Output trust proxy", "High click rate = user validates answers = growing confidence in AI quality"],
                ["Output share/export rate", "Social reinforcement loop", "When users share Deep Research outputs, they anchor colleagues on the platform"],
                ["Alert-to-session conversion", "Monitoring habit trigger", "Alerts fire the cue; conversion measures whether the cue is working"],
            ]
        ) +
        h3("Guardrail Metrics") +
        table(
            ["Guardrail", "Severity", "What to Watch"],
            [
                ["Novelty decay check", pill("danger","danger"), "Flag if GenAI session share drops >15% from D7 to D30 for any activation cohort"],
                ["Keyword search displacement", pill("warning","warning"), "Track if traditional boolean search volume declines as GenAI grows"],
                ["SRM on all rollout experiments", pill("danger","danger"), "Enterprise B2B users self-select into features heavily; SRM violations will be common"],
                ["Hallucination proxy rate", pill("warning","warning"), "High rephrase/correction rate after first answer = user distrust = habit will not form"],
                ["Breadth guardrail: median user", pill("info","info"), "Don't optimize for power users. Track GenAI adoption at P50, not P90"],
            ]
        )
    )

    # Experiment design
    experiments = (
        h2("Experiment Design Portfolio") +
        callout("warning", "The B2B Experiment Constraint",
            p("You cannot do a clean holdout of a core feature on enterprise B2B users the way a consumer app can. "
              "Annual contracts, procurement cycles, and enterprise expectations require creative causal identification.")) +
        table(
            ["Method", "When to Use", "Priority", "Key Tradeoff"],
            [
                ["Staggered Rollout DiD", "Any new GenAI feature launch with phased rollout", pill("success","success")+" Primary", "Requires parallel trends assumption. Firm-size differences across waves can confound"],
                ["Within-Firm Holdout", "Feature launches where individual randomization is possible", pill("success","success")+" Primary", "SUTVA risk — same-firm users compare notes; ethical tension with holdout group"],
                ["Activation Gate Experiment", "Onboarding optimization", pill("info","info")+" High", "Short-run experiment; need 90-day holdout to separate early activation from novelty"],
                ["Feature Discovery Nudge", "Users active but not using GenAI features", pill("info","info")+" High", "Risk of notification fatigue; keep nudge treatment arms narrow and targeted"],
                ["Persona-Stratified Cohort Analysis", "Ongoing measurement (not an experiment)", pill("info","info")+" High", "Observational only — surfaces where impact is strongest but cannot claim causality"],
                ["Long-Run Global Holdout", "Core GenAI surface (Generative Search) is mature", pill("warning","warning")+" Strategic", "Significant opportunity cost; ethically tricky for premium B2B users"],
            ]
        ) +
        h3("Experiment Sequencing") +
        table(
            ["Quarter", "Experiment", "Goal", "Decision It Enables"],
            [
                ["Q3 2026", "Activation Gate Experiment (onboarding)", "Does faster path to GenAI aha-moment lift D7 retention?", "Prioritize onboarding investment vs feature depth"],
                ["Q3 2026", "Feature Discovery Nudge (dormant GenAI users)", "Can we convert non-GenAI active users?", "Identify unrealized TAM within existing customer base"],
                ["Q4 2026", "Staggered Rollout DiD (next feature wave)", "Isolate WAU/DAU impact of new Workflow Agent types", "Prove ROI of agent roadmap to exec team"],
                ["Q4 2026", "Within-Firm Holdout (Generative Grid)", "Clean causal estimate for Grid retention lift", "Grid pricing / feature tiering decision"],
                ["Q1 2027", "Global Holdout — Generative Search", "Gold-standard LTV impact of core GenAI surface", "Justify AI-tier pricing and GenAI investment level"],
                ["Ongoing", "Persona-Stratified Cohort Analysis", "Which user roles benefit most from GenAI habit?", "Targeted onboarding and feature prioritization by segment"],
            ]
        )
    )

    # Strategic implications
    strategy = (
        h2("Strategic Scenarios") +
        grid2(
            card("Scenario A: GenAI IS driving habit",
                p("Signals: Scheduled agents growing, unprompted return rising, D30 retention gap >8pp between adopters and non-adopters") +
                h3("Strategic Actions") +
                ul([
                    "Reframe pricing: AI-tier or usage-based pricing becomes defensible",
                    "Collapse the activation funnel: bottleneck is getting users to first high-quality output",
                    "Invest in scheduled agents as #1 habit anchor — push-to-pull is your retention moat",
                    "Personalization: use query history to suggest next research",
                    "Mobile as second habit trigger: complete the loop proactively",
                ]) +
                callout("success", "Moat",
                    p("Institutional knowledge lock-in: saved agents, grids, templates, and query history make switching catastrophically expensive")),
                pill("Scenario A", "success")),
            card("Scenario B: GenAI is NOT driving habit",
                p("Signals: D30 retention gap between GenAI users and non-users narrows or disappears, novelty decay visible") +
                h3("Strategic Actions") +
                ul([
                    "Stop optimizing GenAI engagement volume — it doesn't predict retention",
                    "Diagnose which specific features do show retention signal",
                    "Invest in onboarding: the problem is likely activation, not the feature itself",
                    "Qualitative research: interview 20 churned users who tried GenAI",
                    "Re-examine the pricing model: don't charge for features that don't retain",
                ]) +
                callout("warning", "Moat",
                    p("Traditional search moat remains; focus on workflow integration and data coverage depth")),
                pill("Scenario B", "warning")),
        ) +
        h3("90-Day PM Action List") +
        table(
            ["Priority", "Action", "Owner Signal", "Success Criteria"],
            [
                ["1", "Define 'GenAI activation moment' for each user persona", "Product + Data", "Single agreed definition per role segment, tracked in event stream"],
                ["2", "Instrument session-level entry trigger attribution", "Engineering + Analytics", "% of sessions tagged as direct / notification / referral"],
                ["3", "Launch activation gate onboarding experiment (Q3)", "Product + Growth", "D7 retention +5pp for treatment vs control"],
                ["4", "Build leading indicator dashboard with weekly cadence", "Analytics", "Unprompted return rate, follow-up query rate, scheduled agent count"],
                ["5", "Run qualitative interviews: churned users who tried GenAI", "Product Research", "5+ user interviews per role segment"],
                ["6", "Align exec team on GenAI pricing hypothesis before Q4 planning", "PM + Strategy", "Single pricing model hypothesis approved for Q4 experiment"],
            ]
        )
    )

    body = tabs("main",
        [("overview","Overview"),("product","Product Context"),("metrics","Metrics"),("experiments","Experiments"),("strategy","Strategy")],
        [("overview",overview),("product",product),("metrics",metrics),("experiments",experiments),("strategy",strategy)]
    )
    return html_page(
        "AlphaSense — DS Analysis Framework",
        "Measuring the true impact of GenAI features on WAU/DAU retention and user habit formation",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 2. ALPHASENSE GENAI IMPACT FRAMEWORK (tabs: Problem, Feature×Habit, Metrics, Experiment, Strategy)
# ─────────────────────────────────────────────────────────────────────────────

def make_alphasense_genai():
    problem = (
        h2("The Core Measurement Problem") +
        callout("warning", "The Novelty Trap",
            p("Every new feature sees an engagement spike at launch. The hard question is: does GenAI produce "
              "sustained habit formation, or is it driven by novelty? The answer determines pricing strategy, "
              "roadmap investment, and retention model.")) +
        grid2(
            card("What we can measure today",
                ul(["Session volume and WAU/DAU","Feature-specific click and activation rates","User cohort retention curves","Self-reported NPS / satisfaction"])),
            card("What we cannot easily measure",
                ul(["Intrinsic habit vs push-driven return","True causal impact (selection: power users adopt first)","Long-run LTV change from GenAI activation","Whether GenAI replaced or supplemented traditional search"])),
        ) +
        h3("Three Competing Hypotheses") +
        table(
            ["Hypothesis", "What the Data Shows", "Strategic Implication"],
            [
                ["H1: GenAI drives genuine habit", "D30 retention gap persists; unprompted return growing; scheduled agents expanding", "AI-tier pricing justified; activation funnel is the bottleneck to fix"],
                ["H2: GenAI drives novelty, not habit", "D7 to D30 decay visible; GenAI session share declining cohort-over-cohort", "Retention moat still in traditional search + data coverage; GenAI is a feature, not a platform"],
                ["H3: Heterogeneous by persona", "Analysts retain via GenAI; C-suite does not; PMs in between", "Persona-specific onboarding and pricing tiers; don't average across roles"],
            ]
        )
    )

    feature_habit = (
        h2("Feature × Habit Loop Map") +
        callout("info", "The Habit Loop Framework",
            p("Cue → Routine → Reward → Investment. For each GenAI feature, map: what triggers use (cue), "
              "what action is taken (routine), what value is delivered (reward), and what makes switching costly (investment).")) +
        table(
            ["Feature", "Cue", "Routine", "Reward", "Investment", "Habit Signal", "Activation Proxy"],
            [
                ["Generative Search", "Research question surfaces", "Natural language query + follow-up thread", "Cited analyst-grade answer in seconds", "Saved search threads, query history", "Unprompted daily return to search bar", "First query with 2+ follow-ups in one thread"],
                ["Deep Research", "Complex project or coverage initiation", "Queue 30-min autonomous analysis", "Analyst-grade company primer / market landscape", "Formatting templates, saved prompts, institutional outputs", "Weekly Deep Research run per active project", "First output downloaded or shared"],
                ["Smart Summaries", "Earnings event or company filing", "Open summary before reading full transcript", "60-second catch-up on key points + analyst Q&A", "Watchlist of covered companies", "Earnings-day return rate vs non-earnings days", "First summary opened within 24h of earnings release"],
                ["Generative Grid", "Cross-company or multi-doc comparison task", "Build multi-document prompt table", "Structured comparative analysis in one view", "Saved grid templates, reusable prompt sets", "Repeat grid creation within same research thread", "First grid with 3+ documents and live feed enabled"],
                ["Workflow Agents", "Recurring research delivery need", "Schedule pre-built or custom agent", "Research pushed proactively — no manual pull", "Custom agent configurations, scheduled cadences", "# scheduled agents per user (push > pull mindset shift)", "First scheduled agent delivering to inbox"],
                ["Due Diligence Workspace", "New deal / M&A opportunity initiated", "Upload VDR + run specialized DD agents", "Deal-ready insights, IC prep, risk surfacing", "Deal workspace with VDR files, custom agents, team sharing", "Workspace sessions per active deal, cross-reference queries", "First workspace with 5+ documents and one AI agent run"],
                ["Monitoring & Alerts", "Platform detects movement on watchlist", "Push notification → open platform to read context", "Ahead of market / competitor on breaking development", "Curated watchlists, alert thresholds, coverage breadth", "Notification-to-session conversion rate", "First alert that triggers a same-session follow-up query"],
            ]
        )
    )

    metrics_tab = (
        h2("Metrics Framework") +
        h3("Primary Retention Metrics") +
        table(
            ["Metric", "Purpose", "Why It Matters", "Implementation Note"],
            [
                ["WAU/DAU ratio by GenAI cohort", "Core retention health", "Is GenAI driving more frequent, consistent engagement?", "Track separately for each feature adoption tier"],
                ["D7 / D30 / D90 retention curves", "Lagging retention", "Does adoption of GenAI shift the churn cliff forward?", "Plot GenAI adopters vs non-adopters, by feature depth"],
                ["Feature adoption breadth", "Engagement depth", "# GenAI features actively used per user per month", "Single-feature vs multi-feature users have different LTV"],
                ["Seat expansion rate", "Business outcome", "Do GenAI-habituated users trigger new license seats?", "Link to CRM expansion events within 90 days of activation"],
                ["Unprompted return rate", "Habit formation", "Sessions initiated without email/notification trigger", "Best single proxy for intrinsic habit; requires session attribution"],
            ]
        ) +
        h3("Leading Indicators") +
        table(
            ["Metric", "Signal Type", "Insight"],
            [
                ["Time-to-first-GenAI in session", "Habit cue strength", "Is GenAI becoming the default starting point?"],
                ["Follow-up query rate (Gen Search)", "Thread depth", "Users who ask 2+ follow-ups are 3x more likely to return next day"],
                ["Scheduled agent count per user", "Push-to-pull mindset shift", "Highest-conviction habit signal"],
                ["Citation click-through rate", "Output trust proxy", "High click rate = user validates answers = growing confidence in AI quality"],
                ["Output share/export rate", "Social reinforcement loop", "When users share Deep Research outputs, they anchor colleagues"],
                ["Alert-to-session conversion", "Monitoring habit trigger", "Conversion measures whether the cue is working"],
            ]
        ) +
        h3("Guardrail Metrics") +
        table(
            ["Guardrail", "Severity", "Rule"],
            [
                ["Novelty decay check", pill("danger","danger"), "Flag if GenAI session share drops >15% from D7 to D30 for any activation cohort"],
                ["Keyword search displacement", pill("warning","warning"), "Track if traditional search volume declines as GenAI grows — displacement vs net-new usage matters"],
                ["SRM on all rollout experiments", pill("danger","danger"), "Enterprise B2B users self-select into features heavily; SRM violations will be common"],
                ["Hallucination proxy rate", pill("warning","warning"), "High rephrase/correction rate after first answer = user distrust = habit will not form"],
                ["Breadth guardrail: median user", pill("info","info"), "Don't optimize for power users. Track GenAI adoption at the P50 user, not the P90"],
                ["SUTVA violations", pill("warning","warning"), "Enterprise colleagues talk. Spillover from treatment to control within same firm is likely"],
            ]
        )
    )

    experiment_tab = (
        callout("warning", "The B2B Experiment Design Constraint",
            p("You cannot do a clean holdout of a core feature on enterprise B2B users. Annual contracts, "
              "procurement cycles, and enterprise expectations mean you need creative causal identification strategies.")) +
        h2("Experiment Portfolio") +
        table(
            ["Method", "When to Use", "Priority", "Key Tradeoff"],
            [
                ["Staggered Rollout DiD", "Any new GenAI feature launch with phased rollout", pill("Primary","success"), "Requires parallel trends assumption; firm-size differences across waves can confound"],
                ["Within-Firm Holdout", "Feature launches where individual randomization is possible", pill("Primary","success"), "SUTVA violations — same-firm users compare notes"],
                ["Activation Gate Experiment", "Onboarding optimization", pill("High","info"), "Short-run experiment; need 90-day holdout to see if activation holds vs novelty"],
                ["Feature Discovery Nudge", "Users active but not using GenAI features", pill("High","info"), "Risk of notification fatigue; keep nudge treatment arms narrow"],
                ["Persona-Stratified Cohort Analysis", "Ongoing measurement (not an experiment)", pill("High","info"), "Observational only — cannot claim causality"],
                ["Long-Run Global Holdout", "Core GenAI surface (Generative Search) is mature", pill("Strategic","warning"), "Significant opportunity cost; ethically tricky for premium B2B users"],
            ]
        ) +
        h3("Experiment Sequencing") +
        table(
            ["Quarter", "Experiment", "Goal", "Decision It Enables"],
            [
                ["Q3 2026", "Activation Gate Experiment (onboarding)", "Does faster path to GenAI aha-moment lift D7 retention?", "Prioritize onboarding investment vs feature depth"],
                ["Q3 2026", "Feature Discovery Nudge (dormant GenAI users)", "Can we convert non-GenAI active users?", "Identify unrealized TAM within existing customer base"],
                ["Q4 2026", "Staggered Rollout DiD (next feature wave)", "Isolate WAU/DAU impact of new Workflow Agent types", "Prove ROI of agent roadmap to exec team"],
                ["Q4 2026", "Within-Firm Holdout (Generative Grid)", "Clean causal estimate for Grid retention lift", "Grid pricing / feature tiering decision"],
                ["Q1 2027", "Global Holdout — Generative Search", "Gold-standard LTV impact of core GenAI surface", "Justify AI-tier pricing and GenAI investment level"],
                ["Ongoing", "Persona-Stratified Cohort Analysis", "Which user roles benefit most from GenAI habit?", "Targeted onboarding and feature prioritization by segment"],
            ]
        )
    )

    strategy_tab = (
        h2("Strategic Decision Framework") +
        grid2(
            card("Scenario A — GenAI IS driving habit",
                p("Signals: Scheduled agents growing, unprompted return rising, D30 retention gap >8pp") +
                h3("Actions") + ul([
                    "Reframe pricing: AI-tier or usage-based pricing becomes defensible",
                    "Collapse the activation funnel: bottleneck is first high-quality output",
                    "Invest in scheduled agents as #1 habit anchor",
                    "Personalization: use query history to suggest next research",
                    "Mobile as second habit trigger: complete the proactive loop",
                ]) + callout("success", "Moat",
                    p("Institutional knowledge lock-in: saved agents, grids, templates make switching catastrophically expensive")),
                pill("Scenario A","success")),
            card("Scenario B — GenAI is NOT driving habit",
                p("Signals: D30 retention gap narrows, novelty decay visible in cohort data") +
                h3("Actions") + ul([
                    "Stop optimizing GenAI engagement volume — it doesn't predict retention",
                    "Diagnose which specific features do show retention signal",
                    "Invest in onboarding — the problem is activation, not the feature",
                    "Qualitative research: interview 20 churned users who tried GenAI",
                    "Re-examine pricing model: don't charge for features that don't retain",
                ]) + callout("warning", "Moat",
                    p("Traditional search moat remains; focus on workflow integration and data coverage depth")),
                pill("Scenario B","warning")),
        ) +
        h3("Business Implications Regardless of Outcome") +
        table(
            ["Area", "Implication"],
            [
                ["Pricing architecture", "If GenAI habit data shows measurable LTV lift, the platform earns the right to separate AI-tier pricing. Scheduled agents and Deep Research are strongest candidates — they deliver quantifiable analyst hour savings."],
                ["Platform vs point tool", "The endgame is making AlphaSense the research infrastructure layer. Scheduled agents, Due Diligence Workspaces, and Enterprise Intelligence uploads make switching catastrophically expensive."],
                ["Persona-led roadmap", "GenAI's WAU/DAU impact is almost certainly heterogeneous across roles. Sell-side analysts → Smart Summaries + Grid; buy-side PMs → Deep Research + Agents; deal teams → Due Diligence Workspace."],
                ["LTV and seat expansion model", "Habit-formed users are the expansion vehicle. When an analyst makes AlphaSense indispensable, they advocate for more licenses. Track whether GenAI-activated users have higher 12-month seat expansion rates."],
            ]
        )
    )

    body = tabs("main",
        [("problem","The Problem"),("feature_habit","Feature × Habit Map"),("metrics","Metrics"),("experiment","Experiment Design"),("strategy","Strategic Implications")],
        [("problem",problem),("feature_habit",feature_habit),("metrics",metrics_tab),("experiment",experiment_tab),("strategy",strategy_tab)]
    )
    return html_page(
        "AlphaSense — GenAI Impact Framework",
        "Deep strategic analysis: measuring the true impact of GenAI features on WAU/DAU retention and user habit formation",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 3. CAUSAL TRAINING STUDY GUIDE
# ─────────────────────────────────────────────────────────────────────────────

def make_causal_training():
    decision = (
        h2("Decision Tree: Which Method to Use?") +
        table(
            ["Condition", "Sample Size", "Recommended Method", "Notes"],
            [
                ["Can be tested (RCT possible)", "Large", "A/B Test (RCT)", "Gold standard. Randomization ensures balance across all confounders. Chi-square balance check validates the experiment."],
                ["Can be tested (RCT possible)", "Small", "Multivariate / Factorial Test", "For low-traffic features or multi-factor experiments. Power calculation required."],
                ["Cannot be tested", "Units can be matched on covariates", "Matching + DiD", "Silver standard. Create synthetic twins, compare pre/post window. SMS credit study used this path."],
                ["Cannot be tested", "No good match units exist", "Time-Series Causal Inference", "Compare trends before/after an intervention over time. Useful for go-to-market or market-level interventions."],
            ]
        )
    )

    confounders = (
        h2("Confounders — What They Are & Examples") +
        callout("info", "Definition",
            p("A confounder is a variable that (1) influences the treatment assignment AND (2) independently affects the outcome. "
              "Without controlling for it, you conflate the confounder's effect with the treatment effect.")) +
        table(
            ["Independent (Treatment)", "Dependent (Outcome)", "Confounder", "Explanation", "Tag"],
            [
                ["SMS credit purchase", "Non-SMS revenue (halo)", "Pre-existing engagement level",
                 "Highly engaged users are more likely to buy SMS credits AND are already on a trajectory of higher Mailchimp spend. Without matching, SMS appears to cause more revenue — but those users were already growing faster.",
                 pill("SMS Study","info")],
                ["SMS credit purchase", "Upgrading Mailchimp plan", "Account age (tenure)",
                 "Older accounts are more likely to try new products like SMS AND are also more likely to upgrade because their contact list has grown over time. Tenure is a confounder for both.",
                 pill("SMS Study","info")],
                ["Sunburn", "Ice cream sales", "Hot weather",
                 "Hot weather causes people to go to the beach → sunburn. Hot weather also makes people crave cold food → ice cream sales. Without controlling for temperature, sunburn looks like it drives ice cream sales.",
                 pill("Classic","neutral")],
                ["Using Mailchimp Forms", "User retention", "Engagement level (self-selection)",
                 "Forms users are already the most engaged users. Highly engaged users retain at higher rates regardless of the feature they use. This is why the Forms team's retention metric was not causal.",
                 pill("Mailchimp","warning")],
            ]
        )
    )

    bias_types = (
        h2("Bias Types") +
        h3("Selection Bias") +
        callout("warning", "Selection Bias",
            p("<strong>Definition:</strong> The group you observe is not representative because of how they self-selected into it. The most motivated, capable, or engaged users end up in the 'treated' group — and they would have outperformed anyway.") +
            p("<strong>Example:</strong> SMS credit buyers at Mailchimp were already the most active users — bigger contact lists, more email sends, higher AOV, more logins. Comparing them directly to average users overstates the impact of SMS. Without matching, you're comparing power users to average users.") +
            p("<strong>Fix:</strong> CEM: match SMS buyers to non-buyers on all 11 pre-purchase covariates. Only then compare outcomes — so you're seeing what SMS caused, not who already was going to succeed.")) +
        h3("Survivorship Bias") +
        callout("danger", "Survivorship Bias",
            p("<strong>Definition:</strong> You only analyze units that 'survived' a filter — users still on the platform, users who completed onboarding, planes that returned from missions.") +
            p("<strong>Example:</strong> WWII: engineers added armor where returning planes had bullet holes. Statistician Wald said: reinforce where there are NO holes — the planes hit there never came back. SMS analogy: if you only study active SMS senders, you miss the users who tried SMS and churned.") +
            p("<strong>Fix:</strong> Include churned users in your cohort window. Include pre-period baseline. Diff-in-diff nets out the trend.")) +
        h3("Confirmation Bias") +
        callout("info", "Confirmation Bias",
            p("<strong>Definition:</strong> You want to see SMS work, so you look for correlations and segments that confirm it.") +
            p("<strong>Example:</strong> Looking at the raw correlation between SMS adoption and revenue lift and presenting it as proof SMS works — without accounting for the fact that better customers adopt SMS.") +
            p("<strong>Fix:</strong> Pre-register your hypothesis. CEM forces you to commit to covariates before looking at outcomes. The placebo test (fake treatment → ~zero effect) is the gold standard."))
    )

    matching_methods = (
        h2("Matching Methods") +
        table(
            ["Method", "How It Works", "Pro", "Con", "Production Verdict"],
            [
                ["Nearest Neighbor (PSM)", "Fit a propensity model. Each treated user matched to closest control by PS distance. Greedy: one pair at a time.",
                 "Simple and interpretable. Good first pass.", "Balance depends entirely on propensity model quality. Drops unmatched controls.",
                 pill("Robustness check","neutral")],
                ["Full Matching", "Globally minimizes total distance across all matches. Each treated user matched to 1+ controls. Variable ratio, no units dropped.",
                 "Keeps all units. Better global balance.", "Still depends on propensity model. Variable ratio complicates weighted estimation.",
                 pill("Coded alternative","neutral")],
                ["CEM (Coarsened Exact Matching)", "Coarsen each covariate into bins. Exact match within the same bin combination. No propensity model needed.",
                 "Balance GUARANTEED by construction. Transparent. Model-free.",
                 "More covariates = more empty bin combinations = more units dropped.",
                 pill("PRODUCTION — 13,501 buyers matched to 522,440 controls","success")],
            ]
        ) +
        callout("success", "Why CEM over PSM for the SMS Study",
            p("PSM balance is assumed from the model — you check it after. CEM balance is guaranteed by construction. "
              "For a study with strong confounders (selection bias from power-user adoption), model-free matching "
              "is the more defensible choice for external audiences."))
    )

    assumptions = (
        h2("Core Causal Assumptions (SUTVA + CIA)") +
        table(
            ["Assumption", "What It Means", "How to Test / Mitigate"],
            [
                ["SUTVA — No Interference", "One unit's treatment doesn't affect another's outcome",
                 "Use cluster randomization; restrict analysis to non-referred users"],
                ["SUTVA — Single Version of Treatment", "All treated units receive the same treatment",
                 "Stratify by treatment intensity; analyze sub-groups"],
                ["CIA (Conditional Independence)", "Given observed covariates, treatment is as-good-as-random",
                 "Cannot be directly tested. Placebo test (pre-period outcome) provides evidence. E-value / Rosenbaum bounds quantify sensitivity."],
                ["Overlap / Common Support", "Every treated unit has a comparable control unit",
                 "Check PS distribution overlap histogram. Trim extreme PS values."],
                ["No Anticipation", "Control units don't change behavior before treatment starts",
                 "Use sharp rollout with no pre-announcement; define control window carefully."],
            ]
        ) +
        h3("Placebo Tests") +
        callout("info", "Placebo Test (Pre-Period ATT)",
            p("Run your matching and estimation on a period BEFORE the actual treatment. If your method is correct, "
              "the estimated ATT should be near zero — there was no treatment yet, so there should be no effect. "
              "If you find a large pre-period effect, your matching is picking up pre-existing trend differences, "
              "not the causal effect of treatment.")) +
        h3("Sensitivity Analysis") +
        callout("neutral", "E-Value and Rosenbaum Bounds",
            p("E-value: how strong would an unmeasured confounder need to be (in terms of risk ratio) to explain "
              "away your result? A high E-value means the result is robust to hidden bias. "
              "Rosenbaum bounds: bound on how much hidden bias could shift your p-value. "
              "If the result holds up to a sensitivity parameter Γ=2, it means a hidden confounder would need to "
              "double the odds of treatment to overturn the finding."))
    )

    did_section = (
        h2("Difference-in-Differences (DiD)") +
        callout("info", "Core Logic",
            p("DiD compares the change in outcomes over time for a treated group vs a control group. "
              "The key assumption is 'parallel trends': in the absence of treatment, both groups would have "
              "followed the same trend. The treatment effect is the difference in trends.")) +
        table(
            ["Component", "Description", "SMS Study Application"],
            [
                ["Pre-period", "Outcome measured before treatment assignment", "6-month window before SMS credit purchase"],
                ["Post-period", "Outcome measured after treatment starts", "6-month window after SMS credit purchase"],
                ["Treated group", "Units that received the treatment", "13,501 users who bought SMS credits"],
                ["Control group", "Matched units that didn't receive treatment", "522,440 matched non-buyers (CEM)"],
                ["DiD estimator", "ATT = (Y_treated_post - Y_treated_pre) - (Y_control_post - Y_control_pre)", "Revenue uplift attributed to SMS adoption after controlling for pre-trends"],
            ]
        ) +
        h3("Parallel Trends Assumption") +
        callout("warning", "Verifying Parallel Trends",
            p("Plot the outcome for treated and control groups for multiple periods BEFORE treatment. "
              "If the lines are parallel (same slope), the parallel trends assumption is plausible. "
              "If they're diverging, your control group is a bad counterfactual."))
    )

    body = tabs("main",
        [("decision","Decision Tree"),("confounders","Confounders"),("bias","Bias Types"),("matching","Matching Methods"),("assumptions","Assumptions"),("did","DiD")],
        [("decision",decision),("confounders",confounders),("bias",bias_types),("matching",matching_methods),("assumptions",assumptions),("did",did_section)]
    )
    return html_page(
        "Causal Inference — Training Study Guide",
        "End-to-end causal training: from bias types to matching methods, DiD, and sensitivity analysis. Grounded in the SMS credit study.",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 4. CHURN / RETENTION MODEL WALKTHROUGH (WebstaurantStore)
# ─────────────────────────────────────────────────────────────────────────────

def make_churn_retention():
    spine = (
        h2("The Spine — 16-Section Interview Script") +
        callout("info", "How to Use This",
            p("Each section gives the words to say, the questions to ask the interviewer, the reasoning behind every "
              "choice, and the follow-ups to expect. Navigate it the way you would drive the shared Google Doc.")) +
        table(
            ["Section", "Key Message"],
            [
                ["0 · The Spine", "Frame the entire case before touching data — business goal first"],
                ["1 · Business Framing", "Ask clarifying questions: what does churn mean here? What's the cost?"],
                ["2 · Business Context", "B2B foodservice: restaurants cycle, seasonal patterns, bulk ordering"],
                ["3 · Label Definition", "Binary churn label; define the observation window carefully"],
                ["4 · Feature Ideation", "RFM + product breadth + order cadence + category mix"],
                ["5 · EDA & Data Quality", "Null rates, class imbalance, outliers, temporal consistency"],
                ["6 · Seasonality", "Restaurant seasonality affects RFM features and label timing"],
                ["7 · Split & Leakage", "Temporal train/test split — never use future data in training features"],
                ["8 · Model Choice", "XGBoost as baseline; logistic regression for interpretability check"],
                ["9 · Hyperparameters", "Grid search on max_depth, learning_rate, n_estimators, subsample"],
                ["10 · Class Imbalance", "Likely 5-15% churn rate; use scale_pos_weight or class weights"],
                ["11 · Evaluation", "AUC-ROC, Precision-Recall, F1; calibration curve for probability outputs"],
                ["12 · SHAP & Decile", "SHAP for feature attribution; decile lift chart for deployment planning"],
                ["13 · Causal / A/B", "From prediction to intervention: how do you validate the model drives action?"],
                ["14 · Production", "Batch scoring vs real-time; model drift monitoring; retraining cadence"],
                ["15 · Python Code", "End-to-end code walkthrough for each stage"],
                ["16 · Follow-ups", "Common follow-up questions and sharp answers"],
            ]
        )
    )

    framing = (
        h2("1 · Business Framing") +
        callout("warning", "Questions I ask first",
            ul([
                "What does 'churn' mean here — no order in 30 days? 60 days? Account closure?",
                "What's the business use case — retention outreach, inventory planning, or something else?",
                "Is the goal to predict churn probability or rank accounts by churn risk?",
                "What actions will be taken on model output? (This shapes threshold choice)",
                "Do you have a sense of the cost of a false positive vs a false negative?",
            ])) +
        callout("neutral", "Talk Track",
            p("<em>\"Before I start building features or picking a model, I want to understand the business problem. "
              "For a B2B foodservice company like WebstaurantStore, 'churn' could mean several things — a restaurant "
              "that closes, a customer who switched to a competitor, or just an account that went dormant for a season. "
              "Each has a different label definition, prediction window, and intervention strategy. Can we nail down "
              "which one we're solving for?\"</em>")) +
        grid2(
            card("If churn = no order in 60 days",
                p("This is a behavioral churn model. Label = 1 if no order in the next 60 days. "
                  "Feature window = last 12 months. Train on historical cohorts with enough post-period data.")),
            card("If churn = account closure / cancellation",
                p("Harder to predict — need a signal that precedes the closure event. "
                  "Declining order frequency, shrinking basket size, category concentration are leading indicators.")),
        )
    )

    label_def = (
        h2("3 · Label Definition") +
        callout("warning", "The Most Important Decision",
            p("The label definition is the most consequential design choice. A bad label makes everything else irrelevant.")) +
        table(
            ["Label Option", "Definition", "Pros", "Cons", "Use When"],
            [
                ["No order in 60 days", "Binary: 1 if customer has zero orders in the 60 days following the observation date", "Clear, measurable, actionable", "Seasonal restaurants may look churned but are just in off-season", "Consistent-order businesses"],
                ["No order in 90 days", "Binary: 1 if no orders in 90-day window", "More robust to short gaps", "Slower signal — you're predicting something that takes longer to confirm", "Businesses with monthly+ order cadence"],
                ["Decline in order frequency", "Continuous: % decline in order frequency vs same period last year", "Captures at-risk before churn", "Harder to threshold; more complex model", "Early warning system"],
                ["Off-cadence order", "Binary: 1 if order arrives more than 1.5x the user's typical inter-order interval", "Personalizes the label to each customer's baseline", "Requires per-customer baseline calculation", "B2B with regular reorder patterns"],
            ]
        ) +
        callout("success", "Recommended for WebstaurantStore",
            p("Off-cadence label design: each customer has a typical reorder interval (e.g., a restaurant that orders every 14 days). "
              "Label = 1 if their next order arrives more than 1.5x their baseline interval. This personalizes churn detection "
              "and accounts for seasonal restaurants whose 60-day gap in January is normal, not churned."))
    )

    features = (
        h2("4 · Feature Ideation") +
        table(
            ["Feature Category", "Examples", "Why It Matters", "Leakage Risk"],
            [
                ["Recency (R)", "Days since last order, days since last login", "Most predictive single feature for churn timing", "Use observation date as cutoff — no post-period data"],
                ["Frequency (F)", "Orders per 30/60/90 days, order count trend (slope)", "Declining frequency = leading indicator of churn", "Trend calculation must end at observation date"],
                ["Monetary (M)", "Average order value, total LTM revenue, revenue trend", "High-value customers may tolerate gaps; low-value churn fast", "Use only pre-period revenue"],
                ["Product Breadth", "# unique categories ordered, # unique SKUs, category concentration (Herfindahl)", "Customers with broad product adoption are harder to replace on a competitor", "Calculate over pre-period window only"],
                ["Order Cadence", "Typical inter-order interval, variance in order timing, # weekend orders", "Irregular cadence = early churn signal; very regular = loyal", "No post-period order timing"],
                ["Account Metadata", "Account age (tenure), business type (restaurant vs catering vs bakery), membership status", "Tenure is a strong confounder for churn; newer accounts churn faster", "Static at observation date"],
                ["Support / Complaints", "# support tickets in last 60 days, complaint resolution time, return rate", "High complaint volume predicts churn regardless of order frequency", "Use pre-period support data"],
                ["Category Mix Change", "Shift in % of revenue from core category vs adjacent categories", "Category drift = customer exploring alternatives", "YoY category mix comparison, pre-period"],
            ]
        ) +
        callout("warning", "Temporal Leakage — The Most Common Mistake",
            p("Features like 'days since last order' must be calculated relative to the observation date, "
              "not the current date. If your observation date is 2024-01-01, your features must use only "
              "data from before 2024-01-01. Including any data from after that date is temporal leakage."))
    )

    split_section = (
        h2("7 · Train/Test Split & Temporal Leakage") +
        callout("danger", "NEVER use random split for time-series data",
            p("Random split leaks future information into training. A customer who churned in June could have their "
              "'days since last order' feature calculated using July data, which your model would never have in production.")) +
        table(
            ["Split Method", "Description", "When to Use"],
            [
                ["Temporal cutoff", "Train on cohorts before date X; test on cohorts after date X", "Standard for churn models with a defined prediction horizon"],
                ["Walk-forward validation", "Multiple train/test windows rolling forward in time", "Better estimate of production performance; catches model drift"],
                ["Hold-out by account cohort", "Train on accounts that joined before year Y; test on accounts from year Y+", "Tests generalization to new accounts (more realistic for B2B)"],
            ]
        ) +
        h3("The SHA512-NTILE Trick") +
        callout("info", "Deterministic Stratified Split",
            p("Hash each account ID with SHA-512, then take the last N digits as a percentile bucket. "
              "Assign buckets 0-79 to train, 80-89 to validation, 90-99 to test. "
              "This produces a deterministic, reproducible split that is stable across reruns — "
              "even if new accounts are added, old accounts stay in their original split bucket. "
              "This prevents data leakage from re-randomization and ensures reproducibility."))
    )

    model_choice = (
        h2("8 · Model Choice") +
        table(
            ["Model", "When to Start Here", "Pros", "Cons"],
            [
                ["Logistic Regression", "Always — use as baseline", "Interpretable, fast, provides probability calibration baseline", "Linear decision boundary; struggles with feature interactions"],
                ["Random Forest", "When LR performance is poor and you need feature importance", "Handles non-linearities; built-in feature importance; robust to outliers", "Slower than LR; harder to calibrate probabilities"],
                ["XGBoost / LightGBM", "Default choice for tabular churn data", "Best accuracy on tabular data; handles missing values; fast with GPU", "Requires hyperparameter tuning; harder to explain without SHAP"],
                ["SHAP + XGBoost", "Production model", "Full interpretability at prediction-level; can explain individual accounts", "Slight inference overhead for SHAP computation"],
            ]
        ) +
        callout("success", "Recommended Stack for WebstaurantStore",
            p("Logistic Regression as baseline → XGBoost as primary model → SHAP for interpretability. "
              "If the LR AUC and XGBoost AUC are within 0.02, deploy LR — simpler, more defensible, easier to debug. "
              "Only deploy XGBoost complexity when it delivers measurable lift."))
    )

    imbalance = (
        h2("10 · Class Imbalance") +
        callout("info", "Expected Imbalance",
            p("B2B churn rates are typically 5-20%. A 10% churn rate means 90% of training examples are non-churn. "
              "A model that always predicts 'no churn' gets 90% accuracy but 0% recall on churners.")) +
        table(
            ["Technique", "How It Works", "When to Use", "Tradeoff"],
            [
                ["Class weights (scale_pos_weight)", "Multiply the loss for positive class by a weight proportional to class imbalance", "Always try first — no information loss", "Doesn't generate new data; may still underperform on very imbalanced classes"],
                ["SMOTE (oversampling)", "Synthetically generate minority class examples by interpolating between existing ones", "When class weights don't produce enough recall improvement", "Can generate unrealistic examples; should only be applied to training set, never test"],
                ["Undersampling majority", "Randomly remove majority class examples to balance the ratio", "When training data is very large and compute is constrained", "Discards potentially useful data"],
                ["Threshold adjustment", "Move the classification threshold below 0.5 to catch more churners", "After training — tune on validation set", "Increases false positives; find the threshold that maximizes F1 or minimizes business cost"],
            ]
        ) +
        callout("warning", "Evaluation Metric Warning",
            p("Never use accuracy to evaluate an imbalanced model. Use AUC-ROC (overall ranking ability), "
              "Precision-Recall AUC (captures performance on the minority class), and F1 at your chosen threshold."))
    )

    eval_section = (
        h2("11 · Evaluation") +
        table(
            ["Metric", "What It Measures", "Churn Model Use"],
            [
                ["AUC-ROC", "How well the model ranks churners above non-churners across all thresholds", "Primary model comparison metric; threshold-independent"],
                ["Precision-Recall AUC", "Performance specifically on the minority (churn) class", "Better than AUC-ROC when churn is very rare (<5%)"],
                ["F1 at chosen threshold", "Harmonic mean of precision and recall at a specific operating point", "Use after choosing the deployment threshold based on business cost"],
                ["Calibration curve (reliability diagram)", "Do predicted probabilities match observed frequencies?", "Critical if model output is used to rank intervention priority (not just classify)"],
                ["Lift / Decile chart", "How much better than random is the model at each decile of predicted probability?", "Shows the business value of the model's ranking — most actionable for sales outreach"],
            ]
        ) +
        h3("Lift Chart Interpretation") +
        callout("neutral", "Reading a Decile Lift Chart",
            p("Sort accounts by predicted churn probability (highest first). Split into 10 equal buckets (deciles). "
              "Compute the actual churn rate in each decile. If the top decile has 4x the baseline churn rate, "
              "your model has a lift of 4x — you can focus retention outreach on 10% of accounts and capture 40% of churners."))
    )

    shap_section = (
        h2("12 · SHAP & Feature Attribution") +
        callout("info", "Why SHAP over Feature Importances",
            p("Feature importances tell you which features are globally important to the model. "
              "SHAP values tell you exactly how each feature contributed to a specific prediction. "
              "For a churn model, you can tell a sales rep: 'This account is at high risk primarily because "
              "their order frequency dropped 40% over the last 60 days and they haven't ordered from their "
              "core category in 3 weeks.'")) +
        table(
            ["SHAP Output", "What It Shows", "Business Application"],
            [
                ["Summary plot (beeswarm)", "Global feature importance + direction of effect for all predictions", "Identify which features most drive churn predictions across all accounts"],
                ["Waterfall plot (single prediction)", "How each feature pushes a specific account above or below the base rate", "Sales rep explanation: 'why is this account flagged?'"],
                ["Dependence plot", "How SHAP value for one feature changes with feature value, and interaction effects", "Identify thresholds (e.g., 'recency > 45 days = sharp SHAP increase')"],
                ["Force plot", "Visualization of all features pushing prediction up or down for one account", "Client-facing explanation of model recommendation"],
            ]
        )
    )

    prod_section = (
        h2("14 · Production") +
        table(
            ["Decision", "Option A", "Option B", "Recommendation"],
            [
                ["Scoring cadence", "Weekly batch scoring (BigQuery/BQ ML)", "Real-time scoring (API endpoint)", "Weekly batch is sufficient for churn — accounts don't churn within hours"],
                ["Feature pipeline", "Pre-computed features in BQ tables", "Real-time feature computation", "Pre-compute in BQ; simpler, cheaper, auditable"],
                ["Model registry", "MLflow / Vertex AI Model Registry", "Custom database", "MLflow for experiment tracking; Vertex AI for production serving"],
                ["Drift monitoring", "Monitor input feature distributions weekly", "Monitor prediction distribution only", "Monitor both: feature drift and prediction drift"],
                ["Retraining trigger", "Time-based (monthly retrain)", "Performance-based (when AUC drops)", "Both: monthly retrain + alert if AUC drops >0.03 vs. baseline"],
            ]
        ) +
        callout("success", "Production Readiness Checklist",
            ul([
                "Temporal train/test split validates production scenario",
                "SHAP explanations built into the output table for each scored account",
                "Model card documenting: intended use, training data, known limitations, fairness considerations",
                "Drift monitoring alert on feature distributions and prediction distribution",
                "Retraining pipeline tested end-to-end before deployment",
            ]))
    )

    body = tabs("main",
        [("spine","The Spine"),("framing","Framing"),("label","Label Def"),("features","Features"),("split","Split"),("model","Model"),("imbalance","Imbalance"),("eval","Evaluation"),("shap","SHAP"),("prod","Production")],
        [("spine",spine),("framing",framing),("label",label_def),("features",features),("split",split_section),("model",model_choice),("imbalance",imbalance),("eval",eval_section),("shap",shap_section),("prod",prod_section)]
    )
    return html_page(
        "Churn / Retention Model — End to End",
        "WebstaurantStore · Sr Data Scientist · ML Case Walkthrough — section-by-section interview script",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 5. INTERVIEW PREP GUIDE
# ─────────────────────────────────────────────────────────────────────────────

def make_interview_prep():
    roadmap = (
        h2("Priority Roadmap") +
        callout("info", "Summary",
            p("SQL is already advanced — de-prioritize it. Lead with behavioral stories (unlocks all rounds) "
              "then product sense frameworks (tested at all 7 companies). ML fundamentals are the biggest gap "
              "for Senior DS roles at Google, Microsoft, Klaviyo, and ServiceNow.")) +
        stats(
            ("7", "Target Companies"),
            ("Senior DS / PA", "Target Roles"),
            ("3-4 weeks", "Prep Horizon"),
            ("Lowest", "SQL Priority"),
        ) +
        card("1. Behavioral / HR Stories", pill("2-3 days","success") +
            p("Every company starts here. Your project portfolio is exceptional — you just need 8–10 crisp STAR stories pre-built so you're not inventing them live.") +
            ul([
                "Write stories for: SMS Cross-Sell ($2.3M), PSM Study (76% lift), Propensity Model ($500K), AskData Bot, JustAnswer retention (+11%)",
                "Prepare for: biggest failure/lesson, disagreement with stakeholder, ambiguous project, end-to-end ownership, influencing without authority",
                "Prep 'Why this company' answers for each target — research their recent product launches first",
            ])) +
        card("2. Product Sense + Metrics Frameworks", pill("3-4 days","success") +
            p("All 7 companies test product sense. Your instincts are strong from SMS work, but you need a repeatable framework you can run in real time — not just project recall.") +
            ul([
                "Master the metric drop framework: segment → external vs internal → leading indicators → funnel step → A/B test hypothesis",
                "Practice 'define success metrics for X' for messaging platforms, CRM tools, marketing automation, subscription SaaS",
                "Drill: North Star vs supporting vs guardrail metrics — why each one exists",
                "Practice out loud: 'SMS engagement dropped 15% — what do you do?' using your actual SMS funnel knowledge",
            ])) +
        card("3. Experimentation / Stats", pill("2 days","success") +
            p("Bayesian A/B, PSM, AIPW, DiD — you've done all of it. The gap is explaining these cleanly to a non-technical interviewer.") +
            ul([
                "Prep a 90-second explanation of Bayesian vs frequentist A/B testing (why you prefer Bayesian for early stopping)",
                "Know: p-value vs posterior probability, Type I/II errors, power, MDE — explain each in plain English",
                "Practice the 'metric is up — was it causal?' question using your PSM study as the answer",
                "Be ready for: 'How would you design an A/B test for feature X?' — use your SMS cross-sell experiment as a template",
            ])) +
        card("4. ML / DS Fundamentals", pill("3-4 days","warning") +
            p("Google, Microsoft, ServiceNow, and Klaviyo will probe ML depth. Your XGBoost/LightGBM work is strong, but expect questions on model internals, regularization, and class imbalance.") +
            ul([
                "Review: bias-variance tradeoff, regularization (L1 vs L2), tree-based model internals (XGBoost vs LightGBM vs RF)",
                "Class imbalance: SMOTE, class weights, downsampling — you used downsampling in the propensity model, know the tradeoffs",
                "Know your model choices: 'Why XGBoost vs logistic regression for propensity?' — have a crisp answer",
                "SHAP: you used it in the churn model — explain SHAP values vs feature importances and why SHAP is better",
                "Review: cross-validation, train/test leakage, and why your SHA512-NTILE split was the right call",
            ])) +
        card("5. SQL Live Assessment", pill("1 day","success") +
            p("You're already advanced. The only gap is interview-speed SQL — writing window functions under pressure without IDE autocomplete.") +
            ul([
                "Practice 5–10 medium problems on StrataScratch (product-analytics style, not algorithmic)",
                "Refresh: LAG/LEAD, DENSE_RANK, self-joins for retention cohorts, funnel step analysis",
                "Practice writing a DAU/WAU/MAU query and a 30-day retention cohort query from memory",
            ]))
    )

    companies = (
        h2("By Company") +
        table(
            ["Company", "Role", "Comp Range", "Top Focus", "Your Edge", "Watch Out"],
            [
                ["Google", "Senior DS (L5/L6)", "$295K–$351K total",
                 "Causal inference depth (AIPW, PSM), Bayesian A/B testing, ML system design",
                 "Bayesian experimentation + PSM + AIPW work is directly what Google probes at L5/L6. AskData Bot (Gemini 2.5 Pro on Vertex AI) shows ML engineering depth.",
                 "Google L5/L6 is rigorous on ML theory. Refresh model internals before the ML round."],
                ["Microsoft", "Senior DS", "$180K–$250K base",
                 "Defining ambiguous problems, connecting analysis to product impact, cross-functional influence",
                 "Microsoft values DS who drive product decisions — your $2.3M SMS experiment and semantic layer work are perfect proof points.",
                 "Microsoft weights behavioral performance heavily. Have 5+ STAR stories ready."],
                ["Salesforce", "Senior DS / Senior PA", "$170K–$240K base",
                 "V2MOM framework alignment, Ohana culture fit, marketing automation product sense (CRM)",
                 "Your marketing automation work at Mailchimp (SMS, email) maps perfectly to Salesforce Marketing Cloud context.",
                 "Salesforce explicitly probes V2MOM — research their current company V2MOM before the interview."],
                ["Adobe", "Senior DS / Senior PA", "$165K–$230K base",
                 "Product sense case studies, A/B test design and interpretation, metric definition for creative/marketing products",
                 "Adobe's focus on creative + marketing SaaS aligns with your Mailchimp experience. Your 5-experiment portfolio is a strong differentiator.",
                 "Adobe asks practical case studies — 'creative engagement dropped, diagnose it.' Practice cold."],
                ["HubSpot", "Senior DS", "$170K–$220K base",
                 "HEART values (Humble, Empathetic, Adaptable, Remarkable, Transparent), marketing automation domain knowledge",
                 "Your AskData Bot + semantic layer shows the exact ML-for-product-productivity mindset HubSpot's Breeze AI team wants.",
                 "HubSpot's culture round is unique — it's a values conversation, not just behavioral. Research their Culture Code doc."],
                ["Klaviyo", "Senior DS", "$200K–$280K total",
                 "Ecommerce marketing automation domain, real-time customer segmentation, Python coding proficiency",
                 "SMS + email experimentation + propensity modeling at Mailchimp = direct Klaviyo domain match.",
                 "Klaviyo does pair programming in Python — practice live coding without IDE hints."],
                ["ServiceNow", "Senior DS", "$175K–$250K total",
                 "ML model knowledge (theory + practice), Python coding, enterprise product context",
                 "ServiceNow DS roles expect you to wear a PM hat — your experiment design + stakeholder translation work is directly relevant.",
                 "ServiceNow is enterprise-focused. Frame your work in terms of enterprise workflows and cross-team influence."],
            ]
        )
    )

    stories = (
        h2("Story Bank — 6 Pre-Built STAR Stories") +
        collapsible("SMS Cross-Sell Experiment", 
            p("<strong>Headline:</strong> $2.3M revenue impact — 96% Bayesian confidence") +
            p("<strong>Use for:</strong> Tell me about your biggest project, business impact, A/B testing experience, working with stakeholders") +
            p("<strong>Key Numbers:</strong> $2.3M attributable revenue, 96% Bayesian posterior probability, 3 treatment arms, 60K users") +
            p("<strong>Depth Signal:</strong> The Bayesian framing was a deliberate choice — Bayesian allows early stopping without inflating Type I error, which frequentist testing can't do cleanly in email experiments with variable open rates."),
            "$2.3M revenue · 96% Bayesian confidence") +
        collapsible("PSM Study — Integrations Causal Inference",
            p("<strong>Headline:</strong> 76% retention lift with Canva integration — causal proof") +
            p("<strong>Use for:</strong> Causal inference questions, observational study design, influence without a controlled experiment") +
            p("<strong>Key Numbers:</strong> 76% retention lift, AIPW doubly-robust estimator, Canva integration, 6-month post-period") +
            p("<strong>Depth Signal:</strong> AIPW over PSM because AIPW is consistent if either the PS model or outcome model is correctly specified — doubly robust. PSM alone gave wrong-sign estimates when the PS model was misspecified early on."),
            "76% retention lift · AIPW doubly-robust") +
        collapsible("SMS Propensity Model",
            p("<strong>Headline:</strong> $500K in targeted upsell revenue — propensity-to-purchase model") +
            p("<strong>Use for:</strong> ML modeling questions, feature engineering, production model deployment, business impact") +
            p("<strong>Key Numbers:</strong> $500K, XGBoost + SHAP, 180+ features, 76% precision at top decile") +
            p("<strong>Depth Signal:</strong> The class imbalance challenge: 3% positive rate. Used downsampling + class weights + threshold tuning. SHAP let us explain predictions to the SMS product team so they could sanity-check the top-scored accounts."),
            "$500K revenue · XGBoost + SHAP") +
        collapsible("AskData Bot (Semantic Layer)",
            p("<strong>Headline:</strong> End-to-end AI analytics assistant — Gemini 2.5 Pro on Vertex AI") +
            p("<strong>Use for:</strong> AI/ML engineering questions, autonomous agent design, cross-functional influence, innovation") +
            p("<strong>Key Numbers:</strong> Gemini 2.5 Pro, Vertex AI, 50+ metrics in semantic layer, 10+ teams using it") +
            p("<strong>Depth Signal:</strong> The hard part wasn't the LLM — it was grounding it in a trusted semantic layer so it couldn't hallucinate metric definitions. Built a YAML-based knowledge layer that the model cites."),
            "Gemini 2.5 Pro · Vertex AI · Semantic Layer") +
        collapsible("JustAnswer Retention Analysis",
            p("<strong>Headline:</strong> +11% retention from subscription model redesign") +
            p("<strong>Use for:</strong> Product analytics questions, defining metrics for subscription SaaS, early career story") +
            p("<strong>Key Numbers:</strong> +11% retention, subscription model, cohort analysis, 3-month intervention timeline") +
            p("<strong>Depth Signal:</strong> Identified that the drop-off was happening at day 14, not day 30 as assumed. This changed the intervention strategy from email re-engagement at day 25 to product friction removal at day 12."),
            "+11% retention · Subscription redesign") +
        collapsible("SMS Churn Propensity Model",
            p("<strong>Headline:</strong> Predicting which SMS subscribers will churn before they disengage") +
            p("<strong>Use for:</strong> End-to-end ML pipeline, label definition challenges, temporal validation, production deployment") +
            p("<strong>Key Numbers:</strong> 5-stage Dataform pipeline, LightGBM, temporal train/test split, 90-day prediction horizon") +
            p("<strong>Depth Signal:</strong> The label definition was the hardest part: SMS 'churn' isn't account closure — it's disengagement. Defined churn as no campaign send for 90 days after a period of active sending. Temporal split was critical to avoid leakage."),
            "LightGBM · Temporal split · 90-day prediction")
    )

    behavioral = (
        h2("Behavioral / HR Q&A") +
        callout("info", "Preparation Rule",
            p("Write out your answers to all of these before your first screen. Do not improvise. Each spoken answer should be 2–3 minutes max.")) +
        card('"Tell me about yourself"',
            p("Frame: Mailchimp DS journey (SMS + ML focus) → AskData Bot (AI innovation) → now targeting Senior DS/PA at companies doing AI + analytics at scale. One sentence on why this company specifically. End with: 'I'm excited to bring this to [Company] because...'")) +
        card('"Tell me about your biggest failure"',
            p("Tell the propensity model story but frame the failure as an earlier version that ignored class imbalance and had terrible precision. Learned: always look at the full precision-recall curve, not just AUC. Applied the lesson to the final model.")) +
        card('"Tell me about a time you disagreed with a stakeholder"',
            p("SMS experiment framing: PM wanted to declare success at 2 weeks based on email opens. You pushed back — needed 4 weeks to see purchase conversion. Built the Bayesian monitoring framework to show daily posterior probability, which let you stop early WITH statistical confidence when the signal was clear.")) +
        card('"Describe a time you worked on an ambiguous problem"',
            p("AskData Bot: no clear spec, no existing system, no precedent at the company. Approach: (1) defined the metric taxonomy first (what is a 'metric'?), (2) built a prototype with 5 metrics, (3) used it in a real stakeholder meeting, (4) iterated based on what broke.")) +
        h3("Company-Specific 'Why Us' Research Angles") +
        table(
            ["Company", "Research Angle"],
            [
                ["Salesforce", "Agentforce — how does your AskData Bot experience connect to Agentforce's autonomous agent vision?"],
                ["Microsoft", "Copilot in Fabric/Power BI — your semantic layer work is directly relevant to how Copilot grounds SQL queries on enterprise data"],
                ["Google", "Gemini in BigQuery / Vertex AI — you already use Gemini 2.5 Pro on Vertex AI; reference this as direct technology alignment"],
                ["Adobe", "Adobe Experience Platform + AI Assistant — their push to make customer data actionable via AI mirrors your AskData Bot work"],
                ["HubSpot", "Breeze AI (HubSpot's AI suite for CRM automation) — your AI productivity tooling (semantic layer, Slack bot) is a natural fit"],
                ["Klaviyo", "IPO'd 2023, dominant in ecommerce SMS + email — your cross-channel SMS/email experimentation portfolio is a direct domain match"],
                ["ServiceNow", "Now Assist AI agents for enterprise workflows — position your autonomous DS agent workflow as the exact pattern they're scaling"],
            ]
        )
    )

    body = tabs("main",
        [("roadmap","Priority Roadmap"),("companies","By Company"),("stories","Story Bank"),("behavioral","Behavioral / HR")],
        [("roadmap",roadmap),("companies",companies),("stories",stories),("behavioral",behavioral)]
    )
    return html_page(
        "Interview Prep Guide",
        "Senior DS / PA interview preparation — 7 companies, priority roadmap, story bank, and behavioral Q&A",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 6. ITEM-TO-ITEM RECOMMENDATION WALKTHROUGH
# ─────────────────────────────────────────────────────────────────────────────

def make_item_to_item():
    spine = (
        h2("The Spine — 17-Section Interview Script") +
        callout("info", "Context",
            p("'Recommend Similar Products' for a 700K-SKU B2B catalog. Section-by-section script for the live case: "
              "the words to say, questions to ask first, reasoning behind each choice, and follow-ups to expect. "
              "Every section ties new ideas back to gradient boosting, SHAP, imbalance, and temporal validation.")) +
        table(
            ["Section", "Key Message"],
            [
                ["0 · The Spine", "Frame the problem as a retrieval + ranking pipeline, not a single model"],
                ["1 · Business Framing", "Ask: what surface? what metric? new or returning buyers?"],
                ["2 · Business Context", "B2B foodservice: 700K SKUs, bulk ordering, cold start is not an edge case"],
                ["3 · Problem Formulation", "Turn 'improve recommendations' into a concrete ML task"],
                ["4 · Data & Signals", "Purchase history, browse events, product catalog, session context"],
                ["5 · Approaches", "Collaborative filtering → content-based → hybrid Two-Tower"],
                ["6 · Co-occurrence", "Item-to-item CF: the bread-and-butter model for PDPs"],
                ["7 · Embeddings", "Product embeddings for cold start and semantic similarity"],
                ["8 · Ranking Features", "User, item, and interaction features for the scoring model"],
                ["9 · Two-Stage Model", "Candidate generation + scoring ranker + re-ranking"],
                ["10 · Cold Start", "New buyer / new product: content-based fallback with category embeddings"],
                ["11 · Evaluation", "Offline: Precision@K, NDCG; Online: CTR, add-to-cart, revenue per session"],
                ["12 · Explainability", "Why did we recommend this? SHAP on the ranker, association rule fallback"],
                ["13 · A/B Testing", "Interleaving, switchback, holdout — which to use and when"],
                ["14 · Production", "Batch vs real-time; FAISS for ANN; latency constraints"],
                ["15 · Python Code", "Co-occurrence matrix, item embeddings, ranking model"],
                ["16 · Follow-ups", "Common follow-up questions and sharp answers"],
            ]
        )
    )

    approaches = (
        h2("5 · Approaches Comparison") +
        table(
            ["Model", "How It Works", "Pros", "Cons", "Use at WebstaurantStore When..."],
            [
                ["Collaborative Filtering", "Finds buyers with similar purchase patterns. Fills a user × item matrix.",
                 "Captures diverse preferences · no content data needed · can recommend outside usual category",
                 "Fails for new users/items with no history (cold start) · needs sufficient behavioral data",
                 "Returning buyers with purchase history. 'Customers like you also bought...' on product pages."],
                ["Content-Based Filtering", "Recommends items similar in metadata to things you've bought, using embeddings.",
                 "Works immediately for new items · explainable ('because you bought X') · no behavior required",
                 "Limited to similar items — no discovery · doesn't capture complementary items well",
                 "New product launches · cold-start buyers · 'bought a commercial fryer → show fry baskets + fryer oil'"],
                ["Hybrid (Two-Tower)", "Neural net with user tower + item tower. Combines behavioral signals + content features.",
                 "Best accuracy · handles cold start via content features · supports diverse rec types",
                 "More complex to build and maintain · slower training · harder to debug",
                 "Personalized homepage once you have enough data. Justified when simpler models plateau."],
            ]
        ) +
        callout("success", "What I'd Propose First",
            p("Start with item-to-item collaborative filtering on the product detail page — "
              "'customers who bought this also bought.' Fast to ship, easy to explain, no cold-start issue (item-level), "
              "and proven in e-commerce. Layer in content-based signals for new products and cold-start users as step two. "
              "The full hybrid comes later once data and team maturity justify it."))
    )

    cold_start = (
        h2("10 · Cold Start") +
        callout("warning", "The WebstaurantStore Priority",
            p("New restaurants open constantly. A brand-new buyer has zero purchase history. You must always have an "
              "answer for cold start. Content-based filtering on product category + inferred business type "
              "(catering vs. pizzeria vs. bakery) is the practical answer.")) +
        table(
            ["Cold Start Type", "Problem", "Solution", "Implementation"],
            [
                ["New buyer (no purchase history)", "No user vector in the collaborative filtering matrix",
                 "Content-based: infer business type from registration data (business name, zip code, category of first browse)",
                 "Look up nearest neighbors by business type in item embedding space"],
                ["New item (no purchase history for SKU)", "No co-occurrence signal for the new SKU",
                 "Content-based: find similar items by product description embedding (sentence-BERT or TF-IDF)",
                 "Index new items into FAISS on launch day using description embeddings"],
                ["Low-frequency buyer (<3 purchases)", "Sparse user vector — CF predictions are noisy",
                 "Hybrid: blend CF score (low weight) with content-based score (high weight) proportional to purchase count",
                 "Weight blending: CF_weight = min(purchase_count / 10, 0.7)"],
            ]
        )
    )

    evaluation = (
        h2("11 · Evaluation") +
        h3("Offline Metrics") +
        table(
            ["Metric", "Formula", "What It Measures"],
            [
                ["Precision@K", "# relevant items in top K / K", "Of the K items shown, how many did the user actually engage with?"],
                ["Recall@K", "# relevant items in top K / total relevant items", "Of all items the user would have liked, how many did we surface?"],
                ["NDCG@K", "Normalized Discounted Cumulative Gain", "Ranking quality — higher-ranked relevant items get more credit"],
                ["Coverage", "# unique items recommended / # items in catalog", "Are we surfacing the long tail, or only popular items?"],
                ["Diversity", "Average pairwise distance in embedding space", "Are recommendations diverse, or just variations of the same item?"],
            ]
        ) +
        h3("Online Metrics") +
        table(
            ["Metric", "What It Measures", "Why It Matters"],
            [
                ["Click-Through Rate (CTR)", "# rec clicks / # rec impressions", "User found the rec relevant enough to investigate"],
                ["Add-to-Cart Rate", "# rec items added to cart / # rec clicks", "The rec drove purchase intent, not just curiosity"],
                ["Revenue per Session Lift", "Revenue/session in treatment vs control", "Ultimate business outcome — did recs drive more spending?"],
                ["Average Cart Size", "Items per order in rec users vs non-rec users", "Are recs driving basket expansion (the key B2B metric)?"],
            ]
        ) +
        callout("warning", "Offline vs Online Gap",
            p("Offline metrics measure historical relevance (did users engage with similar items in the past?). "
              "Online metrics measure actual business impact. A model can have great NDCG but poor revenue lift "
              "if it over-recommends items that are frequently browsed but rarely purchased. Always A/B test online."))
    )

    architecture = (
        h2("9 · Two-Stage Production Architecture") +
        callout("info", "Why Two Stages",
            p("You cannot score all 700K items for every user at query time. Two stages: (1) candidate generation — "
              "fast retrieval of ~1000 candidates from 700K using approximate nearest neighbors or lookup tables. "
              "(2) scoring — precise re-ranking of 1000 candidates using a full-feature model.")) +
        h3("Stage 1 — Candidate Generation") +
        table(
            ["Method", "How It Works", "Latency", "Use Case"],
            [
                ["Item-to-item co-occurrence lookup", "Pre-computed: for each item, top-200 co-purchased items", "<5ms", "PDP recommendations for returning buyers"],
                ["ANN search on item embeddings", "FAISS index: cosine similarity on 128-dim embeddings", "~20ms", "New items, cold-start, semantic similarity"],
                ["Popularity filter", "Top-N items by purchase frequency in the buyer's category", "<1ms", "Cold-start fallback when no history available"],
                ["User embedding lookup", "ANN search in item space against pre-computed user vector", "~20ms", "Personalized homepage for returning users"],
            ]
        ) +
        h3("Stage 2 — Scoring") +
        table(
            ["Model", "Features", "Latency", "When to Use"],
            [
                ["LightGBM ranker", "User-item interaction features, recency, category match, price delta", "~10ms on 1000 candidates", "Default production ranker — fast and interpretable"],
                ["Two-Tower neural net", "User tower: history embeddings; Item tower: content + behavioral embeddings", "~30ms with pre-indexed embeddings", "When LightGBM plateaus; handles cold start better"],
                ["Logistic regression baseline", "Hand-crafted co-occurrence + popularity features", "<5ms", "First baseline; A/B test against more complex models"],
            ]
        ) +
        h3("Stage 3 — Re-ranking") +
        table(
            ["Rule", "What It Does", "Why Not in the Model"],
            [
                ["Diversity filter (MMR)", "Iteratively select next item that maximizes relevance minus similarity to already-selected items", "Hard to encode diversity as a loss function; apply post-hoc as greedy algorithm"],
                ["In-stock filter", "Remove any item currently out of stock or discontinued", "Inventory changes in real time — a model trained last week can't know today's stock levels"],
                ["Freshness / promotional boost", "Multiply score by recency multiplier for new products or items on promotion", "Business teams need to control this without retraining a model"],
                ["In-session deduplication", "Remove items already in the buyer's cart", "Model doesn't have real-time cart state; apply as filter at render time"],
            ]
        )
    )

    ab_testing = (
        h2("13 · A/B Testing for Recommendation Systems") +
        callout("warning", "The Challenge",
            p("Standard A/B testing is harder for rec systems because (1) the same user sees both models over time "
              "if we A/B on pages, and (2) SUTVA is violated — a rec in treatment may influence items the user buys "
              "in control sessions.")) +
        table(
            ["Method", "How It Works", "When to Use", "Trade-off"],
            [
                ["User-level holdout", "Randomly assign each user to treatment or control model for the full experiment", "Default recommendation experiment design", "Clean but slow — need 4+ weeks for most metrics to stabilize"],
                ["Interleaving", "For each query, blend ranked results from model A and model B in one list. User clicks reveal preference.", "Comparing two ranking models head-to-head", "Very fast signal (2-3x faster than holdout) but can't measure revenue impact directly"],
                ["Switchback (time-based)", "Alternate between control and treatment model on a scheduled cycle (e.g., alternate days)", "When user-level assignment is impossible (shared catalog pages)", "Seasonal and day-of-week effects can confound; needs careful design"],
            ]
        )
    )

    body = tabs("main",
        [("spine","The Spine"),("approaches","Approaches"),("coldstart","Cold Start"),("eval","Evaluation"),("arch","Architecture"),("ab","A/B Testing")],
        [("spine",spine),("approaches",approaches),("coldstart",cold_start),("eval",evaluation),("arch",architecture),("ab",ab_testing)]
    )
    return html_page(
        "Item-to-Item Recommendation Engine — End to End",
        "WebstaurantStore · Sr Data Scientist · ML Case Walkthrough — 700K-SKU B2B catalog recommendation system",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 7. MATCHING OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

def make_matching_overview():
    methods_tab = (
        h2("Matching Methods Overview") +
        table(
            ["Method", "Family", "Dimensionality", "Info Loss", "Estimand", "Best For", "Maturity"],
            [
                ["Exact Matching", "Direct", "Only feasible with few categorical covariates", "High", "ATT", "Fewer than 4 categorical covariates, large control pool", pill("Starter","neutral")],
                ["CEM (Coarsened Exact Matching)", "Direct", "Moderate — works with 4-8 covariates", "Medium", "ATT", "Mostly categorical/ordinal covariates; skeptical of PS model; want model-free match", pill("Standard","info")],
                ["PSM (Propensity Score Matching)", "Score-Based", "Handles 5-50+ covariates via 1D projection", "Medium", "ATT", "Many continuous covariates (5-50+); default method in product analytics; explainability matters", pill("Standard","info")],
                ["Mahalanobis Distance Matching", "Direct", "Degrades with 10+ covariates", "Low", "ATT", "Continuous covariates with known correlation structure; small number of predictive covariates", pill("Standard","info")],
                ["Genetic Matching", "Direct", "Handles 5-20 covariates; computationally expensive", "Low", "ATT", "When balance quality is critical; have compute budget (R's Matching package)", pill("Advanced","warning")],
                ["Optimal Matching", "Direct", "Works on any distance metric; O(n^3)", "Low", "ATT", "Small-to-medium samples; greedy NN produces poor matches", pill("Advanced","warning")],
                ["IPW / IPTW (Weighting)", "Weighting", "Handles 5-50+ via PS model", "None", "ATE", "Need ATE across entire population; want to retain all units; large samples", pill("Standard","info")],
                ["AIPW (Doubly Robust)", "Doubly Robust", "Handles 5-50+ with ML nuisance models", "None", "ATT or ATE", "Publication-level rigor; rich feature set; high-stakes decisions; used in Mailchimp Integrations Causal study", pill("Advanced","warning")],
            ]
        )
    )

    decision_tab = (
        h2("Which Matching Method to Use?") +
        table(
            ["Scenario", "Recommended Method", "Why"],
            [
                ["Default product analytics work with 5-50 covariates", pill("PSM","success"), "Handles many continuous covariates; explainable; default in practice"],
                ["High-stakes decision, skeptical reviewers, financial consequences", pill("AIPW","warning"), "Doubly robust: consistent if either PS model or outcome model is correct"],
                ["All covariates are categorical, 4-8 covariates", pill("CEM","info"), "Model-free; balance guaranteed by construction"],
                ["Need ATE (not ATT), want to retain all units", pill("IPW","info"), "No units dropped; estimates ATE"],
                ["Maximum balance quality required, have compute", pill("Genetic Matching","warning"), "Optimizes weights for balance by construction"],
                ["Small sample, greedy NN giving poor matches", pill("Optimal Matching","warning"), "Globally optimal pairings"],
            ]
        ) +
        callout("info", "Practical Rule from Mailchimp Integrations Causal Study",
            p("The study used AIPW (doubly robust) as the primary estimator and PSM only as a sanity check. "
              "PSM produced the wrong sign in early runs when the PS model was misspecified — a reminder that "
              "PSM is not robust to PS model error the way AIPW is. For exploratory work, PSM is fine. "
              "For decisions with financial consequences, use AIPW."))
    )

    assumptions_tab = (
        h2("Universal Assumptions") +
        table(
            ["Assumption", "Plain English", "How to Test"],
            [
                ["Unconfoundedness (CIA)", "Given observed covariates, treatment is as-good-as-random", "Cannot be directly tested. Placebo test provides evidence. E-value quantifies robustness."],
                ["Overlap / Common Support", "Every treated unit has a comparable control", "Check PS distribution overlap histogram; drop units outside common support"],
                ["SUTVA — No Interference", "One unit's treatment doesn't affect another's outcome", "Cluster randomization; restrict to non-referred users"],
                ["SUTVA — Single Version of Treatment", "All treated units receive the same treatment", "Stratify by treatment intensity; analyze sub-groups"],
            ]
        ) +
        h3("What You CAN Test") +
        table(
            ["Test", "What It Checks"],
            [
                ["Overlap histogram", "Positivity — do PS distributions overlap?"],
                ["Post-match SMD", "Balance — are covariates similar after matching?"],
                ["Placebo test", "Unconfoundedness — pre-period ATT should be near zero"],
                ["Variance ratio", "Balance in spread, not just means"],
                ["Effective Sample Size", "Weighting — are extreme weights dominating?"],
            ]
        ) +
        callout("danger", "Unconfoundedness is fundamentally untestable",
            p("You cannot directly test whether there are unmeasured confounders. The placebo test gives "
              "evidence about measured balance but cannot detect confounders you did not collect. "
              "Use sensitivity analysis: E-value measures how strong an unmeasured confounder would need "
              "to be to explain away your result. Rosenbaum bounds: bound on how much hidden bias could "
              "shift your p-value. If PSM, CEM, and AIPW all agree, the result is more robust."))
    )

    checks_tab = (
        h2("Quality Checklist After Any Matching") +
        table(
            ["Check", "What to Look For", "Diagnostic Tool", "Priority"],
            [
                ["Post-match SMD for all covariates", "|SMD| < 0.1 for every covariate", "Love plot, SMD table", pill("Must-have","success")],
                ["Overlap histogram", "PS distributions of treated and control substantially overlap", "Density plot of PS", pill("Must-have","success")],
                ["Placebo test (pre-period ATT)", "Pre-period ATT ≈ 0 — if treated and control were similar before, matching is valid", "Same estimation pipeline on pre-period outcome", pill("Must-have","success")],
                ["Variance ratio (per covariate)", "Variance ratio close to 1.0 — balance in spread, not just means", "Python: t.var() / c.var()", pill("Recommended","info")],
                ["Effective Sample Size (IPW/AIPW only)", "ESS not dominated by a few extreme weights", "ESS = sum(w)^2 / sum(w^2)", pill("IPW only","neutral")],
                ["Sensitivity analysis (E-value)", "E-value > 2 — result is robust to moderate unmeasured confounding", "E-value calculation from estimated effect + SE", pill("Advanced","warning")],
            ]
        ) +
        h3("SMD Formula") +
        pre("SMD = (mean_treated - mean_control) / pooled_std\n"
            "pooled_std = sqrt((var_treated + var_control) / 2)\n\n"
            "# Target: |SMD| < 0.1 for all covariates after matching\n"
            "# Values below 0.1 are conventionally considered 'balanced'") +
        callout("neutral", "The Design-Before-Analysis Principle (Rubin 2007)",
            p("Finalize your matching specification before looking at any outcome data. Balance checks should "
              "be done on covariates only — never use outcome information to guide matching choices. "
              "Peeking at outcomes while tuning your match is a form of p-hacking that inflates false positive rates."))
    )

    sutva_tab = (
        h2("SUTVA Deep Dive — When It Matters in Product") +
        table(
            ["SUTVA Condition", "Violated When...", "Product Example", "Fix"],
            [
                ["No Interference", "One user's treatment affects another's outcome",
                 "Referral program: treated user invites control user, who then behaves differently",
                 "Use cluster randomization; restrict analysis to non-referred users"],
                ["Single Version of Treatment", "Treated units receive meaningfully different versions",
                 "Canva integration: some connect once and forget; others sync 50 images/week",
                 "Stratify by treatment intensity (e.g. canva_sync_tier); analyze sub-groups"],
                ["No Anticipation", "Control users change behavior before treatment starts",
                 "Announced feature: control users sign up elsewhere before rollout",
                 "Use sharp rollout with no pre-announcement; define control window carefully"],
            ]
        )
    )

    body = tabs("main",
        [("methods","Methods"),("decision","Decision Guide"),("assumptions","Assumptions"),("checks","Quality Checks"),("sutva","SUTVA")],
        [("methods",methods_tab),("decision",decision_tab),("assumptions",assumptions_tab),("checks",checks_tab),("sutva",sutva_tab)]
    )
    return html_page(
        "Matching Methods — Overview",
        "Comprehensive guide to observational causal inference matching methods: from Exact Matching to AIPW",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 8. ML MODEL GUIDE
# ─────────────────────────────────────────────────────────────────────────────

def make_ml_model_guide():
    overview = (
        h2("The One Question That Decides Everything") +
        p("Before picking any model, ask: do I have the 'answers' (labels) in my data?") +
        table(
            ["", "Supervised", "Unsupervised"],
            [
                ["Data has answers?", "Yes (labeled)", "No (unlabeled)"],
                ["Goal", "Predict a known target", "Discover hidden patterns"],
                ["You ask", "What will happen?", "What groups exist?"],
                ["Examples", "Churn, sales forecast, fraud", "Segments, anomalies, basket analysis"],
                ["Need a 'right answer' to grade it?", "Yes", "Not directly"],
            ]
        ) +
        callout("info", "There's also a third family",
            p("<strong>Reinforcement learning</strong> — model learns by trial and error from rewards (e.g. pricing bots, recommendations that learn from clicks). "
              "<strong>Semi-supervised</strong> — a few labels + lots of unlabeled data. Useful when labeling is expensive."))
    )

    supervised = (
        h2("Supervised Learning Models") +
        h3("Classification Models") +
        collapsible("Logistic Regression",
            p("<strong>What:</strong> Simple model that outputs a probability (0–100%) for yes/no questions.") +
            p("<strong>Use when:</strong> Fast, simple baseline; need to explain to stakeholders; fairly straightforward relationship.") +
            p("<strong>Example:</strong> Probability a customer churns this month.") +
            p("<strong>Watch out:</strong> Struggles with complex, non-linear patterns.")) +
        collapsible("Decision Tree",
            p("<strong>What:</strong> A flowchart of yes/no questions that leads to an answer.") +
            p("<strong>Use when:</strong> Very easy to read and explain; mix of number and category inputs.") +
            p("<strong>Example:</strong> Rules like 'no order in 30 days AND no loyalty points → likely to churn'.") +
            p("<strong>Watch out:</strong> A single tree overfits (memorizes) easily — use a forest instead.")) +
        collapsible("Random Forest",
            p("<strong>What:</strong> Many decision trees voting together for a more stable answer.") +
            p("<strong>Use when:</strong> Want strong accuracy without much tuning; need feature importance; medium tabular data.") +
            p("<strong>Example:</strong> Predict churn AND see top drivers: recency, spend drop, complaints.") +
            p("<strong>Watch out:</strong> Less interpretable than one tree; bigger and slower.")) +
        collapsible("XGBoost / Gradient Boosting",
            p("<strong>What:</strong> Trees built one after another, each fixing the previous one's mistakes.") +
            p("<strong>Use when:</strong> Want top accuracy on tabular data; can spend time tuning; common winner for churn, propensity, fraud.") +
            p("<strong>Example:</strong> Your SMS propensity model — XGBoost with SHAP for feature attribution.") +
            p("<strong>Watch out:</strong> Needs hyperparameter tuning; requires SHAP for interpretability.")) +
        h3("Regression Models") +
        collapsible("Linear Regression",
            p("<strong>What:</strong> Draws the best-fit line through data to predict a number.") +
            p("<strong>Use when:</strong> Predict a continuous number; want a fast, interpretable baseline; relationship is roughly linear.") +
            p("<strong>Watch out:</strong> Assumes linear relationship; sensitive to outliers; needs feature scaling.")) +
        collapsible("Ridge / Lasso Regression",
            p("<strong>What:</strong> Linear regression with a penalty that stops it from overcomplicating.") +
            p("<strong>Ridge (L2):</strong> Shrinks all coefficients toward zero. Keeps all features.") +
            p("<strong>Lasso (L1):</strong> Can set some coefficients exactly to zero — does feature selection automatically.") +
            p("<strong>Use when:</strong> Many features, some may be irrelevant; want regularization to prevent overfitting."))
    )

    unsupervised = (
        h2("Unsupervised Learning Models") +
        collapsible("K-Means Clustering",
            p("<strong>What:</strong> Groups data points into K clusters by minimizing distance to cluster centers.") +
            p("<strong>Use when:</strong> You want to discover customer segments without predefined categories; exploratory analysis.") +
            p("<strong>Example:</strong> Segment restaurant buyers into: casual/seasonal, bulk-buyer, premium-consistent.") +
            p("<strong>Watch out:</strong> You must choose K; sensitive to scale (normalize features first); assumes spherical clusters.")) +
        collapsible("PCA (Principal Component Analysis)",
            p("<strong>What:</strong> Reduces the number of features while keeping most of the information.") +
            p("<strong>Use when:</strong> Have many correlated features; want to visualize high-dimensional data; preprocessing for other models.") +
            p("<strong>Watch out:</strong> Loses interpretability — components are linear combinations of original features.")) +
        collapsible("Anomaly Detection",
            p("<strong>What:</strong> Flags unusual data points that don't fit the learned pattern.") +
            p("<strong>Use when:</strong> Fraud detection, system failure alerts, unusual account behavior.") +
            p("<strong>Methods:</strong> Isolation Forest, One-Class SVM, Z-score thresholds, autoencoder reconstruction error."))
    )

    evaluation = (
        h2("Model Evaluation Metrics") +
        h3("Classification Metrics") +
        table(
            ["Metric", "Formula", "Use When"],
            [
                ["Accuracy", "Correct predictions / Total predictions", "Balanced classes — useless for imbalanced churn/fraud"],
                ["Precision", "TP / (TP + FP)", "When false alarms are costly (spam filter, underwriting)"],
                ["Recall (Sensitivity)", "TP / (TP + FN)", "When misses are costly (cancer screening, fraud detection)"],
                ["F1 Score", "2 × (Precision × Recall) / (Precision + Recall)", "When you need a balance of precision and recall"],
                ["AUC-ROC", "Area under ROC curve", "Comparing models regardless of threshold; best for ranking"],
                ["PR-AUC", "Area under Precision-Recall curve", "When positive class is rare (<5%) — better than AUC-ROC"],
            ]
        ) +
        h3("Key Concepts") +
        collapsible("Bias-Variance Tradeoff",
            p("<strong>Bias:</strong> Error from wrong assumptions. High bias = underfitting (model too simple to capture patterns).") +
            p("<strong>Variance:</strong> Error from sensitivity to training data. High variance = overfitting (model memorizes training data).") +
            p("<strong>Tradeoff:</strong> Increasing complexity reduces bias but increases variance. The sweet spot is where total error is minimized.") +
            p("<strong>Fix high bias:</strong> More complex model, add useful features, less regularization.") +
            p("<strong>Fix high variance:</strong> More data, simpler model, regularization, cross-validation.")) +
        collapsible("Precision vs Recall — When to Favor Each",
            p("<strong>Favor Precision when:</strong> False alarms are costly. Example: spam filter — don't accidentally block real email.") +
            p("<strong>Favor Recall when:</strong> Missing positives is costly. Example: cancer screening — never miss a case.") +
            p("<strong>F1</strong> is the harmonic mean — use when you need balance between the two.")) +
        collapsible("Cross-Validation",
            p("k-fold: split data into k parts, train on k-1, test on the rest, rotate. Average the scores.") +
            p("More reliable than a single train/test split. Helps detect overfitting and tune hyperparameters.") +
            p("<strong>For time-series data:</strong> Never use random k-fold — use time-based splits (walk-forward validation) to avoid leakage.")) +
        collapsible("Data Leakage",
            p("When information from the future or the answer sneaks into training. Model looks amazing in testing but fails in production.") +
            p("<strong>Causes:</strong> Scaling before the split, using a feature that includes the target, temporal data not split properly.") +
            p("<strong>Fix:</strong> Split first, then fit transforms only on train data. For time-series: use strict temporal cutoff.") +
            p("<strong>Example:</strong> Using 'cancellation date' to predict churn — it already gives away the answer."))
    )

    pick_model = (
        h2("Model Selection Decision Guide") +
        table(
            ["Scenario", "Recommended Model", "Why"],
            [
                ["Quick baseline for any classification problem", "Logistic Regression", "Fast, interpretable, good baseline"],
                ["Tabular data, want maximum accuracy", "XGBoost / LightGBM", "Best-in-class for tabular; handles missing values"],
                ["Need interpretability + accuracy", "XGBoost + SHAP", "Full prediction-level explanations"],
                ["Many correlated features, need feature selection", "Lasso Regression", "L1 penalty zeros out irrelevant features"],
                ["Want to find customer segments", "K-Means Clustering", "Standard segment discovery"],
                ["Very high dimensionality, preprocessing", "PCA then model", "Reduce features while preserving variance"],
                ["Imbalanced classes (fraud, churn)", "XGBoost with scale_pos_weight", "Built-in class weight support"],
                ["High-stakes prediction, need calibrated probabilities", "Calibrated XGBoost / Isotonic Regression", "Probability outputs must match observed frequencies"],
            ]
        )
    )

    concepts = (
        h2("DS Concepts Q&A") +
        collapsible("What is L1 vs L2 regularization?",
            p("A penalty that stops the model from getting too complex. L1 (Lasso): can shrink some weights to zero → drops useless features. L2 (Ridge): shrinks weights smoothly toward zero, keeps all features. <strong>Rule:</strong> Lasso = selection (zeros out). Ridge = shrinks but keeps.")) +
        collapsible("Bagging vs Boosting",
            p("<strong>Bagging:</strong> Train many models in PARALLEL on random data samples, then average/vote. Mainly reduces VARIANCE (overfitting). Example: Random Forest.") +
            p("<strong>Boosting:</strong> Train models in SEQUENCE, each fixing the previous one's mistakes. Mainly reduces BIAS (accuracy). Example: XGBoost, AdaBoost.") +
            p("<strong>Remember:</strong> Bagging = parallel + vote (fix variance). Boosting = sequential + correct (fix bias).")) +
        collapsible("What is the p-value (in plain English)?",
            p("Chance of seeing this result if there were really no effect. Small p-value (<0.05) → result is unlikely to be just luck. It does NOT prove the effect is large or important.")) +
        collapsible("Type I vs Type II error",
            p("<strong>Type I (false positive):</strong> Saying there's an effect when there isn't. <strong>Type II (false negative):</strong> Missing a real effect. <strong>Remember:</strong> Type I = crying wolf. Type II = missing the wolf.")) +
        collapsible("How do you handle imbalanced data?",
            p("<strong>Use the right metric:</strong> Precision, Recall, F1, AUC — not accuracy.") +
            p("<strong>Resample:</strong> Oversample the rare class (SMOTE) or undersample the common one.") +
            p("<strong>Class weights:</strong> Use scale_pos_weight so the model cares more about the rare class.") +
            p("<strong>Threshold:</strong> Adjust the decision threshold (not always 0.5).")) +
        collapsible("What is data leakage and how do you prevent it?",
            p("When info from the future or the answer sneaks into training data. Model looks amazing in testing but fails in production. Fix: split first, then fit transforms only on train data.")) +
        collapsible("Parametric vs Non-Parametric Models",
            p("<strong>Parametric:</strong> Fixed number of parameters (linear/logistic regression). Faster, simpler.") +
            p("<strong>Non-parametric:</strong> Grow with data (KNN, decision trees). More flexible, need more data."))
    )

    body = tabs("main",
        [("overview","Start Here"),("supervised","Supervised"),("unsupervised","Unsupervised"),("eval","Evaluation"),("pick","Pick a Model"),("concepts","DS Concepts")],
        [("overview",overview),("supervised",supervised),("unsupervised",unsupervised),("eval",evaluation),("pick",pick_model),("concepts",concepts)]
    )
    return html_page(
        "ML Models: When to Use Which",
        "Plain-English decision guide — from supervised vs unsupervised down to picking a model and grading it",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 9. PSM EXPLAINER
# ─────────────────────────────────────────────────────────────────────────────

def make_psm_explainer():
    overview = (
        h2("What is PSM?") +
        p("Propensity Score Matching (PSM) is a causal inference technique for estimating treatment effects from observational data — when randomized experiments are not possible.") +
        stats(
            ("e(X)", "Propensity Score: P(T=1 | X)"),
            ("ATT", "Primary estimand (treated units)"),
            ("< 0.1", "Target SMD for balanced covariates"),
            ("0.2 × SD", "Rosenbaum caliper rule (logit PS)"),
        ) +
        grid2(
            callout("info", "What PSM Estimates",
                p("PSM typically estimates the ATT (Average Treatment Effect on the Treated): among users who were treated, "
                  "what was the causal effect? This differs from ATE (effect on everyone).")),
            callout("warning", "PSM is Not Magic",
                p("PSM removes bias from observed confounders only. If a key confounder is unmeasured, PSM cannot "
                  "adjust for it. Always pair with sensitivity analysis.")),
        )
    )

    steps = (
        h2("Step-by-Step Guide") +
        table(
            ["Step", "Title", "Key Action", "Watch Out"],
            [
                ["01", "Define Treatment & Outcome", "Clearly specify binary treatment T and outcome Y. Must have a logical counterfactual.", "None"],
                ["02", "Select Confounding Covariates", "Identify variables X that predict treatment AND affect outcome. Omit post-treatment variables.", "Never include variables measured after treatment starts — they are colliders that will bias your estimate."],
                ["03", "Estimate Propensity Scores", "Fit P(T=1|X) via logistic regression. Score matters more than predictive accuracy.", "None"],
                ["04", "Check Common Support", "Plot PS distributions for treated and control — they must substantially overlap.", "If treated PS is concentrated near 1.0 and control near 0.0, you have near-separation. PSM will produce unreliable estimates."],
                ["05", "Match Units", "Pair each treated unit to control units with similar propensity score.", "None"],
                ["06", "Assess Covariate Balance", "Check SMD after matching. SMD < 0.1 = good balance.", "None"],
                ["07", "Estimate Treatment Effect", "On matched sample: ATT = mean(Y_treated) - mean(Y_matched_controls)", "None"],
                ["08", "Sensitivity Analysis", "Rosenbaum bounds: how strong must unmeasured confounder be to overturn result?", "A significant PSM result can still be driven by unmeasured confounders. Sensitivity analysis is not optional for causal claims."],
            ]
        )
    )

    methods_tab = (
        h2("Matching Methods Comparison") +
        table(
            ["Method", "Mechanism", "Caliper?", "Pros", "Cons", "Best For"],
            [
                ["1:1 Nearest Neighbor", "Each treated unit matched to closest control by PS distance", "No", "Simple, easy to interpret", "Poor matches if no close control exists", "Large control pool with good PS overlap"],
                ["NN + Caliper", "NN matching; discard matches beyond 0.2 × SD of logit PS", "Yes", "Better match quality, eliminates bad matches", "Reduces sample size; some treated units dropped", "Default choice for most product analytics"],
                ["K:1 Nearest Neighbor", "Each treated unit matched to K controls (e.g. 1:3 or 1:5)", "Optional", "Uses more control data, reduces variance", "Worse average match quality as K increases", "Control pool is much larger than treated group"],
                ["Radius / Within-Caliper", "Match to all controls within a fixed PS distance band", "Yes", "Retains more information, weighted average", "Variable number of matches per treated unit", "Rich control pool; caliper width needs careful tuning"],
                ["Kernel Matching", "Weight all controls by kernel function of PS distance", "Implicit", "Uses entire control sample, lower variance", "Harder to interpret; bandwidth choice matters", "Large datasets; want SATT over a weighted sample"],
                ["Optimal Matching", "Minimizes total PS distance globally (linear assignment)", "Optional", "Globally optimal pairings; best average match quality", "Computationally expensive for large n", "Small-to-medium samples where compute is manageable"],
                ["IPW (Inverse Probability Weighting)", "Reweight: treated gets 1/PS, control gets 1/(1-PS)", "No", "No units dropped; estimates ATE not just ATT", "Extreme weights from near-0 or near-1 PS can destabilize", "Need ATE across entire population; use stabilized weights"],
            ]
        ) +
        callout("success", "Recommended Default",
            p("Nearest Neighbor + Caliper (0.2 × SD of logit PS) — best balance of match quality, sample retention, "
              "and interpretability for most product analytics work. Pair with regression adjustment on the matched "
              "sample for additional bias reduction."))
    )

    code_tab = (
        h2("Python Implementation") +
        h3("1. Propensity Score Estimation") +
        pre("""from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

covariates = ['account_age_days', 'plan_tier_encoded',
              'prior_sessions_30d', 'industry_encoded']

X = df[covariates].values
T = df['treatment'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

lr = LogisticRegression(max_iter=1000, C=1.0)
lr.fit(X_scaled, T)

df['ps'] = lr.predict_proba(X_scaled)[:, 1]
df['logit_ps'] = np.log(df['ps'] / (1 - df['ps']))""") +
        h3("2. Caliper Matching") +
        pre("""from sklearn.neighbors import NearestNeighbors

# Rosenbaum & Rubin rule: caliper = 0.2 * SD(logit PS)
caliper = 0.2 * df['logit_ps'].std()

treated = df[df['T'] == 1].copy()
control = df[df['T'] == 0].copy()

ps_ctrl = control['logit_ps'].values.reshape(-1, 1)
ps_trt  = treated['logit_ps'].values.reshape(-1, 1)

nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
nn.fit(ps_ctrl)
distances, indices = nn.kneighbors(ps_trt)

# Drop treated units with no close match
mask = distances.flatten() <= caliper
treated_m = treated.iloc[mask].copy()
control_m = control.iloc[indices.flatten()[mask]].copy()
matched_df = pd.concat([treated_m, control_m])""") +
        h3("3. Balance Check (SMD)") +
        pre("""def standardized_mean_diff(df, covariates):
    rows = []
    for col in covariates:
        t_vals = df.loc[df['T']==1, col]
        c_vals = df.loc[df['T']==0, col]
        mean_diff  = t_vals.mean() - c_vals.mean()
        pooled_std = np.sqrt((t_vals.var() + c_vals.var()) / 2)
        smd = mean_diff / pooled_std if pooled_std > 0 else float('nan')
        rows.append({'covariate': col, 'SMD': smd,
                     'balanced': abs(smd) < 0.1})
    return pd.DataFrame(rows)

smd_after = standardized_mean_diff(matched_df, covariates)
# Check: all |SMD| < 0.1 post-match""") +
        h3("4. ATT Estimation") +
        pre("""from scipy import stats

y_trt  = matched_df.loc[matched_df['T']==1, 'Y']
y_ctrl = matched_df.loc[matched_df['T']==0, 'Y']

att    = y_trt.mean() - y_ctrl.mean()
t_stat, p_val = stats.ttest_ind(y_trt, y_ctrl)

print(f'ATT:     {att:.4f}')
print(f'p-value: {p_val:.4f}')""")
    )

    assumptions_tab = (
        h2("Core Assumptions") +
        table(
            ["Assumption", "What It Means", "Testability"],
            [
                ["Unconfoundedness (CIA)", "Given observed covariates X, treatment T is independent of potential outcomes", "Cannot be directly tested. Placebo test provides indirect evidence."],
                ["Overlap / Positivity", "Every treated unit has a comparable control: 0 < P(T=1|X) < 1 for all X", "Testable: plot PS distributions and check overlap"],
                ["SUTVA — No Interference", "One unit's treatment doesn't affect another's outcome", "Partially testable: check for network effects or referral contamination"],
                ["SUTVA — Single Version of Treatment", "All treated units received the same treatment", "Check: is treatment heterogeneous in intensity or type?"],
            ]
        ) +
        h3("Common Pitfalls") +
        table(
            ["Pitfall", "Severity", "How to Avoid"],
            [
                ["Including post-treatment variables as covariates", pill("High","danger"), "Only use pre-treatment covariates. Post-treatment variables are colliders that induce bias."],
                ["Not checking balance after matching", pill("High","danger"), "Always compute SMD for all covariates after matching. Balance is not guaranteed — verify it."],
                ["Ignoring common support violations", pill("High","danger"), "Drop treated units outside the control PS distribution. Never extrapolate."],
                ["Using PSM result without sensitivity analysis", pill("Medium","warning"), "Run Rosenbaum bounds or E-value. Report robustness to hidden bias."],
                ["Confusing ATT with ATE", pill("Medium","warning"), "PSM estimates ATT (effect on treated). If you need ATE, use IPW or AIPW."],
                ["Not calibrating the PS model", pill("Low","neutral"), "Check PS model calibration (predicted vs actual treatment rates). Miscalibrated PS model produces biased matches."],
            ]
        )
    )

    body = tabs("main",
        [("overview","Overview"),("steps","Step-by-Step"),("methods","Methods"),("code","Python Code"),("assumptions","Assumptions")],
        [("overview",overview),("steps",steps),("methods",methods_tab),("code",code_tab),("assumptions",assumptions_tab)]
    )
    return html_page(
        "PSM Explainer — Propensity Score Matching",
        "End-to-end guide: from defining treatment to sensitivity analysis. Includes Python code for every step.",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 10. RECSYS INTERVIEW PLAYBOOK
# ─────────────────────────────────────────────────────────────────────────────

def make_recsys_playbook():
    framing = (
        h2("How to Open the ML Case") +
        callout("info", "Opening Move — Say This First",
            p('"Before I jump into models, I want to make sure I understand the problem. Can I ask a few clarifying questions?"')) +
        table(
            ["Question to Ask", "Why It Matters", "WebstaurantStore Angle"],
            [
                ["What surface are we building for? Product page, homepage, cart, email?", "Completely changes latency constraints and the right model architecture.", "PDP = complementary items · Homepage = personalized · Cart = session-aware"],
                ["What does success look like for the business?", "Aligns your approach to outcomes the business actually cares about.", "Cart size? Revenue per session? Repeat purchase rate? All are valid north stars."],
                ["Who are the users — new buyers or returning ones?", "Drives how much you need to invest in cold-start handling.", "New restaurants open constantly. Cold start is not an edge case here."],
                ["What data is available today?", "Determines feasibility of behavioral models like collaborative filtering.", "Purchase history? Browse events? Product catalog metadata? Images?"],
                ["Are there any latency or infrastructure constraints?", "Rules out expensive real-time inference models early.", "Product page recs need to load fast — probably <200ms SLA."],
            ]
        ) +
        h3("The ML Framing Template") +
        grid3(
            card("Step 1 — Define the task",
                p("Turn 'improve recommendations' into a concrete ML task. Example: 'Predict the probability that buyer B purchases item I, given their last 30-day purchase history.'")),
            card("Step 2 — Define the label",
                p("What counts as a positive example? Purchase = positive. Impression with no click = negative. Decide implicit vs explicit feedback early — most e-commerce is implicit.")),
            card("Step 3 — Define the baseline",
                p("Always propose a simple baseline first. 'Most popular items' or 'frequently bought together' is fast to ship, easy to explain, and surprisingly hard to beat.")),
        ) +
        callout("neutral", "Anti-Pattern to Avoid",
            p("Do not immediately jump to 'I'd use a Two-Tower neural network.' It signals you can't reason about trade-offs. Start simple, then justify complexity."))
    )

    models = (
        h2("Model Types — Comparison") +
        table(
            ["Model", "How It Works", "Pros", "Cons", "Use at WebstaurantStore When..."],
            [
                ["Collaborative Filtering", "Finds buyers with similar purchase patterns and borrows their preferences. Fills in a user × item matrix.",
                 "Captures diverse preferences · no content data needed · can recommend outside usual category",
                 "Fails for new users/items (cold start) · needs sufficient behavioral data",
                 "Returning buyers with purchase history. 'Customers like you also bought...' on product pages."],
                ["Content-Based Filtering", "Recommends items similar in metadata to things you've bought, using embeddings.",
                 "Works immediately for new items · explainable ('because you bought X') · no behavior required",
                 "Limited to similar items — no discovery · doesn't capture complementary items well",
                 "New product launches · cold-start buyers · 'bought a commercial fryer → show fry baskets + fryer oil'"],
                ["Hybrid (Two-Tower)", "Neural net with a user tower and an item tower. Combines behavioral signals + content features.",
                 "Best accuracy · handles cold start via content features · supports diverse rec types",
                 "More complex to build and maintain · slower training · harder to debug",
                 "Personalized homepage once you have enough data. Justified when simpler models plateau."],
            ]
        ) +
        callout("warning", "Cold Start — The WebstaurantStore Priority",
            p("New restaurants open constantly. A brand-new buyer has zero purchase history. You must always have an "
              "answer for cold start. Content-based filtering on product category + inferred business type "
              "(catering vs. pizzeria vs. bakery) is the practical answer. Bring this up proactively."))
    )

    design = (
        h2("Design Considerations") +
        table(
            ["Consideration", "Definition", "WebstaurantStore Context", "Priority"],
            [
                ["Relevance", "Are the recs actually useful to this user?", "A pizzeria buyer shouldn't see bakery supplies. Category relevance is table stakes.", "Critical"],
                ["Cold Start", "What do you do for new users or new products with no history?", "New restaurants open constantly · new SKUs launch regularly. Two distinct cold start problems.", "Critical"],
                ["Diversity", "Don't recommend the same item type five different ways.", "Buyer has a commercial fryer in cart → don't show 5 more fryers. Show fry baskets, fryer oil, thermometers.", "High"],
                ["Freshness", "Are recs up-to-date with recent behavior and inventory?", "Seasonal menu changes, promotional inventory, new product lines.", "Medium"],
                ["Latency", "How quickly must recs appear on the page?", "Product pages need fast load — cache pre-computed item-to-item scores where possible.", "High"],
                ["Fairness", "Are some product categories systematically under-recommended?", "Niche product lines shouldn't be invisible just because they have fewer purchases in training data.", "Medium"],
                ["Scalability", "Does the system hold up at 400k+ products?", "Multi-stage funnel: candidate generation → scoring → re-ranking.", "High"],
            ]
        )
    )

    metrics_tab = (
        h2("Metrics Framework") +
        h3("Offline Metrics") +
        table(
            ["Metric", "Formula / Description", "When It Matters"],
            [
                ["Precision@K", "# relevant items in top K / K", "Are the K items shown to the user actually relevant?"],
                ["Recall@K", "# relevant items in top K / total relevant items", "Are we surfacing enough of the items the user would want?"],
                ["NDCG@K", "Normalized Discounted Cumulative Gain", "Ranking quality — higher-ranked relevant items get more credit"],
                ["Coverage", "# unique items recommended / # items in catalog", "Prevents recommendation concentration on popular items only"],
                ["Diversity", "Average pairwise distance in embedding space", "Are recommendations diverse, or just variations of the same item?"],
            ]
        ) +
        h3("Online (Business) Metrics") +
        table(
            ["Metric", "What It Measures"],
            [
                ["Click-Through Rate (CTR)", "Did users click on the recommended item?"],
                ["Add-to-Cart Rate from Recs", "Did the click result in purchase intent?"],
                ["Revenue per Session Lift", "Did recs drive more spending per session? (ultimate business outcome)"],
                ["Average Cart Size", "Are recs driving basket expansion? (the key B2B metric for WebstaurantStore)"],
                ["Repeat Purchase Rate from Rec Clicks", "Do users who click recs come back more?"],
            ]
        ) +
        callout("info", "North Star for WebstaurantStore",
            p("Average cart value per session and cart size uplift from recommendations. B2B buyers come to restock — "
              "getting them to add one more complementary item per order is the highest-ROI rec objective."))
    )

    architecture = (
        h2("Production Architecture — Multi-Stage Pipeline") +
        h3("Stage 1 — Candidate Generation (700K → ~1000)") +
        table(
            ["Method", "How It Works", "Latency", "WebstaurantStore Example"],
            [
                ["Item-to-item co-occurrence lookup", "Pre-computed: for each item, top-200 most co-purchased items stored as key-value", "<5ms", "Buyer viewing Vulcan 36\" range → return 200 most co-purchased items pre-computed offline"],
                ["ANN search on item embeddings", "FAISS index: cosine similarity on 128-dim embeddings for semantic similarity", "~20ms", "New product with no purchase history → find nearest neighbors by product description embedding"],
                ["Popularity filter", "Top-N items by purchase frequency in buyer's category", "<1ms", "New buyer with no history: surface top-50 items in 'Commercial Kitchen' category"],
                ["User embedding lookup", "ANN search against pre-computed user vector (for returning buyers)", "~20ms", "Returning buyer with 12 months of history → ANN search in item space against user embedding"],
            ]
        ) +
        h3("Stage 2 — Scoring (1000 → ~50)") +
        table(
            ["Model", "Features", "Latency", "Use When"],
            [
                ["LightGBM ranker", "User features + item features + interaction features (co-purchase rate, price delta, category match)", "~10ms", "Default production ranker — fast and interpretable with SHAP"],
                ["Two-Tower neural net", "User tower: history embeddings; Item tower: content + behavioral embeddings", "~30ms", "When LightGBM plateaus; handles cold start better with content tower"],
            ]
        ) +
        h3("Stage 3 — Re-ranking (50 → 5-10 shown)") +
        table(
            ["Rule", "What It Does", "Why"],
            [
                ["Diversity filter (MMR)", "Select items that maximize relevance minus similarity to already-selected items", "Prevent showing 5 commercial fryers — pick 1 then switch to fry baskets, oil, thermometer"],
                ["In-stock filter", "Remove any item currently out of stock or discontinued", "Inventory changes in real time; model trained last week can't know today's stock levels"],
                ["Freshness boost", "Multiply score by recency multiplier for new products or items on promotion", "Business teams need to control this without retraining"],
                ["In-session deduplication", "Remove items already in buyer's cart", "Model doesn't have real-time cart state; apply as filter at render time"],
            ]
        ) +
        h3("Iteration Roadmap") +
        table(
            ["Phase", "What to Build", "Why This Order"],
            [
                ["Phase 1 (weeks 1-4)", "Item-to-item CF on PDPs + 'buy it again' from purchase history", "Fast to ship · immediately valuable · establishes data collection pipeline · no cold start issue"],
                ["Phase 2 (weeks 5-12)", "Content-based embeddings for cold-start buyers and new products", "Addresses the gap Phase 1 leaves. New restaurants and new SKU launches are now handled."],
                ["Phase 3 (months 3-6)", "Two-Tower hybrid model for homepage personalization", "More data now available · complexity is justified · higher expected revenue lift"],
                ["Phase 4 (ongoing)", "Session-aware re-ranking, A/B testing framework, data drift monitoring", "Continuous improvement · catch model degradation early · enable fast experimentation"],
            ]
        )
    )

    body = tabs("main",
        [("framing","Framing"),("models","Models"),("design","Design"),("metrics","Metrics"),("architecture","Architecture")],
        [("framing",framing),("models",models),("design",design),("metrics",metrics_tab),("architecture",architecture)]
    )
    return html_page(
        "Recommender Systems — Interview Playbook",
        "WebstaurantStore ML case discussion · B2B foodservice e-commerce · 5-tab playbook",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 11. WEBSTAURANT INTERVIEW PREP
# ─────────────────────────────────────────────────────────────────────────────

def make_webstaurant_prep():
    intel = (
        h2("Interview Intel") +
        callout("info", "Format (from Suraj's email)",
            p("Colab notebook shared live. SQL on made-up tables like their real ones. Python on data types, "
              "manipulation, best practices, numpy/pandas/sklearn. Resume tools (PowerBI, SAS) may be probed. "
              "Answers do not have to run — pseudocode is fine.")) +
        grid3(
            card("Colab notebook",
                p("They share a pre-written notebook with blanks or prompts. Start with comments so the structure is visible even if you get stuck on syntax. Run cells as you go — the interviewer can see.")),
            card("SQL on example data",
                p("Made-up tables resembling their real schema: accounts, orders, products, order_items. Expect joins, aggregations, window functions, data cleaning, and a model output table DDL question.")),
            card("Resume-driven deep dives",
                p("You listed numpy, pandas, sklearn, PowerBI, SAS. Any of these may be probed — including internals. Review anything you have not used recently.")),
        ) +
        h3("Question Distribution (InterviewQuery data)") +
        table(
            ["Category", "Questions", "Priority"],
            [
                ["Data Structures & Algorithms", "176", pill("High","warning")],
                ["SQL", "157", pill("High","warning")],
                ["Machine Learning", "120", pill("High","warning")],
                ["Product Sense & Metrics", "73", pill("Medium","info")],
                ["Probability & Statistics", "62", pill("Medium","info")],
            ]
        )
    )

    python_topics = (
        h2("Python Topics") +
        callout("warning", "Their Stated Python Scope",
            p("Data types, simple data manipulation, programming technique and best practices. "
              "Since your resume lists numpy, pandas, sklearn — they may dive into how those work.")) +
        h3("Data Types & Core Python") +
        collapsible("List vs Tuple vs Set vs Dict",
            p("Mutability, ordering, lookup time. Set/dict membership is O(1); list is O(n).") +
            pre("""# Mutable default argument — classic gotcha
def bad(x, lst=[]):   # lst is SHARED across calls!
    lst.append(x); return lst

def good(x, lst=None):
    if lst is None: lst = []
    lst.append(x); return lst

# Set for O(1) membership test
seen = set()
dupes = [x for x in values if x in seen or seen.add(x)]""")) +
        collapsible("List comprehensions & generator expressions",
            p("Preferred over explicit loops. Generators are lazy — critical for large data.") +
            pre("""# List comprehension
evens = [x for x in range(100) if x % 2 == 0]

# Generator expression (lazy, memory-efficient)
evens_gen = (x for x in range(10_000_000) if x % 2 == 0)

# Dict comprehension
word_len = {w: len(w) for w in ['apple', 'banana', 'cherry']}""")) +
        collapsible("Exception handling & context managers",
            pre("""try:
    df = pd.read_csv(path)
except FileNotFoundError:
    print('File not found: ' + path)
except pd.errors.EmptyDataError:
    print('CSV is empty')
finally:
    print('Done regardless')

# Context manager — auto-closes the file
with open('file.txt', 'r') as f:
    data = f.read()""")) +
        h3("pandas (expect heavy emphasis)") +
        collapsible("Filtering & selection: .loc vs .iloc",
            p(".loc is label-based (inclusive end). .iloc is integer-based (exclusive end). Boolean masks use & | ~ not 'and'.") +
            pre("""# Boolean mask — use & | ~ not 'and' 'or' 'not'
mask = (df['category'] == 'A') & (df['revenue'] > 500)
df[mask]

# .query() — cleaner syntax
df.query("category == 'A' and revenue > 500")

# .loc vs .iloc
df.loc[0:3, 'revenue']   # rows 0-3 by LABEL (end inclusive)
df.iloc[0:3, 2]          # first 3 rows by POSITION (end exclusive)""")) +
        collapsible("groupby + agg + transform",
            p("agg() collapses groups to one row. transform() returns same length — perfect for features.") +
            pre("""# Named aggregation
df.groupby('segment').agg(
    total_rev=('revenue', 'sum'),
    avg_orders=('orders', 'mean'),
    n_accounts=('account_id', 'nunique')
)

# transform() — same shape as original df
df['seg_avg'] = df.groupby('segment')['revenue'].transform('mean')
df['rev_vs_seg'] = df['revenue'] / df['seg_avg']  # ratio feature""")) +
        collapsible("Merging / joining DataFrames",
            pre("""result = pd.merge(
    orders, customers,
    left_on='customer_id', right_on='id',
    how='left',
    validate='m:1'   # raises error on accidental fanout
)

# After any join, verify shape didn't explode
print('Before: %d, After: %d' % (len(orders), len(result)))""")) +
        collapsible("Apply vs vectorized operations",
            pre("""# Vectorized (fast) — preferred
df['new'] = df['a'] + df['b']

# np.where — vectorized if-else
import numpy as np
df['flag'] = np.where(df['revenue'] > 1000, 'high', 'normal')

# pd.cut — bin numeric into named categories
df['tier'] = pd.cut(df['revenue'],
                    bins=[0, 100, 1000, np.inf],
                    labels=['low', 'med', 'high'])

# apply — only when vectorized is not possible (slow)
df['clean'] = df['text'].apply(lambda x: x.strip().lower())""")) +
        collapsible("Date/time operations",
            pre("""df['date'] = pd.to_datetime(df['date_str'])
df['year']        = df['date'].dt.year
df['month']       = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday

# RFM recency feature
df['days_since_order'] = (
    pd.Timestamp.today() - df['last_order']
).dt.days

# Resample to weekly revenue
weekly = df.set_index('date')['revenue'].resample('W').sum()"""))
    )

    sql_topics = (
        h2("SQL Topics") +
        callout("info", "Their Stated SQL Scope",
            p("How you pull data, combine tables, simple SQL tests for data problems, clean and prep data "
              "for a model, design a reasonable table to hold model output.")) +
        collapsible("Window functions (LAG, LEAD, DENSE_RANK)",
            pre("""-- 30-day retention cohort
SELECT
    account_id,
    first_order_date,
    DATE_TRUNC(first_order_date, MONTH) AS cohort_month,
    COUNT(DISTINCT DATE_TRUNC(order_date, MONTH)) AS active_months
FROM orders
GROUP BY 1, 2, 3

-- DENSE_RANK for percentile within segment
SELECT
    account_id,
    revenue,
    DENSE_RANK() OVER (PARTITION BY segment ORDER BY revenue DESC) AS rank_in_segment
FROM accounts

-- LAG: detect order gap (churn signal)
SELECT
    account_id,
    order_date,
    LAG(order_date) OVER (PARTITION BY account_id ORDER BY order_date) AS prev_order_date,
    DATE_DIFF(order_date,
              LAG(order_date) OVER (PARTITION BY account_id ORDER BY order_date),
              DAY) AS days_since_last_order
FROM orders""")) +
        collapsible("Anti-joins: accounts with no recent orders",
            pre("""-- Anti-join: accounts with no order in last 60 days
SELECT a.account_id
FROM accounts a
LEFT JOIN orders o
    ON a.account_id = o.account_id
    AND o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
WHERE o.order_id IS NULL

-- Alternative with NOT EXISTS (often faster)
SELECT account_id
FROM accounts a
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.account_id = a.account_id
    AND o.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY)
)""")) +
        collapsible("RFM feature table",
            pre("""SELECT
    account_id,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY)    AS recency_days,
    COUNT(DISTINCT order_id)                           AS frequency,
    SUM(revenue)                                       AS monetary_value,
    COUNT(DISTINCT DATE_TRUNC(order_date, MONTH))      AS active_months,
    COUNT(DISTINCT product_category)                   AS category_breadth,
    DATE_DIFF(CURRENT_DATE(), MIN(order_date), DAY)    AS account_tenure_days
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
GROUP BY account_id""")) +
        collapsible("Model output table DDL",
            pre("""CREATE TABLE IF NOT EXISTS ds.churn_scores (
    account_id       STRING NOT NULL,
    score_date       DATE NOT NULL,
    churn_prob       FLOAT64 NOT NULL,
    churn_decile     INT64 NOT NULL,       -- 1=highest risk, 10=lowest
    model_version    STRING NOT NULL,
    top_feature_1    STRING,               -- SHAP top feature name
    top_feature_2    STRING,
    top_feature_3    STRING,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (account_id, score_date)
);""")) +
        h3("Likely Schema They Will Use") +
        pre("""accounts(account_id, name, segment,
         membership_status, created_at)

orders(order_id, account_id, order_date,
       revenue, category, status)

products(product_id, sku, department,
         price, category)

order_items(order_id, product_id,
            qty, unit_price)""") +
        h3("Likely Problem Types") +
        ul([
            "Anti-join: accounts with no recent orders",
            "RFM rollup: recency, frequency, monetary per account",
            "Cohort retention: % still ordering M months later",
            "Moving average revenue per account",
            "Model output table DDL with audit columns",
            "Data quality: null rates, dup PKs, negative revenue",
            "Point-in-time feature table (no label leakage)",
        ])
    )

    day_of = (
        h2("Day-Of Tips") +
        callout("success", "Core Philosophy (They Told You Explicitly)",
            p("Thinking out loud beats a silent right answer. Pseudocode beats buggy code. Asking the interviewers beats guessing and moving forward.")) +
        table(
            ["#", "Tactic"],
            [
                ["1", "Start every problem with 2-3 comments outlining your approach before writing code"],
                ["2", "Name variables clearly — even in pseudocode (churn_rate not x)"],
                ["3", "Pause and ask if something is unclear — they grade communication"],
                ["4", "If you forget a function name, describe what it does ('there's a pandas function that groups and aggregates — something like groupby + agg')"],
                ["5", "State your assumptions explicitly ('I'm assuming order_date is a timestamp, not a string')"],
                ["6", "Mention edge cases even if you don't handle them ('I'd also check for NULL account_ids in production')"],
                ["7", "After writing SQL, narrate: 'this gives me one row per account with their RFM features'"],
                ["8", "For ML questions: frame → baseline → complexity. Never jump straight to the complex model."],
            ]
        ) +
        h3("Python Quick-Fire Q&A") +
        collapsible("What's the difference between a list and a tuple?",
            p("Lists are mutable (you can change them). Tuples are immutable (fixed). Tuples are slightly faster and hashable (can be used as dict keys). Use tuples for data that shouldn't change.")) +
        collapsible("What's the difference between .loc and .iloc?",
            p(".loc uses label-based indexing (column names, index labels). .iloc uses integer-based indexing (row 0, column 2). Both return slices — .loc is inclusive on both ends; .iloc excludes the end.")) +
        collapsible("What's the danger with fillna(method='ffill')?",
            p("It propagates the last valid value forward. Fine for time series gaps, but can introduce leakage if applied to the full dataset before a temporal train/test split.")) +
        collapsible("Why is apply() slow?",
            p("apply() runs a Python function on each row/element — no vectorization. Use numpy vectorized operations or pandas built-ins whenever possible. apply() is a last resort.")) +
        collapsible("What's the difference between merge() and join()?",
            p("pd.merge() is flexible — merge on any columns, control how (inner/left/right/outer), handles duplicate column names. df.join() is a shortcut that merges on the index by default."))
    )

    body = tabs("main",
        [("intel","Interview Intel"),("python","Python Topics"),("sql","SQL Topics"),("dayof","Day-Of Tips")],
        [("intel",intel),("python",python_topics),("sql",sql_topics),("dayof",day_of)]
    )
    return html_page(
        "WebstaurantStore Round 2 Prep",
        "Technical interview with Suraj — Colab notebook, SQL + Python + tools",
        body
    )

# ─────────────────────────────────────────────────────────────────────────────
# 12. PLAYSTATION — SENIOR PRODUCT ANALYST PREP
# ─────────────────────────────────────────────────────────────────────────────

def make_playstation():
    # --- Business & Revenue ---
    business = (
        h2("Where PlayStation sits inside Sony") +
        p("PlayStation is Sony's \"Game &amp; Network Services\" (G&amp;NS) segment — one of seven Sony segments "
          "(alongside Music, Pictures, Entertainment/Technology &amp; Services, Imaging &amp; Sensing Solutions, "
          "Financial, and Other). It's Sony's " + b("largest segment by revenue") + " but not its highest-margin "
          "one — Music and Imaging &amp; Sensing Solutions both run richer operating margins.") +
        stats(
            ("¥4,685.7B", "G&NS sales, FY25 (ended Mar '26)"),
            ("¥463.3B", "G&NS operating income, FY25 (record)"),
            ("9.9%", "G&NS operating margin"),
            ("125M", "PlayStation Network MAU, Mar '26"),
        ) +
        table(
            ["Sony segment", "FY25 sales", "FY25 op. income", "Op. margin"],
            [
                [b("Game &amp; Network Services"), "¥4,685.7B", "¥463.3B", "9.9%"],
                ["Music", "¥2,120.1B", "¥447.0B", "21.1%"],
                ["Imaging &amp; Sensing Solutions", "¥2,059.0B", "¥357.3B", "17.4%"],
                ["Entertainment, Technology &amp; Services", "¥2,260.5B", "¥158.6B", "7.0%"],
                ["Pictures", "¥1,499.3B", "¥104.9B", "7.0%"],
            ]
        ) +
        callout("info", "A senior framing line worth saying out loud",
            p("G&amp;NS generates the most revenue in the Sony portfolio, but hardware is a low-margin, "
              "near-breakeven business — the profit comes from software, add-on content, and subscriptions. "
              "That's the \"razor and blades\" model: sell the console close to cost, monetize the ongoing relationship.")) +
        h2("Three revenue lines (FY25)") +
        bars([("Digital Software & Add-on Content", 2415.3), ("Hardware & Others", 1391.6), ("Network Services", 763.1)],
             prefix="¥", suffix="B") +
        caption("Source: Sony FY2025 (fiscal year ended March 2026) earnings release, G&NS segment note. Bars show FY25 sales by revenue line.") +
        table(
            ["Revenue line", "FY25 sales", "Definition", "Direction"],
            [
                [b("Digital Software &amp; Add-on Content"), "¥2,415.3B", "First- and third-party game sales, DLC, in-game/microtransactions, sold digitally or via disc.", "Growing — the profit engine."],
                [b("Network Services"), "¥763.1B", "PlayStation Plus subscriptions plus other online-service revenue.", "Fastest-growing line."],
                [b("Hardware &amp; Others"), "¥1,391.6B", "PS5 console unit sales (standard/Digital Edition/Pro), accessories, peripherals.", "Declining — unit sales down; margin near breakeven."],
            ]
        ) +
        callout("neutral", "FY26 forecast — say this if asked about outlook",
            p("Sony guides G&amp;NS sales down 6% (fewer hardware units) but operating income up 30% to ¥600B — "
              "mainly because FY25 included a one-off ¥120.1B Bungie impairment that won't repeat, plus a richer "
              "first-party software slate (SAROS, Marvel's Wolverine). Excluding one-time items, underlying profit "
              "is expected to grow at a double-digit rate.")) +
        h2("PlayStation Network scale — MAU and seasonality") +
        bars([("Dec '22", 112), ("Dec '23", 123), ("Mar '25", 124), ("Jun '25", 123), ("Dec '25", 132), ("Mar '26", 125)], suffix="M") +
        caption("Source: Sony investor disclosures. MAU in millions. Notice the December peak (holiday gifting/play) and the "
                "March step-down — this exact seasonal pattern is the first thing to rule out in any \"engagement dropped "
                "quarter-over-quarter\" question.") +
        h2("PlayStation Plus — the subscription engine") +
        bars([("Essential", 62), ("Premium", 22), ("Extra", 16)], suffix="%") +
        caption("Subscriber mix by tier, most recent disclosed breakdown (~50M total subscribers). Premium and Extra together "
                "are 38% of the base, up from 30% two years earlier — Sony's upsell motion is working.") +
        table(
            ["Tier", "What it includes", "US monthly price (post May '26 hike)"],
            [
                [b("Essential"), "Online multiplayer, cloud save, monthly free games.", "$10.99"],
                [b("Extra"), "+ a rotating game catalog (hundreds of titles).", "$16.99"],
                [b("Premium"), "+ cloud streaming and a classic-games library.", "~$19.99"],
            ]
        ) +
        callout("warning", "Live tension to know about",
            p("Sony just raised PS Plus prices across all three tiers (May 2026) while also rotating 12 titles out of "
              "Extra/Premium (July 21). PS Plus churn is running around 7.8%. That combination — price up, catalog down, "
              "in the same window — is a natural \"diagnose the churn spike\" prompt (see the Diagnose tab)."))
    )

    # --- Core Products ---
    product_areas = [
        ("PS5 hardware (Standard / Digital Edition / Pro)",
         "The platform itself — 93M+ units sold lifetime. Priced near cost; the entry point that creates a PSN account and "
         "unlocks everything downstream. Memory/component cost (BOM) is a live margin lever right now.",
         ["Hardware unit sell-through", "Hardware gross margin", "Console price elasticity", "Digital Edition mix"]),
        ("PlayStation Plus (Essential / Extra / Premium)",
         "The subscription line, ~50M subscribers, ¥763.1B in FY25 Network Services revenue. The main monetization and "
         "retention lever once someone owns a console.",
         ["Subscriber count & tier mix", "Tier upgrade rate", "Churn rate", "ARPU per tier"]),
        ("PlayStation Store (digital storefront)",
         "Where users buy games, DLC, and add-on content digitally — the delivery mechanism for the largest revenue line "
         "(Digital Software & Add-on Content, ¥2,415.3B FY25).",
         ["Store conversion rate", "Digital vs physical mix", "Add-on / DLC revenue per buyer", "Recommendation CTR"]),
        ("First-party studios & exclusives",
         "Sony's owned studios — Naughty Dog, Insomniac, Guerrilla, Santa Monica Studio, Bungie — that produce the exclusive "
         "titles which are PlayStation's real moat. Upcoming: SAROS, Marvel's Wolverine.",
         ["First-party attach rate", "Launch-window engagement lift", "Live-service title retention"]),
        ("Cross-platform PC releases",
         "A real strategic shift: former PS5 exclusives (God of War, Horizon, Spider-Man) now ship on PC/Steam later, trading "
         "some exclusivity for incremental software revenue and franchise reach.",
         ["PC port revenue (incremental)", "Console vs PC cannibalization", "Time-to-PC-port"]),
        ("Cloud streaming & Remote Play",
         "Premium-tier cloud streaming (play without downloading) plus Remote Play. Infrastructure-cost-sensitive — every "
         "quality improvement has a bandwidth/CDN cost tradeoff.",
         ["Cloud session count", "Streaming quality / buffering rate", "Premium retention from cloud usage"]),
    ]
    products = callout("info", "How to use this tab",
        p("These are the surfaces you'd actually plausibly own metrics for as a Senior Product Analyst. Know what each one "
          "is, what it's for, and which 2-3 metrics anchor it — that's the level of depth interviewers probe for."))
    for name, desc, metrics in product_areas:
        products += card(name, p(desc) + pill_row(metrics))

    # --- Journey & Segments ---
    lifecycle = ["Awareness", "Console purchase", "Account creation / onboarding", "First game purchase",
                 "Engagement loop", "Subscription upsell", "Retention", "Churn / win-back"]
    journey = (
        h2("The end-to-end customer journey") +
        chip_flow(lifecycle) +
        caption("Every metric on the Metrics tab hangs off one of these stages. When asked to define or improve a metric, name the stage first.") +
        h2("Journey stage detail") +
        table(
            ["Stage", "What happens", "Primary risk"],
            [
                [b("Awareness"), "Marketing, exclusive-title trailers, console launch hype.", "Competing console/PC launches split attention."],
                [b("Console purchase"), "Buys PS5 (retail, bundle, or promo) — often the biggest single spend.", "Price sensitivity, component cost pressure on Sony's side."],
                [b("Onboarding"), "Creates/links PSN account, sets up profile, connects to friends.", "Account-creation friction, PS4&rarr;PS5 migration confusion."],
                [b("First purchase"), "Buys or redeems first digital title, often a pack-in or PS Plus monthly game.", "Low first-purchase intent if catalog isn't compelling."],
                [b("Engagement loop"), "Regular sessions, multiplayer, trophies, live-service content drops.", "Content-drought periods between big releases."],
                [b("Subscription upsell"), "Essential &rarr; Extra &rarr; Premium tier progression.", "Users don't perceive incremental value at the next tier."],
                [b("Retention"), "Continues playing/subscribing across console generations.", "Console-generation aging (PS4 users going dormant)."],
                [b("Churn / win-back"), "Cancels PS Plus or goes dormant; may be reactivated via notifications/rewards.", "Price increases and catalog rotation both raise churn risk."],
            ]
        ) +
        h2("How to segment any PlayStation metric") +
        p("When a metric moves, these are the cuts that usually explain it — have this list ready before you're asked to \"segment further.\"") +
        mini_grid([
            ("Subscription tier", "Free/no-PS-Plus, Essential, Extra, Premium — very different economics and engagement per tier."),
            ("Platform generation", "PS4 vs PS5 — the PS4 base is aging and naturally going dormant, independent of anything Sony does."),
            ("Engagement depth", "Casual vs core vs hardcore — hardcore users dominate variance in playtime metrics."),
            ("Region", "US/EU/Japan/Asia — different price points, catalog availability, and console-cycle timing."),
            ("Tenure / lifecycle", "New (<90 days), active, lapsing, churned — the same aggregate can hide different stories per cohort."),
            ("Title / genre played", "Single-player narrative vs live-service multiplayer — session length and frequency differ by an order of magnitude."),
        ], cols=2)
    )

    # --- Core Metrics (L1 -> L2 -> L3) ---
    metric_tree = [
        ("Monthly Active Users (MAU)", "125M (Mar '26)",
         "MAU = New/reactivated MAU + Returning MAU &minus; Churned/dormant MAU",
         [("New MAU", "Accounts active for the first time this month. Leading indicator: monthly hardware unit sell-through."),
          ("Reactivated MAU", "Accounts dormant &ge;60 days that became active again — spikes around major exclusive launch windows."),
          ("PS4&rarr;PS5 migration rate", "% of active PS4 accounts also active on PS5 within the same quarter."),
          ("PS4 monthly dormancy rate", "% of last month's PS4 MAU inactive this month — rises structurally as the PS4 fleet ages."),
          ("Churned MAU", "Accounts active last month, inactive this month.")]),
        ("Avg. Playtime per MAU", "Total play time +1% YoY (Q4 FY25)",
         "Avg Playtime = Sessions per MAU &times; Avg Session Length",
         [("Sessions per MAU", "Total play sessions &divide; MAU — a frequency/habit metric."),
          ("Avg session length (min)", "Total minutes &divide; total sessions — a depth metric, read separately from frequency."),
          ("Live-service release cadence", "# of major content drops/seasons shipped per month — a leading indicator for sessions/MAU."),
          ("PS Plus catalog net adds", "# titles added minus removed from Extra/Premium per month — leads sessions/MAU and subscription revenue."),
          ("Multiplayer session share", "% of sessions that are online multiplayer — they run measurably longer than single-player."),
          ("Matchmaking queue time / latency", "Median seconds to match + median ms latency — a direct cap on session length.")]),
        ("PS Plus (Network Services) Revenue", "¥763.1B FY25",
         "PS Plus Revenue = Subscribers &times; Tier Mix &times; Price per Tier &minus; Refunds/Churn",
         [("Tier upgrade rate", "% of Essential upgrading to Extra (and Extra&rarr;Premium) per month — the main revenue-per-sub lever."),
          ("Price elasticity", "% change in subscriber volume per % change in price — measured around each price change."),
          ("Catalog net adds by tier", "# titles added minus removed per month in Extra/Premium — leads engagement and churn."),
          ("Trial-to-paid conversion", "% of free-trial starts (e.g. bundled at console purchase) that convert to paid."),
          ("Annual vs monthly billing mix", "% on annual plans — annual members are insulated from short-term churn shocks."),
          ("Voluntary churn rate by tier", "% in each tier cancelling per month, excluding payment-failure churn.")]),
        ("Software Attach Rate", "317.9M lifetime software / 93M+ hardware units",
         "Attach Rate = Software units &divide; Hardware units (cohort-aged, not blended)",
         [("First-party attach rate", "First-party units &divide; hardware units, aged by hardware-purchase cohort."),
          ("Third-party attach rate", "Third-party units &divide; hardware units, aged by hardware-purchase cohort."),
          ("Digital mix %", "Digital software units &divide; total software units — digital converts faster post-purchase."),
          ("Subscriber vs non-subscriber delta", "Attach for Extra/Premium subs minus non-subs — isolates catalog-substitution effects."),
          ("Avg discount depth on software", "Unit-weighted average % off list price — a lever and a confound on attach rate."),
          ("First-party release count", "# of major first-party titles shipped per quarter — the main supply-side lever.")]),
        ("G&NS Operating Income", "¥463.3B FY25 (record, +12% YoY)",
         "Operating Income = Sales &minus; COGS (hardware BOM, royalties) &minus; OpEx (marketing, studios, R&D) &plusmn; one-time items",
         [("Hardware gross margin per unit", "(ASP &minus; BOM) &divide; ASP — Sony flagged memory/component pricing as a live pressure."),
          ("First-party revenue mix %", "First-party revenue &divide; total software revenue — first-party carries higher margin."),
          ("One-time impairment charges", "Non-recurring write-downs (e.g. ¥120.1B Bungie in FY25) — exclude to read the underlying trend."),
          ("R&D / next-gen spend as % of sales", "Next-gen platform investment &divide; sales — a deliberate near-term margin drag."),
          ("FX impact on sales/OI", "Yen value of the FX contribution, as broken out in Sony's own segment notes.")]),
    ]
    metrics = callout("info", "Decompose every metric top-down",
        p("For each L1 (north-star) metric: write the L2 formula that breaks it into components, then name the specific L3 "
          "metrics — each with a real definition — you'd pull up first if the L1 moved. Vague \"drivers\" don't survive a "
          "follow-up; named metrics do."))
    for l1, l1v, l2, l3 in metric_tree:
        l3_rows = [[b(n), d] for n, d in l3]
        body = field("L2 — formula / leading indicators", l2) + table(["Metric", "Definition"], l3_rows)
        metrics += card(l1, body, pill=l1v)

    # --- Diagnose a Metric ---
    diagnose_qs = [
        ("Average playtime per MAU dropped 8% quarter-over-quarter. Walk me through your diagnosis.",
         "Composite ratio (total hours ÷ MAU)",
         ["Is this total hours &divide; MAU (mean, pulled by heavy users) or median per-user hours? That changes what could be driving it.",
          "QoQ or YoY? Given PSN MAU peaks every December, a Q4&rarr;Q1 QoQ comparison is expected to fall — I'd want the YoY view too.",
          "Same platform mix (PS4/PS5) and region in both periods?"],
         ["PS4 vs PS5", "Region", "PS Plus sub vs free", "New vs tenured MAU", "Genre of last-played title"],
         [("Seasonality", "Compare YoY, not just QoQ, and check the MAU seasonality chart.", "December MAU (132M) is a known seasonal peak; the next quarter naturally steps down — this alone can explain most of an 8% QoQ move."),
          ("Comp-base / mix effect", "Did last quarter include a blockbuster live-service finale or exclusive launch that inflated the baseline?", "A huge prior-quarter exclusive can make this quarter look like a decline when it's really 'no equivalent event this time.'"),
          ("Denominator dilution (who vs what)", "Did MAU grow faster than total hours? A hardware promo pulling in low-engagement accounts drags the average down.", "A successful holiday hardware promo can look like an 'engagement problem' when it's actually acquisition success diluting the average."),
          ("Instrumentation", "Any change to how playtime/cross-play hours are logged?", "Cross-play or privacy-setting changes can silently undercount hours."),
          ("Cross-platform leakage", "Are cross-buy titles (former exclusives now on PC) pulling hours off PlayStation?", "Hours moving to PC for a cross-buy title isn't churn — the player is still engaged, just off-platform.")],
         "Suppose segmentation shows the drop is concentrated entirely in the new-MAU cohort acquired via a holiday hardware promo, while tenured-MAU playtime is flat YoY. That points to a denominator/mix effect from a successful acquisition push, not a real engagement problem.",
         "Report both a blended avg-playtime metric and a tenured-MAU-only version going forward, so acquisition success doesn't get mistaken for an engagement decline. Track the new cohort's playtime ramp over the next 2 quarters to confirm it's just early-lifecycle."),
        ("MAU declined for two consecutive quarters despite PS Plus subscriber counts holding steady. What's going on?",
         "Rate / count metric",
         ["Declining vs prior quarter, or vs the same quarter last year (controls for seasonality)?",
          "Is the decline global, or concentrated in specific regions?",
          "Is 'MAU' counting PS4 and PS5 together, or reported separately?"],
         ["Platform generation (PS4 vs PS5)", "Region", "PS Plus sub vs free", "Tenure (new vs long-standing)"],
         [("End-of-console-cycle effect", "Is the decline concentrated in PS4-only accounts?", "The PS4 install base naturally ages out of activity years after PS5 launch — structural, expected, not a product failure."),
          ("Content drought", "Was there a gap in major first-party or live-service releases in the window?", "Fewer big launches means fewer reasons for lapsed casual players to log back in."),
          ("Competitive dynamics", "Did a competitor run a major promo (e.g. a Game Pass price cut) or ship a major exclusive?", "Attention is zero-sum — a strong competitor moment can pull marginal players away temporarily."),
          ("Account consolidation", "Any platform change merging duplicate or linked PSN accounts?", "A dedup/consolidation event can look like organic MAU loss but is really an accounting artifact.")],
         "PS Plus subscribers staying flat while overall MAU falls suggests the erosion is concentrated in the free/casual, non-paying segment — not the core paying base. That's a real but lower-severity finding: less alarming for near-term revenue, still relevant for the future upsell funnel.",
         "Split MAU reporting into 'PS Plus MAU' vs 'Free MAU' so leadership doesn't conflate a declining casual footprint with a declining monetizable base. Separately, model the PS4 fleet's natural retirement curve so future quarters aren't re-diagnosed as a surprise."),
        ("PS Plus tier-upgrade rate (Essential &rarr; Extra) has stalled for two straight quarters.",
         "Rate metric (conversion)",
         ["Stalled = flat, or actually declining?",
          "Upgrade rate as % of the Essential base, or absolute upgrade count (affected by base-size changes)?",
          "Any recent redesign of the store homepage or upsell placement?"],
         ["Tenure on Essential", "Acquired via promo vs full price", "Region", "Redeemed current month's free game"],
         [("Catalog quality dip", "Compare recent Extra catalog additions/removals against prior quarters.", "Fewer compelling titles added to Extra weakens the value story for upgrading."),
          ("Widened price gap", "Check timing against the tier price changes.", "After the May '26 hike, the $ gap between Essential and Extra grew — upgrading costs relatively more even if the catalog didn't change."),
          ("Product/UX regression", "Diff the upsell placement/impression rate before and after any homepage redesign.", "A redesign can bury the upgrade prompt below the fold — a fixable bug, not a demand problem."),
          ("Saturation of ready-to-convert users", "Look at upgrade rate by Essential tenure cohort.", "If high-intent subscribers already converted earlier, the remaining base is naturally lower-intent."),
          ("Competitive substitution", "Any concurrent competitor catalog or price move?", "A stronger competing subscription catalog can reduce the perceived need to upgrade tier.")],
         "Checking upsell banner impression logs shows the 'Try Extra free' placement was moved below the fold in a recent homepage redesign — a measurable drop in impressions precedes the drop in upgrades by exactly one release cycle. That's a product/UX regression, not a demand-side issue.",
         "Restore or redesign the upsell placement, and A/B test the new version rather than shipping it blind. Add catalog-freshness score as a standing leading indicator so future stalls are caught earlier."),
        ("Software attach rate fell right after the new console generation's biggest launch-window hardware promo.",
         "Composite ratio (continuous)",
         ["Attach rate defined as lifetime cumulative units, or trailing-12-month? Blended snapshot, or aged by hardware cohort?",
          "Digital and physical counted the same way?",
          "Is this first-party attach, third-party attach, or both combined?"],
         ["First-party vs third-party", "Digital vs physical", "By title/genre", "Extra/Premium sub vs non-sub"],
         [("Denominator spike (who vs what)", "Did hardware sell-through spike from a promo/price cut in the same window?", "New buyers haven't had time to buy their first game yet — a timing/denominator effect on a blended snapshot, not less demand."),
          ("Thin release slate", "Was there a gap in first-party releases immediately after the hardware promo?", "If the big first-party title lands next quarter, attach naturally catches up once it ships."),
          ("Subscription cannibalization", "Compare attach rate for Extra/Premium subs vs non-subs.", "Subscribers may play included catalog titles instead of buying — a real substitution effect worth separating out."),
          ("Promo/pricing timing mismatch", "Was there a software discount that ended right as hardware sales spiked?", "New buyers missing a software sale window buy later — again a timing artifact.")],
         "Plotting attach rate by hardware-purchase cohort age (rather than a blended point-in-time snapshot) shows each cohort's individual attach curve is completely normal — the blended metric fell only because the newest, youngest cohort got much larger relative to older cohorts. It's a mix/timing artifact.",
         "Report attach rate by hardware-cohort age going forward, not as a single blended snapshot. Separately quantify any genuine subscription-cannibalization effect with a controlled subscriber vs non-subscriber comparison."),
        ("PS Plus churn rate spiked right after the May 2026 price increase.",
         "Rate metric",
         ["Which tier(s)? Essential is most price-sensitive.",
          "Voluntary cancellation, or payment-failure-driven churn?",
          "One-time spike at the renewal date, or a sustained elevated rate?"],
         ["Tier", "Monthly vs annual billing", "Region (was the hike staggered?)", "Pre-hike engagement level"],
         [("Expected price elasticity", "Compare actual churn against finance's pre-launch elasticity model.", "Some churn from a price hike is anticipated and already priced into the business case — that portion isn't a 'problem.'"),
          ("Billing-cycle mechanics", "Does the spike line up exactly with the first renewal date after the hike?", "A spike concentrated at renewal dates is a real but expected, mechanical effect of when subscribers see the new price."),
          ("Compounding catalog removal", "Cross-reference the 12-title catalog rotation date against the churn spike.", "Sony's price hike and a 12-title Extra/Premium catalog exit landed in the same window — losing value and paying more at once compounds churn."),
          ("Competitive response", "Did a competitor cut price or add content in the same period?", "Price-sensitive subscribers have an easy substitute to switch to right when PlayStation's price went up.")],
         "The actual churn spike exceeds finance's pre-launch elasticity model, and the excess is concentrated among Essential subscribers who were also affected by the catalog rotation — pointing to the catalog removal as a compounding, controllable factor on top of the expected price effect.",
         "Decompose churn into a price-driven component (expected, modeled) and a catalog/competitive-driven component (actionable). Recommend not scheduling future price increases in the same window as major catalog rotations."),
        ("Digital storefront conversion rate (visit &rarr; purchase) dropped on PS5 but stayed flat on PS4.",
         "Rate metric",
         ["Conversion defined as any purchase (incl. microtransactions) or full-game purchases only?",
          "Which store surface — homepage, search, or individual game pages?",
          "Any release notes or A/B tests that shipped to PS5 only in the window?"],
         ["Store surface/page", "New-release vs back-catalog", "PS Plus sub vs non-sub", "User tenure"],
         [("PS5-specific UI change", "Check the release/experiment log for anything PS5-only shipped in the window.", "PS5 and PS4 often run different store client versions — a PS5-only redesign is the first thing to check."),
          ("Catalog mix shift", "Did the PS5 storefront skew toward pricier new-release titles recently?", "A mix shift toward higher-priced titles can lower conversion rate even with stable purchase intent."),
          ("Subscription substitution", "Compare Extra/Premium growth rate on PS5 vs PS4.", "If PS Plus growth is concentrated on PS5, more users browse-and-redeem included titles instead of buying — a substitution effect."),
          ("Checkout/payment bug", "Funnel break-down: browse &rarr; add to cart &rarr; complete purchase, by platform.", "A platform-specific checkout regression would show as a drop concentrated at one funnel step.")],
         "Funnel breakdown shows the drop is concentrated specifically at the 'add to cart &rarr; complete purchase' step on PS5, coinciding exactly with a checkout-flow redesign release — a product regression at a specific step, not a broad demand issue.",
         "Fix or roll back the specific checkout step. Separately, track 'browse &rarr; subscription redemption' as its own successful outcome so healthy PS Plus browsing stops looking like a broken purchase funnel."),
    ]
    open_model = (
        p("Say this before touching a single hypothesis — it signals structure, not improvisation. Four filters, cheap/boring &rarr; expensive/exotic:") +
        mini_grid([
            ("1. Is it real?", "Rule out a data/instrumentation issue first."),
            ("2. Who vs. what?", "Fewer people, or the same people doing less?"),
            ("3. Seasonal/market vs. product?", "PSN has strong Dec-peak seasonality — expected vs fixable."),
            ("4. Localize", "Only now: which segment/step explains most of it."),
        ], cols=4) +
        callout("success", "If you blank, anchor on this",
            p(b("\"Real, then who-vs-what, then seasonal-vs-product, then localize.\""))))
    diagnose = (
        callout("info", "Prompt style to expect",
            p("\"Average playtime dropped — walk me through your diagnosis.\" This is the real question asked in your last "
              "PlayStation interview, live as a framework you can reuse on any metric they hand you.")) +
        collapsible("Open with this: the mental model that sets the tone", open_model) +
        h2("The 5-step framework") +
        steps_list([
            ("1", "Clarify the metric", "Nail the exact definition, window, and comparison basis before hypothesizing — QoQ vs YoY changes everything given PSN's seasonality."),
            ("2", "Segment", "Slice by platform generation, tier, region, tenure, and title/genre — the aggregate number is almost always hiding a concentrated sub-population."),
            ("3", "Rule out, cheap to expensive", "Data/instrumentation &rarr; market/seasonal &rarr; mix/denominator &rarr; product change &rarr; competitive effect. Work in that order."),
            ("4", "Isolate", "Find the specific segment or funnel step that explains most of the movement, and confirm the size adds up to the headline number."),
            ("5", "Recommend", "End with a decision-ready recommendation and an owner — not just an explanation."),
        ]) +
        h2("Practice questions — full worked diagnosis")
    )
    for q, mtype, clarify, segs, ruleouts, isolate, rec in diagnose_qs:
        inner = (field("Clarifying questions", "") + ul(clarify) + pill_row(segs) +
                 table(["Suspect", "How to check", "PlayStation-specific angle"],
                       [[b(s), c, a] for s, c, a in ruleouts]) +
                 field("Isolate / likely finding", isolate) +
                 callout("success", "Recommendation", p(rec)))
        diagnose += collapsible(f"{q} <span class='pill neutral'>{mtype}</span>", inner)

    # --- A/B Test Design ---
    experiments = [
        ("Redesign the Essential &rarr; Extra upgrade prompt on the PS Store homepage to lift tier-upgrade rate", "Rate",
         "If we show a clearer 'Try Extra free for 7 days' banner with catalog highlights on the PS Store homepage, then Essential&rarr;Extra upgrade rate rises, because most Essential subscribers under-appreciate the Extra catalog today (an awareness gap, not a lack of interest).",
         "User-level, bucketed by PSN account ID among active Essential subscribers who haven't upgraded — keeps a user consistent across devices.",
         "Essential &rarr; Extra upgrade rate within 30 days of exposure (RATE metric).",
         "Banner click-through rate, trial-start rate, trial-to-paid conversion, catalog page visits.",
         "Essential cancellation rate (don't scare people out of PS Plus entirely), support ticket volume, page-load performance.",
         "Baseline upgrade rate &asymp; 2%/month. Detect a 15% relative lift (2.0% &rarr; 2.3%), &alpha;=0.05, power=80%. n &asymp; 36,600 per arm.",
         ["Novelty effect — a new banner earns clicks just for being new; compare week-1 vs week-3/4 to check for decay.",
          "Seasonality — avoid launching across a big PS Plus monthly-game-drop day, which spikes platform-wide engagement.",
          "Frequency capping — cap banner exposures so fatigue doesn't bias later weeks of the test."],
         "Ship if the upgrade-rate lift persists past week 2 (post-novelty) and Essential cancellation/complaint rate stays flat."),
        ("New personalized game-recommendation model on the PS Store home feed", "Continuous (+ rate secondary)",
         "If we replace the rule-based 'popular in your region' rail with a personalized ML recommendation model, then avg playtime attributable to recommended titles rises, because matching titles to individual taste surfaces relevant games users wouldn't find via generic popularity.",
         "User-level, stratified by engagement tier (casual/core/hardcore) — hardcore users drive outsized playtime variance and could otherwise imbalance the arms.",
         "Avg minutes played from store-recommended titles over 14 days (CONTINUOUS — expect right-skew; report median + a winsorized/log-transformed mean, not a raw mean).",
         "Click-through rate on the recommendation rail (RATE), purchase/redeem rate from the rail, distinct-titles-played (checking for a filter-bubble effect).",
         "Overall store revenue (a 'discovery' win shouldn't cannibalize higher-margin promoted placements), page-load latency, genre diversity of what's surfaced.",
         "Baseline attributable playtime &asymp; 45 min/14 days, SD &asymp; 60 min. Detect +6 min (~13%). n &asymp; 1,600 per arm — an order of magnitude smaller than the rate example, because a continuous metric carries far more per-user signal.",
         ["Heavy right-skew from binge players — use a log-transform or trimmed mean, not the raw mean.",
          "Interaction with the PS Plus monthly free game — a huge exogenous driver; stratify by whether the user redeemed it.",
          "Novelty of 'new recommendations' wearing off after the first couple of weeks."],
         "Ship if the lift holds in weeks 3-4 (post-novelty) without hurting overall store revenue or genre diversity."),
        ("Test a discounted introductory price for first-time PS Plus sign-ups", "Rate + continuous guardrail",
         "If new-to-PS-Plus accounts see a discounted first month ($4.99 vs $10.99 Essential), then trial-to-paid conversion rises enough to grow net subscription revenue after 90 days, because price is a meaningful barrier for console-only buyers who've never tried a paid tier.",
         "Geo- or cohort-based rollout rather than pure per-user pricing (fairness/optics of charging different prices) — verify balance with an SRM check before trusting results.",
         "90-day net PS Plus revenue per exposed new account — blends conversion &times; price &times; early churn; this is the real business question, not raw sign-up rate.",
         "Trial-start rate, day-30/day-90 retention of the discounted vs standard cohort, downgrade/cancel rate right after price reverts to full at month 2.",
         "Cannibalization (only test on truly never-subscribed accounts), brand/price-perception spillover to other tiers, reversion-churn spike.",
         "Revenue-per-account is noisy and right-skewed, and the real read requires waiting through the 90-day retention window — expect a larger sample and longer runtime than a simple conversion test.",
         ["The classic trap: a conversion lift funded entirely by discount-seekers who churn the moment price reverts is a loss — always read conversion together with post-reversion retention.",
          "Geo-based pricing raises fairness/regulatory optics — flag this explicitly rather than defaulting to per-user pricing."],
         "Ship only if net revenue per exposed account is positive after the discount period ends, measured with actual reversion-churn data — not assumed."),
        ("Faster matchmaking algorithm to cut multiplayer queue times", "Continuous",
         "If we relax skill-based matchmaking strictness slightly to widen the eligible player pool, then queue wait time drops and session length/frequency rise, because long queues are a top driver of session abandonment in multiplayer titles.",
         "Match- or shard/geo-level randomization rather than pure per-player — an individual's queue time depends on who else is in the eligible pool, so per-user assignment can leak between arms (a classic interference problem).",
         "Median queue wait time (CONTINUOUS — use median given a heavy right tail from off-peak hours).",
         "Session length, sessions/week, match-abandonment rate, post-match retention (did they queue again).",
         "Match fairness/skill-gap complaints, win-rate variance (a wider pool risks more mismatched games), player-reported toxicity/satisfaction.",
         "High variance by time-of-day and region — stratify by peak/off-peak and region before pooling, or the confound swamps the effect.",
         ["Network-effects/interference — prefer geographic or shard-level randomization over per-player to avoid arms contaminating each other's queue pools.",
          "Time-of-day and regional population size are large confounders; must stratify, not just randomize and hope."],
         "Ship if queue time drops without a matching rise in abandonment or mismatch complaints, validated across both peak and off-peak windows."),
        ("Push notification + login-streak reward to win back PS Plus subscribers lapsed 30+ days", "Rate",
         "If we send a personalized 'come back and claim your reward' push plus a login-streak bonus to lapsed subscribers, then 30-day reactivation rate rises, because many lapses are attention-driven (life got busy) rather than deliberate abandonment.",
         "User-level among subscribers inactive 30+ days; a true holdout group receives no notification at all.",
         "Reactivation rate — logged in AND played &ge;1 session within 14 days of send.",
         "Login-streak completion rate, 30-day retention of reactivated users (not just the one-time bounce-back), notification unsubscribe rate.",
         "Notification opt-out rate (don't burn the channel), support/complaint volume, comparison against the true holdout rather than a naive before/after.",
         "Baseline spontaneous 14-day reactivation among lapsed users ~3%; detecting a +1pp absolute lift is a standard two-proportion sample-size calculation, moderate sample size.",
         ["Regression-to-the-mean / survivorship — some lapsed users would've returned anyway; the holdout isolates the true incremental effect.",
          "A one-time reward-driven bounce-back that doesn't persist past the reward window is a weak win — track sustained engagement, not just the open."],
         "Ship if incremental reactivation vs the holdout is positive AND reactivated users show real follow-on engagement, not just a single reward-driven login."),
        ("Increase cloud-streaming bitrate/resolution for PS Plus Premium to improve retention", "Rate (+ continuous leading indicators)",
         "If we raise the streaming bitrate ceiling for Premium cloud-play sessions, then 90-day Premium retention improves, because streaming-quality complaints (lag, artifacting) are a top cited reason for Premium churn in support tickets.",
         "User-level among Premium subscribers with sufficient bandwidth — requires a bandwidth-eligibility filter so the treatment isn't invisible or harmful to low-bandwidth users.",
         "90-day Premium retention rate (RATE) — a long-horizon primary, so a leading-indicator readout is needed before the full window closes.",
         "Streaming session length, session abandonment/buffering-event rate, in-session quality complaints, cloud-session frequency.",
         "Bandwidth/CDN cost per session (higher bitrate raises infra cost — weigh against retention $ value), stream failure rate for users near the bandwidth cutoff.",
         "90-day retention is a long-horizon, low-variance rate metric — needs a large sample and long runtime; use leading indicators (abandonment, complaints) for an earlier readout.",
         ["This is fundamentally a unit-economics question, not just a UX win — convert the retention lift into $ and compare against incremental CDN/bandwidth cost before recommending a ship.",
          "Bandwidth-eligibility filtering is itself a selection risk — results may not generalize to the full Premium base, which likely needs a separate lower-bitrate variant."],
         "Ship if the retention lift's revenue value exceeds the incremental streaming cost, and explicitly scope the recommendation to the bandwidth-eligible population it was tested on."),
    ]
    exp_read_first = (
        h3("Rate / proportion metric") + pill_row(["e.g. conversion, upgrade rate, churn"]) +
        p("n per group = (z<sub>&alpha;/2</sub> + z<sub>&beta;</sub>)&sup2; &times; [p&#8321;(1&minus;p&#8321;) + p&#8322;(1&minus;p&#8322;)] / (p&#8321;&minus;p&#8322;)&sup2;. "
          "Worked example: baseline 2%, target 2.3%, &alpha;=0.05, power=80% &rarr; n &asymp; 36,600 per arm. Low-incidence rate metrics need large samples because most users contribute a '0'.") +
        h3("Continuous metric") + pill_row(["e.g. playtime, session length, queue time"]) +
        p("n per group &asymp; 16 &times; &sigma;&sup2; / &delta;&sup2; (rule of thumb at 80% power, &alpha;=0.05). Worked example: SD &asymp; 60 min, detect a 6-minute shift &rarr; n &asymp; 1,600 per arm — an order of magnitude smaller than the rate example, because each user carries a richer, continuous signal.") +
        callout("neutral", "Say this out loud — it's the senior signal",
            p("This is exactly why platform-wide metrics like MAU need months to move, while a focused continuous metric like 'session length among already-active players' can be read in days. Always name which type of metric you're using and why it drives your runtime.")))
    experiments_html = (
        callout("info", "How to use this",
            p("Each card is an interview prompt. Structure every spoken answer as: clarify &rarr; hypothesis &rarr; randomization unit &rarr; primary/secondary/guardrails (naming rate vs continuous explicitly) &rarr; sample size &rarr; the big caveats &rarr; decision rule.")) +
        collapsible("Read first: sample sizing, rate vs. continuous metrics", exp_read_first) +
        h2("Experiment prompts"))
    for q, mtype, hyp, rand, prim, sec, guard, size, gotchas, dec in experiments:
        inner = (field("Hypothesis", hyp) + field("Randomization unit", rand) +
                 grid3(field("Primary", prim), field("Secondary", sec), field("Guardrails", guard)) +
                 field("Sample size", size) +
                 field("Gotchas & caveats", "") + ul(gotchas) +
                 callout("success", "Decision rule", p(dec)))
        experiments_html += collapsible(f"{q} <span class='pill neutral'>{mtype}</span>", inner)

    body = tabs("ps",
        [("business", "Business & Revenue"), ("products", "Core Products"), ("journey", "Journey & Segments"),
         ("metrics", "Core Metrics"), ("diagnose", "Diagnose a Metric"), ("experiments", "A/B Test Design")],
        [("business", business), ("products", products), ("journey", journey),
         ("metrics", metrics), ("diagnose", diagnose), ("experiments", experiments_html)])
    return html_page(
        "PlayStation — Senior Product Analyst Interview Prep",
        "Business fluency + the two question archetypes — diagnosing a metric decline and designing an A/B test. Numbers are Sony's FY2025 (year ended March 2026) disclosures.",
        body)


def _topic_list(topics):
    """topics = [(title, summary, [bullets], tip_or_None)]"""
    out = ""
    for title, summary, bullets, tip in topics:
        inner = ul(bullets)
        if tip:
            inner += callout("info", "Interview tip", p(tip))
        summ = f"<span class='tag'>{summary}</span>" if summary else ""
        out += collapsible(f"{title} {summ}", inner)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 13. A/B TESTING STATS — SENIOR PRODUCT ANALYST PREP
# ─────────────────────────────────────────────────────────────────────────────

def make_ab_test_stats():
    foundations = (
        p("Move quickly through this section — interviewers expect fluency here, not a lecture.") +
        h3("Distribution types at a glance") +
        table(["Distribution", "Example metric", "Key property to remember"],
            [["Normal", "Sample means / proportions (via CLT)", "Symmetric — most standard tests rely on the sampling distribution being normal, not the raw data"],
             ["Binomial", "Conversion, click, signup (0/1 per user)", "Underlies proportion tests; variance depends on p(1&minus;p), largest around p = 0.5"],
             ["Poisson", "# purchases, # tickets per user", "Assumes variance = mean — often violated (overdispersion) in real data"],
             ["Log-normal / heavy-tailed", "Revenue per user, session duration", "A few 'whales' dominate the mean; the median is often more stable"]]) +
        _topic_list([
            ("Distribution types", "Normal, binomial, Poisson, log-normal",
             ["Normal — sample means and proportions converge here via CLT even when raw data isn't normal, as long as n is large",
              "Binomial — binary per-user outcomes (converted / didn't), underlies proportion tests",
              "Poisson — count data (# purchases, # tickets); assumes variance = mean, often violated in practice",
              "Log-normal / heavy-tailed — revenue, session duration; a few whales dominate the mean"],
             "Interviewers care less about naming the distribution and more about whether you know it changes which test and which summary stat (mean vs. median) is trustworthy."),
            ("Central Limit Theorem", "Why t-tests work even on non-normal raw data",
             ["The sampling distribution of a mean/proportion tends toward normal as n grows, regardless of the underlying data's shape",
              "This is why a t-test on average revenue/user is defensible even though individual revenue is heavily right-skewed",
              "Convergence is slower for very skewed or heavy-tailed metrics — small samples can still misbehave"], None),
            ("Hypothesis testing fundamentals", "Null vs. alternative, Type I/II error",
             ["Null hypothesis (H0): no effect / no difference; alternative (H1): there is a difference",
              "Type I error (&alpha;): false positive — concluding there's an effect when there isn't",
              "Type II error (&beta;): false negative — missing a real effect",
              "One-tailed vs. two-tailed: two-tailed is the safer default unless you have a strong directional prior"], None),
            ("p-values and confidence intervals", "Correct interpretation, common misreads",
             ["p-value = probability of seeing data this extreme (or more) if the null were true — NOT the probability the null is true",
              "95% CI = if you repeated the experiment many times, 95% of such intervals would contain the true effect",
              "'CIs overlap' is not the same test as 'difference is not significant' — don't eyeball CI overlap as a substitute for the actual test",
              "Statistical significance &ne; practical/business significance — always check the effect size against a meaningful threshold"], None),
        ]))

    metrics = (
        p("The recurring interview move: name the metric's data type, then name the test and the failure mode if you used the wrong one.") +
        h3("Metric type &rarr; test to use") +
        table(["Metric type", "Example", "Test to use", "Why"],
            [["Continuous, roughly symmetric", "Avg. session count, page load time", "Two-sample t-test", "CLT makes the mean trustworthy; t-test directly compares averages"],
             ["Continuous, right-skewed / heavy-tailed", "Revenue per user, session duration", "Log-transform + t-test, Mann-Whitney U, or bootstrap CI", "Raw mean is unstable with outliers"],
             ["Binary / rate", "Conversion rate, CTR, signup rate", "Two-proportion z-test / chi-square", "Outcome is 0/1 per user; z-test compares two proportions directly"],
             ["Rare binary event", "Fraud rate, cancellation rate", "Fisher's exact test", "Normal approximation breaks down at very low counts/rates"],
             ["Count", "# purchases, # support tickets per user", "Poisson or negative binomial regression", "Handles non-negative discrete counts; negative binomial covers overdispersion"],
             ["Ratio (numerator & denominator vary)", "Revenue/session, clicks/impressions", "Delta method for variance, then z/t-test", "Naive variance ignores covariance between numerator and denominator"],
             ["Zero-inflated", "Revenue/user where most spend $0", "Two-part model — test conversion + revenue-given-conversion separately", "A single blended mean hides which part of the funnel moved"]]) +
        h3("t-test vs. z-test vs. Mann-Whitney U — explained simply") +
        table(["Test", "In plain English", "Use it when", "Skip it when"],
            [["t-test", "\"Is the average of Group A different from Group B, once we account for how noisy the data naturally is?\"", "Comparing means of a continuous metric between two groups", "Metric is binary/count, or data is heavily skewed with a small sample"],
             ["z-test (proportions)", "\"Is the percentage who converted in Group A different from Group B?\"", "Comparing two rates/proportions with a reasonably large sample", "Sample is very small or the event is very rare — use Fisher's exact test"],
             ["Mann-Whitney U", "\"Ignoring exact values, do users in Group B tend to rank higher than Group A?\"", "Continuous metric is heavily skewed / has extreme outliers and you don't trust the mean", "You need the size of the difference in real units — this only tells you rank/ordering"]]) +
        callout("info", "Rule of thumb",
            p("A t-test and a z-test both ask 'how different are the averages, given normal noise' — t-test for continuous numbers, z-test for percentages/rates. Mann-Whitney U asks a softer question — 'which group tends to score higher' — without needing the mean to be trustworthy.")) +
        _topic_list([
            ("Continuous metrics (revenue, time on page)", "t-test, but watch skew",
             ["Standard tool: two-sample t-test on the mean",
              "Right-skewed data (whales) makes the raw mean unstable and slows CLT convergence",
              "Fixes: log-transform, winsorize/cap top X% (pre-registered), trimmed mean, or bootstrap for the CI",
              "Mann-Whitney U as a non-parametric alternative when you don't trust the mean at all"], None),
            ("Rate / binary metrics (conversion, CTR)", "z-test for proportions, chi-square",
             ["Two-proportion z-test or chi-square test of independence",
              "Low base-rate events need much larger samples for the same power",
              "Fisher's exact test for very small samples or very rare events"], None),
            ("Count metrics (# purchases, # tickets)", "Poisson vs. negative binomial",
             ["Poisson assumes variance = mean — real-world counts are usually overdispersed",
              "Negative binomial regression handles overdispersion correctly",
              "For large volumes, treating counts as roughly continuous with a bootstrap CI is often good enough"], None),
            ("Ratio metrics (revenue/session, CTR)", "Delta method — naive variance is wrong",
             ["When both numerator and denominator vary per unit, the naive variance formula understates uncertainty",
              "The Delta method gives the correct standard error for a ratio of two random variables",
              "A common senior-level trip-up: candidates divide two means without adjusting the variance"], None),
            ("Zero-inflated metrics (revenue/user)", "Two-part model, not log-transform",
             ["Can't log-transform zeros directly — the 'did they convert at all' signal gets lost",
              "Two-part model: test (a) conversion rate as binary, and (b) revenue given conversion, separately",
              "Blending both questions into a single average masks which part actually moved"], None),
            ("Multi-modal / mixture distributions", "Aggregate mean can hide the real story",
             ["Metric behaves very differently across segments (power users vs. new users)",
              "An aggregate mean can show 'flat' while masking offsetting effects — Simpson's Paradox risk",
              "Segment before aggregating, or include segment as a covariate"], None),
            ("General-purpose tools", "Bootstrap, CUPED, rank-based tests",
             ["Bootstrap resampling — distribution-free CI when you don't trust parametric assumptions",
              "CUPED-style variance reduction — see the CUPED tab",
              "Rank-based / non-parametric tests when in doubt about the underlying shape"], None),
        ]))

    power = (
        p("The math and decision framework for sizing a test before it launches.") +
        h3("How sample size responds to each lever") +
        table(["Lever", "&uarr; Increase it &rarr; required sample size", "&darr; Decrease it &rarr; required sample size"],
            [["Alpha (&alpha;)", "Goes down — easier to hit 'significant', but more false positives", "Goes up — harder to hit significant, fewer false positives"],
             ["Power (1 &minus; &beta;)", "Goes up — need more data to reliably catch a real effect", "Goes down — accept a higher chance of missing a real effect"],
             ["MDE — min detectable effect", "Goes down — easier to detect a bigger effect", "Goes up sharply — sample scales as 1/MDE&sup2;, so halving MDE roughly quadruples sample size"],
             ["Metric variance", "Goes up — a noisier metric needs more data", "Goes down — e.g. via CUPED; less noise needs less data"],
             ["Baseline rate toward 50%", "Goes up — variance of a proportion peaks near p = 0.5", "Goes down — variance shrinks near 0% or 100%"]]) +
        h3("Powering the primary vs. secondary vs. guardrail metrics") +
        table(["Metric role", "How to power it", "How to read its result"],
            [["Primary", "Sized to ~80% power at its MDE — this normally sets N", "Standard two-sided test; this is the ship gate"],
             ["Secondary", "Often left underpowered on purpose", "Directional only — read effect size + CI; a null &ne; 'no effect', don't gate on it"],
             ["Guardrail", "Give it its own harm margin and power for THAT; usually already well-powered", "Non-inferiority — passes if the CI rules out a regression worse than the margin; often one-sided"]]) +
        callout("info", "Power is per-metric",
            p("One N gives different power to each metric depending on its variance and MDE. Size the test on the MAX required N across the primary and critical guardrails — if a guardrail needs more data than the primary, it sets your runtime.")) +
        h3("Unequal traffic splits — when to consider them") +
        table(["Scenario", "Why go unequal", "Typical split"],
            [["Risky or expensive change", "Minimize users exposed to something that might backfire", "90/10 or more extreme"],
             ["Gradual ramp-up", "Catch catastrophic bugs, SRM, or guardrail violations before full exposure", "1% &rarr; 10% &rarr; 50% over time"],
             ["Cost-constrained treatment", "Treatment calls an expensive service or uses more compute", "Skewed toward control, e.g. 80/20"],
             ["Known/stable baseline arm", "Control barely varies, so it needs less new data (Neyman allocation)", "Skewed toward the higher-variance arm"],
             ["Standard test, no constraint", "Maximizes statistical power for a fixed total sample size", "50/50 — the default"]]) +
        h3("Unequal traffic splits — what they cost you") +
        table(["Split", "Total sample size needed vs. 50/50, for the same power"],
            [["50/50", "1x — baseline, most efficient"], ["70/30", "~1.2x"], ["80/20", "~1.6x"], ["90/10", "~2.8x"], ["95/5", "~5.3x"]]) +
        h3("A/B/n and multivariate testing vs. a simple A/B test") +
        table(["", "Simple A/B", "A/B/n (3+ variants)", "Multivariate / factorial"],
            [["What's tested", "One change vs. control", "Several distinct variants vs. control", "Multiple factors changed simultaneously, testing combinations"],
             ["Traffic per arm", "50/50 — maximizes power", "~1/n traffic each, less powered per comparison", "Splits across all factor combinations — power per cell shrinks fast"],
             ["Multiple comparisons", "One comparison, no correction", "n&minus;1 comparisons — needs Bonferroni/FDR", "Main effects AND interactions — correction essential"],
             ["What you learn", "Does the change work?", "Which variant works best?", "Do A and B work, and do they interact?"],
             ["When to use", "Default — clean, well-powered", "Several genuine options to compare at once", "You suspect two changes interact"]]) +
        h3("Bayesian vs. Frequentist, side by side") +
        table(["", "Frequentist", "Bayesian"],
            [["Core question", "How unusual is this data if there's truly no effect?", "Given this data, what's the probability B beats A?"],
             ["Output", "p-value, confidence interval", "Posterior probability, credible interval"],
             ["Continuous monitoring", "Inflates false positives (peeking) unless sequential", "Naturally supports monitoring as data accumulates"],
             ["Requires a prior?", "No", "Yes — weakly informative or historical-data-based"],
             ["Stakeholder framing", "'5% chance of this pattern if no effect' — often misread", "'92% probability B is better than A' — maps to a decision"],
             ["Common use", "Pre-registered fixed-duration, regulatory contexts", "Live dashboards, early-stopping-friendly platforms"]]) +
        _topic_list([
            ("The core relationship: MDE, power, alpha, sample size", "See the sensitivity table above",
             ["Minimum Detectable Effect (MDE) — the smallest true effect you're willing to reliably detect",
              "Power (1 &minus; &beta;), typically 80% — probability of detecting a real effect if it exists",
              "Significance level (&alpha;), typically 5% — the false-positive rate you accept",
              "Higher-variance metrics need more sample for the same MDE — where CUPED pays off",
              "MDE is the strongest lever — sample size scales as 1/MDE&sup2;"], None),
            ("Powering secondary & guardrail metrics", "Power is per-metric — size N for the max",
             ["Power depends on each metric's OWN variance and MDE, so one N gives different power to every metric",
              "Secondary metrics: fine to leave underpowered — read directionally, never as a ship gate",
              "Guardrails flip the risk: the feared error is a missed regression, so you want power to CATCH harm",
              "Guardrails are usually high-traffic, low-variance, so often better-powered than the primary at the same N",
              "Give each guardrail a 'harm margin' and evaluate as non-inferiority: passes if the CI rules out a regression worse than the margin",
              "Test guardrails one-sided (only the harmful direction), sometimes at a lenient alpha",
              "Design-time fix: run the power calc for the primary AND each critical guardrail, then take the MAX required N"],
             "I size on the max required N across the primary and critical guardrails, not the primary alone. Guardrails I read as non-inferiority; secondaries are directional and I don't gate on them."),
            ("Pre-registered vs. post-hoc power", "Post-hoc power is a trap answer",
             ["Power should be calculated BEFORE the experiment, based on assumed effect size and variance",
              "Post-hoc power (after a non-significant result) is statistically circular — a common interview trap",
              "If a result is null, ask 'was this test adequately powered for a meaningful effect?' decided in advance"], None),
            ("Bayesian vs. Frequentist A/B testing", "Different interpretation, same data",
             ["Frequentist: 'if there were truly no effect, how likely is data this extreme?' — p-value + fixed threshold",
              "Bayesian: 'given this data, what's the probability B is better than A?' — posterior + credible interval that maps to a decision",
              "Bayesian supports continuous monitoring without the peeking penalty — why many platforms use it for live dashboards",
              "Bayesian requires a prior — a poorly chosen prior can bias early reads on low-traffic tests",
              "In practice: frequentist for pre-registered gates; Bayesian for live dashboards and early stopping"],
             "Bayesian for early monitoring and stakeholder communication because the output maps directly to a decision; frequentist when I need a pre-registered, audit-defensible gate."),
            ("Unequal traffic splits (e.g., 90/10)", "Trade efficiency for exposure control",
             ["50/50 is the most statistically efficient split for a fixed total sample size",
              "Recompute the sample-size/power calc using the ACTUAL allocation ratio, not 50/50",
              "Check SRM against the intended ratio (e.g., 90/10), not against 50/50",
              "Lean harder on CUPED/variance reduction to offset the efficiency cost",
              "If ramping allocation over time, be careful pooling data across differently-allocated periods"],
             "A 90/10 split needs roughly 2.8x the total traffic of a 50/50 split to detect the same effect size."),
            ("A/B/n and multivariate (factorial) testing", "More arms = smaller per-arm sample + more comparisons",
             ["Adding arms costs power multiplicatively — 2 to 4 arms roughly doubles the traffic needed",
              "Interaction effects are the unique value of a true factorial design",
              "Only run a full factorial when you have a real hypothesis that the factors interact",
              "Pre-register which comparisons matter so the multiple-comparisons correction isn't overly conservative",
              "Adaptive designs like multi-armed bandits reallocate traffic toward better arms in real time"],
             "Use a multivariate test only when you have a real hypothesis that two changes interact — otherwise two sequential simple tests are cheaper and easier to interpret."),
        ]))

    design = (
        p("The practical pitfalls of actually running a test — the highest-yield section for a Senior PA round.") +
        h3("Core assumptions behind A/B testing") +
        table(["Assumption", "What it means", "What breaks if it's violated"],
            [["SUTVA (no interference)", "One user's assignment doesn't affect another's outcome", "Network effects/marketplaces bias the estimate — treatment leaks into control"],
             ["Stable, correct randomization", "Every unit has a known, typically equal, probability of assignment", "SRM, selection bias, or confounded comparisons"],
             ["Independent observations", "Each user's outcome is independent of others', given assignment", "Underestimated variance / overstated significance when observations are clustered"],
             ["Stationarity over the window", "The treatment-outcome relationship doesn't change systematically over the test", "Novelty/primacy, seasonality, or a mid-test change distort the read"],
             ["Consistent treatment delivery", "Every treated unit actually receives the treatment", "Non-compliance (ad blockers, flag bugs) dilutes the effect toward zero"],
             ["Metric measurable in-window", "The outcome can be observed before the test ends", "Forced to rely on short-term proxies for slow effects"]]) +
        h3("Limitations — what A/B testing can't tell you") +
        table(["Limitation", "Why it's a limitation", "What to reach for instead"],
            [["Can't measure effects slower than the window", "LTV, retention, brand effects unfold over months", "Long-term holdouts, surrogate/leading-indicator metrics"],
             ["Can't test when randomization isn't feasible", "Pricing, policy rollouts, already-launched features", "Quasi-experimental — DiD, PSM/CEM, RD, Synthetic Control"],
             ["Can't isolate effects when users interact", "Marketplaces, social, referral loops", "Cluster-randomized designs (randomize by market/group)"],
             ["Tells you outcome, not mechanism", "A/B answers 'did it work,' not 'why'", "Secondary metrics, qualitative research, funnel/segment analysis"],
             ["Rare/tiny effects need huge samples", "Power for rare outcomes or tiny MDEs is expensive", "CUPED/variance reduction, proxy metrics, or a longer test"],
             ["A single test is one data point", "One result could be a false positive or fail to replicate", "Replication, holdouts, triangulating multiple methods"]]) +
        h3("Common experiment pitfalls at a glance") +
        table(["Pitfall", "What it looks like", "Detect / fix"],
            [["Sample Ratio Mismatch (SRM)", "Split doesn't match intended ratio (48/52 instead of 50/50)", "Chi-square goodness-of-fit; if detected, invalidate and fix before rerunning"],
             ["Peeking / optional stopping", "Checking daily, stopping as soon as it looks significant", "Pre-register a fixed duration/sample, or use a sequential/always-valid method"],
             ["Multiple comparisons", "Testing many metrics/segments inflates false positives", "Bonferroni/FDR correction, or limit to pre-declared metrics"],
             ["Novelty / primacy effect", "Big day-1 lift that fades (or grows)", "Plot the trend over time, not just the endpoint; consider running longer"],
             ["Randomization/analysis mismatch", "Randomized by user but analyzed by session", "Match the unit of randomization to the unit of analysis"],
             ["Skipped A/A test", "New platform or metric never sanity-checked", "Run an A/A test first — should show 'no difference' ~(1&minus;&alpha;) of the time"]]) +
        h3("Novelty effect — how to check for it") +
        table(["Detection method", "What it tells you"],
            [["Plot the daily (not cumulative) treatment effect", "Reveals whether the lift is shrinking, growing, or flat"],
             ["Exposure-time analysis (days since first exposure)", "Separates 'newness to the user' from calendar-time noise"],
             ["Segment by new vs. returning users", "Novelty is usually strongest in returning/engaged users"],
             ["Treatment &times; time-index interaction term", "A significant negative interaction is a formal signal the effect is decaying"],
             ["Small pilot with an extended tail", "Cheap early warning before committing full traffic"]]) +
        h3("Novelty effect — how to treat it") +
        table(["Treatment / mitigation", "Why it works"],
            [["Extend the test until the trend stabilizes", "Avoids basing a permanent decision on a temporary spike"],
             ["Base the decision on the later-window effect", "Better approximates long-run behavior once novelty wears off"],
             ["Use a rolling/windowed estimate", "Makes the decay pattern visible instead of averaging it away"],
             ["Run a long-term holdout after launch", "Confirms whether the effect persists once fully live"],
             ["Re-test on a fresh cohort after novelty fades", "Cross-checks whether the lift is about value vs. just newness"]]) +
        _topic_list([
            ("Assumptions and limitations of A/B testing", "See the two tables above",
             ["Assumptions: SUTVA, correct randomization, independent observations, stationarity, consistent delivery, in-window metric",
              "Limitations: can't measure slow effects, can't run without randomization, can't isolate with interaction, only outcome not mechanism, single result may be a false positive",
              "Knowing both lists cold is a strong senior signal"],
             "Structure the answer as assumptions (what must hold for validity) separately from limitations (what it fundamentally can't tell you even when valid)."),
            ("Sample Ratio Mismatch (SRM)", "Randomization bug detector",
             ["Check: does the actual split match the intended split? Test with chi-square goodness-of-fit",
              "SRM signals a bug in randomization, logging, or bot filtering — not a real effect",
              "If detected, the whole read is invalid — fix and rerun, don't 'adjust' a broken split"], None),
            ("A/A tests", "Sanity-check the pipeline before trusting it",
             ["Split into two identical arms with no treatment difference",
              "Should show no significant difference ~(1&minus;&alpha;) of the time",
              "Useful before trusting a new platform, metric definition, or randomization unit"], None),
            ("Multiple testing & peeking", "Dashboards inflate false positives",
             ["Multiple comparisons: many metrics/segments increases the chance something looks significant by chance",
              "Peeking: checking daily and stopping when significant inflates the true false-positive rate",
              "Fix: pre-register a fixed sample/duration, or use sequential testing (always-valid p-values)"], None),
            ("Novelty & primacy effects", "Don't trust the day-1 read",
             ["Users react to something new just because it's new — early lift can fade or take time to appear",
              "Detect: see the detection table above",
              "Treat: base the decision on the steady-state effect, not the day-1 spike",
              "If lift decays fast toward zero, ask whether the change delivers real ongoing value"],
             "Plot the daily effect, check if it's flattening, and if it's still decaying, extend the test or hold out a group post-launch rather than ship off a day-1 read."),
            ("Randomization unit & interference", "Match the analysis unit to the assignment unit",
             ["Randomize and analyze at the same unit — mismatches inflate false confidence",
              "SUTVA violations / network effects break standard independence assumptions",
              "Seasonality and day-of-week effects can masquerade as treatment effects in short tests"], None),
        ]))

    holdout = (
        p("A holdout is a measurement tool for something already shipped, not a ship/no-ship gate — the framing interviewers check for.") +
        h3("Holdout vs. standard A/B test") +
        table(["", "Standard A/B test", "Holdout"],
            [["Purpose", "Decide whether to ship a change", "Continuously measure the ongoing impact of something already shipped"],
             ["Duration", "Days to weeks — reach the pre-registered sample size", "Months to indefinite — capture long-run/compounding effects"],
             ["Group size", "Often 50/50 for max power", "Usually small (1–10%) since it runs long and is a standing opportunity cost"],
             ["Decision made?", "No — the test result IS the decision", "Yes — already shipped to everyone else; the holdout is a measurement instrument"],
             ["What it measures", "Immediate/short-term effect, sometimes distorted by novelty", "Steady-state, compounding, or decayed effect"],
             ["Statistical approach", "Fixed-duration test, pre-registered stopping rule", "Ongoing monitoring — re-analyzed periodically as a rolling comparison"]]) +
        h3("Evaluating a holdout — the 5-step cadence") +
        table(["Step", "What you do"],
            [["1", "Re-run the standard comparison (t-test / z-test / CUPED-adjusted) between holdout and exposed on each review cadence"],
             ["2", "Plot the effect as a trend over time, not a single number — watch for growth, stability, or decay"],
             ["3", "Re-validate randomization periodically — check the holdout's composition hasn't drifted from the exposed group"],
             ["4", "Adjust for seasonality by comparing like-for-like time windows or modeling it explicitly"],
             ["5", "Translate the current effect into a business-facing number ('what we'd lose per month if this were off for everyone')"]]) +
        _topic_list([
            ("What is a holdout?", "A long-running control group kept out of something already shipped",
             ["A group deliberately excluded from a feature already rolled out to everyone else, kept as a persistent control",
              "Used to continuously measure cumulative/long-term impact — not to decide whether to ship",
              "Common in marketing (keep 5% out of all sends) and platform features (rec-algorithm or pricing holdouts)"],
             "An A/B test decides whether to ship; a holdout measures the ongoing value of something already shipped, especially once effects compound."),
            ("When you need a holdout", "Ongoing investment, compounding effects",
             ["Prove ongoing value of a persistent program, not just a one-time ship decision",
              "The effect compounds or decays slowly over months — a 2-week A/B can't see it",
              "Leadership needs a standing answer to 'what if we turned this off?'",
              "Something shipped to 100% without a proper test and you want to retroactively measure it",
              "Finance needs an ongoing causal read on a program's value"], None),
            ("How to evaluate / test a holdout", "Re-run the comparison periodically",
             ["See the step-by-step table above",
              "The core statistical tools are the same as an A/B test — what changes is you re-run on a schedule"], None),
            ("How to size and design a holdout", "Small %, long duration, explicit sunset plan",
             ["Size trades power (bigger = tighter CIs) against opportunity cost — most are small (1–10%)",
              "Decide the review cadence upfront and pre-register what result ends the holdout",
              "Consider a rotating/refreshed holdout to avoid the same users feeling permanently disadvantaged",
              "Document an explicit sunset plan — holdouts have a real cost"], None),
            ("Pitfalls specific to holdouts", "Drift, seasonality, interference, fatigue",
             ["Population drift — differential churn makes the holdout non-representative over time",
              "Seasonality — December vs June comparisons differ; compare like-for-like windows",
              "Interference — ecosystem effects mean holdout users are indirectly affected (SUTVA violation)",
              "Holdout fatigue — stakeholders push to shrink/end holdouts once results look favorable",
              "Under-analysis risk — teams stop taking it seriously even though it's the only causal read left"], None),
        ]))

    cuped = (
        callout("info", "Why it comes up",
            p("CUPED is a strong differentiator — most PA candidates know power analysis but few can explain variance reduction. Even a clean two-sentence summary signals depth.")) +
        h3("CUPED — the 4 steps") +
        table(["Step", "What you do"],
            [["1", "Pick a covariate X measured BEFORE the experiment, correlated with outcome Y — usually Y's own pre-period value"],
             ["2", "Compute &theta; = Cov(Y, X) / Var(X) — a simple regression coefficient, from pooled or control-group data"],
             ["3", "Adjust every user's metric: Y_cuped = Y &minus; &theta;(X &minus; mean(X))"],
             ["4", "Run your normal test on Y_cuped instead of raw Y — same mean, smaller variance"]]) +
        _topic_list([
            ("Why CUPED", "Shrink variance without more traffic",
             ["Power is limited by metric variance — less variance means detecting smaller effects or faster significance",
              "Users who spent/converted more before the experiment tend to do so during it too, regardless of treatment",
              "CUPED strips that predictable variance out before testing"], None),
            ("How it works", "Adjust the metric with a pre-period covariate",
             ["See the step-by-step table above",
              "The covariate X must be measured before the experiment, so treatment can't have affected it"], None),
            ("Why it's unbiased", "Randomization keeps the means equal",
             ["Because assignment is random, E[X] is the same in treatment and control",
              "Subtracting &theta;(X &minus; mean(X)) shifts both arms equally, so the effect on the mean is unchanged",
              "Only the variance shrinks — you remove variation in Y explained by X, unrelated to treatment"], None),
            ("How much variance reduction to expect", "Roughly &rho;&sup2; of variance removed",
             ["Remaining variance is roughly (1 &minus; &rho;&sup2;) of the original, where &rho; is the correlation between X and Y",
              "A correlation of 0.5 &rarr; about 25% variance reduction &rarr; meaningfully shorter/more sensitive tests"], None),
            ("Practical gotchas", "New users, weak covariates, CUPAC",
             ["New users with no pre-period history need special handling — imputation or separate analysis",
              "Works best when the covariate reflects stable behavior (tenure, historical spend)",
              "CUPAC extension: use an ML model's prediction of Y from pre-experiment features as X"], None),
        ]))

    beyond = (
        p("Shows you know when true randomization isn't available and what to reach for instead — a breadth signal.") +
        h3("Quasi-experimental methods compared") +
        table(["Method", "Use when", "Key assumption", "Example"],
            [["Difference-in-Differences", "Feature/policy rolled out to one group without randomization", "Parallel trends — both groups would've moved the same way absent treatment", "Feature launched in one region only"],
             ["Propensity Score Matching (PSM)", "Observational data with a self-selected treated group", "All relevant confounders observed and included", "Users who opted into a feature vs. similar users who didn't"],
             ["Coarsened Exact Matching (CEM)", "Large control pool; want guaranteed balance without a propensity model", "No unmeasured confounders among the coarsened covariates", "Matching SMS buyers to lookalike non-buyers on 11 pre-purchase covariates"],
             ["Inverse Probability Weighting (IPW)", "Want to use ALL units instead of dropping unmatched ones", "Correct propensity model + positivity", "Weight opted-in users by 1/propensity to rebuild a pseudo-population"],
             ["Doubly Robust (AIPW)", "Want a safety net against getting one model wrong", "Only ONE of the two models needs to be correct", "Combine IPW with an outcome-regression model for a robust estimate"],
             ["Regression Discontinuity", "Treatment assigned by a threshold on a continuous variable", "Users just above/below the cutoff are otherwise identical", "Offer triggered above a spend tier"],
             ["Synthetic Control", "One treated unit, many untreated ones", "A weighted mix of untreated units can mimic the treated pre-trend", "Single market/city launch"],
             ["Causal Impact (BSTS)", "One treated time series, good control series exist", "Control series' relationship to treated stays stable across intervention", "Estimating lift from a workflow change using pre/post time series"],
             ["Instrumental Variables", "Unmeasured confounder + a valid instrument available", "Instrument affects outcome only through treatment", "Name-drop level for this interview"]]) +
        _topic_list([
            ("Difference-in-Differences (DiD)", "Compare the change over time, not the level",
             ["Used when a feature/policy rolled out to one group without randomization",
              "Effect = (Post &minus; Pre)treated &minus; (Post &minus; Pre)control",
              "Key assumption: parallel trends",
              "Common for geo/market-level rollouts"], None),
            ("Propensity Score Matching (PSM)", "Match self-selected treated users to similar controls",
             ["For observational data with a self-selected treated group",
              "Estimate each user's propensity from observable covariates",
              "Match treated to controls with similar scores, then compare outcomes",
              "Corrects for measurable selection bias — only on confounders you observed"], None),
            ("Coarsened Exact Matching (CEM)", "Guaranteed balance, no propensity model",
             ["Bins each covariate, then exact-matches within bin combinations — balance guaranteed by construction",
              "Sidesteps PSM's biggest risk: a misspecified propensity model",
              "Works best with a large control pool relative to the treated group",
              "Verify balance with SMDs and a Love plot; pair with a placebo test"],
             "CEM plus a placebo test and multi-estimator triangulation (PSM/IPW/doubly-robust all agreeing) is exactly the rigor a senior interview probes for."),
            ("Inverse Probability Weighting (IPW)", "Reweight instead of match — use every unit",
             ["Estimate each unit's propensity from observed covariates",
              "Weight each unit by 1/(probability of the treatment it got) — treated by 1/p, controls by 1/(1&minus;p)",
              "Rebuilds a pseudo-population where treatment looks random",
              "Keeps all units (no discarded controls) — more efficient with good overlap",
              "Tiny propensities get huge weights — trim/stabilize and check positivity"],
             "PSM matches and throws away non-matches; IPW keeps everyone and reweights them so groups look balanced."),
            ("Doubly Robust / AIPW", "Two models, only one has to be right",
             ["Combines a propensity model (like IPW) and an outcome-regression model",
              "Unbiased if EITHER model is correctly specified — two chances instead of one",
              "AIPW is the standard doubly-robust estimator",
              "Still can't fix unmeasured confounding"],
             "I'd report PSM, IPW, and a doubly-robust AIPW estimate together — if all three agree, I'm confident the effect isn't a modeling artifact."),
            ("Regression Discontinuity (RD)", "Compare just above vs. just below a cutoff",
             ["Treatment assigned by a threshold on a continuous variable",
              "Compare outcomes just above vs. just below — assumed near-identical except for treatment",
              "Good fit for 'eligibility rule' style product decisions"], None),
            ("Synthetic Control", "Build a weighted 'twin' from untreated units",
             ["For one treated unit with many untreated ones",
              "Construct a weighted combination that mimics the treated pre-treatment trend",
              "Use that synthetic twin as the counterfactual after treatment",
              "Common for market-level launches"], None),
            ("Causal Impact / BSTS", "Bayesian version of Synthetic Control",
             ["Builds a Bayesian structural time-series model using correlated control series, fit on the pre-period",
              "Projects forward to generate a counterfactual as a full posterior distribution",
              "Produces a credible interval on the cumulative causal effect",
              "Same core assumption as Synthetic Control"], None),
            ("Instrumental Variables (name-drop)", "Isolate causal effect via an unconfounded lever",
             ["Used when there's an unmeasured confounder but you have an instrument affecting treatment only",
              "Rarely expected in depth for a Senior PA interview — name it and give the one-sentence intuition"], None),
            ("Correlation vs. causation, confounders, regression to the mean", "Why quasi-experimental methods exist",
             ["Confounders — variables affecting both treatment assignment and outcome, creating spurious association",
              "Regression to the mean — extreme values move toward average on remeasurement, can look like an effect",
              "Knowing when experimentation isn't feasible, and which method fits, is itself the senior signal"], None),
        ]))

    eval_tab = (
        p("Basics of ML model evaluation — the metrics, and the higher-yield skill of knowing which one to check. The last topic ties back to A/B testing.") +
        h3("Confusion matrix — where every metric comes from") +
        table(["", "Predicted positive", "Predicted negative"],
            [["Actual positive", "True Positive (TP) — correct hit", "False Negative (FN) — a miss (Type II error)"],
             ["Actual negative", "False Positive (FP) — false alarm (Type I error)", "True Negative (TN) — correct pass"]]) +
        callout("info", "Overlap with A/B testing",
            p("A False Positive is a Type I error (false alarm), a False Negative is a Type II error (a miss). Precision cares about FP; recall cares about FN.")) +
        h3("Classification metrics at a glance") +
        table(["Metric", "Formula", "In plain English", "Optimize it when"],
            [["Accuracy", "(TP + TN) / all", "Of all predictions, how many were right?", "Classes balanced AND every error costs the same"],
             ["Precision", "TP / (TP + FP)", "Of everything flagged positive, how many really were?", "False positives are expensive — spam, fraud blocks"],
             ["Recall (TPR)", "TP / (TP + FN)", "Of all real positives, how many did we catch?", "Missing a positive is expensive — disease screening, churn"],
             ["F1 score", "2 &middot; (P &middot; R) / (P + R)", "Harmonic mean of precision & recall", "You care about FP and FN together and classes are imbalanced"],
             ["F&beta; score", "(1+&beta;&sup2;)&middot;P&middot;R / (&beta;&sup2;&middot;P + R)", "F1 but weighted — &beta;>1 favors recall", "One error type is worse but both still matter"],
             ["Specificity (TNR)", "TN / (TN + FP)", "Of all real negatives, how many did we clear?", "The cost of false alarms on the negative class matters"],
             ["ROC-AUC", "Area under TPR-vs-FPR curve", "Probability the model ranks a random positive above a random negative", "Comparing discrimination on roughly balanced classes"],
             ["PR-AUC", "Area under precision-recall curve", "Ranking quality focused on the rare positive class", "Highly imbalanced data where ROC-AUC looks deceptively high"],
             ["Log loss", "&minus;&Sigma; y&middot;log(p)", "Punishes confident-but-wrong predictions", "You need trustworthy probabilities, not just a label"],
             ["Brier score", "mean( (p &minus; y)&sup2; )", "MSE of predicted probabilities — calibration + accuracy", "Probabilities feed a downstream expected-value calc"]]) +
        h3("When to check what — pick the metric for the problem") +
        table(["Scenario / business goal", "Metric(s) to check", "Why"],
            [["Imbalanced classes, rare positive", "PR-AUC, F1, recall — NOT accuracy", "A model predicting 'all negative' scores 99% accuracy while catching zero positives"],
             ["False positives are expensive", "Precision", "Spam filter, fraud block, ad spend — each false flag has a real cost"],
             ["False negatives are expensive", "Recall", "Cancer screening, churn, fraud — a missed positive is the costly error"],
             ["Both errors matter, classes skewed", "F1 (or F&beta;)", "Single balanced score; F&beta; when one error type is worse"],
             ["Compare models threshold-free", "ROC-AUC", "Summarizes ranking across every cutoff"],
             ["Rank quality on a rare class", "PR-AUC", "ROC-AUC flatters imbalanced data; PR-AUC is the honest read"],
             ["Probabilities drive a decision", "Log loss + calibration (Brier)", "You need the probability itself to be right, not just the rank"],
             ["Balanced classes, equal error cost", "Accuracy (with F1 as a sanity check)", "Simple and interpretable — only when justified"],
             ["Continuous / regression target", "RMSE, MAE, R&sup2;, MAPE", "See the regression-metrics table below"]]) +
        h3("Regression metrics (continuous target)") +
        table(["Metric", "What it measures", "Use it when"],
            [["MAE", "Mean absolute error — average miss in the target's own units", "You want a robust, interpretable error"],
             ["RMSE", "Root mean squared error — penalizes large misses more", "Big individual errors are disproportionately bad"],
             ["R&sup2;", "Share of variance explained vs. predicting the mean", "Communicating goodness-of-fit; comparing against a naive baseline"],
             ["MAPE", "Mean absolute percentage error", "Errors are naturally relative (demand/revenue) — but blows up near zero"]]) +
        _topic_list([
            ("Precision vs. recall trade-off", "You rarely max both at once",
             ["Lowering the threshold flags more positives — recall up, precision usually down",
              "The PR curve shows the full trade-off; F1/F&beta; collapses it to one point",
              "Never say 'improve accuracy' on an imbalanced problem — name the error you care about"],
             "If asked 'precision or recall?', answer with the business cost: which is worse here — a false alarm or a miss?"),
            ("Choosing the classification threshold", "0.5 is an arbitrary default",
             ["The 0.5 cutoff is a convention — tune it to the business objective",
              "Set it to hit a target precision/recall, or maximize expected value with a cost matrix",
              "Calibrate first if thresholding on probabilities"], None),
            ("Why accuracy lies on imbalanced data", "The base-rate trap",
             ["If 1% churn, predicting 'no churn' for everyone is 99% accurate and useless",
              "Accuracy hides the errors that matter when the positive class is rare",
              "The single most common evaluation mistake interviewers probe for"], None),
            ("ROC-AUC vs. PR-AUC", "Which curve to trust on imbalance",
             ["ROC-AUC plots TPR vs. FPR — great for balanced problems",
              "On heavy imbalance ROC-AUC can look excellent because true negatives are easy — PR-AUC exposes weak positive-class performance",
              "Rare positive class &rarr; lead with PR-AUC; balanced &rarr; ROC-AUC is fine"], None),
            ("Calibration — are the probabilities honest?", "Good ranking &ne; good probabilities",
             ["A model can rank perfectly (high AUC) yet output systematically too-high/low probabilities",
              "Check with a reliability diagram and the Brier score",
              "Fix with Platt scaling or isotonic regression — matters when probabilities feed a decision"], None),
            ("Offline metric vs. online outcome — the A/B tie-in", "A better AUC doesn't guarantee business lift",
             ["Offline metrics measure prediction quality on historical data; they don't prove business impact",
              "A model with higher offline AUC can lose in production if it doesn't change behavior",
              "Validate offline, then confirm impact with an online A/B test on the business metric"],
             "Offline metrics get us a candidate model; the A/B test is what earns the ship decision."),
            ("Validation done right — no leakage", "Train / validation / test, and time",
             ["Tune on validation, report the final number once on a held-out test set",
              "For time-dependent data, use a temporal split (train on past, test on future), not random k-fold",
              "Watch for target leakage — features that secretly encode the outcome"], None),
        ]))

    cases = (
        p("Before you can interpret mixed results, you have to choose the right metrics — product judgment for what to measure, statistical judgment for whether it's testable.") +
        h3("Choosing metric roles — product and statistical criteria") +
        table(["Metric role", "Product lens — why pick it", "Statistical lens — can you test it"],
            [[b("Primary"), "Maps 1:1 to the hypothesis; pick exactly one — multiple 'primary' metrics is a multiple-testing problem",
              "Check baseline variance; confirm the effect is detectable given traffic; favor CUPED-able metrics"],
             [b("Secondary"), "Explains the mechanism behind the primary; map to distinct steps of the mechanism",
              "Fine to be underpowered — directional signal, not a gate; still check its distribution"],
             [b("Guardrail"), "Protects what the business won't trade away — latency, opt-out, errors, trust & safety; chosen before results",
              "Often one-sided, sometimes stricter alpha; needs low natural variance to catch small regressions"]]) +
        callout("info", "Interview-ready summary",
            p("Primary is the one metric tied to your hypothesis with enough sensitivity to detect an effect; secondaries explain why it moved and can be underpowered; guardrails are picked independent of the hypothesis, tested one-sided, and need low variance.")) +
        h3("Reading mixed results across the three roles") +
        table(["Primary", "Secondary", "Guardrail", "Read / recommended action"],
            [["Up (sig.)", "Up (sig.)", "Flat", "Clean win — ship"],
             ["Up (sig.)", "Down (sig.)", "Flat", "Real trade-off: quantify both in $, check if the decline was expected, decide on net value"],
             ["Up (sig.)", "Flat / not sig.", "Flat", "Ship, but don't overclaim the secondary as validated — likely just underpowered"],
             ["Not sig.", "Up (sig.)", "Flat", "Don't ship on secondary alone; treat as a leading indicator, check if primary was underpowered"],
             ["Up (sig.)", "Flat", "Down (sig.)", "No-ship (usually) — guardrails are near hard constraints; investigate root cause"],
             ["Not sig.", "Flat", "Down (sig.)", "Clear no-ship — no upside to offset the guardrail cost"],
             ["'Significant' but tiny lift", "&mdash;", "&mdash;", "Statistically significant &ne; practically significant — check against your MDE / business threshold"],
             ["Up (sig.) in aggregate", "&mdash;", "&mdash;", "Check segments before shipping — could be Simpson's Paradox"],
             ["Big early lift, fades", "&mdash;", "&mdash;", "Novelty/primacy effect — look at the trend line, not the day-1 read"],
             ["Aggregate flat + SRM detected", "&mdash;", "&mdash;", "Invalidate the whole read — fix randomization bug, rerun"],
             ["Up (sig.), wide CI near zero", "&mdash;", "&mdash;", "Fragile positive — extend the test or run a confirmatory follow-up"]]))

    interview_qs = [
        ("\"The result isn't significant but the number looks big — what's your read?\"", "Underpowered vs. truly no effect",
         ["Check the confidence interval width, not just the point estimate — a wide CI suggests underpowered",
          "Compare observed sample size to the pre-registered power calculation",
          "Consider whether the effect size is even above the pre-set MDE"]),
        ("\"How would you size a test for a rare/high-variance metric?\"", "Power analysis + variance reduction",
         ["Walk through MDE/power/alpha/sample-size — rare events and high variance both push required sample up sharply",
          "Mention CUPED or covariate-adjustment to reduce required sample without more traffic",
          "Consider a proxy leading-indicator metric for an earlier read"]),
        ("\"You detect SRM mid-experiment — what do you do?\"", "Invalidate, diagnose, fix, rerun",
         ["An SRM invalidates the current read regardless of the treatment effect",
          "Investigate: bot filtering, logging bugs, redirect issues, asymmetric exclusion criteria",
          "Fix the root cause and rerun — don't reweight or 'correct' the existing data"]),
        ("\"PM wants to ship after 2 days because it looks great — what do you say?\"", "Peeking risk + novelty effect",
         ["Stopping early on a favorable look inflates the false-positive rate (peeking)",
          "Early lift often isn't representative of steady-state behavior (novelty)",
          "Propose honoring the pre-registered duration or using a sequential-testing method"]),
        ("\"Design an experiment end-to-end for [some product change]\"", "The structured walkthrough",
         ["Hypothesis: what change, what mechanism, what behavior should move",
          "Metric choice: primary (decision), secondary (story), guardrails (constraints)",
          "Design: randomization unit, MDE, required sample/duration, segments",
          "Analysis plan: which test per metric type, pre-registered stopping rule, multiple-comparisons handling",
          "Pitfalls to flag: SRM checks, novelty effects, guardrail trade-offs, Simpson's Paradox"]),
    ]
    interview_html = p("Common question shapes for this round — practice a crisp, structured answer for each rather than improvising live.")
    for title, summary, bullets in interview_qs:
        interview_html += card(title, ul(bullets), pill=summary)

    body = tabs("abt",
        [("foundations", "Foundations"), ("metrics", "Metrics & Distributions"), ("power", "Power Analysis"),
         ("design", "Experiment Design"), ("holdout", "Holdouts"), ("cuped", "CUPED"), ("beyond", "Beyond A/B"),
         ("eval", "Model Evaluation"), ("cases", "Decision Cases"), ("interview", "Interview Patterns")],
        [("foundations", foundations), ("metrics", metrics), ("power", power), ("design", design),
         ("holdout", holdout), ("cuped", cuped), ("beyond", beyond), ("eval", eval_tab),
         ("cases", cases), ("interview", interview_html)])
    return html_page(
        "A/B Testing Stats — Senior Product Analyst Prep",
        "Applied depth, not stats-analyst depth: correct intuition, spotting pitfalls, and translating results into ship/no-ship calls.",
        body)


# ─────────────────────────────────────────────────────────────────────────────
# 14. BINANCE.US — SENIOR PRODUCT ANALYST PREP
# ─────────────────────────────────────────────────────────────────────────────

def make_binance_us():
    lifecycle = ["Register", "KYC / verify", "Fund / deposit", "First trade", "Repeat / active", "Earn / stake", "Withdraw"]

    # --- Concepts ---
    concepts = (
        h2("The whole product in one breath") +
        p("Two personas — " + b("beginners") + " vs " + b("active traders") + ". Four things users do, three ways the company makes money.") +
        table(["Users can…", "Product", "Concrete example"],
            [[b("Buy / sell"), "Instant Buy", "Tap \"Buy $100 of Bitcoin\" — done in seconds, no order book."],
             [b("Trade"), "Advanced Trade", "Place a limit order to buy 0.1 BTC only if the price drops to $100,000."],
             [b("Swap"), "Convert", "Turn $500 of ETH directly into SOL in one step."],
             [b("Earn interest"), "Staking", "Lock up your ETH and earn ~4% a year in rewards."]]) +
        callout("info", "How Binance.US makes money — 3 ways",
            p(b("Trading fees") + " — a 0.02% taker fee on a $1,000 Advanced Trade = $0.20.") +
            p(b("Spread on Instant Buy") + " — you buy at a price slightly above market; that small markup is the margin.") +
            p(b("Staking service fee") + " — Binance keeps ~10–40% of the staking rewards you earn.")) +
        h2("Core crypto vocabulary") +
        table(["Term", "Plain-English meaning", "Example", "Why an analyst cares"],
            [[b("Maker order"), "A limit order that rests on the book instead of filling instantly — you ADD liquidity.", "Post \"buy BTC at $99k\" while it trades at $100k; it waits on the book until price falls.", "Lowest fee (0% at Binance.US). Maker/taker mix = liquidity + revenue health."],
             [b("Taker order"), "An order that fills immediately against the book — you REMOVE liquidity.", "Hit \"buy now\" at market and instantly match the best sell order on the book.", "Higher fee (~0.01–0.02%). Retail tends to be taker-heavy."],
             [b("Spread"), "The built-in margin on Instant Buy / Convert (no maker/taker there).", "Instant Buy shows BTC at $100,200 to buy vs $99,800 to sell — that ~$400 gap is the spread.", "The retail revenue lever — different economics from Advanced Trade."],
             [b("Staking"), "Lock Proof-of-Stake coins (ETH, SOL…) to earn network rewards. Like a savings account for crypto.", "Stake 10 SOL at ~7%/yr &rarr; accrue ~0.7 SOL over a year, minus Binance's fee.", "Engagement + retention + Earn revenue. Locked assets = stickier users."],
             [b("Order types"), "Market (fill now), Limit (fill at a set price), Stop-limit / OCO (conditional).", "A stop-limit: \"sell my ETH if it falls to $3,000\" to cap a loss automatically.", "Advanced-trader feature depth; adoption signals a serious user."],
             [b("AUC"), "Assets Under Custody — total $ value of everything users hold on the platform.", "1M users holding $5B of crypto &rarr; AUC = $5B.", "Scale + trust metric, but it moves with crypto price, not just behavior."]]) +
        h2("Product surfaces & personas") +
        mini_grid([
            ("Instant Buy (OCBS)", "Home-screen one-tap buy/sell. Priced with a spread. Persona: beginner. Simple, less price control."),
            ("Advanced Trade (Spot)", "Order book, charts, limit/market/stop orders, APIs. Maker/taker fees. Persona: active trader. Where volume & fee revenue live."),
            ("Convert", "Swap crypto&harr;crypto or crypto&harr;USD. Spread-based. Low-friction way to move between assets."),
            ("Earn / Staking", "Earn rewards on 25+ assets (+ Boost). Revenue = service fee on rewards. A retention & cross-sell surface."),
        ], cols=2) +
        callout("warning", "Regulatory frame — say this once, early",
            p("Binance.US = BAM, a separate U.S. entity (not global Binance). Licensed & compliance-first. Operates in " +
              b("45 states — not NY, TX, HI, VT") + ". That means state-level geo rollouts are a natural experiment tool, "
              "and KYC / risk disclosures are mandatory constraints, not optional friction."))
    )

    # --- Metrics & Stickiness ---
    metrics = (
        h2("The lifecycle you own") +
        chip_flow(lifecycle) +
        caption("Every metric below hangs off one of these stages. When asked to define or improve a metric, name the stage it lives in first.") +
        h2("Key metric definitions") +
        table(["Metric", "Definition", "Why it matters", "Watch-out"],
            [[b("KYC completion rate"), "% of sign-ups who pass identity verification.", "Biggest single drop-off; gates everything downstream.", "Much of it is compliance-mandated — improve the UX, not the requirement."],
             [b("Funded-account rate"), "% of verified users who make a first deposit.", "Top of the money funnel — nothing happens until funded.", "Split by method (ACH/card/wire); funding failures masquerade as intent drops."],
             [b("Time-to-first-trade"), "Median time from sign-up (or funding) to first trade.", "Captures intent before it cools.", "Heavy-tailed — use median, not mean."],
             [b("Activation rate"), "% of funded users who place a first trade.", "The 'aha' conversion.", "Beginners vs traders differ hugely — always segment by persona."],
             [b("Trading DAU/MAU"), "Daily &divide; monthly active traders (stickiness proxy).", "Habit strength — do people come back?", "'Active' must be a value action (a trade), not a login or price-check."],
             [b("Trading volume"), "$ notional traded.", "Direct driver of fee revenue.", "Whale-concentrated — one large trader can swing the aggregate."],
             [b("ARPU"), "Revenue per user (fees + spread + staking fee).", "Core monetization metric.", "Split by persona: spread-heavy retail vs fee-heavy traders."],
             [b("Net deposits"), "Deposits &minus; withdrawals.", "Real-money momentum & trust signal.", "A withdrawal &ne; churn (users self-custody to cold wallets)."],
             [b("Retention (30/90d)"), "% still active/funded at day N.", "Durable value, not just acquisition.", "Confounded by market regime — anchor to a price baseline."],
             [b("Staking participation"), "% of holders with staked assets.", "Engagement + Earn revenue; locks assets in.", "Rising staking can suppress trading volume — read them together."]]) +
        card("Deep dive: Stickiness (they will ask this)",
            p(b("Definition.") + " Stickiness = how habitual usage is. Classic measure is " + b("DAU/MAU") + ": if it's 0.5, the average monthly user shows up ~15 of 30 days.") +
            p(b("Crypto nuance.") + " Define 'active' as a " + b("value action") + " — placed a trade, deposited, or manages staked assets — not just opening the app to watch price. A price-checker isn't sticky in a way that makes money.") +
            mini_grid([
                ("Engagement", "Did they interact at all? (opens, sessions) — broadest, weakest."),
                ("Stickiness", "Do they come back habitually? (DAU/MAU, days-traded/month)."),
                ("Retention", "Are they still here at day N? (30/90-day survival)."),
            ], cols=3) +
            callout("danger", "How it gets gamed",
                p("Counting logins or price-checks as 'active' inflates DAU/MAU. A push notification can spike DAU without creating any real habit. Tie stickiness to trades, and always read it against the market regime — trading is bursty and swings with volatility."))) +
        callout("success", "Senior framing line",
            p("For any metric movement, separate " + b("market-driven") + " change (expected — don't over-react) from " +
              b("product-driven") + " change (fixable — act). The response is completely different."))
    )

    # --- A/B Experiments ---
    experiments_data = [
        ("Redesign the KYC / identity-verification flow to lift completion", "KYC", "Low", "Low",
         "If we simplify verification (fewer steps, clearer error messaging, better doc-upload UX), then KYC completion rate rises, because much of the drop-off is confusion/friction — not the legal requirement itself.",
         "User-level, assigned at KYC entry (one-time event, no contamination).",
         "KYC completion rate within N days of starting verification.",
         "Step-level drop-off, time-to-verify, downstream funded-account rate and first-trade rate.",
         "Fraud/AML approval quality (do NOT let bad actors through), manual-review queue volume, compliance rejection rate, support tickets.",
         ["Compliance-bound: the variant must still meet the legal requirement — get Compliance sign-off pre-launch.",
          "Approval quality is the real guardrail — a completion 'lift' that raises fraud is a loss, not a win.",
          "Some drop-off is document availability, not UX — you can't fix that portion.",
          "Verification can take days (manual review) → widen the conversion window.",
          "Novelty: Low (one-time flow). Market sensitivity: Low for KYC itself."],
         "Ship only if completion is up AND approval-quality/fraud is flat AND downstream funding isn't degraded. A cleaner funnel that admits worse accounts fails."),
        ("Add a 'fund your account' nudge right after KYC to lift funded-account rate", "Deposit", "Low", "Medium",
         "If we show a funding screen with method options (ACH/card/wire) immediately after verification, then first-deposit rate rises, because intent is highest right after a user finishes KYC.",
         "User-level, assigned at KYC completion.",
         "First-deposit rate within 7 days.",
         "Deposit sub-funnel (method selected → initiated → succeeded), time-to-first-deposit, first-trade rate, median deposit amount.",
         "Funding success rate (ACH failures), chargeback/fraud rate, withdrawal-within-7-days, support tickets.",
         ["Funding reliability confounds intent: separate 'chose to deposit' from 'deposit succeeded'.",
          "Deposit amounts are heavy-tailed → use a binary conversion primary + median (winsorized) amount, not mean $.",
          "Market sensitivity: Medium — a rally inflates deposits in BOTH arms; block/stratify.",
          "Novelty: Low (one-time onboarding moment)."],
         "Ship if deposit rate is up, funding success holds, and there's no offsetting withdrawal spike."),
        ("Guided first-trade prompt at end of onboarding to lift activation", "First trade", "High", "High",
         "If we surface a guided first-trade / Instant-Buy prompt right after funding, then first-trade rate rises, because we capture buying intent at its peak (many first trades happen same-day as funding).",
         "User-level, assigned at funding completion.",
         "First-trade rate within 7 days of funding.",
         "Time-to-first-trade, week-1 trade count, repeat-trade rate, Instant Buy vs Advanced Trade split, 14-day ARPU.",
         "Buyer's-remorse signal (immediate sell/withdraw), trade reversals, core onboarding / homepage health, support volume.",
         ["Novelty: HIGH — a new prompt gets clicks just for being new. Plot the daily/weekly effect and watch for decay.",
          "Market sensitivity: HIGH — first trades are driven by price excitement; stratify by regime, run across bull and flat/bear windows.",
          "A volume lift can pull in less-engaged users — treat that as a real quality tradeoff, not a pure win."],
         "Don't call it on week-1 data. Require the lift to persist into week 2+ (novelty gone) and to hold outside a pure bull run before shipping."),
        ("Staking cross-sell banner to holders of eligible assets", "Earn", "Medium", "High",
         "If we prompt holders of eligible PoS assets to stake, then staking participation rises, because idle holdings are latent Earn demand.",
         "User-level among holders of &ge;1 eligible asset.",
         "Staking-enrollment rate.",
         "Staked $ amount, Earn revenue per user, number of assets staked.",
         "Trading volume (staking LOCKS assets — watch cannibalization), withdrawal rate, net deposits, support tickets.",
         ["Cannibalization tradeoff: staking can reduce trading (locked assets) → judge on NET revenue (Earn + trading).",
          "Market sensitivity: HIGH but inverted — users stake more in bear markets and trade more in bull markets; stratify.",
          "Whale skew: a few large holders dominate staked $ → report enrollment rate + median, cap the dollar metric.",
          "Novelty: Medium."],
         "Ship if net revenue (Earn + trading combined) is up and withdrawals don't spike — not just because enrollment rose."),
        ("Reduce taker fees for a segment (pricing experiment)", "Repeat / active", "High", "High",
         "If we lower taker fees for a segment, then trading volume rises enough to offset the lower rate, because lower cost drives more and larger trades (fee elasticity).",
         "Prefer geo/state-level or time-based rollout over per-user (fairness/optics). Verify balance with an SRM check.",
         "Net trading-fee revenue per user (volume × rate) — not volume alone.",
         "Trades per user, volume per user, active-trader rate, maker/taker mix.",
         "Total revenue (don't buy volume at a loss), wash-trading / fee-gaming abuse, whale exploitation.",
         ["Whale-dominated: a handful of traders can make the result look great or terrible — segment whales out and cap/winsorize.",
          "Novelty: HIGH — a promo spikes then reverts; run long and check post-promo retention, not just in-promo volume.",
          "Market sensitivity: HIGH — regime drives volume far more than fees; keep arms concurrent and use diff-in-diff / CUPED.",
          "Fee elasticity is the real question — a volume lift that lowers net revenue is a loss."],
         "Ship only if NET revenue is positive after the novelty spike decays and after controlling for regime — and only if it isn't a whale artifact."),
        ("Launch Recurring Buy (DCA) to lift retention", "Repeat / active", "Low", "Medium",
         "If we let users schedule recurring buys, then 30/90-day retention and net deposits rise, because automated commitment builds habit independent of price.",
         "User-level randomized ACCESS to the feature — never opt-in vs non-opt-in (opt-in users self-select as higher-intent).",
         "30-day retention (leading indicator: recurring-buy setup rate).",
         "Net deposits, deposit frequency, days-active/stickiness, churn.",
         "Withdrawal rate, failed scheduled charges (funding reliability), cancellation rate, support tickets.",
         ["Long-horizon primary (retention) → needs a long runtime; don't read it early.",
          "Market sensitivity: Medium-High — bear markets drive churn regardless of feature; run across regimes or use a long holdout + CUPED.",
          "This feature is deliberately novelty- and volatility-resistant (that's the point) — a good story to make explicitly.",
          "Selection bias is the classic trap — measure via randomized access, not by comparing adopters to non-adopters."],
         "Ship on a durable retention lift that holds across a market regime — not on setup-rate alone."),
    ]
    exp_read = (
        h3("Novelty effect") + pill_row(["time-based decay"]) +
        p("A new UI element gets extra clicks just for being new; the effect fades. " + b("Detect:") + " plot the treatment effect by day/week — if it decays toward zero after 1–2 weeks, it's novelty. Compare new users vs returning users. " + b("Decide:") + " never call a winner on week-1 data; require the effect to persist into the steady-state window.") +
        h3("Market regime (bull / bear)") + pill_row(["the master confounder"]) +
        p("Crypto price swings drive deposits, trading, and retention more than any feature — a lift during a rally may be the market, not you. " + b("Design:") + " keep arms concurrent, block/stratify so both arms see the same market, run across bull and bear windows. " + b("Detect:") + " interact treatment &times; regime/volatility. " + b("Decide:") + " trust effects that are concurrent and consistent across regimes; use CUPED to strip market-driven baseline variance.") +
        callout("neutral", "Also always",
            p("Run an SRM (chi-square) check before trusting any result, correct for peeking / multiple looks, and use a binary or winsorized primary when revenue is whale-dominated.")))
    experiments = (
        callout("info", "How to use this",
            p("Each card is an interview prompt. Structure every spoken answer as: clarify &rarr; hypothesis &rarr; randomization &rarr; primary / secondary / guardrails &rarr; sizing &rarr; the two big caveats (novelty + market regime) &rarr; decision rule.")) +
        collapsible("Read first: the two caveats they always probe", exp_read) +
        h2("Experiment prompts"))
    for q, stage, novelty, market, hyp, rand, prim, sec, guard, gotchas, dec in experiments_data:
        inner = (pill_row([f"Novelty risk: {novelty}", f"Market sensitivity: {market}"]) +
                 field("Hypothesis", hyp) + field("Randomization unit", rand) +
                 grid3(field("Primary", prim), field("Secondary", sec), field("Guardrails", guard)) +
                 field("Gotchas & caveats", "") + ul(gotchas) +
                 callout("success", "Decision rule", p(dec)))
        experiments += collapsible(f"{q} <span class='pill neutral'>{stage}</span>", inner)

    # --- Diagnose a Decline ---
    diagnose = (
        callout("info", "Prompt",
            p("\"Trading activity dropped 12% week-over-week. Walk me through your diagnosis.\" This is your funnel-drop 'fire' story as a live framework.")) +
        collapsible("Open with this: the mental model that sets the tone",
            p("Say this before you touch a single hypothesis — it's a 'verbal table of contents' that tells the interviewer you're structured. Four filters, cheap/boring &rarr; expensive/exotic (Occam's razor for metrics):") +
            mini_grid([
                ("1. Is it real?", "Rule out a data/instrumentation issue before believing the number."),
                ("2. Who vs. what?", "Fewer people doing it, or the same people doing less of it?"),
                ("3. Market vs. product?", "Whole space is down (expected) vs. something we broke (fixable)."),
                ("4. Localize", "Only now: which segment/step explains most of the drop."),
            ], cols=4) +
            field("Opening script (first ~20 seconds)",
                "\"Before I dive into hypotheses, let me lay out how I'd approach any metric decline: first I'd confirm the number is real — not a data or instrumentation issue. Then whether the drop is from fewer people or the same people doing less. Then I'd separate market-driven causes — the whole space is down, expected — from product-driven causes we can actually fix. Only then would I drill into which specific segment explains the drop. Let me start with a couple of clarifying questions...\"") +
            callout("success", "If you blank, anchor on this",
                p(b("\"Real, then who-vs-what, then market-vs-product, then localize.\"") + " Four words, then execute the 5-step process below."))) +
        h2("The 5-step framework") +
        steps_list([
            ("1", "Scope the drop", "Quantify it: how big, since when, and which exact metric? 'Trades' down could mean fewer traders, fewer trades per trader, or lower volume — each is a different problem."),
            ("2", "Segment", "Slice by persona (Instant Buy vs Advanced), new vs existing, state/geo, asset/pair, acquisition channel, platform, and whale vs retail."),
            ("3", "Rule out", "Walk the suspect checklist below out loud — eliminate the boring/expected causes before chasing a product bug."),
            ("4", "Isolate", "Find the one segment or funnel step that explains most of the drop. Confirm the size adds up to the top-line move."),
            ("5", "Recommend", "Tie the finding to a decision and an owner: monitor, fix, or escalate. State the 'so what' a PM can act on today."),
        ]) +
        h2("Rule-out checklist") +
        table(["Suspect", "How to check", "Binance-specific angle"],
            [[b("Market regime"), "Compare against BTC/ETH price + total market volume in the window.", "If the whole market is flat/down, the drop is expected — monitor, don't panic."],
             [b("Mix shift"), "Did a marketing push change the new-user blend?", "More low-intent Instant-Buy users can drag averages without anything breaking."],
             [b("Funding friction"), "Deposit/ACH/wire success rate; 'insufficient balance' errors.", "Very live at Binance.US (they cut funding failures 34%) — blocked deposits kill trades."],
             [b("Product / fee change"), "Any release, UI, or fee change shipped in the window?", "Cross-check the changelog and running experiments."],
             [b("Asset availability"), "Was a popular pair delisted or restricted?", "Fewer tradable assets = fewer trades, concentrated in specific users."],
             [b("Data / instrumentation"), "Window incompleteness, pipeline break, event tracking gap.", "Confirm the event schema still fires before trusting the number."],
             [b("Whale drop-off"), "Is volume down but trader count flat?", "A few large traders leaving can swing aggregate volume — segment them out."],
             [b("Trust / security event"), "Withdrawal spike, outage, cancel-only mode, negative news.", "Signals fear-driven behavior, not a funnel bug — different response entirely."]]) +
        callout("success", "How to close the answer",
            p("\"I'd first establish whether this is " + b("market-driven") + " — in which case we monitor and set expectations — or " + b("product/funnel-driven") + ", in which case I isolate the broken segment and hand product a specific fix with an owner and expected impact.\""))
    )

    # --- Feature Areas ---
    feature_areas = [
        ("Instant Buy (fiat buy/sell)",
         "The simple, one-tap way to buy or sell crypto with USD — no order book, no chart-reading. The beginner surface, priced with a spread.",
         [("Fiat buy/sell conversion rate", "% of attempted USD-to-crypto purchases that complete successfully."),
          ("Funded-account rate", "% of verified users who make a first purchase/deposit."),
          ("Repeat-purchase rate", "% of buyers who come back and buy again within 30 days."),
          ("Spread revenue", "The markup earned on each buy/sell — the main way this surface makes money.")]),
        ("Advanced Trade (Spot trading)",
         "The order-book trading screen with charts and order types for active traders. Where trading volume and fee revenue live.",
         [("Trading volume", "Total $ value of everything bought/sold in a period."),
          ("Active traders", "Unique users who placed at least one trade in the period."),
          ("Trades per active trader", "How often the typical trader trades — a habit/frequency signal."),
          ("Take rate", "Trading-fee revenue &divide; volume — how much is earned per dollar traded."),
          ("Maker/taker mix", "Share of volume from resting orders vs instant-fill orders — a liquidity health signal.")]),
        ("Convert",
         "A simple way to swap one crypto for another (or for USD) in one step, without touching the order book. Spread-based, like Instant Buy.",
         [("Convert completion rate", "% of attempted conversions that go through successfully."),
          ("Convert volume", "Total $ value swapped through Convert in a period."),
          ("Convert-to-hold ratio", "Do users convert and then hold the new asset, or immediately sell/withdraw it?")]),
        ("Earn / Staking",
         "Ways to earn passive income just for holding crypto — lock up a coin and get paid rewards over time, like interest on a savings account.",
         [("Staking participation rate", "% of eligible holders who have staked at least some balance."),
          ("Assets in Earn (AUM)", "Total $ value of crypto currently staked/earning yield."),
          ("Earn revenue", "The service fee kept from the staking rewards paid out."),
          ("Staker retention", "Do staked users stick around longer than non-stakers at 30/90 days?")]),
        ("Wallet & portfolio",
         "Where your crypto actually lives on the platform — custody, moving it in/out via deposits and withdrawals, and seeing everything you own in one view.",
         [("Assets Under Custody (AUC)", "Total $ value of everything all users hold on the platform."),
          ("Deposit/withdrawal success rate", "% of funding attempts that complete without error."),
          ("Net deposits", "Deposits minus withdrawals — a real-money momentum and trust signal."),
          ("Portfolio-page engagement", "How often users check their holdings — a trust/habit signal, separate from trading.")]),
        ("Trading API",
         "Lets power users and institutions automate their own trading instead of clicking through the app — same order book, programmatic access.",
         [("API-driven volume share", "% of total trading volume placed through the API vs the app/website."),
          ("Active API users", "Unique accounts placing orders via API in a period."),
          ("API reliability", "Uptime and response latency — a trust metric for power users who depend on it.")]),
    ]
    features = callout("info", "Purpose",
        p("These are the real Binance.US surfaces only — no global-Binance products (margin, futures, options, P2P, Launchpad, the debit card, mining pools, or white-label exchange), since those aren't part of what you'd work on here. Keep answers high level."))
    for name, desc, ms in feature_areas:
        features += card(name, p(desc) + table(["Metric", "Plain-English definition"], [[b(n), d] for n, d in ms]))

    # --- Culture & Change ---
    culture_qas = [
        ("Tell me about a time priorities changed mid-project and you had to pivot.", True, "Strong",
         "Concrete, quantified, and shows the full arc: disagree, get overruled, pivot fully, deliver a fair result.",
         ["I recommended against reordering the SMS sign-up flow because my sizing showed it would lose more bookings than it gained.",
          "The product team overruled me and decided to launch it as a real test anyway — the direction changed mid-analysis.",
          "I stopped arguing and switched roles: instead of blocking it, I designed the fairest possible test of their idea.",
          "I even widened the main measurement window so the new flow wouldn't be judged unfairly for taking longer.",
          "The test came back flat and we rolled back — but the team got a real answer instead of an unresolved argument."],
         "When my recommendation was overruled, I put my energy into designing a fair test instead of relitigating the decision."),
        ("How do you operate when the roadmap isn't clearly defined?", True, "Mid",
         "This is a principle, not a story — fine as a philosophy but interviewers will push for a specific instance. Have the L1–L3 framework story ready as the concrete backup.",
         ["Before starting any project, I ask one question: what decision does this inform, and who owns it.",
          "That question alone stops me from doing work that doesn't actually move anything forward.",
          "For every new ask, I pin down 5 things upfront: the real business question, the expected impact, the exact scope, the output format, and the deadline.",
          "This isn't always popular in the moment — people want you to just start — but it's appreciated later because it prevents wasted work.",
          "If something genuinely can't be defined yet, I say that out loud instead of quietly guessing."],
         "I treat an unclear roadmap as a signal to ask sharper questions, not a reason to wait."),
        ("Tell me about a time the company's strategy shifted and it changed what you were tracking or building.", True, "Strong",
         "Concrete, quantified, clear before/after — and it ends in a permanent tracking change, not just a one-time insight.",
         ["Finance flagged a 10% year-over-year drop in SMS revenue-per-user and wanted to know what had broken.",
          "I dug in and found nothing was broken — the product team had quietly shifted strategy, from waiting for customers to find SMS to actively pushing it to millions of existing email users.",
          "That shift brought in a different, lower-spending type of customer, which pulled the average down even though the business was healthier overall.",
          "I reframed it: this isn't a red flag, it's the expected math of a strategy they'd already chosen.",
          "I recommended splitting the metric going forward so future strategy shifts wouldn't cause the same false alarm."],
         "My job was to catch up to a strategy change the business had already made and make sure our metrics reflected it honestly."),
        ("Describe a time leadership made a call that invalidated or changed work you'd already done.", True, "Strong",
         "Concrete, quantified, and shows real negotiation skill — reversing a 'hard no' without a turf fight.",
         ["Legal pushed a compliance disclaimer live on our highest-value page with no review, and it dropped conversion 10 points overnight.",
          "When I raised it, Legal's first answer was a hard no: 'this is a legal requirement, it cannot be reverted.'",
          "Instead of treating that as the end, I split the issue in two: the requirement itself was fixed, but how it was implemented was not.",
          "I proposed a safe, reversible test of a lighter version — so Legal could say yes without giving up anything.",
          "The lighter version won and conversion fully recovered, with zero compliance risk taken."],
         "I don't treat a 'no' as final — I look for the part of the decision that's actually still open."),
        ("What frustrates you in a fast-paced environment, and how do you handle it?", True, "Mid",
         "Good, mature framing — but it's a philosophy, not a story. Pair with a concrete instance if a hiring manager probes.",
         ["What frustrates me most is unclear scoping — starting work that isn't tied to an actual decision.",
          "The second thing is data-quality problems that surface mid-analysis and slow everything down.",
          "For the first, my fix is always asking 'what decision does this inform' before I start.",
          "For the second, I focus on what I can control: documenting gaps clearly, flagging them early, being upfront about caveats.",
          "I try to turn frustration into a process fix rather than a complaint."],
         "My rule: if something frustrates me twice, I build a process so it doesn't get a third chance to."),
        ("Tell me about a time you had to wear multiple hats or manage many things at once with limited resources.", True, "Strong",
         "Concrete, quantified, and shows systems-building under load, not just grinding through.",
         ["In one week, I had to deliver 5 full experiment readouts at the same time, each needing data validation, metric checks, statistics, and a clear write-up.",
          "In that same week, I also built a tracker dashboard giving the whole team visibility into every experiment.",
          "All 5 readouts shipped at full quality — nothing was cut or rushed.",
          "My manager called it impressive; in the moment it didn't feel that way, because the system I'd built made it feel normal.",
          "The tracker outlasted that week and became a permanent team tool."],
         "For most people that week would've been a crisis — for me it was just how I work, because I'd already built the systems."),
        ("How do you move fast without cutting corners, especially where compliance matters?", True, "Mid",
         "Directly answers the question, but it's the same underlying event as 'invalidated work'. Pick one framing per interview and keep this in reserve.",
         ["A required legal change was hurting conversion badly, and the pressure was to accept it since 'legal requirements can't be tested.'",
          "I moved fast, but not by skipping validation — I proposed a real test comparing the heavy disclaimer against a lighter, still-compliant version.",
          "I made sure Legal reviewed and signed off on the new wording before it went live, so compliance was never at risk.",
          "The test ran on a normal, properly-sized timeline — I didn't shortcut the statistics under pressure.",
          "We got a real, trustworthy answer in about a month instead of an untested guess."],
         "Speed for me means removing unnecessary delay, not removing rigor."),
        ("Tell me about a time you made a call with incomplete data and had to self-correct quickly.", True, "Strong",
         "Concrete, quantified, and shows self-correction before being caught — one of the rarest, most trusted signals.",
         ["I ran an experiment, got a negative result, and shared it with the team — who started planning next steps based on it.",
          "After sharing, I noticed the test groups weren't actually balanced, which meant the result couldn't be trusted.",
          "I went back to the team immediately and told them not to act on it, before anyone else caught it.",
          "I traced the bug to the testing tool's bucketing logic, fixed it, and reran the experiment.",
          "The corrected version came back a winner — the opposite conclusion — and I made a permanent rule to check group balance before sharing any result."],
         "I'd rather walk back my own result in front of the team than let a bad decision get made on it."),
        ("Tell me about a time you had to learn something new quickly because the business needed it.", True, "Mid",
         "Excellent technical depth, but the question is about speed and this reads as a deliberate multi-week study. Say how quickly you picked up CEM, or swap in a faster-turnaround example.",
         ["When SMS launched, leadership needed proof it actually grew the business, not just added a revenue line.",
          "A normal A/B test wasn't possible — you can't randomly assign who chooses to buy SMS credits.",
          "I learned and applied Coarsened Exact Matching, a causal-inference technique the team hadn't used before, to build a fair comparison group.",
          "I validated it with balance checks and a placebo test, and cross-checked it against three other methods.",
          "The result — a 79% revenue lift — directly changed the company's roadmap and became a trusted method for future studies."],
         "When the standard tool (an A/B test) wasn't available, I picked up the right technique instead of settling for a weaker analysis."),
        ("How comfortable are you in a true startup environment, with fast and less-structured pace?", False, "Weak",
         "This is an honest reframe, not a proof point — there's no real story behind it. Say it briefly and pivot fast to the SMS 0-to-1 example.",
         ["My companies (JustAnswer, Mailchimp/Intuit) weren't classic startups, so I don't have a literal seed-stage-chaos story — better to be upfront.",
          "The credible answer: SMS at Mailchimp behaved like a 0-to-1 startup inside a large company — a brand-new channel with no existing metrics, playbooks, or shared definitions.",
          "I built the operating structure myself (metrics framework, semantic layer, reporting automation) instead of inheriting one."],
         "My company wasn't a startup, but the channel I owned was — I was building the playbook, not following one."),
    ]
    strong_n = sum(1 for _, _, s, _, _, _ in culture_qas if s == "Strong")
    mid_n = sum(1 for _, _, s, _, _, _ in culture_qas if s == "Mid")
    weak_n = sum(1 for _, _, s, _, _, _ in culture_qas if s == "Weak")
    tone_map = {"Strong": "success", "Mid": "warning", "Weak": "danger"}
    culture = (
        callout("info", "How to use this",
            p("Questions the recruiter screen actually asked (startup culture, shifting priorities, strategy pivots, frustration). Each answer is pulled from your real stories — say it in your own words, don't recite it. The strength rating is a real grade — read the note on anything Mid or Weak before the interview.")) +
        stats((strong_n, "Strong"), (mid_n, "Mid — needs shoring up"), (weak_n, "Weak — no real story")))
    for q, sourced, strength, note, points, closer in culture_qas:
        inner = (pill_row([("From your stories" if sourced else "Best fit — no direct story"), f"Strength: {strength}"]) +
                 callout(tone_map[strength], "Why this rating", p(note)) +
                 ul(points) +
                 callout("success", "Closing line", p(closer)))
        culture += collapsible(q, inner)

    body = tabs("bnb",
        [("concepts", "Concepts"), ("metrics", "Metrics & Stickiness"), ("experiments", "A/B Experiments"),
         ("diagnose", "Diagnose a Decline"), ("features", "Feature Areas & Metrics"), ("culture", "Culture & Change")],
        [("concepts", concepts), ("metrics", metrics), ("experiments", experiments),
         ("diagnose", diagnose), ("features", features), ("culture", culture)])
    return html_page(
        "Binance.US — Senior Product Analyst Interview Prep",
        "Product fluency + the two question archetypes. Say the watch-outs out loud in interviews — they are the senior signal.",
        body)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

CANVASES = [
    ("alphasense-ds-analysis-framework",  make_alphasense_ds),
    ("alphasense-genai-impact-framework", make_alphasense_genai),
    ("causal-training-study-guide",       make_causal_training),
    ("churn-retention-model-walkthrough", make_churn_retention),
    ("interview-prep-guide",              make_interview_prep),
    ("item-to-item-recommendation-walkthrough", make_item_to_item),
    ("matching-overview",                 make_matching_overview),
    ("ml-model-guide",                    make_ml_model_guide),
    ("psm-explainer",                     make_psm_explainer),
    ("recsys-interview-playbook",         make_recsys_playbook),
    ("webstaurant-interview-prep",        make_webstaurant_prep),
    ("playstation-senior-product-analyst-prep", make_playstation),
    ("ab-test-stats-prep",                make_ab_test_stats),
    ("binance-us-prep",                   make_binance_us),
]

# Hand-authored canvases with no make_* function. They live as static folders
# next to this script and are copied into OUT_DIR verbatim.
STATIC_CANVASES = [
    "handshake-senior-ds-prep",
    "wise-regional-product-analyst-prep",
]

# Landing-page metadata: (category, [(slug, title, description, tag), ...])
INDEX_SECTIONS = [
    ("Product Analyst Prep", [
        ("handshake-senior-ds-prep", "Handshake — Senior Data Scientist, Product Analytics",
         "Three-sided marketplace fluency, measurable L1&rarr;L3 metric trees plus a recruiter/job-seeker view, diagnosis, experiment design, where A/B tests break, DS&harr;ML (Relevance) collaboration, an AI case-study framework, and the Job-Creation PM collaboration interview.", "Handshake"),
        ("playstation-senior-product-analyst-prep", "PlayStation — Senior Product Analyst Prep",
         "Sony/PlayStation business fluency, L1&rarr;L3 metric trees, metric-decline diagnosis, and A/B test design.", "PlayStation"),
        ("binance-us-prep", "Binance.US — Senior Product Analyst Prep",
         "Crypto product fluency, stickiness metrics, 6 experiment designs, decline diagnosis, and behavioral Q&A.", "Binance.US"),
        ("wise-regional-product-analyst-prep", "Wise — Senior Product Analyst Prep",
         "Cross-border fintech business fluency, US-market product scope, measurable L1&rarr;L3 metric trees, metric diagnosis, A/B test design, and a community-sourced SQL question bank.", "Wise"),
        ("ab-test-stats-prep", "A/B Testing Stats — Senior PA Prep",
         "10-tab applied stats: metrics & tests, power analysis, holdouts, CUPED, quasi-experiments, model eval, decision cases.", "Stats"),
    ]),
    ("Interview Prep", [
        ("interview-prep-guide", "Interview Prep Guide",
         "Priority roadmap, 7-company breakdown, story bank, and behavioral Q&A for Senior DS / PA interviews.", "General"),
        ("webstaurant-interview-prep", "WebstaurantStore Round 2 Prep",
         "Technical interview prep: Python topics (pandas, numpy), SQL patterns, Colab format, day-of tips.", "WebstaurantStore"),
    ]),
    ("ML Case Walkthroughs", [
        ("churn-retention-model-walkthrough", "Churn / Retention Model — End to End",
         "16-section interview script: business framing, label definition, features, XGBoost, SHAP, production deployment.", "ML"),
        ("item-to-item-recommendation-walkthrough", "Item-to-Item Recommendation Engine",
         "17-section walkthrough for a 700K-SKU B2B catalog: co-occurrence, embeddings, two-stage ranking, cold start.", "RecSys"),
        ("recsys-interview-playbook", "Recommender Systems — Interview Playbook",
         "5-tab playbook: framing, model types, design considerations, metrics, multi-stage production architecture.", "RecSys"),
        ("ml-model-guide", "ML Models: When to Use Which",
         "Supervised vs unsupervised, model comparison, and core DS concepts.", "ML"),
    ]),
    ("AlphaSense", [
        ("alphasense-genai-impact-framework", "AlphaSense — GenAI Impact Framework",
         "Feature &times; habit-loop map, metrics framework, experiment design portfolio, strategic scenarios.", "AlphaSense"),
        ("alphasense-ds-analysis-framework", "AlphaSense — DS Analysis Framework",
         "Role analysis, product context, metrics design, causal inference, and a 90-day plan.", "AlphaSense"),
    ]),
    ("Causal Inference", [
        ("matching-overview", "Matching Methods Overview",
         "CEM, PSM, AIPW, a decision guide, and quality checks.", "Causal"),
        ("psm-explainer", "PSM Explainer",
         "Step-by-step propensity score matching, Python code, and common pitfalls.", "Causal"),
        ("causal-training-study-guide", "Causal Inference Study Guide",
         "Bias types, confounders, DiD, and sensitivity analysis.", "Causal"),
    ]),
]

INDEX_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --bg:#0f0f0f; --bg2:#1a1a1a; --border:#2e2e2e; --text:#e8e8e8; --text2:#a0a0a0; --text3:#666; --accent:#4f8ef7; }
body { background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
.container { max-width:940px; margin:0 auto; padding:44px 24px; }
h1 { font-size:28px; font-weight:700; margin-bottom:6px; }
.subtitle { color:var(--text2); margin-bottom:28px; }
h2.section { font-size:15px; font-weight:600; color:var(--text2); text-transform:uppercase; letter-spacing:.05em; margin:30px 0 12px; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
@media(max-width:640px){ .grid { grid-template-columns:1fr; } }
a.card { display:block; background:var(--bg2); border:1px solid var(--border); border-radius:10px; padding:18px 20px; text-decoration:none; transition:border-color .15s, transform .1s; }
a.card:hover { border-color:var(--accent); transform:translateY(-1px); }
.card-title { color:var(--text); font-weight:600; font-size:15px; margin-bottom:5px; }
.card-desc { color:var(--text2); font-size:13px; line-height:1.55; }
.card-foot { display:flex; justify-content:space-between; align-items:center; margin-top:10px; }
.tag { display:inline-block; background:rgba(79,142,247,.15); color:var(--accent); border-radius:999px; font-size:11px; padding:2px 9px; }
.url { color:var(--text3); font-size:11px; font-family:"JetBrains Mono",monospace; }
hr { border:none; border-top:1px solid var(--border); margin:26px 0; }
footer { color:var(--text3); font-size:12px; margin-top:36px; }
"""

def make_index():
    base = BASE_URL.rstrip("/") + "/"
    total = sum(len(items) for _, items in INDEX_SECTIONS)
    sections_html = ""
    for cat, items in INDEX_SECTIONS:
        cards = ""
        for slug, title, desc, tag in items:
            cards += (f'<a class="card" href="{slug}/index.html">'
                      f'<div class="card-title">{title}</div>'
                      f'<div class="card-desc">{desc}</div>'
                      f'<div class="card-foot"><span class="tag">{tag}</span>'
                      f'<span class="url">{base}{slug}/</span></div></a>')
        sections_html += f'<h2 class="section">{cat}</h2><div class="grid">{cards}</div>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MyGitPages — Canvases</title>
<style>{INDEX_CSS}</style>
</head>
<body>
<div class="container">
<h1>MyGitPages</h1>
<p class="subtitle">Standalone HTML versions of all my Cursor canvases — open in any browser, no Cursor required. {total} canvases.</p>
<hr>
{sections_html}
<footer>Generated by generate_html.py &middot; hosted on GitHub Pages.</footer>
</div>
</body>
</html>"""

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    created = []
    for name, fn in CANVASES:
        folder = os.path.join(OUT_DIR, name)
        os.makedirs(folder, exist_ok=True)
        out_path = os.path.join(folder, "index.html")
        with open(out_path, "w") as f:
            f.write(fn())
        created.append(out_path)
        print(f"✓  {out_path}")

    # Static (hand-authored) canvases — copied, not generated
    src_root = os.path.dirname(os.path.abspath(__file__))
    for name in STATIC_CANVASES:
        src = os.path.join(src_root, name)
        dst = os.path.join(OUT_DIR, name)
        if not os.path.isdir(src):
            print(f"!  skipped {name} — not found at {src}")
            continue
        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        created.append(os.path.join(dst, "index.html"))
        print(f"✓  {os.path.join(dst, 'index.html')}  (static)")

    # Landing page
    index_path = os.path.join(OUT_DIR, "index.html")
    with open(index_path, "w") as f:
        f.write(make_index())
    print(f"✓  {index_path}")

    # .nojekyll so GitHub Pages serves every file as-is
    nojekyll = os.path.join(OUT_DIR, ".nojekyll")
    open(nojekyll, "w").close()
    print(f"✓  {nojekyll}")

    print(f"\nDone — {len(created)} canvases + index.html written to {OUT_DIR}")
