#!/usr/bin/env python3
"""Build the DS 501 course site from course.yml.

    python3 tools/build_site.py            -> docs/  (what GitHub Pages serves)
    python3 tools/build_site.py --preview  -> one self-contained file

Same shape as tools/build_deck.py: one Python data file in, finished HTML out.
"""
import argparse
import html
import json
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
C = yaml.safe_load((ROOT / "course.yml").read_text(encoding="utf-8"))
CO, WEEKS = C["course"], C["weeks"]
REPO = CO["repo_slug"]
RELEASED = int(CO.get("released_through", 0))

NAV = [("index", "Schedule"), ("syllabus", "Syllabus"), ("project", "Project"),
       ("readings", "Papers"), ("resources", "Resources")]

CSS = """
:root{
  --bordo:#7A1F2B; --bordo-card:#8E2D3A; --red:#C8102E; --red-dark:#9E0B23;
  --gold:#E9C46A; --paper:#FBF8F5; --card:#FFFFFF; --line:#E7DCD5;
  --ink:#2A2526; --ink-soft:#3A3335; --muted:#6E6467;
  --green:#2E6B5E; --green-bg:#E9F2EE; --green-ink:#1E4D43;
  --chip:#F2E6E3; --band:#F8F1EE; --rose:#FCEBEC; --on-dark:#FBF8F5; --on-dark-2:#F0D9DC;
  box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#1B1416; --card:#241A1D; --line:#3D2B2F;
    --ink:#F4EAE7; --ink-soft:#E6D9D6; --muted:#B49CA0;
    --chip:#3A2529; --band:#241A1D; --rose:#3A1E23; --green-bg:#1C2A27; --green-ink:#9FD3C5;
  }
}
:root[data-theme="dark"]{
  --paper:#1B1416; --card:#241A1D; --line:#3D2B2F;
  --ink:#F4EAE7; --ink-soft:#E6D9D6; --muted:#B49CA0;
  --chip:#3A2529; --band:#241A1D; --rose:#3A1E23; --green-bg:#1C2A27; --green-ink:#9FD3C5;
}
*,*::before,*::after{box-sizing:inherit}
html{scroll-padding-top:calc(72px + env(safe-area-inset-top,0px));-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink-soft);
  font-family:"Source Sans 3","Source Sans Pro",system-ui,sans-serif;
  font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}
.mono{font-family:"IBM Plex Mono",ui-monospace,monospace}
a{color:var(--red-dark);text-underline-offset:2px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) a{color:#F19AA7}}
.wrap{max-width:1060px;margin:0 auto;padding:0 28px}

/* fixed strip so content never shows under a translucent status bar */
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);
  background:var(--bordo);z-index:40}

header.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;background:var(--bordo);
  color:var(--on-dark);border-bottom:3px solid var(--red)}
.bar .wrap{display:flex;align-items:center;gap:22px;min-height:66px;flex-wrap:wrap}
.brand{font-weight:600;font-size:19px;color:var(--on-dark);text-decoration:none;
  display:flex;align-items:baseline;gap:10px}
.brand .code{font-family:"IBM Plex Mono",monospace;color:var(--gold);letter-spacing:1px}
nav.main{display:flex;gap:4px;margin-left:auto;flex-wrap:wrap}
nav.main a{color:var(--on-dark-2);text-decoration:none;font-size:16px;padding:7px 13px;
  border-radius:999px}
nav.main a:hover{background:var(--bordo-card);color:#fff}
nav.main a[aria-current]{background:var(--gold);color:var(--bordo);font-weight:600}
a:focus-visible,button:focus-visible{outline:3px solid var(--gold);outline-offset:2px}

/* hero: the course story, which every week opener also uses */
.hero{background:var(--bordo);color:var(--on-dark);padding:56px 0 48px}
.hero h1{font-size:clamp(34px,5.2vw,54px);line-height:1.08;margin:0 0 14px;font-weight:600;
  color:var(--on-dark);max-width:17ch}
.hero .sub{color:var(--on-dark-2);max-width:62ch;margin:0 0 34px;font-size:19px}
.path{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
.path span{background:var(--bordo-card);border:1px solid rgba(233,196,106,.35);
  border-radius:999px;padding:8px 17px;font-size:16px;color:var(--on-dark)}
.path span:last-child{background:var(--gold);color:var(--bordo);font-weight:600;border-color:var(--gold)}
.path i{color:var(--gold);font-style:normal}
.meta{margin-top:30px;color:var(--on-dark-2);font-size:16px;
  border-top:1px solid rgba(251,248,245,.22);padding-top:18px}

main{padding:46px 0 70px}
h2{font-size:30px;font-weight:600;color:var(--bordo);margin:46px 0 14px;
  padding-bottom:7px;border-bottom:2px solid var(--chip)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) h2{color:#F0C0C8}}
h2:first-child{margin-top:0}
h3{font-size:21px;font-weight:600;color:var(--ink);margin:30px 0 8px}
p{max-width:72ch}

/* schedule */
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
table.sched{width:100%;border-collapse:collapse;font-size:16px;min-width:720px}
table.sched th{background:var(--bordo);color:var(--on-dark);text-align:left;
  padding:13px 15px;font-weight:600}
table.sched td{padding:14px 15px;border-bottom:1px solid var(--line);vertical-align:top}
table.sched tr:nth-child(even) td{background:var(--band)}
table.sched tr:last-child td{border-bottom:none}
.wk a{font-family:"IBM Plex Mono",monospace;color:var(--red);text-decoration:none;
  font-weight:600;white-space:nowrap}
.wk a:hover{text-decoration:underline}
.topic b{color:var(--ink);font-size:17px}
.lessonlist{color:var(--muted);font-size:15px;line-height:1.5}
.due{font-family:"IBM Plex Mono",monospace;font-size:14px;color:var(--muted);white-space:nowrap}
.mats a{display:inline-block;margin-right:9px;font-size:15px}

/* week page */
.weekhead{display:flex;gap:34px;align-items:flex-start;background:var(--bordo);
  color:var(--on-dark);border-radius:16px;padding:34px 38px;margin-bottom:8px}
.weekhead .n{font-family:"IBM Plex Mono",monospace;font-size:76px;font-weight:600;
  line-height:.85;color:var(--gold)}
.weekhead h1{margin:0 0 8px;font-size:34px;font-weight:600;color:var(--on-dark)}
.weekhead p{margin:0;color:var(--on-dark-2);max-width:60ch}
.lesson{display:flex;gap:16px;align-items:baseline;padding:13px 2px;border-bottom:1px solid var(--line)}
.lesson .c{font-family:"IBM Plex Mono",monospace;color:var(--red);font-weight:600;
  min-width:52px;white-space:nowrap}
ul{max-width:72ch}
li{margin:5px 0}

.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 26px}
.keypoint{background:var(--bordo);color:var(--on-dark);border-radius:14px;padding:20px 26px}
.keypoint b{color:var(--gold)}
.keypoint p{color:var(--on-dark);margin:0}
.practice{background:var(--green-bg);border-left:7px solid var(--green);border-radius:10px;
  padding:20px 26px}
.practice b{color:var(--green-ink)}
.mistake{background:var(--rose);border-left:7px solid var(--red);border-radius:10px;padding:20px 26px}
.mistake b{color:var(--red-dark)}
.colab{display:inline-block;margin-top:12px;background:var(--bordo);color:var(--on-dark);
  text-decoration:none;font-family:"IBM Plex Mono",monospace;font-size:15px;
  padding:10px 20px;border-radius:999px}
.colab:hover{background:var(--red);color:#fff}
.colab.alt{background:transparent;color:var(--bordo);border:2px solid var(--bordo);margin-left:8px}
.colab.alt:hover{background:var(--bordo);color:var(--on-dark)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .colab.alt{color:var(--gold);border-color:var(--gold)}}
.soon{color:var(--muted);font-style:italic}
.pager{display:flex;justify-content:space-between;gap:14px;margin-top:44px;
  border-top:1px solid var(--line);padding-top:20px;font-size:16px}

footer{background:var(--bordo);color:var(--on-dark-2);padding:34px 0;font-size:15px}
footer a{color:var(--gold)}
footer .wrap{display:flex;gap:18px;flex-wrap:wrap;justify-content:space-between}

@media (max-width:640px){
  body{font-size:17px}
  .weekhead{flex-direction:column;gap:14px;padding:26px}
  .weekhead .n{font-size:54px}
  .hero{padding:40px 0 34px}
  nav.main{margin-left:0;width:100%}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Source+Sans+3:ital,wght@0,400..700;1,400..700&'
         'family=IBM+Plex+Mono:wght@400;600&display=swap">')


def e(s):
    return html.escape(str(s), quote=False)


def colab(nb):
    return (f"https://colab.research.google.com/github/{REPO}"
            f"/blob/main/notebooks/student/{nb}.ipynb")


def released(w):
    return w["num"] <= RELEASED


def deck(w, ext):
    return f"slides/{w['deck']}.{ext}" if w.get("deck") else None


def nav(active, single):
    out = []
    for key, label in NAV:
        href = f"#{key}" if single else ("index.html" if key == "index" else f"{key}.html")
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{href}"{cur}>{e(label)}</a>')
    return "".join(out)


def link(key, single):
    return f"#{key}" if single else f"{key}.html"


# ------------------------------------------------------------------ pages
def page_index(single):
    rows = []
    for w in WEEKS:
        n = w["num"]
        ms = C["milestones"].get(n)
        extra = f'<br>Project: {e(ms)}' if ms else ""
        href = link(f"week{n:02d}", single)
        rows.append(
            f'<tr><td class="wk"><a href="{href}">Week {n}</a></td>'
            f'<td class="topic"><b>{e(w["title"])}</b>'
            f'<div class="lessonlist">{e(w["practice"])} · {e(w["dataset"])}</div></td>'
            f'<td class="lessonlist">'
            + "<br>".join(f'<span class="mono" style="color:var(--red)">{c}</span> {e(t)}'
                          for c, t in w["lessons"])
            + "</td>"
            + (f'<td class="mats"><a href="{deck(w, "pdf") or href}">Slides</a>'
               f'<a href="{colab(w["notebook"])}">Lab</a></td>'
               if released(w) else '<td class="mats"><span class="soon">Coming soon</span></td>')
            +
            f'<td class="due">Lab [date]<br>Quiz [date]{extra}</td></tr>'
        )
    story = ["a question", "data", "understanding", "models", "communication", "responsibility"]
    chips = '<i>→</i>'.join(f"<span>{e(s)}</span>" for s in story)
    return (
        f'<section class="hero"><div class="wrap">'
        f'<h1>{e(CO["title"])}</h1>'
        f'<p class="sub">{e(CO["blurb"])}</p>'
        f'<div class="path">{chips}</div>'
        f'<p class="meta">{e(CO["meeting"])} &nbsp;·&nbsp; '
        f'{e(CO["institution"])}, {e(CO["city"])} &nbsp;·&nbsp; {e(CO["semester"])}</p>'
        f"</div></section>"
        f'<main><div class="wrap">'
        f"<h2>Schedule</h2>"
        f'<p>Everything for a week is on that week’s page: the deck, the reading handout, '
        f'the lab notebook, the quiz and the papers. Dates are placeholders until the '
        f"semester calendar is fixed.</p>"
        f'<div class="tablewrap"><table class="sched">'
        f'<tr><th style="width:9%">Week</th><th style="width:27%">Topic and practice</th>'
        f'<th style="width:28%">Lessons</th><th style="width:17%">Materials</th>'
        f'<th style="width:19%">Due</th></tr>'
        + "".join(rows) + "</table></div>"
        f'<h2>Before the first class</h2>'
        f'<p>Open a Google account you can use with Colab, read the '
        f'<a href="{link("syllabus", single)}">syllabus</a>, and start thinking about a '
        f'question you would like to answer with data. You choose a project topic in '
        f'Week 1 and confirm it in Week 3.</p>'
        f'<div class="keypoint"><p><b>Key point:</b> start with the decision someone '
        f"would make differently if they knew the answer, not with the dataset.</p></div>"
        f"</div></main>"
    )


def page_syllabus(single):
    arows = "".join(
        f'<tr><td><b>{e(a["item"])}</b></td><td class="due">{e(a["weight"])}</td>'
        f'<td>{e(a["detail"])}</td></tr>' for a in C["assessment"])
    books = "".join(f"<li>{e(b)}</li>" for b in C["books"])
    return (
        f'<main><div class="wrap"><h2>Syllabus</h2>'
        f'<p>{e(CO["code"])} is a {e(CO["level"].lower())} course at {e(CO["institution"])}, '
        f'{e(CO["city"])}. Students arrive from computer science, engineering, economics, '
        f"business and the social sciences, so the course assumes no prior data science and "
        f"builds the programming alongside the ideas.</p>"
        f'<p>{e(CO["meeting"])}</p>'
        f"<h3>How a week runs</h3>"
        f"<ul><li>Three lessons of 45 minutes, each with a scenario worked in pairs and one "
        f"Check Your Understanding question.</li>"
        f"<li>One practice of 45–60 minutes in class, finished as homework.</li>"
        f"<li>A quiz of 15 multiple-choice questions, plus one short applied question "
        f"from Week 2 on.</li>"
        f"<li>Two or three required papers, with a half-page note due at the next class.</li></ul>"
        f"<h2>Marking</h2>"
        f'<div class="tablewrap"><table class="sched">'
        f'<tr><th style="width:26%">Component</th><th style="width:14%">Weight</th>'
        f'<th style="width:60%">Notes</th></tr>{arows}</table></div>'
        f"<p>Weights come from the syllabus document and must match this table before "
        f"the semester starts.</p>"
        f"<h2>Using AI tools</h2>"
        f"<p>You may use an AI assistant to explain concepts, debug your own code and "
        f"improve your writing. You must be able to explain every line you submit. Work "
        f"you cannot explain is treated as work you did not do.</p>"
        f"<p>State in your submission which tool you used and what for. That statement "
        f"costs you no marks. Omitting it does. Week 11 treats reviewing AI-written code "
        f"as a skill in its own right, including the failure modes to look for.</p>"
        f"<h2>Companion texts</h2><ul>{books}</ul>"
        f"<p>None is required to buy. The relevant chapters are listed on each week’s page.</p>"
        f"<h2>Tools</h2>"
        f'<p>{e(CO["tools"])} Every notebook opens in Colab with no local setup.</p>'
        f"</div></main>"
    )


def page_project(single):
    ms = "".join(
        f'<tr><td class="wk">Week {k}</td><td><b>{e(v)}</b></td></tr>'
        for k, v in sorted(C["milestones"].items()))
    return (
        f'<main><div class="wrap"><h2>Course project</h2>'
        f"<p>You work on one dataset and one question for the whole semester and present "
        f"the result in Week 12. The project is individual. The point is not a high score "
        f"on a benchmark; it is a defensible answer to a real question, with the "
        f"uncertainty stated honestly.</p>"
        f"<h2>Milestones</h2>"
        f'<div class="tablewrap"><table class="sched">'
        f'<tr><th style="width:16%">Week</th><th>Milestone</th></tr>{ms}</table></div>'
        f"<h2>Choosing a question</h2>"
        f"<p>Good questions here are small, local and answerable. Skopje air quality, a "
        f"North Macedonian open dataset, public transport, or something from your own "
        f"field of work. A question that needs data you cannot get is not a project.</p>"
        f'<div class="mistake"><p><b>Common mistake:</b> choosing the dataset first and '
        f"then hunting for a question inside it.</p></div>"
        f"<h2>Handbook</h2>"
        f"<p>The full brief, the marking guide and the notebook template are in the "
        f"<i>DS 501 Course Project Handbook</i>. [Link]</p>"
        f"</div></main>"
    )


def page_readings(single):
    out = []
    for w in WEEKS:
        req = "".join(f"<li>{e(r)}</li>" for r in w["required"])
        opt = "".join(f"<li>{e(r)}</li>" for r in w["optional"])
        out.append(
            f'<h3>Week {w["num"]} · {e(w["title"])}</h3>'
            f"<p><b>Required</b></p><ul>{req}</ul>"
            f'<p style="color:var(--muted)"><b>Optional</b></p><ul>{opt}</ul>')
    return (
        f'<main><div class="wrap"><h2>Papers to read</h2>'
        f"<p>Each week has two or three required papers and two or three optional ones. "
        f"For every required paper, bring a half-page note to the next class: the "
        f"problem, the key idea, and how it connects to the week. One quiz question each "
        f"week may refer to the required reading.</p>"
        f'<div class="practice"><p><b>In practice</b> Week 1 teaches Keshav’s three-pass '
        f"method. Use the first pass on every paper here, and all three on the ones you "
        f"cite in your project.</p></div>"
        + "".join(out)
        + "<p>Page numbers and IBU library links are added before the syllabus is "
          "published.</p></div></main>"
    )


def page_resources(single):
    return (
        f'<main><div class="wrap"><h2>Resources</h2>'
        f"<h3>Running the code</h3>"
        f"<p>Every lab opens in Google Colab from its week page. Nothing needs installing "
        f"on your own machine, and every dataset loads from a public URL. For a local "
        f"setup, install Python 3.11 or later plus the packages listed at the top of "
        f"each notebook.</p>"
        f"<h3>References you will use every week</h3>"
        f"<ul><li>pandas user guide and API reference</li><li>NumPy reference</li>"
        f"<li>matplotlib and Plotly galleries</li><li>scikit-learn user guide</li>"
        f"<li>SQLite documentation, for Week 4</li>"
        f"<li>Apache Spark Python API, for Week 11</li></ul>"
        f"<h3>Datasets</h3>"
        f"<p>Palmer Penguins, Telco churn, Chinook, Titanic, Gapminder, Diamonds, COMPAS, "
        f"and open data from North Macedonian portals. All public.</p>"
        f"<h3>Getting help</h3>"
        f"<p>Ask in class, in the course channel, or in office hours. If you are stuck on "
        f"code, bring the error message and the smallest example that produces it.</p>"
        f"<h3>Fixing this site</h3>"
        f'<p>This site is a public repository. Found a broken link, a wrong date or a '
        f'typo? <a href="{e(CO["repo"])}/issues">Open an issue</a> or send a pull '
        f"request. Corrections are welcome and credited.</p>"
        f"</div></main>"
    )


def page_week(w, single):
    n = w["num"]
    lessons = "".join(
        f'<div class="lesson"><span class="c">{c}</span><span>{e(t)}</span></div>'
        for c, t in w["lessons"])
    req = "".join(f"<li>{e(r)}</li>" for r in w["required"])
    opt = "".join(f"<li>{e(r)}</li>" for r in w["optional"])
    ms = C["milestones"].get(n)
    msline = f"<li><b>Project milestone:</b> {e(ms)} — [date]</li>" if ms else ""
    prev = (f'<a href="{link(f"week{n-1:02d}", single)}">← Week {n-1}: '
            f'{e(WEEKS[n-2]["title"])}</a>') if n > 1 else "<span></span>"
    nxt = (f'<a href="{link(f"week{n+1:02d}", single)}">Week {n+1}: '
           f'{e(WEEKS[n]["title"])} →</a>') if n < 12 else "<span></span>"
    return (
        f'<main><div class="wrap">'
        f'<div class="weekhead"><div class="n">{n:02d}</div><div>'
        f"<h1>{e(w['title'])}</h1><p>{e(w['purpose'])}</p></div></div>"
        f"<h2>Lessons</h2>{lessons}"
        f"<h2>Slides</h2>"
        f"<p>One deck covers all three lessons. The speaker notes are written as student "
        f"reading text, so the deck and its notes together are the week’s handout.</p>"
        + (f'<a class="colab" href="{deck(w, "pdf")}">View slides (PDF)</a>'
           f'<a class="colab alt" href="{deck(w, "pptx")}" download>'
           f'PowerPoint with speaker notes</a>'
           if released(w) and w.get("deck") else
           '<p class="soon">Slides are posted before the class.</p>')
        +
        f"<h2>Practice</h2>"
        f'<div class="practice"><p><b>{e(w["practice"])}</b> — {e(w["dataset"])}</p>'
        f"<p>Work through the guided code, then the exercises marked ✏️. Every lab "
        f"produces one measured result you must report and interpret. Submit the notebook "
        f"with all cells executed.</p>"
        + (f'<a class="colab" href="{colab(w["notebook"])}">Open the lab in Colab</a>'
           f'<a class="colab alt" href="{CO["repo"]}/raw/main/notebooks/student/'
           f'{w["notebook"]}.ipynb">Download .ipynb</a>'
           if released(w) else '<p class="soon">The lab notebook is posted before the class.</p>')
        + "</div>"
        f"<h2>Quiz</h2>"
        f"<p>15 multiple-choice questions, 25–30 minutes, covering lessons "
        f"{w['lessons'][0][0]} to {w['lessons'][2][0]}. Questions use the wording of the "
        f"Key Terms slides. <i>[Link]</i></p>"
        f"<h2>Papers</h2><p><b>Required</b></p><ul>{req}</ul>"
        f'<p style="color:var(--muted)"><b>Optional</b></p><ul>{opt}</ul>'
        f"<h2>Due this week</h2>"
        f"<ul><li><b>Practice {n}:</b> [date]</li>"
        f"<li><b>Quiz {n}:</b> [date]</li>{msline}</ul>"
        f'<div class="pager">{prev}{nxt}</div>'
        f"</div></main>"
    )


def shell(title, body, active, single, router=""):
    inline_css = f"<style>{CSS}</style>"
    css_ref = inline_css if single else '<link rel="stylesheet" href="assets/ds501.css">'
    return (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1, '
        f'viewport-fit=cover">'
        f"<title>{e(title)}</title>"
        f'<meta name="description" content="{e(CO["code"])} {e(CO["title"])} at '
        f'{e(CO["institution"])}: schedule, slides, labs, quizzes and papers.">'
        f"{FONTS}{css_ref}</head><body>"
        f'<header class="bar"><div class="wrap">'
        f'<a class="brand" href="{link("index", single)}">'
        f'<span class="code">{e(CO["code"])}</span>'
        f'<span>{e(CO["title"])}</span></a>'
        f'<nav class="main">{nav(active, single)}</nav></div></header>'
        f'<div id="root">{body}</div>'
        f'<footer><div class="wrap">'
        f'<span>{e(CO["institution"])}, {e(CO["city"])}</span>'
        f'<span><a href="{e(CO["instructor_page"])}">{e(CO["instructor"])}</a> · '
        f'{e(CO["semester"])}</span>'
        f'<span><a href="{e(CO["repo"])}">Source on GitHub</a></span>'
        f"</div></footer>{router}</body></html>"
    )


def build_bodies(single):
    pages = {
        "index": (f'{CO["code"]} · {CO["title"]}', page_index(single)),
        "syllabus": (f'Syllabus · {CO["code"]}', page_syllabus(single)),
        "project": (f'Course project · {CO["code"]}', page_project(single)),
        "readings": (f'Papers to read · {CO["code"]}', page_readings(single)),
        "resources": (f'Resources · {CO["code"]}', page_resources(single)),
    }
    for w in WEEKS:
        pages[f"week{w['num']:02d}"] = (
            f'Week {w["num"]} · {w["title"]} · {CO["code"]}', page_week(w, single))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true",
                    help="write one self-contained file instead of docs/")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.preview:
        pages = build_bodies(True)
        bodies = {k: v[1] for k, v in pages.items()}
        router = (
            "<script>(function(){var P=" + json.dumps(bodies).replace("</", "<\\/") + ";"
            "var r=document.getElementById('root');"
            "function go(){var k=(location.hash||'#index').slice(1);"
            "if(!P[k])k='index';r.innerHTML=P[k];"
            "var base=k.indexOf('week')===0?'index':k;"
            "document.querySelectorAll('nav.main a').forEach(function(a){"
            "a.toggleAttribute('aria-current',a.getAttribute('href')==='#'+base)});"
            "window.scrollTo(0,0);}"
            "window.addEventListener('hashchange',go);go();})();</script>")
        out = Path(args.out or "/mnt/user-data/outputs/ds501-static-preview.html")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(shell(pages["index"][0], "", "index", True, router), encoding="utf-8")
        print(f"{out}  {out.stat().st_size/1024:.0f} kB")
        return

    docs = ROOT / "docs"
    (docs / "assets").mkdir(parents=True, exist_ok=True)
    (docs / "assets" / "ds501.css").write_text(CSS, encoding="utf-8")
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    # Published decks: copy slides/<deck>.pdf|.pptx for released weeks into docs/slides/.
    out = docs / "slides"
    shutil.rmtree(out, ignore_errors=True)
    for w in WEEKS:
        if released(w) and w.get("deck"):
            out.mkdir(exist_ok=True)
            for ext in ("pdf", "pptx"):
                src = ROOT / deck(w, ext)
                if not src.exists():
                    raise SystemExit(f"missing {src.relative_to(ROOT)} for week {w['num']}")
                shutil.copyfile(src, out / src.name)
    for key, (title, body) in build_bodies(False).items():
        active = "index" if key.startswith("week") else key
        (docs / f"{key}.html").write_text(shell(title, body, active, False), encoding="utf-8")
        print("wrote docs/" + key + ".html")


if __name__ == "__main__":
    main()
