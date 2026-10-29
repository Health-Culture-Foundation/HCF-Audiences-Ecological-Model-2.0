# How sleep research and guidance tag their audiences

Research note, 2026-10-22, by Claude (Claude Code) for HCF; not yet reviewed by a person.
Companion table: [`sources.csv`](sources.csv) (22 rows, one per source).

Goal: feed an audience taxonomy built on the five socio-ecological levels
(intrapersonal, interpersonal, institutional, community, public policy).

## Bottom line

- **Sleep sources tag *populations* well and *actors* hardly at all.** PubMed
  MeSH reliably tags who a paper is about (Adolescent, Students, Child, Adult,
  Infant). The organization or legislator a recommendation is aimed at is
  almost never tagged, even when the abstract names them.
- **The hypothesis mostly holds, with one nuance.** MeSH has no descriptor for
  legislators, school boards or employers as actors. "Policy Makers" is only an
  entry term under *Administrative Personnel*, and that heading appears on 0
  school-start-time, 0 DST and 0 workplace-sleep records. The nearest thing is
  the **subheading** "/organization & administration" (on 48 of 246 indexed
  school-start-time records), plus setting tags such as *Schools* and
  *Workplace*. These show where something happens. They don't show who should
  act.
- **Our own taxonomy has the same gap.** The `hcf-sleep-advice` audience
  vocabulary (17 tags) is entirely intrapersonal, plus one interpersonal tag
  (`parents-and-caregivers`) and one referral flag (`talk-to-a-clinician`). It
  has no tag for schools, employers, communities or policymakers. The repo's own
  guideline summary sets school start times aside as "context only" because it
  is policy rather than personal advice.

## 1. What the existing repo already records

All paths are under `/Users/kalmangacs/Local Sites/hcf-sleep-advice/`.

| Finding | Where |
|---|---|
| The audience vocabulary has 17 tags: all-ages-and-cultures (default), adults, children-and-teens, parents-and-caregivers, students, shift-workers, travelers, people-with-insomnia, people-with-reflux, people-who-snore-or-may-have-sleep-apnea, people-with-a-late-body-clock, talk-to-a-clinician, needs-money-or-equipment, region-or-culture-specific, older-adults, pregnant-people, infants | `data/sleep-advice.json` → `audienceTags`; defined in `SCHEMA.md` (`audience`, `audienceNote`) |
| Each tag is one of three things: a population (age, life stage, condition, job or travel situation), a caring relationship (`parents-and-caregivers`: "Acted on by someone caring for another person"), or a constraint (`needs-money-or-equipment`, `region-or-culture-specific`). None is an organization or policy actor. | same |
| Counts over the 111 active concepts: all-ages-and-cultures 77 (64 have only that tag), adults 17, talk-to-a-clinician 15, people-with-insomnia 7, needs-money-or-equipment 6, parents-and-caregivers 5, snore/apnea 5, region-or-culture 3, children-and-teens 3, reflux 2, travelers 2, shift-workers 2, students 2, late-body-clock 1, infants 1, pregnant 1, older-adults 1 | `data/sleep-advice.csv` `audience` column |
| `later-school-start-times` is tagged `children-and-teens; parents-and-caregivers`. The note in the literature search says it is "policy advice that parents and schools can act on". Schools have no tag. | `TAXONOMY.md` l.48–49; `research/lit-search-2026-10/myths-audiences-gaps.md` |
| "Later school start times / permanent standard time … This is policy rather than personal advice, so it is context only." | `research/lit-search-2026-10/guidelines.md` l.43 |
| The `condition` facet ("Especially relevant for") uses ICD-11 codes as stand-ins for populations: insomnia, sleep apnea, reflux, late body clock, jet lag, shift work, anxiety. Shift work is coded as a condition (7A64), not an occupation or employer setting. | `editorial/facets.json` |
| Some `audienceNote` text records structural constraints that sit at the community or policy level, but only as free text: cooling assumes air conditioning (hot climates, shared rooms); daylight is hard at high latitudes; melatonin is OTC in some countries and prescription-only in others; cannabis legality differs by country and state. | `data/sleep-advice.csv` `audienceNote` |
| The literature-search format has a free-text `population` field and no actor or audience field. 278 findings were recorded. Population strings are rich (for example "rotating night shift workers (30 studies)" or "adolescents; parents/caregivers"), but no finding records who is meant to act. | `research/lit-search-2026-10/FORMAT.md`; `*.json` |
| Audiences already covered by the literature search: school start times, bedtime routines, sleep duration by age, infants and bed-sharing, pregnancy (from 28 weeks), menopause, shift workers (Shriane 2023, 18 guidelines), older adults (naps, hypnotics, light), college students, insomnia with mental disorders, siesta | `research/lit-search-2026-10/myths-audiences-gaps.md` |
| Advice that flips between audiences: naps are recommended for shift workers but are a myth as a remedy for insomnia, and melatonin is not for minors. The repo frames these as population conflicts, not actor conflicts. | same |
| The "Work & School Deadlines" and "Work/School Responsibilities" sleep-thief categories are written for the individual ("I will finish schoolwork by 9 pm"), not for the school or employer that sets the deadline. | `TAXONOMY.md` l.458–497; `editorial/facets.json` `problem` |

