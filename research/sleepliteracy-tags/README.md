# SleepLiteracy.org audience tagging: current state

Researched by Claude (Claude Code) for HCF; not yet reviewed by a person. Data pulled 2026-10-22 from the live site's REST API and theme source. Term-level detail, with a first-guess socio-ecological level per term, is in [`terms.csv`](terms.csv) (46 rows) in this folder. Raw term lists from the REST API are in `raw/`.

## 1. Where it is defined

Theme: `/Users/kalmangacs/Local Sites/sleepliteracy2.0/sleepliteracy/wp-content/themes/viv-child/`

There is no `register_taxonomy()` call in the theme PHP. All three taxonomies are ACF-registered (ACF JSON in `acf-json/`):

| Taxonomy slug | ACF file | Label | Post type | Hierarchical | REST base |
|---|---|---|---|---|---|
| `audience` | `taxonomy_67c1de6429da9.json` | Audiences | `resource` | yes | `audience` |
| `upper-lvl-audience` | `taxonomy_69af082684dc5.json` | Upper-level audiences | `resource` | yes (but flat, 2 terms) | `upper-lvl-audience` |
| `organization-audience` | `taxonomy_69a32e4e10788.json` | Organization Audiences (menu label "Audience") | `organization` | yes | `organization-audience` |

Related field groups:
- `group_68565d115a89c.json` "Rewrite Audience" (on `resource`): a repeater with `audience` (taxonomy select, save_terms 0) + `label` (text). Lets an editor show a different label for an audience term on one resource's card. Applied by the `vivgb_card_terms` filter in `vivgb/theme-vivgb.php` (~line 35).
- `group_69a732351509f.json` and `group_69af08f224236.json`: an `Image` (`thumbnail_id`) field on `upper-lvl-audience` and `organization-audience` terms (icons for the switcher modal).

Other resource taxonomies, for context: `topic`, `resourse_type` (sic, label "Types"), `resource_tag`, `rights`.

PHP that reads these taxonomies:
- `lib/organization.php`: shortcodes `[res_audience_switcher]` (resources page modal: top page = `upper-lvl-audience` parents, facet `resource_audiences`; choosing `help-others` opens a "Choose Your Audience" page with the full `audience` tree, facet `resource_sections`) and `[orgs_audience_switcher]` (defaults `term=audience`, `facet=resource_sections`).
- `vivgb/cards/organization.php`, `vivgb/cards/popup-organization.php`: show `organization-audience` + `organization-tags` on org cards; the popup query joins parent and child `organization-audience` terms.
- `lib/cm_import_cron.php` (CredibleMind importer): sets every imported org to `organization-audience` term 366 ("Help myself") and every imported resource to `audience` term **354**. Term 354 does not exist in any public taxonomy (REST returns 404 for `/audience/354`). It also reads CredibleMind's own `audienceType` field (`name`, `longName`) but does not appear to map it onto WP terms.

## 2. Term counts

From `https://sleepliteracy.org/wp-json/wp/v2/{taxonomy}?per_page=100` (one page each; `X-WP-Total` confirms):

| Taxonomy | Terms | Terms in use (count > 0) |
|---|---|---|
| `upper-lvl-audience` | 2 | 2 |
| `audience` | 27 (incl. 3 grouping nodes) | 20 |
| `organization-audience` | 17 | 2 (only the two parents) |

Content: 344 published resources (`/wp-json/wp/v2/resource`), 481 organizations (`/wp-json/wp/v2/organization`).

### upper-lvl-audience (resources)
- Help Yourself (401): 293. Description: "Find resources for your personal wellbeing journey"
- Help Others (400): 54. Description: "Resources to support others in their wellbeing"
- Every resource has at least one; 3 have both.

### audience (resources), tree with own counts
- General Public (42)
  - By Age (0): Kids (6-12) 5, Seniors (60+) 0, Young Adults 14, Youth 13
  - By Gender (0): Men 1, Women 3
  - by identity or Community (0): African American 0, LGBTQIA+ 0
  - College 14, Employees 4, Municipal employees 0, Parents 27
- Healthcare Professionals (24), slug `healthcare`
- K-12 Eductors (10)
- Millitary & Law Enforcement (3)
- PR (1)
- Pro2Pro (3)
- Science Journalism (3)
- Universities (13): Professors 5, Students 15
- Veterans (1)
- Workplace (3)

No term has a description.

### organization-audience (organizations)
- Help myself (366): 424 orgs
- Help Others (367): 57 orgs, with 15 children all at 0: Athletes and Coaches; Corporate Sector; Educational Community; Healthcare Professionals; Media and Creative Professionals; Military and Law Enforcement; Non-Profit Organizations; Parents and Caregivers; Public Health & Policymakers; Religious and Community Leaders; Researchers in Sleep and Health; Shift Workers & Hospitality; Special Populations; Transportation Workers; Wellness & Fitness Professionals.
- Every org has exactly one term, always a parent.

## 3. How visitors see it (https://sleepliteracy.org/resources/)

