#!/usr/bin/env python3
"""Build Audience v0.2 outputs from taxonomy/v0.2/audiences-v0.2.csv and taxonomy/v0.2/partners/*.csv.

Outputs (generated, don't edit):
  taxonomy/v0.2/audiences-v0.2.json     plain tree for websites (hcfhub.org copies this)
  taxonomy/v0.2/audiences-v0.2.jsonld   SKOS
  taxonomy/v0.2/AUDIENCES-v0.2.md       readable view
  crosswalks/v0.2/*.sssom.tsv           code crosswalks (SOC, ISCO, NUCC, MeSH, OMB, v0.1) and partner crosswalks
  crosswalks/v0.2/audiences-to-pubmed-age-filters.sssom.tsv   age bands to PubMed's age filters (taxonomy/v0.2/pubmed-age-filters.csv)

Python 3.10+, standard library only:  python3 -I scripts/build_v02.py
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "taxonomy/v0.2"
OUT_X = ROOT / "crosswalks/v0.2"
BASE = "https://health-culture.org/vocab/audiences-v0.2/"
DATE = "2026-10-28"
AXES = {
    "for": ("Who it's for", "Who the resource speaks to: the person meant to read, watch or act. The same tree names who carries the message (messenger)."),
    "about": ("Who it's about", "Whose health it is about. Only groups the resource names."),
    "stage": ("Where they are with it", "Where the audience is with the behavior, from not started to in recovery."),
}
CODES = {  # column: (file stem, curie prefix, base IRI, label)
    "soc": ("audiences-to-soc2018", "soc", "https://www.bls.gov/soc/2018/#", "US Standard Occupational Classification 2018"),
    "isco": ("audiences-to-isco08", "isco", "http://data.europa.eu/esco/isco/C", "ILO ISCO-08"),
    "nucc": ("audiences-to-nucc", "nucc", "https://taxonomy.nucc.org/?searchTerm=", "NUCC Health Care Provider Taxonomy"),
    "mesh": ("audiences-to-mesh", "mesh", "http://id.nlm.nih.gov/mesh/", "MeSH"),
    "omb": ("audiences-to-omb-spd15-2024", "omb", "https://spd15revision.gov/#", "OMB SPD 15 (2024) minimum categories"),
    "v01": ("audiences-v0.2-to-v0.1", "hcfaud01", "https://health-culture.org/vocab/audiences/", "HCF audiences v0.1"),
}
PARTNERS = {  # file stem: (curie prefix, base IRI, title)
    "hcfhub-campaigns-v1": ("hcfcase", "https://hcfhub.org/vocab/audience/", "hcfhub.org campaign audience ids before v0.2"),
    "sleepliteracy": ("sl", "https://sleepliteracy.org/taxonomy/audience/", "SleepLiteracy.org audience terms"),
    "samhsa-ebprc": ("samhsa", "https://www.samhsa.gov/libraries/evidence-based-practices-resource-center#", "SAMHSA Evidence-Based Practices Resource Center filters (partial)"),
    "lrmi-educational-audience-role": ("lrmi", "http://purl.org/dcx/lrmi-vocabs/educationalAudienceRole/", "LRMI educational audience role"),
    "schema-org": ("schema", "https://schema.org/", "schema.org audience types"),
    "train-course-audience": ("traincourse", "urn:hcf:train:course-audience:", "TRAIN Learning Network course audience filter (Massachusetts TRAIN, 2026-10-29)"),
    "train-profile-role": ("trainrole", "urn:hcf:train:profile-role:", "TRAIN Learning Network learner profile roles (2026-10-29)"),
    "train-credit-types": ("traincredit", "urn:hcf:train:credit-type:", "TRAIN Learning Network credit types; the profession each credit is for"),
}
HEAD = ["subject_id", "subject_label", "predicate_id", "object_id", "object_label", "mapping_justification", "author_label", "mapping_date", "comment"]


def split(s):
    return [x for x in (s or "").split("|") if x]


def load():
    rows = list(csv.DictReader(open(SRC / "audiences-v0.2.csv", encoding="utf-8")))
    ids = {r["id"] for r in rows}
    assert len(ids) == len(rows), "duplicate ids"
    for r in rows:
        assert r["axis"] in AXES, f"{r['id']}: bad axis {r['axis']}"
        assert not r["parent"] or r["parent"] in ids, f"{r['id']}: missing parent {r['parent']}"
    return rows


def sssom(path, prefixes, title, lines):
    head = [f"# title: {title}", "# license: https://creativecommons.org/licenses/by/4.0/", "# curie_map:"]
    head += [f"#   {k}: {v}" for k, v in prefixes.items()]
    head += ["#   skos: http://www.w3.org/2004/02/skos/core#", "#   semapv: https://w3id.org/semapv/vocab/"]
    body = ["\t".join(HEAD)] + ["\t".join(str(x) for x in l) for l in lines]
    path.write_text("\n".join(head + body) + "\n", encoding="utf-8")


def main():
    rows = load()
    by = {r["id"]: r for r in rows}

    # PubMed age filters (hcfhub.org#137): each age band's MeSH age headings and the PubMed filter tags that
    # search them, so a site can build a PubMed link from a Who it's about value. MeSH ids and age ranges were
    # checked at id.nlm.nih.gov; each tag was checked against PubMed E-utilities (adolescent[filter] = adolescent[mh]).
    ages = list(csv.DictReader(open(SRC / "pubmed-age-filters.csv", encoding="utf-8")))
    for a in ages:
        assert a["id"] in by and by[a["id"]]["axis"] == "about", f"pubmed-age-filters: {a['id']} is not an about id"
    pubmed = {}
    for a in ages:
        pubmed.setdefault(a["id"], []).append(a)

    # Plain JSON tree for websites.
    concepts = []
    for r in rows:
        c = {"id": r["id"], "label": r["label"], "parent": r["parent"] or None, "axis": r["axis"]}
        for k in ("soc", "isco", "nucc", "mesh", "omb"):
            if r[k]:
                c[k] = split(r[k])
        if r["v01"]:
            c["v01"] = r["v01"]
        if r["definition"]:
            c["definition"] = r["definition"]
        if r["id"] in pubmed:
            ps = pubmed[r["id"]]
            c["pubmed"] = {"mesh": [p["mesh"] for p in ps], "filter": " OR ".join(f"{p['pubmed_filter']}[filter]" for p in ps)}
        concepts.append(c)
    (SRC / "audiences-v0.2.json").write_text(json.dumps({
        "_about": "HCF Audiences v0.2. Generated by scripts/build_v02.py from audiences-v0.2.csv. CC BY 4.0, Health Culture Foundation.",
        "version": "0.2", "axes": {k: {"label": v[0], "definition": v[1]} for k, v in AXES.items()},
        "concepts": concepts}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # SKOS JSON-LD.
    graph = [{"id": BASE + ax, "type": "skos:ConceptScheme", "prefLabel": t, "definition": d} for ax, (t, d) in AXES.items()]
    for r in rows:
        n = {"id": BASE + r["id"], "type": "skos:Concept", "prefLabel": r["label"], "inScheme": BASE + r["axis"]}
        if r["parent"]:
            n["broader"] = BASE + r["parent"]
        else:
            n["topConceptOf"] = BASE + r["axis"]
        if r["definition"]:
            n["definition"] = r["definition"]
        if r["mesh"]:
            n["closeMatch"] = [CODES["mesh"][2] + m for m in split(r["mesh"])]
        graph.append(n)
    ctx = {"skos": "http://www.w3.org/2004/02/skos/core#", "id": "@id", "type": "@type",
           "prefLabel": {"@id": "skos:prefLabel", "@language": "en"}, "definition": {"@id": "skos:definition", "@language": "en"},
           "inScheme": {"@id": "skos:inScheme", "@type": "@id"}, "broader": {"@id": "skos:broader", "@type": "@id"},
           "topConceptOf": {"@id": "skos:topConceptOf", "@type": "@id"}, "closeMatch": {"@id": "skos:closeMatch", "@type": "@id"}}
    (SRC / "audiences-v0.2.jsonld").write_text(json.dumps({"@context": ctx, "@graph": graph}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    # Markdown view.
    def depth(r):
        d, p = 0, r["parent"]
        while p:
            d, p = d + 1, by[p]["parent"]
        return d
    md = ["# HCF Audiences v0.2", "", "Generated by `scripts/build_v02.py` from `audiences-v0.2.csv`. Codes are stored for crosswalks, never shown as labels.", ""]
    for ax, (t, d) in AXES.items():
        md += [f"## {t}", "", d, ""]
        for r in rows:
            if r["axis"] != ax:
                continue
            codes = " · ".join(f"{k.upper()} {', '.join(split(r[k]))}" for k in ("soc", "isco", "nucc", "mesh", "omb") if r[k])
            md.append("  " * depth(r) + f"- **{r['label']}** `{r['id']}`" + (f" — {codes}" if codes else ""))
        md.append("")
    (SRC / "AUDIENCES-v0.2.md").write_text("\n".join(md), encoding="utf-8")

    # Code crosswalks.
    OUT_X.mkdir(parents=True, exist_ok=True)
    pfx = {"hcfaud": BASE}
    for col, (stem, cp, iri, title) in CODES.items():
        lines = []
        for r in rows:
            for code in split(r[col]):
                lines.append([f"hcfaud:{r['id']}", r["label"], "skos:closeMatch", f"{cp}:{code}", "", "semapv:ManualMappingCuration", "Claude (unreviewed)", DATE, ""])
        sssom(OUT_X / f"{stem}.sssom.tsv", {**pfx, cp: iri}, f"HCF Audiences v0.2 to {title}", lines)

    # Age bands to PubMed: object is the MeSH age heading; pubmed_filter is the search tag for it.
    sssom(OUT_X / "audiences-to-pubmed-age-filters.sssom.tsv", {**pfx, "mesh": CODES["mesh"][2]}, "HCF Audiences v0.2 age bands to PubMed age filters",
          [[f"hcfaud:{a['id']}", by[a["id"]]["label"], a["predicate"], f"mesh:{a['mesh']}", a["mesh_label"], "semapv:ManualMappingCuration", "Claude (unreviewed)", "2026-10-29",
            f"PubMed filter {a['pubmed_filter']}[filter] ({a['mesh_ages']}). {a['comment']}".strip()] for a in ages])

    # Partner crosswalks: their term on the left, ours on the right.
    for stem, (cp, iri, title) in PARTNERS.items():
        lines = []
        for p in csv.DictReader(open(SRC / "partners" / f"{stem}.csv", encoding="utf-8")):
            t = p["target_id"]
            assert not t or t in by, f"{stem}: unknown target {t}"
            lines.append([f"{cp}:{p['source_id'].replace(' ', '%20')}", p["source_label"], p["predicate"] or "semapv:NoMapping",
                          f"hcfaud:{t}" if t else "", by[t]["label"] if t else "", "semapv:ManualMappingCuration", "Claude (unreviewed)", DATE, p["comment"]])
        sssom(OUT_X / f"{stem}-to-audiences-v0.2.sssom.tsv", {cp: iri, **pfx}, f"{title} to HCF Audiences v0.2", lines)

    print(f"{len(rows)} concepts:", {ax: sum(r['axis'] == ax for r in rows) for ax in AXES})


if __name__ == "__main__":
    main()
