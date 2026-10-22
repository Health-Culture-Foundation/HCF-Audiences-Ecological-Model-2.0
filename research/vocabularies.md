# Audience vocabularies to align with (HCF ecological audience taxonomy)

Researched 22 Oct 2026 by Claude (Claude Code) for HCF; not yet reviewed by a person. Everything below was checked against the primary source named, unless marked **(unverified)**.

Level codes used below. McLeroy et al. 1988: **IP** intrapersonal, **INT** interpersonal, **ORG** institutional/organizational, **COM** community, **POL** public policy. CDC four-level model ([CDC, About Violence Prevention](https://www.cdc.gov/violence-prevention/about/index.html), checked): **Individual**, **Relationship**, **Community** (settings such as schools, workplaces, neighborhoods), **Societal** (broad norms and policies). Crosswalk already decided in hcf-guides#6: IP→Individual, INT→Relationship, ORG+COM→Community, POL→Societal.

**Two axes we need to keep apart:**
- **Population:** who the content is *about*, or whose health is at stake (e.g. adolescents, shift workers).
- **Role:** who *uses* the content, and in what capacity (e.g. teacher, clinician, policymaker).

A health educator (role) can be reading about adolescents (population). Most vocabularies blur the two. The notes below say how each one handles it.

---

## 1. schema.org `audience` and Audience types

- **What:** the general web vocabulary. `audience` is "the intended group for whom something was created", and its value is an `Audience` (Thing > Intangible > Audience).
- **Namespace:** `https://schema.org/` (checked against V30.1, 2026-09-16).
- **Licence:** CC BY-SA 3.0 ([schema.org/docs/terms.html](https://schema.org/docs/terms.html)).
- **Where `audience` can be used:** CreativeWork, Event, LodgingBusiness, PlayAction, Product, Service. Related properties: `serviceAudience` (Service), `medicalAudience` (MedicalWebPage), `recipient`, `permitAudience`, `touristType`.

| Type | Defines | Notes |
|---|---|---|
| `Audience` | `audienceType` (Text): "The target group associated with a given audience (e.g. veterans, car owners, musicians, etc.)"; `geographicArea` (AdministrativeArea) | Free text only, no controlled list |
| `EducationalAudience` | `educationalRole` (Text): "An educationalRole of an EducationalAudience." | The schema.org page names no value list. LRMI supplies one (section 2) |
| `PeopleAudience` | `healthCondition` (MedicalCondition), `requiredGender`, `requiredMinAge`, `requiredMaxAge`, `suggestedAge` (QuantitativeValue), `suggestedGender` (GenderType/Text), `suggestedMinAge`, `suggestedMaxAge`, `suggestedMeasurement` | Subtypes: `MedicalAudience`, `ParentAudience` |
| `MedicalAudience` | (inherits PeopleAudience) "Target audiences for medical web pages." | Subtype: `Patient` |
| `Patient` | Is a Person, MedicalAudience and PeopleAudience. "A patient is any person recipient of health care services." Adds `diagnosis`, `drug`, `healthCondition` | **Patient is a type, not a MedicalAudienceType member** |
| `MedicalAudienceType` (enumeration) | Members: **`Clinician`, `MedicalResearcher`** (only these two) | "Target audiences types for medical web pages." |
| `BusinessAudience` | `numberOfEmployees`, `yearlyRevenue`, `yearsInOperation` (QuantitativeValue) | Describes an organization as the audience |
| `Researcher` | "Researchers." (direct subtype of Audience) | |

- **Population vs role:** schema.org leans to population. PeopleAudience (age, gender, health condition) is about who the people *are*. Role shows up in only three places: `educationalRole` (free text), the two MedicalAudienceType members (Clinician, MedicalResearcher), and the `Researcher` type. `audienceType` is free text that can hold either.
- **Levels:** PeopleAudience, Patient and healthCondition → IP (also the population facet at any level). ParentAudience → INT. Clinician/MedicalResearcher/Researcher → role facet, typically working at ORG. BusinessAudience → ORG (an organization as the audience). There are no types for policy or community actors: `audienceType` text with `additionalType` pointing at our concept URI is the hook.

## 2. LRMI / DCMI Educational Audience Role

- **What:** DCMI LRMI Task Group concept scheme, published as a DCMI Community Specification: "the primary or intended roles of the audience (beneficiary) of the resource being described". Intended as values for schema.org `educationalRole`.
- **URI:** `http://purl.org/dcx/lrmi-vocabs/educationalAudienceRole/` (Turtle checked by content negotiation). Human page: https://www.dublincore.org/specifications/lrmi/concept_schemes/educationalAudienceRole. Created 2017-03-01, modified 2022-10-18. The other LRMI schemes in the same namespace: alignmentType, educationalUse, interactivityType, learningResourceType.
- **Licence:** CC BY 4.0 (in the RDF and on the scheme index page).
- **Full term list (8 concepts, labels and definitions from the RDF):**

| Concept | prefLabel | Definition | Level fit |
|---|---|---|---|
| `audRole:administrator` | administrator | "A trainer or educator with administrative authority and responsibility." | ORG |
| `audRole:generalPublic` | general public | "The public at large." | IP (or COM/POL as "the public") |
| `audRole:mentor` | mentor | "Someone who advises, trains, supports, and/or guides." | INT |
| `audRole:parent` | parent | "A father, mother, or legal guardian." | INT |
| `audRole:peerTutor` | peer tutor | "The peer learner serving as tutor of another learner." (`skos:broader audRole:student`) | INT |
| `audRole:professional` | professional | "Someone already practicing a profession; an industry partner, or professional development trainer." | ORG (default), any |
| `audRole:student` | student | "The learner or trainee." | IP |
| `audRole:teacher` | teacher | "A person who has been trained to implement educational methods and practices." | INT/ORG |

- **Population vs role:** pure role. It has no age, condition or demographic terms. "Beneficiary" in the description means the intended user.
- **Gaps for HCF:** no caregiver, patient, clinician, policymaker, funder, journalist or community leader. `professional` is the only catch-all. The open "caregiver/patient handling" question in Viv-Resource-Library#4 comes from this gap.

## 3. MeSH: Persons (M01) and organization/policy descriptors

- **What:** NLM Medical Subject Headings. Category M is "Named Groups" and **M01 is Persons (D009272)**. Note: "Population Groups" (D044382) is only one branch inside it (M01.686, racial/geographic groupings), not the whole tree.
- **URI pattern:** `http://id.nlm.nih.gov/mesh/{DUI}` (e.g. http://id.nlm.nih.gov/mesh/D009272). Tree numbers and UIDs below came from the id.nlm.nih.gov SPARQL endpoint, current graph `<http://id.nlm.nih.gov/mesh>`, queried 22 Oct 2026. Labels were cross-checked through the `/mesh/lookup/descriptor` API.
- **Licence:** NLM MeSH Terms and Conditions (https://www.nlm.nih.gov/databases/download/terms_and_conditions_mesh.html): free with no fees, NLM must be credited as the source, and NLM endorsement must not be implied. Anyone redistributing must keep the copy current or state the MeSH version used. Not a Creative Commons licence.
- **Population vs role:** MeSH M01 mixes the two in one tree. Most branches are populations (age, condition, ethnicity, Patients, Prisoners). **M01.526 Occupational Groups** is the role branch, and family roles (Parents, Caregivers, Spouses, Friends) sit in between. MeSH is a *subject* vocabulary: it says what an article is about, not who it was written for. Use it on the population facet, and on the role facet only as a `skos:closeMatch`.

### 3a. M01 Persons: all second-level descriptors (M01.xxx)

Level column = suggested McLeroy fit when the term is used as an audience.

| Tree | DUI | Label | Fit |
|---|---|---|---|
| M01 | D009272 | Persons | — |
| M01.050 | D000023 | Abortion Applicants | IP |
| M01.055 | D032721 | Adult Children | INT |
| M01.060 | D009273 | Age Groups | IP (population) |
| M01.066 | D057229 | Alcoholics | IP |
| M01.072 | D056352 | Athletes | IP |
| M01.079 | D000075482 | Bedridden Persons | IP |
| M01.085 | D017028 | Caregivers | INT |
| M01.097 | D002670 | Child, Abandoned | IP |
| M01.100 | D000073922 | Child, Adopted | IP |
| M01.102 | D002671 | Child, Exceptional | IP |
| M01.106 | D016241 | Child of Impaired Parents | IP/INT |
| M01.107 | D000073921 | Child, Foster | IP |
| M01.108 | D054540 | Child, Orphaned | IP |
| M01.111 | D002676 | Child, Unwanted | IP |
| M01.120 | D003253 | Consultants | ORG (role) |
| M01.135 | D019548 | Crime Victims | IP |
| M01.142 | D057237 | Criminals | IP |
| M01.150 | D006233 | Persons with Disabilities | IP |
| M01.159 | D064891 | Disaster Victims | IP |
| M01.169 | D055030 | Drug Users | IP |
| M01.189 | D054242 | Emigrants and Immigrants | IP/COM |
| M01.210 | D063948 | Enslaved Persons | IP |
| M01.219 | D000078822 | Ex-Smokers | IP |
| M01.228 | D005197 | Famous Persons | — |
| M01.252 | D033062 | Friends | INT |
| M01.264 | D000066502 | Grandparents | INT |
| M01.270 | D000091202 | Health Disparate Minority and Vulnerable Populations | COM (population) |
| M01.276 | D018577 | Homebound Persons | IP |
| M01.325 | D006703 | Ill-Housed Persons | IP/COM |
| M01.352 | D033221 | Jehovah's Witnesses | — |
| M01.380 | D007872 | Legal Guardians | INT |
| M01.385 | D017057 | Medically Uninsured | IP |
| M01.390 | D008571 | Men | IP |
| M01.395 | D008611 | Mentors | INT |
| M01.416 | D033242 | Minors | IP |
| M01.427 | D066189 | Missionaries | — |
| M01.438 | D009099 | Multiple Birth Offspring | — |
| M01.482 | D000078405 | Non-Smokers | IP |
| M01.526 | D009274 | Occupational Groups | ORG (role) |
| M01.620 | D010290 | Parents | INT |
| M01.643 | D010361 | Patients | IP |
| M01.665 | D000069636 | Pedestrians | IP/COM |
| M01.686 | D044382 | Population Groups | COM (population) |
| M01.729 | D011329 | Prisoners | IP |
| M01.755 | D012036 | Refugees | IP/COM |
| M01.774 | D035842 | Research Subjects | IP |
| M01.776 | D060386 | Sex Workers | IP |
| M01.778 | D012747 | Sexual Partners | INT |
| M01.781 | D035781 | Siblings | INT |
| M01.785 | D012847 | Single Person | IP |
| M01.808 | D000074285 | Smokers | IP |
| M01.816 | D018454 | Spouses | INT |
| M01.848 | D013334 | Students | IP (role in LRMI sense) |
| M01.860 | D017741 | Survivors | IP |
| M01.873 | D019452 | Terminally Ill | IP |
| M01.898 | D014019 | Tissue Donors | IP |
| M01.909 | D063106 | Transgender Persons | IP |
| M01.920 | D014171 | Transients and Migrants | IP/COM |
| M01.925 | D066027 | Transplant Recipients | IP |
| M01.927 | D000096967 | Unvaccinated Persons | IP |
| M01.928 | D000066988 | Vegetarians | IP |
| M01.930 | D014728 | Veterans | IP |
| M01.935 | D014789 | Visitors to Patients | INT |
| M01.955 | D014838 | Volunteers | COM |
| M01.975 | D014930 | Women | IP |
| M01.987 | D000069602 | Working Poor | IP/COM |

### 3b. Selected third-level descriptors

- **Age Groups (M01.060):** Adolescent D000293 (.057) · Adult D000328 (.116) · Birth Cohort D000089822 (.261) · Child D002648 (.406) · Infant D007223 (.703). (Aged, Middle Aged, Young Adult and Child, Preschool are fourth level or below; not pulled.)
- **Persons with Disabilities (M01.150):** Amputees D000674 · Children with Disabilities D019988 · Persons with Intellectual Disabilities D019989 · Persons with Psychiatric Disorders D028642 · Persons with Hearing Disabilities D019986 · Persons with Visual Disabilities D019987 · Para-Athletes D000080050.
- **Health Disparate Minority and Vulnerable Populations (M01.270):** Black or African American D001741 · Amish D061365 · Arabs D018912 · Asian American Native Hawaiian and Pacific Islander D000094202 · Hispanic or Latino D006630 · Indigenous Peoples D000081034 · Jews D007585 · Romani People D006178 · Sexual and Gender Minorities D000072339 · Vulnerable Populations D035862.
- **Parents (M01.620):** Fathers D005220 · Mothers D009035 · Single Parent D015406 · Gestational Carriers D013533.
- **Patients (M01.643):** Inpatients D007297 · Outpatients D010045 · Nursing Home Residents D000099308 · No-Show Patients D000067455 · Child/Adolescent, Hospitalized/Institutionalized (D002673, D002674, D000298, D000299).
- **Students (M01.848):** Student Dropouts D013332 · Students, Health Occupations D013336.
- **Volunteers (M01.955):** Healthy Volunteers D064368 · Hospital Volunteers D006758.
- **Women (M01.975):** Pregnant People D037841 · Women, Working D014931 · Battered Women D018585 · Physicians, Women D010822 · Dentists, Women D003816.
- **Occupational Groups (M01.526), the role branch:** Administrative Personnel D000288 (.070) · Astronauts D018480 · Correctional Facilities Personnel D000093762 · Counselors D000072117 (.225) · Ethicists D026822 · Farmers D000067565 · Foreign Professional Personnel D005551 · Frontline Workers D000098724 · **Government Employees D000071296 (.446)** · **Health Personnel D006282 (.485)** · Inventors D062068 · Laboratory Personnel D059232 · Lawyers D033241 · Librarians D016245 · Metal Workers D000085924 · Military Personnel D008889 · Miners D000067572 · **Educational Personnel D000071195 (.702)** (→ Faculty D005178, School Teachers D000070777) · Personal Trainers D000098562 · Pilots D000070356 · Power Plant Operators D000096246 · Religious Personnel D065834 · **Research Personnel D012108 (.839)** · **Social Workers D000068217 (.919)** · Truck Drivers D000095402.
- **Health Personnel (M01.526.485) children:** Allied Health Personnel D000488 (→ Community Health Workers D003150 at M01.526.485.067.080) · Anatomists D054814 · Anesthetists D000072077 · Audiologists D000072018 · Caregivers D017028 · Case Managers D000071959 · Coroners and Medical Examiners D003334 · Dental Staff D003797 · Doulas D059037 · Emergency Medical Dispatcher D000071822 · **Epidemiologists D000072158** · Faculty, Dental/Medical/Nursing (D005179/D005180/D005181) · **Health Educators D040441** · **Health Facility Administrators D006270** · Infection Control Practitioners D016357 · Medical Chaperones D061348 · Medical Laboratory Personnel D017056 · Medical Staff D008503 · Nurses D009726 · Nursing Staff D009740 · Nutritionists D064686 · Occupational Therapists D000072087 · Optometrists D000072162 · Personnel, Hospital D010564 · Pharmacists D010595 · Physical Therapists D059825 · Physician Executives D008486 · Physicians D010820 · Psychologists D000098484 · Psychotherapists D000082383 · Respiratory Therapists D000099128 · Traditional Medicine Practitioners D000095083 · Veterinarians D018634.

### 3c. MeSH for organizations, settings and policy actors (outside M01)

Current-graph tree numbers. These are *subjects* (settings, actions), not person groups. In SSSOM they suit the level concepts or the setting facet, not audience roles.

| Fit | DUI | Label | Tree number(s) |
|---|---|---|---|
| IP | D015438 | Health Behavior | F01.145.488 |
| IP | D007722 | Health Knowledge, Attitudes, Practice | F01.100.150.500; N05.300.150.410 |
| IP | D012648 | Self Care | E02.900; I03.050.563; N02.421.784.680 |
| INT | D007398 | Interpersonal Relations | F01.829.401 |
| INT | D005190 | Family | F01.829.263; I01.880.853.150 |
| INT | D005195 | Family Relations | F01.829.263.370; I01.880.853.150.439 |
| INT | D010379 | Peer Group | F01.829.316.483 |
| INT | D012944 | Social Support | I01.880.853.500.600 |
| ORG | D009938 | Organizations | N03.540 |
| ORG | D009939 | Organizations, Nonprofit | N03.540.630 |
| ORG | D012952 | Societies | N03.540.828 |
| ORG | D000047 | Academies and Institutes | N03.540.052 |
| ORG | D006268 | Health Facilities | N02.278 |
| ORG | D012574 | Schools | I02.783; J03.832 |
| ORG | D014495 | Universities | I02.783.830; J03.832.830 |
| ORG | D017132 | Workplace | N01.824.245.925; N04.452.677.975 |
| ORG | D004651 | Employment | N01.824.245 |
| ORG | D007221 | Industry | J01.576 |
| ORG | D016134 | Organizational Policy | I01.655.500.550; N03.623.500.550 |
| ORG | D015279 | Organizational Culture | N04.452.606 |
| ORG | D017049 | Employer Health Costs | (tree not pulled) |
| COM | D003153 | Community Health Services | N02.421.143 |
| COM | D003256 | Community Participation | N02.421.143.212; N03.540.245.360 |
| COM | D019058 | Community Networks | I01.880.853.500.300; L01.313.500.750.300.184; N02.421.143.202 |
| COM | D018672 | Community Health Planning | N03.349.650.185 |
| COM | D055812 | Community-Based Participatory Research | H01.770.644.193; N05.425.104 |
| COM | D012111 | Residence Characteristics | N01.224.791; N06.850.505.400.800 |
| COM | D000091542 | Neighborhood Characteristics | I01.880.853.500.525; N01.224.791.775; N06.850.505.400.800.775 |
| COM | D000076624 | Built Environment | N06.230.145.500 |
| COM | D012931 | Social Environment | I01.880.853.500 |
| COM/POL | D011634 | Public Health | H02.403.720; N01.400.550; N06.850 |
| COM/POL | D015980 | Public Health Practice | N06.850.780 |
| COM/POL | D011635 | Public Health Administration | N04.452.794 |
| COM/POL | D006293 | Health Promotion | H02.403.720.750.380.579; N02.421.726.407.579 |
| COM/POL | D058015 | Health Communication | L01.143.350; N02.208 |
| COM/POL | D008402 | Mass Media | L01.462.500.590 |
| COM/POL | D061108 | Social Media | L01.224.230.110.500.750; L01.462.500.751 |
| COM/POL | D020452 | Journalism | L01.737.498 |
| COM/POL | D060756 | Social Networking | L01.143.910 |
| POL | D057766 | Policy | I01.655; N03.623 |
| POL | D011640 | Public Policy | I01.655.500.608; I01.880.604.825.608; N03.623.500.608 |
| POL | D006291 | Health Policy | I01.655.500.608.400; I01.880.604.825.608.400; N03.623.500.608.428 |
| POL | D011050 | Policy Making | N03.706.742 |
| POL | D007878 | Legislation as Topic | N03.706.615 |
| POL | D011057 | Politics | I01.738 |
| POL | D006076 | Government | I01.409; N03.540.348 |
| POL | D006077 | Government Agencies | I01.409.418; N03.540.400 |
| POL | D010344 | Patient Advocacy | I01.880.604.631; N03.706.678 |
| POL | D000073597 | Stakeholder Participation | I01.738.805; I03.743 |
| POL | D066262 | Social Norms | F01.829.750; I01.880.853.903 |
| POL | D064890 | Social Determinants of Health | I01.240.425.756; N01.224.425.762; N01.400.675 |
| — | D004463 | Ecology | (biological; not the socio-ecological model) |

**Checked and not in MeSH (no descriptor or entry term found):** "Social Ecology", "socio-ecological"/"socioecological", "ecological model", "Legislators", "Lawmaker", "Journalists", "Advocacy" (only Patient Advocacy exists). MeSH has no concept for the socio-ecological model itself, so our level concepts have nothing to map to there.
**Useful entry term:** "Policy Makers" (T000960, from POPLINE 1993) is an entry term under **Administrative Personnel D000288**, the closest MeSH match for a policymaker audience. Government Employees D000071296 is the alternative.

## 4. What our own GitHub issues already say

### Viv-Resource-Library#4: "Audience taxonomy: local lists, shared list, crosswalk to LRMI roles"
- Plan: track audience "the same way `taxonomies/resource-type/` tracks type: every library's audience list, one shared list, a crosswalk, and the LRMI mapping."
- Local lists to collect (quoted): "Sleep Literacy (Help Yourself / Help Others + roles + sub-roles, with counts), VLCT roles and service areas, VivCE specialties (summary), IHA glossary term audiences (everyone / patients / professionals / specialists), Civic Learning Week intended audience + grade level, EAD grade level, record schema `audience` enum".
- Shared list design: "roles + separate facets for age (`typicalAgeRange`), and "for me / for someone I help"". This already separates role from population (age) and adds a third axis, *for whom* (self or other).
- Deliverables: `taxonomies/audience/local-lists.json`, `crosswalk.sssom.tsv` local → shared → LRMI `educationalAudienceRole`, schema enum plus a drift check. Open: "Decide caregiver/patient handling (see the LRMI issue)".
- No comments yet. It does not mention ecological levels.

### health-glossary#11: "Audience doors for the glossary (like Sleep Literacy's Help Yourself / Help Others)"
- Option 1 (quoted): "**For me / For someone I help / For my work** → then a role (patient, caregiver, health educator, clinician, communicator/journalist)."
- Option 2: "Two doors: "I'm looking this up" / "I'm explaining this to someone.""
- Option 3: the existing per-term field `data/ai/audience.json`: "everyone 118, patients 93, professionals 94, specialists 38 of 343".
- Options 4–5: jargon slider; audience-specific exports (patient handout, clinician "words to avoid" list, journalist style sheet).
- Recommendation in the issue: "2, with 5 as a paid/showcase layer." Open checkboxes: decide option; map audiences to LRMI roles; link to Sleep Literacy `teaches`. No comments.
- For our taxonomy: "For me / someone I help / my work" lines up with IP / INT / ORG-and-up.

### hcf-guides#3: "HCF vs SleepLiteracy positioning (socio-ecological model) + content audit and scoring rubric"
- Uses the **CDC four levels**: "Individual", "Relationship", "Community", "Societal". Level examples from its table: Relationship = "Roommates, partners, friends, family, peer leaders". Community = "Campus schedules and housing, workplace shifts, clinic pathways, school start times, what a health department publishes". Societal = "Norms…, policy…, media, and how health information is produced, licensed and shared".
- Audiences: SleepLiteracy "talks to people"; HCF "talks to **people who run systems and shape health messages**: campus wellbeing staff, public health communicators, clinicians, other health groups, funders."
- Key rule: "the brand test is now about the reader (people vs professionals), not the level." This is the population-vs-role split in another form: the *level* is what a post is about, the *reader* is the audience.
- Rubric SEM tag codes: "I = individual, R = relationship, C = community, S = societal".
- Last comment: Viv-Resource-Library#35 "stores McLeroy's five levels and rolls them up to the four used here (institutional + community → Community; policy → Societal)".

### hcf-guides#6: "Open Health Communication Declaration: draft text, continuum, maturity checklist"
- Declares "**An ecological tagging vocabulary:** … the five levels of influence in *Theory at a Glance* [23]: individual, interpersonal, organizational, community and policy." Source verified in that issue: McLeroy, Bibeau, Steckler & Glanz (1988), *Health Education Quarterly* 15(4):351–377, doi:10.1177/109019818801500401. Theory at a Glance Table 1 wording: "intrapersonal, interpersonal, institutional, community, public policy".
- "Decision (reversible): publish five levels with a crosswalk to CDC's four." SKOS concept scheme plus SSSOM mappings.
- Proposes an "Open health-comms vocabulary + crosswalks: specialty, topic and audience terms mapped to MeSH, with a public "request a term" queue" (modeled on NASA GCMD).
- Actor list from the summarized editors' statement: "Platforms and social media companies", "Regulators", "Everyone with a role (schools, universities, funders, researchers, publishers, professional societies, health systems, tech companies, civil society)", "Society". This is a ready-made list of ORG/POL actors.
- 22 Oct: the audience taxonomy moves to new repo `vivwebsolutions/HCF-Audiences-Ecological-Model-2.0`, seeded from SleepLiteracy's `audience` / `upper-lvl-audience` / `organization-audience` terms. Global Health Advocacy Incubator is to be cited as the policy-level example.

## 5. Other audience vocabularies (only what was confirmed)

- **ERIC (US Dept of Education) `audience` field.** 11 values, confirmed through the ERIC API (`api.ies.ed.gov/eric`, record counts on 22 Oct 2026): Administrators (26,951) · Community (3,695) · Counselors (4,319) · Media Staff (4,590) · Parents (7,377) · Policymakers (22,892) · Practitioners (124,182) · Researchers (28,498) · Students (12,428) · Support Staff (1,271) · Teachers (82,218). Pure role list. It is the only one found with **Policymakers** and **Community** as reader roles, which covers POL and COM. Licence: US federal work, likely public domain **(unverified)**. No URIs: the values are plain strings.
- **Healthy People 2030 (ODPHP) browse categories** (https://odphp.health.gov/healthypeople/objectives-and-data/browse-objectives). *Population Groups*: Adolescents, Children, Infants, LGBT, Men, Older Adults, Parents or Caregivers, People with Disabilities, Women, Workforce. *Settings and Systems*: Community, Environmental Health, Global Health, Health Care, Health Insurance, Health IT, Health Policy, Hospital and Emergency Services, Housing and Homes, Public Health Infrastructure, Schools, Transportation, Workplace. Other top-level groups: Health Conditions, Health Behaviors, Social Determinants of Health. Population Groups is the population facet. Settings and Systems is a good ORG/COM/POL setting list. No URIs. US gov work **(licence unverified)**.
- **MedlinePlus health topics, "Demographic Groups"**: Children and Teenagers · Men · Older Adults · Population Groups · Women. Population only and coarse. No URIs.
- **Concannon et al. 2012, "7Ps of Stakeholder Engagement"** (J Gen Intern Med 27(8):985–991, doi:10.1007/s11606-012-2037-1). The abstract (Europe PMC) confirms the name "7Ps of Stakeholder Engagement". The category list is **(unverified)**: patients and the public, providers, purchasers, payers, policy makers, product makers, principal investigators. PMC full text was behind a CAPTCHA, so check it before citing. It is a role list for research partners and fits ORG/POL actors well. A PCORI "13 Ps" list could not be confirmed and is left out.
- **Not checked / not found:** CDC Health Literacy audience lists (not researched for lack of a clear primary list).

## Alignment recommendation

| Part of our taxonomy | Map to | How |
|---|---|---|
| **Level concepts** (5 McLeroy + 4 CDC) | Our own SKOS scheme. No external vocabulary has the socio-ecological model (MeSH has no "social ecology" descriptor) | Cite McLeroy 1988 and CDC with `dct:source`. Five→four with `skos:broadMatch`. Optional `skos:relatedMatch` to MeSH anchors: IP→Health Behavior D015438, INT→Interpersonal Relations D007398, ORG→Organizations D009938, COM→Community Health Services D003153 / Residence Characteristics D012111, POL→Public Policy D011640 / Health Policy D006291 |
| **Role facet** (who uses it) | LRMI `educationalAudienceRole` first (CC BY 4.0, has URIs), emitted as schema.org `EducationalAudience/educationalRole` | `exactMatch` where possible: parent, mentor, peerTutor, teacher, student, administrator, generalPublic. Everything health-specific (clinician, health educator, communicator, funder, policymaker) is `narrowMatch` to `audRole:professional` |
| Role facet, health roles | MeSH M01.526 Occupational Groups as `closeMatch` (Health Personnel D006282, Health Educators D040441, Epidemiologists D000072158, Health Facility Administrators D006270, Social Workers D000068217, Research Personnel D012108, Educational Personnel D000071195, Government Employees D000071296, Administrative Personnel D000288 for policymakers). Clinician / researcher also map to schema.org `MedicalAudienceType` Clinician / MedicalResearcher | Use `closeMatch` not `exactMatch`: MeSH says what an article is about, not who reads it |
| Role facet, COM/POL readers | ERIC audience strings (Policymakers, Community, Administrators, Researchers, Practitioners) as `closeMatch` literals; the 7Ps after verification | ERIC has no URIs: record them as `sssom:object_label` with the object_source set to ERIC |
| **Population facet** (who it's about) | MeSH M01 Persons (age groups, patients, conditions, vulnerable populations, family roles), schema.org `PeopleAudience` properties (`suggestedMinAge`/`suggestedMaxAge`, `healthCondition`, `suggestedGender`) and Healthy People 2030 Population Groups | Population terms carry a MeSH DUI. Age is numeric (schema.org / LRMI `typicalAgeRange`), not a concept, as Viv-Resource-Library#4 already planned |
| **"For me / someone I help / my work" axis** | No external equivalent. Own small scheme | Default mapping: IP / INT / ORG-and-up |
| **Organization/setting facet** (where it applies) | Healthy People 2030 Settings and Systems for labels; MeSH N-tree descriptors (Schools D012574, Universities D014495, Workplace D017132, Health Facilities D006268, Government Agencies D006077, Organizations, Nonprofit D009939) for IDs; schema.org `BusinessAudience` when the audience is an organization | |
| **Patient / caregiver** (open in VRL#4) | Population: MeSH Patients D010361, Caregivers D017028. Role: no LRMI term, so use our own concepts with `broadMatch audRole:generalPublic` (patient) and `relatedMatch audRole:parent` (caregiver). schema.org `Patient` type for markup | Decision for the issue |