## 2. Patterns across the 22 sampled sources

### a. MeSH tags who a paper is about, not who should act
Every school-start-time record checked carries Adolescent, Students or Schools.
MEDLINE counts for records with "school start time(s)" in the title or
abstract (246 MEDLINE-indexed out of 297 in PubMed):

| MeSH | Records |
|---|---|
| Adolescent | 206 |
| Schools | 168 |
| Students | 129 |
| /organization & administration (any heading) | 48 |
| Parents | 9 |
| Public Policy | 8 |
| Health Policy | 3 |
| Policy Making | 2 |
| Legislation as Topic | 0 |
| Administrative Personnel (= "Policy Makers") | 0 |

The AAP 2014 statement "urges high schools and middle schools" and "supports
the efforts of school districts". Its MeSH tags are Adolescent, Schools*,
Students and *Societies, Medical*. Its publication type is Journal Article;
Review, not Guideline or Policy.

### b. Organization tags usually describe the author
*Foundations* (NSF), *Academies and Institutes* and *Societies, Medical*
(AASM, AAP) appear on the consensus statements. These describe who
published the paper. The only "organization" a reader can filter on is
the one that wrote it.

### c. Policy statements often carry no policy tags
- The AASM DST position (Rishi 2020) asks for a change in federal law. Its full
  text names Congress and legislation. Its MeSH tags are Accidents, Traffic;
  Circadian Rhythm*; Photoperiod*; Seasons; Sleep; United States, with no Public
  Policy. Across 189 MEDLINE DST records: Public Policy 7, Legislation as Topic 0,
  Circadian Rhythm 101.
- The AASM 2017 school-start position *is* tagged Public Policy* and Guideline,
  and it names "communities, school boards, and educational institutions". This
  is the best-tagged policy source in the sample, and it still has no tag for
  the actor.
- Ziporyn 2020 is the opposite case. It has Public Policy* and California but no
  population tag at all.

### d. Workplace papers tag the setting, not the employer
Redeker 2019 is explicitly about "employer-initiated interventions". Its tags
are Workplace, Occupational Health and Health Promotion. Across 180 MEDLINE
workplace-sleep intervention records: Workplace 64, Occupational Health 40,
Personnel Staffing and Scheduling 38, Shift Work Schedule 14, Nurses 10,
Administrative Personnel 0, Organizational Policy 0. Shriane 2023 (shift-worker
guidelines) does not even carry *Shift Work Schedule*, though that descriptor
has existed since 2018. Its population appears only in the author keywords.

### e. Community and environment papers tag the exposure
The WHO noise update (Smith 2022) is tagged Noise, Transportation and Aircraft.
It has no tag for residents and none for transport or planning authorities.
Across 408 MEDLINE noise or light-at-night sleep records: City Planning 0,
Environmental Policy 0, Public Policy 1, Urban Population 6, Residence
Characteristics 20.

### f. Web guidance tags readers, not actors
- **CDC's CMS has an audience field.** The page script sets `audience = 'gen'`,
  and the navigation offers "For Everyone" and "Health Care Providers". That is a
  reader-type vocabulary, not a level vocabulary.
- **NHLBI's deprivation page addresses "you" only.** It names school performance
  and productivity as outcomes but gives schools and employers nothing to do.
- **Sleep Foundation, sleepeducation.org, MedlinePlus and NHS** all ship
  schema.org JSON-LD, and none uses the `audience` property.
- **Healthy People 2030 is the exception.** It has setting groupings ("Schools")
  and objective-level tags (AH-R07: Schools, Adolescents, Sleep). AH-R07 ("Increase
  the proportion of secondary schools with a start time of 8:30 AM or later",
  status: Research) is the only sleep objective whose unit of measure is an
  organization.

### g. Some sources do name actors at several levels, in the prose
- **NIOSH nurses training.** The stated audience is "Registered Nurses", but
  Part 2 covers "workplace strategies managers can implement". Module 12 is
  "Action Steps for Nurse Managers" and Module 3 is "Impacts on Employers".
