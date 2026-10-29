#!/usr/bin/env python3
"""Build the static review site in docs/ (served by GitHub Pages) from the CSV and SSSOM files.

Run after build.py:  python3 -I scripts/build.py && python3 -I scripts/site.py
Python 3.10+, standard library only.
"""
import csv
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
REPO = "https://github.com/Health-Culture-Foundation/HCF-Audiences-Ecological-Model-2.0"

LEVEL_COLORS = {"intrapersonal": "l1", "interpersonal": "l2", "institutional": "l3", "community": "l4", "public-policy": "l5"}


def read(path):
    with open(ROOT / path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_sssom(path):
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    meta = [l[2:] for l in lines if l.startswith("# ")]
    body = [l for l in lines if not l.startswith("#")]
    rows = list(csv.DictReader(body, delimiter="\t"))
    title = next((m.split(": ", 1)[1] for m in meta if m.startswith("mapping_set_title")), path)
    comment = next((m.split(": ", 1)[1] for m in meta if m.startswith("comment")), "")
    return title, comment, rows


def split(s):
    return [x.strip() for x in (s or "").split("|") if x.strip()]


e = html.escape

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1c1a;--muted:#5d5a54;--line:#e3dfd6;--card:#fff;--accent:#2f5d50;--banner:#fff4d6;--banner-fg:#5a4500;
--l1:#2f6f9f;--l2:#6a5aa8;--l3:#a35a2a;--l4:#2f7d4f;--l5:#9a2f4a;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161615;--fg:#ecebe7;--muted:#a9a59c;--line:#33312d;--card:#1f1e1c;--accent:#7cc0aa;--banner:#3a3016;--banner-fg:#f3dc9a;
--l1:#7fb6e0;--l2:#b2a6ec;--l3:#e6a074;--l4:#7fcf9d;--l5:#ec8aa3;}}
:root[data-theme="dark"]{--bg:#161615;--fg:#ecebe7;--muted:#a9a59c;--line:#33312d;--card:#1f1e1c;--accent:#7cc0aa;--banner:#3a3016;--banner-fg:#f3dc9a;
--l1:#7fb6e0;--l2:#b2a6ec;--l3:#e6a074;--l4:#7fcf9d;--l5:#ec8aa3;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.banner{background:var(--banner);color:var(--banner-fg);padding:8px 16px;font-size:14px;text-align:center}
header{border-bottom:1px solid var(--line);padding:16px}
header .wrap{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:baseline}
header .brand{font-weight:700;text-decoration:none;color:var(--fg);margin-right:auto}
nav a{text-decoration:none;font-size:15px;margin-right:14px}
nav a[aria-current]{font-weight:700;text-decoration:underline}
.wrap{max-width:1100px;margin:0 auto}
main{padding:24px 16px 48px}
h1{font-size:30px;line-height:1.2;margin:0 0 8px}
h2{font-size:22px;margin:36px 0 8px}
h3{font-size:18px;margin:24px 0 6px}
.lede{font-size:18px;color:var(--muted);max-width:760px}
.levels{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:20px 0}
.level{background:var(--card);border:1px solid var(--line);border-top:5px solid var(--c);border-radius:8px;padding:14px}
.level .n{font-size:13px;color:var(--c);font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.level h3{margin:2px 0 6px}
.level p{margin:6px 0;font-size:15px}
.level .q{font-size:13px;color:var(--muted);font-style:italic}
.l1{--c:var(--l1)}.l2{--c:var(--l2)}.l3{--c:var(--l3)}.l4{--c:var(--l4)}.l5{--c:var(--l5)}
.pill{display:inline-block;border:1px solid var(--c,var(--line));color:var(--c,var(--muted));border-radius:999px;padding:0 8px;font-size:12px;white-space:nowrap}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--card);margin:10px 0 20px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}
th{font-size:13px;color:var(--muted);font-weight:600;background:var(--bg)}
tr:last-child td{border-bottom:0}
td.sub{padding-left:28px}
.muted{color:var(--muted)}
.small{font-size:13px}
input[type=search]{width:100%;max-width:420px;padding:9px 12px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);font-size:15px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:14px 16px}
svg text{fill:var(--fg);font-family:inherit}
footer{border-top:1px solid var(--line);padding:16px;font-size:13px;color:var(--muted)}
code{font-size:13px}
"""

PAGES = [("index.html", "Levels"), ("audiences.html", "Audiences"), ("communication.html", "Communication direction"),
         ("advocacy.html", "Advocacy"), ("crosswalks.html", "Crosswalks"), ("references.html", "References")]


def page(fname, title, body, script=""):
    nav = "".join(f'<a href="{f}"{" aria-current=page" if f == fname else ""}>{e(t)}</a>' for f, t in PAGES)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{e(title)} · HCF Audiences</title><style>{CSS}</style></head>
<body>
<div class="banner">Draft 0.1, not yet reviewed by a person. Researched and drafted by Claude (Claude Code) for the Health Culture Foundation.</div>
<header><div class="wrap"><a class="brand" href="index.html">HCF Audiences · Ecological Model</a><nav>{nav}</nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">Content <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, attribution "Health Culture Foundation".
NCI's quoted definitions are U.S. public domain. MeSH courtesy of the U.S. National Library of Medicine (no endorsement implied).
Built from <a href="{REPO}">the repository</a> by <code>scripts/site.py</code>. Downloads: <a href="data/">data files</a>.</div></footer>
{script}</body></html>
"""


