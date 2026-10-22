# HCF Audiences: Ecological Model 2.0

A shared way to tag **who a health resource is for, and who acts on it**,
organized by the five levels of influence of the socio-ecological model. Any
library, glossary or website can use it. Sleep is the first worked example.

**Status: draft 0.1.** Private for now. Researched and drafted by Claude
(Claude Code) for the Health Culture Foundation; nothing here has been
reviewed by a person yet. Tracking issue: #1.

Part of the [Open Health Communication Declaration](https://github.com/vivwebsolutions/hcf-guides/issues/6),
which promises an "ecological tagging vocabulary" built on the five levels.

## What's in it

**Browse the audiences: [taxonomy/AUDIENCES.md](taxonomy/AUDIENCES.md)**

| Path | What it is |
|---|---|
| [`vocab/ecological-levels.*`](vocab/) | The five levels of influence (McLeroy, Bibeau, Steckler & Glanz 1988, [doi:10.1177/109019818801500401](https://doi.org/10.1177/109019818801500401)), as presented in NCI's public-domain [*Theory at a Glance*](https://cancercontrol.cancer.gov/sites/default/files/2020-06/theory.pdf) (2005), Table 1. Plain-language labels and definitions, NCI's wording kept as a note. SKOS as Turtle and JSON-LD, built from CSV. |
| [`vocab/cdc-sem-levels.*`](vocab/) | CDC's four-level model (individual, relationship, community, societal), which HCF already uses ([hcf-guides#3](https://github.com/vivwebsolutions/hcf-guides/issues/3)). CDC publishes no URIs, so they're minted here. |
| [`vocab/communication-direction.*`](vocab/communication-direction.csv) | Who is talking to whom: professional to public, **professional to professional** (SleepLiteracy's Pro2Pro, split into guidance, materials to pass on, training, research, running programs), professional to decision-maker, peer to peer, public to professional. |
| [`vocab/advocacy/`](vocab/advocacy/ADVOCACY.md) | **HCF advocacy framework v0.1**: a 7-phase advocacy tag (axis A) that also works as one axis of a fuller framework, with tactic, target, jurisdiction, venue, outcome, and optional goal type and theory of change. Each axis is its own SKOS scheme. Crosswalks to GHAI's steps (labels only), CDC's Policy Process, the policy cycle, Kingdon and HFRP. |
| [`taxonomy/audiences.csv`](taxonomy/audiences.csv) | **Audience taxonomy v0.1**: 62 concepts, each placed at one level. Source of truth. Also as [Turtle](taxonomy/audiences.ttl) and [JSON-LD](taxonomy/audiences.jsonld). |
| [`crosswalks/`](crosswalks/) | SSSOM mapping files: five levels → CDC four; levels → MeSH; levels → Viv Resource Library *What Works* facet; audiences → MeSH, → LRMI roles; SleepLiteracy's tags → audiences. |
| [`research/sleepliteracy-tags/`](research/sleepliteracy-tags/) | Inventory of SleepLiteracy.org's three audience taxonomies (46 terms), the seed for v0.1. |
| [`research/vocabularies.md`](research/vocabularies.md) | Existing audience vocabularies we align with: schema.org, LRMI, MeSH Persons (M01), ERIC, Healthy People 2030, and our own issues. |
| [`research/sleep-research-tagging/`](research/sleep-research-tagging/) | **Findings:** how 22 sleep studies, guidelines and web pages tag their audiences. |
| [`research/example-orgs/`](research/example-orgs/) | 22 example organizations across the five levels. |
| [`research/advocacy-frameworks/`](research/advocacy-frameworks/README.md) | Research behind the advocacy framework: 12 frameworks with licences checked, and a draft note asking GHAI to open its guide. |
| [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) | What v0.1 doesn't settle, with the default applied, and numbers to verify. |

## The five levels

| # | Level | Plain label | Who acts here (examples) | CDC four-level |
|---|---|---|---|---|
| 1 | Intrapersonal | The person | the person themselves, patients, learners | Individual |
| 2 | Interpersonal | Close relationships | parents and caregivers, partners, friends and roommates, clinicians one-to-one, teachers and coaches | Relationship |
| 3 | Institutional or organizational | Organizations | school and campus leaders, HR and workplace health staff, health care leaders; schools, employers, clinics | Community |
| 4 | Community | Community | public health practitioners, community health workers, community and faith leaders, communicators, journalists, coalitions, health departments | Community (and Societal, for norms) |
| 5 | Public policy | Policy | policymakers, regulators and agency staff, courts and judges, policy advocates; advocacy organizations, governments | Societal |

The level IDs (`intrapersonal`, `interpersonal`, `institutional`, `community`,
`public-policy`) match the `ecologicalLevel` facet in the Viv Resource
Library's *What Works* taxonomy ([Viv-Resource-Library#35](https://github.com/vivwebsolutions/Viv-Resource-Library/issues/35)),
so a resource's level and its audience's level use one vocabulary.

## Three rules

1. **An audience sits at the level where it acts.** A parent reading about a
   teen's sleep is level 2. A principal changing the bell schedule is level 3.
   A legislator writing a start-time bill is level 5.
2. **Who it's for ≠ who it's about.** *Roles* (parent, school leader,
   policymaker) say who uses a resource. *Populations* (teens, shift workers,
   older adults) say whose health it's about. Tag both: *school and campus
   leaders* + *teens*.
3. **Crosswalks, not merges.** Each library keeps its own tags and maps them
   here with SSSOM files, following the Viv Resource Library's
   [interoperability rules](https://github.com/vivwebsolutions/Viv-Resource-Library/blob/main/docs/interoperability.md)
   (SKOS + SSSOM, MeSH as hub). SleepLiteracy's 46 terms are mapped in
   [`crosswalks/sleepliteracy-to-audiences.sssom.tsv`](crosswalks/sleepliteracy-to-audiences.sssom.tsv).

## What the research found

- **Sleep research tags who a study is about, almost never who should act.**
  Across 246 MEDLINE records on school start times, *Adolescent* appears 206
  times, *Public Policy* 8 and *Legislation as Topic* 0, though many of these
  papers ask school districts or legislators to act. MeSH has no descriptor for
  legislators, school boards or employers. Web guidance (CDC, NHS, MedlinePlus,
  AASM, Sleep Foundation) mostly sets no schema.org `audience` at all.
  See [the findings](research/sleep-research-tagging/README.md).
- **Our own lists have the same gap.** SleepLiteracy has no audience term at the
  policy level and two at the community level, and 77% of its resources carry
  no `audience` term. hcf-sleep-advice's 17 audience tags are all levels 1–2.
- **No external vocabulary covers the levels.** MeSH, schema.org and LRMI have
  nothing for the socio-ecological model, and their role lists stop at
  "professional". ERIC is the only one with *Policymakers* and *Community* as
  reader roles, and it has no URIs. So the levels and the role facet are ours;
  populations borrow MeSH IDs.
- **Policy-level example:** the [Global Health Advocacy Incubator](https://www.advocacyincubator.org/),
  an initiative of the Campaign for Tobacco-Free Kids that supports
  civil-society advocates to pass and strengthen public health policies (food
  and nutrition, health systems, injury prevention, tobacco). By its own count:
  217 policies passed or strengthened, in 38 countries; it works in 40+
  countries (to verify; see [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md)).
- **Advocacy steps can be a facet of their own.** GHAI's guide (4 phases, 12
  steps) can be shared but not adapted, and no CC BY health-advocacy process
  framework turned up. The public-domain CDC Policy Process plus the policy
  cycle and Kingdon's streams are enough to write our own 7-phase tag, with
  GHAI's steps as crosswalk labels. It's built: the phases can be used alone,
  or with the other axes of the [advocacy framework](vocab/advocacy/ADVOCACY.md).

## Build

Edit the CSV files, then:

```sh
python3 -I scripts/build.py
```

Python 3.10+, standard library only. It writes the Turtle, JSON-LD, Markdown
view and the audience SSSOM files, and checks that every level and broader
link exists. The level crosswalks (`crosswalks/ecological-levels-*.sssom.tsv`)
are hand-written.

IRIs under `https://health-culture.org/vocab/` are placeholders until a public
home is chosen.

## License

[CC BY 4.0](LICENSE), attribution "Health Culture Foundation". NCI's quoted
definitions are U.S. government work in the public domain. MeSH is produced by
the U.S. National Library of Medicine; no NLM endorsement is implied. LRMI
concept schemes are CC BY 4.0 (DCMI). Cited works keep their own licenses.