- **Paruthi 2016.** It lists who to educate ("children, teenagers, families,
  school professionals, healthcare providers/trainees, and the general public")
  and adds "informing public policy". Its MeSH has none of these.
- **NSF adolescent recommendations (Dautovich 2026).** It explicitly frames factors at
  "individual, social, and societal levels" and calls for school start times,
  permanent standard time and sleep health equity. MeSH reduces this to
  Adolescent, Adolescent Health and Foundations. The policy content survives only
  in the author keywords.
- **Hartstein 2024 (NSF screens).** It names "public health advocates, families,
  and industry" once, in the closing section. Industry (device and app makers) is
  untagged. Most of the intervention evidence it reviews is delivered through
  parents or families, which is interpersonal.

### h. Surveys tag respondents richly, institutions as sampling units only
ACHA-NCHA IIIb asks individual sleep items: N3Q13 sleep onset, N3Q14/15
weeknight and weekend hours, N3Q16A–D waking early, daytime sleepiness, trouble
falling asleep and days rested, and N3Q66P "Sleep difficulties" as a barrier to
academic performance. It also has many respondent descriptors (year in school,
residence including fraternity or sorority housing, visa status). The
institution appears only as `SCHOOLID`. No item measures institutional
practices such as class start times or residence-hall quiet hours.

## 3. Population vs actor: the core distinction

| Source | Population (about) | Actor (should act) | Is the actor tagged? |
|---|---|---|---|
| AAP 2014 school start | teens | school districts, middle and high schools | No (*Schools* setting only) |
| AASM 2017 school start | middle and high school students | communities, school boards | No (*Public Policy* topic only) |
| CA SB 328 | pupils | districts and charter schools (rural exempt) | n/a (statute) |
| HP2030 AH-R07 | adolescents | secondary schools (unit of measure) | Yes, *Schools* setting |
| Redeker 2019 | workers | employers | No (*Workplace* setting) |
| NIOSH training | nurses | nurses and nurse managers | Only nurses ("target audience") |
| AASM DST 2020 | whole US population | Congress, states | No |
| Smith 2022 noise | residents | regulators, planners (implied) | No |
| Hartstein 2024 | children, teens | families, industry | No |
| later-school-start-times (repo) | children-and-teens | schools, districts | No; tagged parents-and-caregivers |

The pattern: population tags describe the person whose sleep changes. Actor
tags would describe the person or body that has to do something. In sleep
research these are often two different parties: the evidence is measured on
teens, but the lever is a district bell schedule.

## 4. Implications for the audience taxonomy

The taxonomy should model two facets, not one.

1. **`population`**: whose sleep the advice is about. Use the existing 17 tags;
   they map well to MeSH age groups and the ICD-11 condition facet.
2. **`actor`** (who acts), with values grouped by ecological level:
   - **Intrapersonal:** self.
   - **Interpersonal:** parent or caregiver, bed partner, roommate or family.
   - **Institutional:** school or district, college or university, employer or
     manager, clinician or health system, child care provider.
   - **Community:** neighborhood or housing provider, community organization,
     local planners and noise authorities.
   - **Policy:** legislators (state or federal), regulators, insurers or payers,
     public-health agencies.

When importing from PubMed, MeSH can suggest actors as weak signals only:

- *Schools*, *Workplace* and *Child Care* suggest a setting, and possibly an
  institutional actor.
- *Public Policy*, *Health Policy* and *Legislation as Topic*, and the subheadings
  "/legislation & jurisprudence" and "/organization & administration", suggest
  the policy or institutional level.
- *Parents* suggests the interpersonal level.

Absence of these tags is **not** evidence that no actor is addressed. The DST,
WHO noise, Shriane and Paruthi records all lack them. For the actor facet, read
the abstract or recommendations section by hand.

Gaps where no source in the sample spoke to the actor:

- Insurers and payers: none of the 22 sources addresses them. The closest is HP2030
  SH-02 on getting adults with apnea symptoms evaluated.
- Urban planners: no source addresses them by name.
- Product makers: device and app makers are named once (Hartstein, "industry").

## 5. Stats to verify before reuse

- AAP 2014 "8.5-9.5 hours" for teens, versus the AASM/NSF "8-10 h". Both are
  quoted correctly from their sources, but they disagree.
- CDC age table (14–17 h newborn … 7–8 h for 65+, "18–60 years 7 or more"):
  check against Paruthi 2016, Watson 2015 and Hirshkowitz 2015 before quoting.
- NHLBI "50 to 70 million Americans" with chronic sleep disorders: an old,
  widely repeated figure. Find its primary source.
- REST of Your Life "81.9% strongly agree": a single-site pre/post pilot with no
  control group.
- HP2030 objective statuses ("Getting worse", etc.) change as data updates.
- SB 328 details (8:00 middle, 8:30 high, effective July 1 2022, rural exemption
  undefined): **unverified**. The leginfo statute page returned 403, so these
  come from news and association coverage.
- All MEDLINE tag counts were run 2026-10-22 and drift as indexing continues.
  The searches are title/abstract keyword sets, so they show proportions, not a
  full census.

## 6. Method and limits

- **Repo:** I read README, SCHEMA, the lit-search README, FORMAT and the
  myths-audiences-gaps notes, `editorial/facets.json`, and the `audience` and
  `audienceNote` columns of `data/sleep-advice.csv`. I grepped TAXONOMY.md.
- **PubMed:** MeSH, publication types and keywords came from E-utilities efetch.
  Counts came from esearch with `medline[sb]`. PMCID PMC13181348 for Hartstein
  2024 was confirmed with the PMC ID converter.
- **Full text:** PMC full text was scanned for actor words in Hartstein, Paruthi,
  Watson, Rishi (DST), Redeker and Shriane. The AAP 2014 and AASM 2017 full texts
  were blocked, so I worked from the abstracts.
- **Web pages:** fetched by curl or WebFetch. The NIOSH description came from
  WebFetch, because a direct curl of the subpage got a 403.
- **ACHA:** codebook PDF text extracted with pdftotext.