def tbl(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def ref(key, refs):
    r = refs[key]
    return f'<a href="references.html#{key}" title="{e(r["citation"])}">[{e(r["short"])}]</a>'


# ------------------------------------------------------------------ pages
def index(levels, cdc, aud, refs):
    cdc_by = {c["id"]: c for c in cdc}
    _, _, xw = read_sssom("crosswalks/ecological-levels-to-cdc-sem.sssom.tsv")
    counts = {l["id"]: sum(1 for a in aud if a["level"] == l["id"]) for l in levels}
    cards = []
    for l in levels:
        c = LEVEL_COLORS[l["id"]]
        cards.append(f"""<div class="level {c}"><div class="n">Level {l['notation']} · {e(l['pref_label'])}</div>
<h3>{e(l['plain_label'])}</h3><p>{e(l['definition'])}</p>
<p class="small"><b>Sleep example:</b> {e(l['sleep_example'])}</p>
<p class="q">NCI (2005): “{e(l['source_definition'])}”</p>
<p class="small"><a href="audiences.html#{l['id']}">{counts[l['id']]} audiences</a> · CDC: {e(cdc_by[l['cdc_sem']]['pref_label'])}</p></div>""")
    # 5 -> 4 diagram
    y5 = {l["id"]: 40 + i * 56 for i, l in enumerate(levels)}
    y4 = {c["id"]: 54 + i * 66 for i, c in enumerate(cdc)}
    lines = []
    for m in xw:
        s, o = m["subject_id"].split(":")[1], m["object_id"].split(":")[1]
        dash = ' stroke-dasharray="5 4"' if "related" in m["predicate_id"] else ""
        lines.append(f'<line x1="250" y1="{y5[s]}" x2="450" y2="{y4[o]}" stroke="var(--muted)" stroke-width="1.5"{dash}/>')
    boxes5 = "".join(f'<rect x="20" y="{y5[l["id"]]-20}" width="230" height="40" rx="6" fill="none" stroke="var(--{LEVEL_COLORS[l["id"]]})" stroke-width="2"/>'
                     f'<text x="34" y="{y5[l["id"]]+5}" font-size="14">{l["notation"]}. {e(l["pref_label"].replace(" level", ""))}</text>' for l in levels)
    boxes4 = "".join(f'<rect x="450" y="{y4[c["id"]]-20}" width="170" height="40" rx="6" fill="none" stroke="var(--line)" stroke-width="2"/>'
                     f'<text x="464" y="{y4[c["id"]]+5}" font-size="14">{e(c["pref_label"])}</text>' for c in cdc)
    svg = f'''<svg viewBox="0 0 640 310" width="100%" style="max-width:640px" role="img" aria-label="Five levels mapped to CDC four levels">
<text x="20" y="14" font-size="12" fill="var(--muted)">McLeroy et al. 1988 / NCI (five levels)</text><text x="450" y="14" font-size="12">CDC (four levels)</text>
{''.join(lines)}{boxes5}{boxes4}</svg>'''
    body = f"""<h1>Audiences by ecological level</h1>
<p class="lede">A shared way to tag <b>who a health resource is for, and who acts on it</b>, using the five levels of influence of the
socio-ecological model. Any library, glossary or website can use it. Sleep is the first worked example.</p>
<p class="small muted">Levels from McLeroy et al. (1988) {ref('mcleroy1988', refs)}, as presented in NCI's <i>Theory at a Glance</i> (2005), Table 1 {ref('nci2005', refs)}.
Crosswalked to CDC's four-level model {ref('cdc-sem', refs)}.</p>
<h2>The five levels</h2><div class="levels">{''.join(cards)}</div>
<h2>Three rules</h2>
<div class="grid2">
<div class="box"><b>1. An audience sits at the level where it acts.</b><br>A parent reading about a teen's sleep is level 2. A principal changing the bell schedule is level 3. A legislator writing a start-time bill is level 5.</div>
<div class="box"><b>2. Who it's for ≠ who it's about.</b><br><i>Roles</i> (parent, school leader, policymaker) say who uses a resource. <i>Populations</i> (teens, shift workers) say whose health it's about. Tag both.</div>
<div class="box"><b>3. Crosswalks, not merges.</b><br>Each library keeps its own tags and maps them here with SSSOM files {ref('sssom2022', refs)}, using SKOS {ref('skos', refs)} and MeSH {ref('mesh', refs)} as the hub.</div>
</div>
<h2>Five levels → CDC's four</h2>
<p class="small muted">Solid line: close or broader match. Dashed: related. Details on the <a href="crosswalks.html">crosswalks</a> page.</p>
{svg}
<h2>What else is here</h2>
<ul>
<li><a href="audiences.html">Audiences</a>: {len(aud)} concepts placed at the five levels, mapped to MeSH, LRMI and SleepLiteracy's tags.</li>
<li><a href="communication.html">Communication direction</a>: professional to public, professional to professional (SleepLiteracy's Pro2Pro), and more.</li>
<li><a href="advocacy.html">Advocacy framework</a>: a 7-phase tag for policy-level resources that also works as one axis of a fuller framework.</li>
<li><a href="references.html">References</a>: every source, with licence and what it was used for.</li>
</ul>"""
    return page("index.html", "Levels", body)


def audiences(levels, aud):
    by = {a["id"]: a for a in aud}
    secs = []
    for l in levels:
        c = LEVEL_COLORS[l["id"]]
        rows = [a for a in aud if a["level"] == l["id"]]
        trs = []
        for a in rows:
            sub = a["broader"] and by[a["broader"]]["level"] == l["id"]
            maps = [f'MeSH <a href="https://meshb.nlm.nih.gov/record/ui?ui={m.split()[0]}">{e(m)}</a>' for m in split(a["mesh"])]
            maps += [f"schema:{e(s)}" for s in split(a["schema_org"])] + [f"LRMI {e(x)}" for x in split(a["lrmi_role"])]
            seeds = ", ".join(f"<code>{e(s)}</code>" for s in split(a["sleepliteracy_seed"]))
            text = " ".join([a["pref_label"], a["alt_labels"], a["definition"], a["notes"]]).lower()
            trs.append(f'<tr data-q="{e(text)}"><td class="{"sub" if sub else ""}">{"↳ " if sub else ""}<b>{e(a["pref_label"])}</b>'
                       f'<div class="small muted">{e(", ".join(split(a["alt_labels"])))}</div></td>'
                       f'<td><span class="pill">{e(a["facet"])}</span></td><td>{e(a["definition"])}'
                       f'{"<div class=small><i>e.g. " + e(a["sleep_example"]) + "</i></div>" if a["sleep_example"] else ""}'
                       f'{"<div class=\'small muted\'>" + e(a["notes"]) + "</div>" if a["notes"] else ""}</td>'
                       f'<td class="small">{"<br>".join(maps)}</td><td class="small">{seeds}</td></tr>')
        secs.append(f'<section id="{l["id"]}" class="{c}"><h2><span class="pill">Level {l["notation"]}</span> {e(l["plain_label"])} '
                    f'<span class="muted small">({e(l["pref_label"].lower())})</span></h2><p class="muted">{e(l["definition"])}</p>'
                    + tbl(["Audience", "Facet", "Means", "Maps to", "SleepLiteracy tag"], trs) + "</section>")
    body = f"""<h1>Audiences</h1>
<p class="lede">{len(aud)} audiences, each placed at the level where it acts. <b>Population</b> entries say who a resource is about; combine them with a role
(<i>parents and caregivers</i> + <i>teens</i>).</p>
<p><input type="search" id="q" placeholder="Filter, e.g. teacher, shift, policy" aria-label="Filter audiences"></p>
{''.join(secs)}
<p class="small muted">Source: <code>taxonomy/audiences.csv</code>. Also as <a href="data/audiences.ttl">Turtle</a>, <a href="data/audiences.jsonld">JSON-LD</a>, <a href="data/audiences.csv">CSV</a>.</p>"""
    js = """<script>document.getElementById('q').addEventListener('input',function(){var q=this.value.toLowerCase();
document.querySelectorAll('tr[data-q]').forEach(function(r){r.style.display=!q||r.dataset.q.indexOf(q)>-1?'':'none'})});</script>"""
    return page("audiences.html", "Audiences", body, js)


def scheme_table(rows, extra=None):
    trs = []
    for r in rows:
        sub = bool(r.get("broader"))
        cells = f'<td class="{"sub" if sub else ""}">{"↳ " if sub else ""}<b>{e(r["pref_label"])}</b><div class="small muted">{e(", ".join(split(r.get("alt_labels", ""))))}</div></td>'
        cells += f'<td>{e(r.get("definition", ""))}{"<div class=small><i>e.g. " + e(r["example"]) + "</i></div>" if r.get("example") else ""}'
        cells += f'{"<div class=\'small muted\'>" + e(r["notes"]) + "</div>" if r.get("notes") else ""}</td>'
        if extra:
            cells += extra(r)
        trs.append(f"<tr>{cells}</tr>")
    return trs


def communication(refs):
    rows = read("vocab/communication-direction.csv")
    body = f"""<h1>Communication direction</h1>
<p class="lede">Who is talking to whom. This is not a level of influence: pair it with an audience role, which says <i>which</i> professional and so which level.</p>
<p>SleepLiteracy's <code>Pro2Pro</code> tag means <b>professional to professional</b>, a very large category. It is split here by what the professional does with the resource.</p>
{tbl(["Direction", "Means", "SleepLiteracy tag"], scheme_table(rows, lambda r: f'<td class="small">{e(r.get("sleepliteracy_seed", ""))}</td>'))}
<p class="small muted">Source: <code>vocab/communication-direction.csv</code>. Also as <a href="data/communication-direction.ttl">Turtle</a>, <a href="data/communication-direction.jsonld">JSON-LD</a>.</p>"""
    return page("communication.html", "Communication direction", body)


AXES = [("phases", "A", "Advocacy phase", False), ("tactics", "B", "Tactic", False), ("targets", "C", "Target", False),
        ("jurisdiction", "D", "Jurisdiction", False), ("venue", "E", "Decision venue", False), ("outcomes", "F", "Outcome sought", False),
        ("goal-type", "G", "Policy goal type", True), ("theory-of-change", "H", "Theory of change", True)]


def advocacy(refs):
    phases = [p for p in read("vocab/advocacy/phases.csv") if not p["notation"].startswith("x")]
    cross = [p for p in read("vocab/advocacy/phases.csv") if p["notation"].startswith("x")]
    _, _, fw = read_sssom("crosswalks/policy-frameworks-to-advocacy-phases.sssom.tsv")
    _, _, gh = read_sssom("crosswalks/ghai-steps-to-advocacy-phases.sssom.tsv")

    def col(maps, prefix, pid):
        hits = [m for m in maps if m["subject_id"].startswith(prefix) and m["object_id"] == "hcfph:" + pid]
        return "<br>".join(f'{e(m["subject_label"])}{" <span class=muted>(related)</span>" if "related" in m["predicate_id"] else ""}' for m in hits) or '<span class="muted">—</span>'

    xrows = []
    for p in phases + cross:
        ghai = [m for m in gh if m["object_id"] == "hcfph:" + p["id"] and "step" in m["subject_id"]]
        xrows.append(f'<tr><td><b>{p["notation"] if not p["notation"].startswith("x") else "any"}. {e(p["pref_label"])}</b></td>'
                     f'<td>{col(fw, "cdcpp:", p["id"])}</td><td>{col(fw, "cycle:", p["id"])}</td><td>{col(fw, "kingdon:", p["id"])}</td>'
                     f'<td>{col(fw, "hfrp:", p["id"])}</td><td>{"<br>".join(e(m["subject_label"]) for m in ghai) or "—"}</td></tr>')
    axes_html = []
    for f, letter, title, opt in AXES:
        rows = read(f"vocab/advocacy/{f}.csv")
        trs = scheme_table(rows, lambda r: f'<td class="small">{", ".join("<code>" + e(a) + "</code>" for a in split(r.get("audiences", "")))}</td>'
                           f'<td class="small muted">{e(r.get("informed_by", ""))}</td>')
        axes_html.append(f'<h3 id="{f}">{letter}. {e(title)}{" <span class=pill>optional</span>" if opt else ""}</h3>'
                         + tbl(["Value", "Means", "Links to audiences", "Informed by"], trs))
    body = f"""<h1>Advocacy framework</h1>
<p class="lede">For resources at the public-policy level: where in the advocacy process does this help, and how?</p>
<div class="grid2">
<div class="box"><b>Simple: tag one phase.</b><ol style="margin:6px 0 0;padding-left:20px">{''.join(f"<li>{e(p['pref_label'])}</li>" for p in phases)}</ol>
<p class="small">Plus two tags for work at any phase: <i>{e(cross[0]['pref_label'])}</i>, <i>{e(cross[1]['pref_label'])}</i>.</p></div>
<div class="box"><b>Full: add any other axis.</b> Each axis is separate, so one resource can carry several tags.
<p class="small">A guide to testifying at a city council hearing: <i>Win the decision</i> × <i>Testify and brief</i> × <i>Decision-makers</i> × <i>City or county</i> × <i>Legislature or council</i> × <i>Political will</i>.</p>
<p class="small">Axes: {' · '.join(f'<a href="#{f}">{letter} {e(t)}</a>' for f, letter, t, _ in AXES)}</p></div>
</div>
<h2>How the phases line up with other frameworks</h2>
<p class="small muted">The phases are written in HCF's own words on top of CDC's public-domain Policy Process {ref('cdc-policy-process', refs)},
the policy cycle {ref('lasswell1956', refs)} {ref('jann2007', refs)} and Kingdon's multiple streams {ref('kingdon1984', refs)}, checked against
the Composite Logic Model's policy goals {ref('coffman2009', refs)}. GHAI's <i>Advocacy Action Guide</i> {ref('ghai2024', refs)} may be shared but not adapted,
so its step names appear here only as matching labels.</p>
{tbl(["HCF phase", "CDC Policy Process", "Policy cycle", "Kingdon", "HFRP policy goals", "GHAI steps (labels)"], xrows)}
<h2>The axes</h2>
<p class="small muted">All labels and definitions are HCF's wording. "Informed by" names where a category idea came from; no text is copied.</p>
{''.join(axes_html)}"""
    return page("advocacy.html", "Advocacy", body)


def crosswalks(refs):
    files = sorted((ROOT / "crosswalks").glob("*.sssom.tsv"))
    secs, toc = [], []
    for p in files:
        title, comment, rows = read_sssom(f"crosswalks/{p.name}")
        anchor = p.name.replace(".sssom.tsv", "")
        toc.append(f'<li><a href="#{anchor}">{e(title)}</a> <span class="muted small">({len(rows)})</span></li>')
        trs = [f'<tr><td><code>{e(r["subject_id"])}</code><div class="small">{e(r["subject_label"])}</div></td>'
               f'<td><span class="pill">{e(r["predicate_id"].replace("skos:", ""))}</span></td>'
               f'<td><code>{e(r["object_id"])}</code><div class="small">{e(r["object_label"])}</div></td>'
               f'<td class="small muted">{e(r.get("comment", "") or "")}</td></tr>' for r in rows]
        secs.append(f'<h2 id="{anchor}">{e(title)}</h2><p class="small muted">{e(comment)}</p>'
                    f'<p class="small"><a href="data/{p.name}">Download SSSOM</a></p>' + tbl(["From", "Match", "To", "Note"], trs))
    body = f"""<h1>Crosswalks</h1>
<p class="lede">How these vocabularies line up with others, as SSSOM mapping files {ref('sssom2022', refs)}. Match types are SKOS {ref('skos', refs)}:
<b>exact</b> (interchangeable), <b>close</b> (good for search), <b>broad</b>/<b>narrow</b> (the other side is more general/specific), <b>related</b> (associated).</p>
<ul>{''.join(toc)}</ul>{''.join(secs)}"""
    return page("crosswalks.html", "Crosswalks", body)


def references(refs):
    groups = {}
    for r in refs.values():
        groups.setdefault(r["group"], []).append(r)
    secs = []
    for g, rs in groups.items():
        lis = "".join(f'<li id="{r["key"]}" style="margin-bottom:10px">{e(r["citation"])}'
                      f'{" <a href=" + chr(34) + e(r["url"]) + chr(34) + ">" + e(r["url"]) + "</a>" if r["url"] else ""}'
                      f'<div class="small muted">Licence: {e(r["licence"])}. Used for: {e(r["used_for"])}</div></li>' for r in rs)
        secs.append(f"<h2>{e(g)}</h2><ol>{lis}</ol>")
    sleep = read("research/sleep-research-tagging/sources.csv")
    lis = "".join(f'<li>{e(s["source"])}{" · " + (chr(60) + "a href=" + chr(34) + e(s["url_or_doi"]) + chr(34) + chr(62) + e(s["url_or_doi"]) + "</a>" if s["url_or_doi"].startswith("http") else e(s["url_or_doi"])) if s["url_or_doi"] else ""}</li>' for s in sleep)
    secs.append(f'<h2>Sleep sources sampled for the tagging study</h2><p class="small muted">The 22 studies, guidelines and pages whose audience tagging was examined.</p><ol class="small">{lis}</ol>')
    body = f"""<h1>References</h1>
<p class="lede">Every source used, with its licence and what it was used for. Where a work is copyrighted, only its ideas are used and it is cited, not copied.</p>
{''.join(secs)}"""
    return page("references.html", "References", body)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "data").mkdir(parents=True)
    levels = read("vocab/ecological-levels.csv")
    cdc = read("vocab/cdc-sem-levels.csv")
    aud = read("taxonomy/audiences.csv")
    refs = {r["key"]: r for r in read("references.csv")}
    for name, html_ in [("index.html", index(levels, cdc, aud, refs)), ("audiences.html", audiences(levels, aud)),
                        ("communication.html", communication(refs)), ("advocacy.html", advocacy(refs)),
                        ("crosswalks.html", crosswalks(refs)), ("references.html", references(refs))]:
        (OUT / name).write_text(html_, encoding="utf-8")
        print("wrote docs/" + name)
    files = list((ROOT / "vocab").glob("*.*")) + list((ROOT / "vocab/advocacy").glob("*.*")) + list((ROOT / "taxonomy").glob("*.*")) + list((ROOT / "crosswalks").glob("*.tsv"))
    links = []
    for f in sorted(files):
        if f.suffix in (".csv", ".ttl", ".jsonld", ".tsv"):
            dest = OUT / "data" / (("advocacy-" if f.parent.name == "advocacy" else "") + f.name)
            shutil.copy(f, dest)
            links.append(f'<li><a href="{dest.name}">{dest.name}</a></li>')
    data_page = page("data/index.html", "Data files",
                     "<h1>Data files</h1><p>CC BY 4.0. CSV is the source; Turtle and JSON-LD are SKOS; TSV files are SSSOM crosswalks.</p>"
                     f"<ul>{''.join(links)}</ul>")
    for f, _ in PAGES:  # nav links point one level up from data/
        data_page = data_page.replace(f'href="{f}', f'href="../{f}')
    data_page = data_page.replace('href="data/"', 'href="./"')
    (OUT / "data/index.html").write_text(data_page, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    md = ["# References", "", "_Generated by `scripts/site.py` from [`references.csv`](references.csv). Also on the site's references page._", ""]
    groups = {}
    for r in refs.values():
        groups.setdefault(r["group"], []).append(r)
    for g, rs in groups.items():
        md += [f"## {g}", ""]
        for r in rs:
            url = f" <{r['url']}>" if r["url"] else ""
            md.append(f"- <a id=\"{r['key']}\"></a>**[{r['short']}]** {r['citation']}{url}  \n  _Licence:_ {r['licence']}. _Used for:_ {r['used_for']}")
        md.append("")
    md += ["## Sleep sources sampled for the tagging study", "", "See [`research/sleep-research-tagging/sources.csv`](research/sleep-research-tagging/sources.csv) (22 sources).", ""]
    (ROOT / "REFERENCES.md").write_text("\n".join(md), encoding="utf-8")
    print("wrote REFERENCES.md")
    print("wrote docs/data/ (", len(links), "files )")


if __name__ == "__main__":
    main()
