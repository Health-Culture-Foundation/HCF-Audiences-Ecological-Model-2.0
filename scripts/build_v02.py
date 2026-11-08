#!/usr/bin/env python3
"""Build Audience v0.2 outputs from taxonomy/v0.2/audiences-v0.2.csv and taxonomy/v0.2/partners/*.csv.

Outputs (generated, don't edit):
  taxonomy/v0.2/audiences-v0.2.json     plain tree for websites (hcfhub.org copies this)
  taxonomy/v0.2/audiences-v0.2.jsonld   SKOS
  taxonomy/v0.2/AUDIENCES-v0.2.md       readable view
  crosswalks/v0.2/*.sssom.tsv           code crosswalks (SOC, ISCO, NUCC, MeSH, OMB, v0.1) and partner crosswalks
  crosswalks/v0.2/audiences-to-pubmed-age-filters.sssom.tsv   age bands to PubMed's age filters (taxonomy/v0.2/pubmed-age-filters.csv)
  crosswalks/v0.2/audiences-to-{icd10cm,snomed,loinc-answers}.sssom.tsv   Who it's about to clinical codes (taxonomy/v0.2/clinical-codes.csv)
  taxonomy/v0.2/fhir/                   HL7 FHIR: CodeSystem, a useContext per concept, and definitional Groups (R4 and R5)

Python 3.10+, standard library only:  python3 -I scripts/build_v02.py
"""
import csv
import html
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
    "gravity-sdoh-category": ("sdohcc", "http://hl7.org/fhir/us/sdoh-clinicalcare/CodeSystem/SDOHCC-CodeSystemTemporaryCodes#", "Gravity Project SDOH domains (SDOH Clinical Care IG 3.0.0, ValueSet SDOHCC-ValueSetSDOHCategory)"),
}
# FHIR systems. clinical-codes.csv names them by the short key.
FHIR_SYS = {
    "hcfaud": "https://health-culture.org/vocab/audiences-v0.2",
    "icd10cm": "http://hl7.org/fhir/sid/icd-10-cm",
    "snomed": "http://snomed.info/sct",
    "loinc": "http://loinc.org",
    "nucc": "http://nucc.org/provider-taxonomy",
    "gender": "http://hl7.org/fhir/administrative-gender",
    "uct": "http://terminology.hl7.org/CodeSystem/usage-context-type",
}
CLINICAL = {  # system key in clinical-codes.csv: (file stem, curie prefix, base IRI, title)
    "icd10cm": ("audiences-to-icd10cm", "icd10cm", "http://hl7.org/fhir/sid/icd-10-cm#", "ICD-10-CM"),
    "snomed": ("audiences-to-snomed", "sct", "http://snomed.info/id/", "SNOMED CT findings"),
    "loinc": ("audiences-to-loinc-answers", "loinc", "https://loinc.org/", "LOINC screening answers (question=answer)"),
}
# Lifestyle medicine instruments (hcfhub.org#137): questions an EHR already asks, and which answers say who a
# resource should be about. instruments/<id>.csv holds one row per item (an item can repeat with a different
# rule, e.g. by sex); the answer types below give each item's options and the value each option stands for.
INSTRUMENTS = {
    "aclm-short-assessment": {
        "title": "ACLM Lifestyle Medicine Short Assessment",
        "publisher": "American College of Lifestyle Medicine",
        "source": "https://connect.lifestylemedicine.org/viewdocument/lifestyle-medicine-short-assessment",
        "about": "The patient-completed lifestyle assessment in ACLM's Epic Foundation build (Lifestyle Medicine Whole Person Health Index, "
                 "Nova release note 923516, May 2026) and in eClinicalWorks 12.0.4 (Nov 2026). Items follow ACLM's Short Assessment Form "
                 "(2024), which embeds the Physical Activity Vital Sign and the PHQ-2. Labels here are short paraphrases, not ACLM's wording.",
        "copyright": "Instrument (c) 2024 American College of Lifestyle Medicine, adapted from the Loma Linda University/ACLM short form (2019). "
                     "PHQ-2 (c) Pfizer, free to use. Item labels are paraphrased; use ACLM's form for the questions as asked. "
                     "Cut-offs and mappings to HCF Audiences are Health Culture Foundation's (CC BY 4.0) and unreviewed.",
    },
}
ITEM_SYS = "https://health-culture.org/vocab/audiences-v0.2/lifestyle-items"
ANSWERS = {  # answer type: [(value, label, LOINC answer code)]
    "scale-0-10": [(i, str(i), "") for i in range(11)],
    "often-6": [(0, "Never", ""), (1, "Less than once a week", ""), (2, "1-3 times a week", ""), (3, "4-6 times a week", ""),
                (4, "1-2 times a day", ""), (5, "More than 3 times a day", "")],
    "freq-4": [(0, "Not at all", "LA6568-5"), (1, "Several days", "LA6569-3"), (2, "More than half the days", "LA6570-1"), (3, "Nearly every day", "LA6571-9")],
    "sleep-hours": [(3.5, "Less than 4 hours", ""), (4.5, "4-5 hours", ""), (5.5, "5-6 hours", ""), (6.5, "6-7 hours", ""), (7.5, "7-8 hours", ""),
                    (8.5, "8-9 hours", ""), (9.5, "9 hours or more", "")],
    "yes-no": [(1, "Yes", "LA33-6"), (0, "No", "LA32-8")],
    "pillars": [("nutrition", "Nutrition", ""), ("physical-activity", "Physical activity", ""), ("sleep", "Sleep", ""), ("stress", "Stress management", ""),
                ("connectedness", "Social connectedness", ""), ("risky-substances", "Avoiding risky substances", "")],
    "protein": [(k, k.replace("-", " ").capitalize(), "") for k in ("beef-pork-lamb", "processed-meat", "poultry", "wild-game", "nuts-seeds", "fish-seafood",
                                                                    "beans-legumes", "dairy", "eggs")],
    "number": [],
}
FOCUS = {"nutrition", "physical-activity", "sleep", "stress", "connectedness", "risky-substances", "tobacco", "alcohol", "cannabis", "drugs"}
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

    # Clinical codes and FHIR context (hcfhub.org#137): Who it's about values as a clinician's record states them,
    # so a site can match a patient's coded situation to resources. ICD-10-CM codes were checked at NLM Clinical
    # Tables; SNOMED and LOINC codes come from the Gravity SDOHCC 3.0.0 package examples. match: exact | prefix |
    # answer (LOINC question=answer).
    clinical = list(csv.DictReader(open(SRC / "clinical-codes.csv", encoding="utf-8")))
    context = list(csv.DictReader(open(SRC / "fhir-context.csv", encoding="utf-8")))
    for x in clinical + context:
        assert x["id"] in by and by[x["id"]]["axis"] == "about", f"{x['id']} is not an about id"
    for x in clinical:
        assert x["system"] in CLINICAL and x["match"] in ("exact", "prefix", "answer"), x
    codes_of, ctx_of = {}, {}
    for x in clinical:
        codes_of.setdefault(x["id"], []).append(x)
    for x in context:
        ctx_of.setdefault(x["id"], {})[x["context"]] = x["value"]
    gravity = {}
    for g in csv.DictReader(open(SRC / "partners/gravity-sdoh-category.csv", encoding="utf-8")):
        if g["target_id"]:
            gravity.setdefault(g["target_id"], []).append(g["source_id"])

    def age_range(v):
        lo, hi = v.split("-")
        return int(lo), (int(hi) if hi else None)

    instruments = {}
    for iid, meta in INSTRUMENTS.items():
        items = list(csv.DictReader(open(SRC / "instruments" / f"{iid}.csv", encoding="utf-8")))
        for x in items:
            assert x["answer"] in ANSWERS, f"{iid}/{x['item']}: unknown answer type {x['answer']}"
            for g in split(x["gives"]):
                k, v = g.split(":")
                assert (k == "focus" and (v in FOCUS or v == "*")) or (k in ("about", "stage") and v in by and by[v]["axis"] == ("about" if k == "about" else "stage")), f"{iid}/{x['item']}: bad gives {g}"
        instruments[iid] = {**meta, "items": items}

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
        if "age" in ctx_of.get(r["id"], {}):
            c["ages"] = list(age_range(ctx_of[r["id"]]["age"]))
        if "gender" in ctx_of.get(r["id"], {}):
            c["gender"] = ctx_of[r["id"]]["gender"]
        if r["id"] in codes_of:
            c["clinical"] = [{"system": x["system"], "code": x["code"], "match": x["match"], "display": x["display"]} for x in codes_of[r["id"]]]
        if r["id"] in gravity:
            c["gravity"] = gravity[r["id"]]
        concepts.append(c)
    (SRC / "audiences-v0.2.json").write_text(json.dumps({
        "_about": "HCF Audiences v0.2. Generated by scripts/build_v02.py from audiences-v0.2.csv. CC BY 4.0, Health Culture Foundation.",
        "version": "0.2", "axes": {k: {"label": v[0], "definition": v[1]} for k, v in AXES.items()},
        "concepts": concepts,
        "answers": {k: [{"value": v, "label": l, **({"loinc": c} if c else {})} for v, l, c in opts] for k, opts in ANSWERS.items()},
        "instruments": {iid: {**{k: v for k, v in m.items() if k != "items"}, "items": [
            {k: v for k, v in {"item": x["item"], "section": x["section"], "label": x["label"], "answer": x["answer"], "loinc": x["loinc"], "unit": x["unit"],
             "from": x["from"], "sex": x["sex"], "rule": x["rule"], "gives": split(x["gives"]), "basis": x["basis"]}.items() if v} for x in m["items"]]}
            for iid, m in instruments.items()}}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

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

    # Who it's about to clinical codes. A prefix row stands for every code under it.
    for key, (stem, cp, iri, title) in CLINICAL.items():
        sssom(OUT_X / f"{stem}.sssom.tsv", {**pfx, cp: iri}, f"HCF Audiences v0.2 to {title}",
              [[f"hcfaud:{x['id']}", by[x["id"]]["label"], "skos:relatedMatch" if x["match"] != "exact" else "skos:closeMatch", f"{cp}:{x['code']}", x["display"],
                "semapv:ManualMappingCuration", "Claude (unreviewed)", "2026-11-07", f"match: {x['match']}. Source: {x['source']}."] for x in clinical if x["system"] == key])

    fhir(rows, by, codes_of, ctx_of, age_range, instruments)

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


def fhir(rows, by, codes_of, ctx_of, age_range, instruments):
    """HL7 FHIR views of the vocabulary, in taxonomy/v0.2/fhir/.

    - CodeSystem-hcf-audiences-v0.2.json: the whole vocabulary as one is-a hierarchy (R4; valid in R5).
    - usage-context.json: for each concept, the UsageContext a resource tagged with it carries (usage-context-type:
      For -> user, with NUCC codes where we have them; age bands -> age as a Range in years; sex -> gender;
      everything else on About and Stage -> focus, with its clinical codes).
    - Bundle-Group-R4.json / -R5.json: a definitional Group for each Who it's about concept, the people it is about
      (R4 actual=false; R5 membership=definitional). Several codes in one characteristic mean any of them.
    - Questionnaire-<instrument>.json: each lifestyle instrument as an R4 Questionnaire, items coded with LOINC where
      LOINC has the question and with our lifestyle-items codes otherwise, so a QuestionnaireResponse from an EHR can be read.
    Groups describe a kind of person. They never list members: the vocabulary carries no data about anyone.
    """
    out = SRC / "fhir"
    out.mkdir(exist_ok=True)
    S = FHIR_SYS
    narrative = lambda t: {"status": "generated", "div": f'<div xmlns="http://www.w3.org/1999/xhtml">{html.escape(t)}</div>'}
    ours = lambda r: {"system": S["hcfaud"], "code": r["id"], "display": r["label"]}
    uct = lambda code: {"system": S["uct"], "code": code}

    def nest(parent):
        res = []
        for r in rows:
            if (r["parent"] or None) == parent:
                n = {"code": r["id"], "display": r["label"]}
                if r["definition"]:
                    n["definition"] = r["definition"]
                n["property"] = [{"code": "axis", "valueString": r["axis"]}]
                kids = nest(r["id"])
                if kids:
                    n["concept"] = kids
                res.append(n)
        return res
    write = lambda name, obj: (out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write("CodeSystem-hcf-audiences-v0.2.json", {
        "resourceType": "CodeSystem", "id": "hcf-audiences-v0.2", "url": S["hcfaud"], "version": "0.2", "name": "HCFAudiences",
        "title": "HCF Audiences v0.2", "text": narrative(f"HCF Audiences v0.2: {len(rows)} concepts on three axes (for, about, stage)."), "status": "draft", "experimental": True, "publisher": "Health Culture Foundation",
        "description": "Who a health resource is for, who it is about, and where they are with the behavior. Group-level descriptions only: no concept identifies a person.",
        "copyright": "CC BY 4.0", "caseSensitive": True, "hierarchyMeaning": "is-a", "content": "complete", "count": len(rows),
        "property": [{"code": "axis", "type": "string", "description": "for (who it's for; also messenger), about (who it's about) or stage"}],
        "concept": nest(None)})

    def codings(r):
        cs = [ours(r)]
        for x in codes_of.get(r["id"], []):
            if x["match"] != "answer":
                cs.append({"system": S[x["system"]], "code": x["code"], "display": x["display"]})
        return cs

    def contexts(r):
        ctx = ctx_of.get(r["id"], {})
        if r["axis"] == "for":
            return [{"code": uct("user"), "valueCodeableConcept": {"coding": [ours(r)] + [{"system": S["nucc"], "code": n} for n in split(r["nucc"])], "text": r["label"]}}]
        if "age" in ctx:
            lo, hi = age_range(ctx["age"])
            rng = {"low": {"value": lo, "unit": "years", "system": "http://unitsofmeasure.org", "code": "a"}}
            if hi is not None:
                rng["high"] = {"value": hi, "unit": "years", "system": "http://unitsofmeasure.org", "code": "a"}
            return [{"code": uct("age"), "valueRange": rng}]
        if "gender" in ctx:
            return [{"code": uct("gender"), "valueCodeableConcept": {"coding": [{"system": S["gender"], "code": ctx["gender"]}, ours(r)], "text": r["label"]}}]
        return [{"code": uct("focus"), "valueCodeableConcept": {"coding": codings(r), "text": r["label"]}}]
    write("usage-context.json", {
        "_about": "For each HCF Audiences v0.2 concept, the FHIR UsageContext (R4/R5) a resource tagged with it carries. Generated by scripts/build_v02.py.",
        "useContext": {r["id"]: contexts(r) for r in rows}})

    def group(r, release):
        ch = []
        for u in contexts(r):
            c = {"code": {"coding": [u["code"]]}, "exclude": False}  # Group.characteristic.code is a CodeableConcept; UsageContext.code a Coding
            c.update({k: v for k, v in u.items() if k.startswith("value")})
            ch.append(c)
        g = {"resourceType": "Group", "id": f"hcfaud-{r['id']}", "text": narrative(f"{r['label']}: a definitional group, no members."), "type": "person", "name": r["label"], "code": {"coding": [ours(r)]}, "characteristic": ch}
        if release == "R4":
            g["actual"] = False
        else:
            g["membership"] = "definitional"
            if r["definition"]:
                g["description"] = r["definition"]
        return g
    for release in ("R4", "R5"):
        write(f"Bundle-Group-{release}.json", {"resourceType": "Bundle", "id": f"hcf-audiences-v0.2-groups-{release.lower()}", "type": "collection",
            "entry": [{"fullUrl": f"{S['hcfaud']}/Group/hcfaud-{r['id']}", "resource": group(r, release)} for r in rows if r["axis"] == "about" and r["parent"]]})

    for iid, m in instruments.items():
        seen, items = set(), []
        for x in m["items"]:
            if x["item"] in seen:
                continue
            seen.add(x["item"])
            code = [{"system": S["loinc"], "code": x["loinc"]}] if x["loinc"] else []
            code.append({"system": ITEM_SYS, "code": x["item"], "display": x["label"]})
            it = {"linkId": x["item"], "code": code, "text": x["label"], "type": "integer" if x["answer"] == "number" else "choice"}
            if x["from"]:
                it.update({"type": "integer", "readOnly": True})
            opts = ANSWERS[x["answer"]]
            if it["type"] == "choice":
                if x["answer"] in ("pillars", "protein"):
                    it["repeats"] = True
                it["answerOption"] = [{"valueCoding": {"system": S["loinc"], "code": c, "display": l} if c else {"system": ITEM_SYS, "code": f"{x['answer']}-{v}", "display": l}} for v, l, c in opts]
            items.append(it)
        sections = []
        for it in items:
            sec = next(x["section"] for x in m["items"] if x["item"] == it["linkId"])
            if not sections or sections[-1]["linkId"] != sec:
                sections.append({"linkId": sec, "text": sec.replace("-", " ").capitalize(), "type": "group", "item": []})
            sections[-1]["item"].append(it)
        write(f"Questionnaire-{iid}.json", {"resourceType": "Questionnaire", "id": iid, "text": narrative(m["title"] + " (paraphrased items)"),
            "url": f"{S['hcfaud']}/Questionnaire/{iid}", "name": "".join(w.capitalize() for w in iid.split("-")), "title": m["title"] + " (paraphrased)",
            "status": "draft", "experimental": True, "publisher": "Health Culture Foundation", "description": m["about"], "copyright": m["copyright"],
            "item": sections})


if __name__ == "__main__":
    main()
