# Open questions

Things v0.1 does not settle. Each one has a default already applied (marked
**Default**) so work can continue; change the default and rebuild if it's wrong.
The same list is mirrored as checkboxes on the tracking issue (#1).

## Model and structure

- [ ] **Where does an audience sit: where it acts, or what the content is about?**
  **Default:** where it *acts*. A parent is level 2 even when reading about a
  teen's sleep; a principal is level 3. The resource's own level (what it tries
  to change) is a separate tag: see the What Works `ecologicalLevel` facet
  (Viv-Resource-Library#35), which uses the same five IDs as this repo.
- [ ] **Population vs role as two facets.** **Default:** yes. Populations
  (teens, shift workers) say who a resource is *about*; roles say who *uses* it.
  The sleep-research note found that research tags populations and almost never
  roles. Is "population" the right word for readers, or "who it's about"?
- [ ] **Table 1 groups "Institutional Factors" and "Community Factors" under a
  "Community Level" heading** in the 2005 NCI PDF, while the text lists five
  separate levels. **Default:** five levels, as in the text and McLeroy 1988.
  Worth a look in the original paper before publishing.
- [ ] **Should an audience have more than one level?** Health departments,
  professional societies, researchers and platforms act at several levels.
  **Default:** one home level per concept, with the others in the editorial
  note. A resource can still carry several audience tags.
- [ ] **Where do researchers, funders and platforms belong?** None of them is a
  level of influence; they shape all of them. **Default:** community level, with
  a note. Alternative: a separate "knowledge and money" group outside the levels.
- [ ] **Is "Help Yourself / Help Others" a facet of its own?** It lines up with
  health-glossary#11's "For me / For someone I help / For my work" doors.
  **Default:** not modelled as concepts; `the-person` maps to Help Yourself, and
  Help Others maps (narrow) to the organization group. A three-door scheme
  (me / someone I help / my work) could map to levels 1 / 2 / 3-5.
- [ ] **SleepLiteracy uses "Help Yourself" as "general reader"** (19 of 27
  Parents resources are also tagged Help Yourself). Keep that meaning, or retag?

## Terms

- [ ] **Age bands.** SleepLiteracy says Seniors 60+, MeSH Aged is 65+, AASM's
  pediatric bands differ from SleepLiteracy's Kids (6-12). **Default:** store
  ages as numbers (schema.org `suggestedMinAge`/`suggestedMaxAge`) and keep the
  concepts loose.
- [ ] **SleepLiteracy terms with no home yet:** `special-populations` (undefined), and grouping-only nodes `by-age`,
  `by-gender`, `by-identity-or-community`. (Pro2Pro = professional to
  professional, per Kalman 22 Oct: now mapped to `vocab/communication-direction`.)
- [ ] **Identity groups** (LGBTQIA+, Black and African American) are populations
  here. Culturally tailored outreach is also a community-level action. Enough?
- [ ] **Missing audiences** to consider: insurers and payers, urban planners and
  housing authorities, librarians, app and device makers (partly covered by
  `platforms-and-tech`), sleep technologists, school nurses, coaches' governing
  bodies, unions. No sampled source addressed insurers or planners.
- [ ] **Patient vs caregiver handling** is still open in Viv-Resource-Library#4.
  **Default:** both are roles here (patients at level 1, caregivers at level 2),
  with MeSH Patients/Caregivers as matches.

- [ ] **Pro2Pro is a large category.** v0.1 splits it by what the professional
  does with it: guidance for practice, materials to pass on, training,
  research, running programs. **Default:** a separate *communication
  direction* scheme, not an audience or a level. The audience roles say which
  professional. Are five sub-types right? Is "materials to pass on" (made for
  professionals, read by the public) worth its own direction?

## Advocacy

Built in v0.1 ([`vocab/advocacy/ADVOCACY.md`](vocab/advocacy/ADVOCACY.md)):
the 7 phases work alone **and** as axis A of the multi-axis framework
(Kalman, 22 Oct: "I want BOTH"). Research and licence notes:
[`research/advocacy-frameworks/`](research/advocacy-frameworks/README.md).

- [ ] **GHAI's guide is shareable, not adaptable.** Its PDF says it may be
  shared and used with full attribution but not changed or adapted without
  GHAI's consent (works like CC BY-ND; the website's copyright page is
  stricter). **Default:** link to it; its 4 phase / 12 step names appear only
  as crosswalk labels (`crosswalks/ghai-steps-to-advocacy-phases.sssom.tsv`).
- [ ] **7 phases or 8?** **Default:** 7, with "Build support" and "Check
  what's working" as tags that apply at any phase. Make "Build support" its own
  phase (GHAI's "Collaborate") instead?
- [ ] **Optional axes G (goal type) and H (theory of change)** are built but
  marked optional. Keep both? H is probably only for funders and evaluators.
- [ ] **Tactic and outcome axes borrow category ideas** from copyrighted
  advocacy-evaluation work (HFRP Composite Logic Model, CEI Advocacy Strategy
  Framework, ORS Impact Pathways for Change). Labels and definitions are HCF's
  own and each concept says what informed it. Comfortable with that, or ask
  CEI/HFRP?
- [ ] **Ask GHAI to open the framework** under CC BY 4.0. A ~140-word draft is
  in the research note (§5), addressed to info@advocacyincubator.org. Kalman to
  decide and send; Claude did not send anything.
- [ ] **Community Tool Box licence conflict** (footer CC BY-NC-SA 4.0 vs a
  no-alteration use policy). Ask KU (communityhealth@ku.edu) before excerpting?
- [ ] **Test on real resources:** tag 10 advocacy resources (GHAI, Start School
  Later, AASM standard-time materials) on all axes to see which axes earn
  their keep.

## Identifiers and publishing

- [ ] **Public home for the IRIs.** Placeholders under
  `https://health-culture.org/vocab/` (same as hcf-sleep-advice). Needs a
  resolver before anyone else uses them.
- [ ] **Make the repo public?** Private for now, like hcf-sleep-advice.
- [ ] **Reviewer.** Nothing here has been checked by a person. Who reviews the
  level placements and the crosswalk predicates?

## Numbers to verify before they appear in copy

- [ ] GHAI: 217 policies passed or strengthened; 38 countries with policy wins;
  advocates in 40+ countries; 5B+ people protected (all self-reported, read from
  its homepage 2026-10-22; check the exact "40+" wording in a browser). 38 and
  40+ count different things: don't merge them.
- [ ] SleepLiteracy: 265 of 344 resources (77%) have no `audience` term
  (REST API, 2026-10-22).
- [ ] Start School Later: 165+ chapters; 31 states introduced and 15 passed
  start-time bills (its own figures).
- [ ] Cribs for Kids partner counts conflict across its pages (600+, 1,450+,
  2,000+).
- [ ] MEDLINE tag counts in `research/sleep-research-tagging/` are keyword
  searches run on 2026-10-22: read them as proportions, not a census.
- [ ] See also "Stats to verify" in `research/sleep-research-tagging/README.md`
  (SB 328 details, NHLBI's "50 to 70 million", AAP vs AASM hour ranges).