- Banner: "Tell us who you are to get content tailored to you." with a **Get personalized** button. The modal is titled "Find Your Wellbeing Resources" ("Find tools and resources to help individuals, groups, or drive systems-level change") and offers two cards: Help Yourself / Help Others. Help Others continues to "Choose Your Audience", a checkbox tree of the full `audience` taxonomy with counts, Select All / Deselect All per branch, and a "See Results" button.
- A dropdown next to search, facet "Resource Audiences": All Resources / Help Yourself (293) / Help Others (54).
- Left sidebar facets: **by Audience** (facet heading "Resource Sections"), **by Topic**, **by Type**, **by Rights**. by Audience shows the top level only, with + to expand: General Public (69), Healthcare Professionals (24), Universities (17), K-12 Eductors (10), Workplace (3), Science Journalism (3), Pro2Pro (3), Millitary & Law Enforcement (3), Veterans (1), PR (1).
- Facet counts roll up children (General Public shows 69 vs 42 own; Universities 17 vs 13 own), so they don't match the REST `count`.
- Typos ship to visitors: "K-12 Eductors", "Millitary".

## 4. Observations

**Coverage**
- 265 of 344 resources (77%) have no `audience` term. 264 of those are Help Yourself only. The audience taxonomy is effectively a Help Others feature. The importer's term 354 not existing is a likely cause for imported resources (WordPress skips integer term IDs that don't exist), but I haven't confirmed that from the DB.
- 6 `audience` terms are unused (Seniors, Municipal employees, African American, LGBTQIA+, plus the 3 grouping nodes at 0). All 15 `organization-audience` children are unused, so organizations have only a binary self/others split.
- Tagging is uneven: one resource carries 11 audience terms and two carry 10 (e.g. "One in 10 College Students Still Think About Suicide", id 42709, has 10 including Workplace and K-12 Educators). Over-tagging like this weakens the filter.

**Two parallel vocabularies**
- Resources use `upper-lvl-audience` + `audience`. Organizations use `organization-audience`, which folds the same self/others split and a sector list into one tree. The wording differs: "Help Yourself" vs "Help myself"; "Healthcare Professionals" slug `healthcare` vs `healthcare-professionals`; "Millitary & Law Enforcement" vs "Military and Law Enforcement"; "Parents" vs "Parents and Caregivers"; "K-12 Eductors" + "Universities" vs "Educational Community"; "Workplace"/"Employees" vs "Corporate Sector".
- The org list is closer to a sector list (who acts) and already includes policy and community roles. The resource list mixes populations and roles.

**Population vs role vs setting mixed at the same level**
- Populations (who the sleep is about): Kids, Youth, Young Adults, Seniors, Men, Women, African American, LGBTQIA+, Veterans, College, Students.
- Roles (who acts for others): Parents, Healthcare Professionals, K-12 Educators, Professors, PR, Science Journalism.
- Institutions or settings: Universities, Workplace, Military & Law Enforcement.
- Examples: Universities (institution) is the parent of Students (population) and Professors (role). General Public, the population bucket, contains Parents (a role) and Employees/Municipal employees (employer-defined groups). "Teens" isn't a term; "Youth" and "Young Adults" have no age ranges, while Kids (6-12) and Seniors (60+) do.

**Duplicates and overlaps**
- College (under General Public) vs Universities > Students.
- Employees vs Workplace vs Municipal employees.
- Veterans vs Millitary & Law Enforcement.
- Youth vs Kids (6-12) vs Young Adults.

**Help Yourself vs audience conflict**
- Parents is tagged Help Yourself on 19 of its 27 resources, although parenting content is interpersonal. "Help Yourself" seems to mean "consumer-facing", not "acting on your own sleep". That affects any mapping to the socio-ecological levels.

**Gaps against the five socio-ecological levels**
- Intrapersonal: well covered (age, gender, identity, students) but mostly unused below the top level.
- Interpersonal: Parents, Healthcare Professionals, Professors. No caregivers of older adults, partners/bed partners, or coaches (coaches exist only in the unused org term).
- Institutional/organizational: Universities, K-12, Workplace, Military & Law Enforcement. No employers/HR, health systems, shift-work industries, or transportation (the last two exist only as unused org terms).
- Community: only PR and Science Journalism. No community or faith leaders, nonprofits, or public health practitioners (all exist only as unused org terms).
- Public policy: **no `audience` term at all**. The only policy term is the unused org term "Public Health & Policymakers", which itself mixes community and policy.

**Oddities**
- Unexplained labels: "Pro2Pro", "PR".
- Inconsistent casing: "by identity or Community" vs "By Age"/"By Gender"; "Help myself".
- Taxonomy slug typo `resourse_type` (not audience, but it sits in the same filter UI).
- REST returns `&amp;` in names (e.g. `Millitary &amp; Law Enforcement`). The CSV unescapes them.
- The "Rewrite Audience" repeater means card labels can differ from term names per resource, so the front-end label isn't always the taxonomy name.

## 5. Suggested-level tally (first guess, see CSV notes)

| Level | audience | org-audience | upper-lvl |
|---|---|---|---|
| intrapersonal | 12 | 1 | 1 |
| interpersonal | 3 | 3 | 0 |
| organizational | 4 | 5 | 0 |
| community | 2 | 3 | 0 |
| policy | 0 | 1 | 0 |
| unclear | 6 (3 are grouping nodes) | 4 | 1 |

## Sources
- https://sleepliteracy.org/wp-json/wp/v2/taxonomies
- https://sleepliteracy.org/wp-json/wp/v2/audience?per_page=100
- https://sleepliteracy.org/wp-json/wp/v2/upper-lvl-audience?per_page=100
- https://sleepliteracy.org/wp-json/wp/v2/organization-audience?per_page=100
- https://sleepliteracy.org/wp-json/wp/v2/resource?per_page=100&page=1..4 (term assignments)
- https://sleepliteracy.org/wp-json/wp/v2/organization?per_page=100&page=1..5
- https://sleepliteracy.org/resources/ (rendered in the browser pane; facets load via JS)
