# Example organizations by socio-ecological level

Research date: 2026-10-22. Researched by Claude (Claude Code) for HCF; "I" below is Claude. Not yet reviewed by a person.
Companion data: [`orgs.csv`](orgs.csv) (22 rows, columns: level, org_name, url, ror_id, wikidata_qid, description, why_this_level, sleep_related, verified, notes).

**What "verified" means:** *yes* = I fetched the org's own page and checked the claim. *partial* = based on search snippets, secondary sources or registry entries only, or the site blocked fetching. *no* = not checked; don't publish it without checking.
Quotes are under 15 words and come from the pages fetched on the date above.

---

## 1. Required policy example: Global Health Advocacy Incubator (GHAI)

- **URL:** https://www.advocacyincubator.org/ (about: https://www.advocacyincubator.org/about)
- **Parent org:** the footer says "We are an initiative of the Campaign for Tobacco-Free Kids". The About page says CTFK launched GHAI in **2014**.
- **What it does:** it supports civil society advocates in passing or strengthening public health policies. The homepage says it "uses the power of advocacy to reduce preventable deaths" by changing policies. The About page says it gives partners "direct, systematic, ongoing technical assistance".
- **Issue areas** (homepage program list): Food and Nutrition; Health Systems Strengthening; Injury Prevention; Capacity Strengthening; and Saving Lives from Tobacco Use, which links out to CTFK. The About page lists "food and nutrition, health systems strengthening and injury prevention". CTFK's About page frames it as food and nutrition, injury **and overdose** prevention, and health system resilience and equity.
- **Figures shown today on the homepage stats block (all self-reported by GHAI):**
  - **217** policies passed or strengthened
  - **38** countries where we've supported policy wins
  - **5B+** people protected (About page: "more than 5 billion people")
  - Works with advocates "in more than 40 countries" (from the What We Do section)
  - So the brief's wording, "217 policies passed or strengthened in 38 countries" and "40+ countries", matches today's site. The two country counts measure different things: 38 is where policies were won, and 40+ is where GHAI works. The copy must keep them separate.
- **Caveat:** the site returns HTTP 403 to curl, so I read these figures through WebFetch's page rendering. Before shipping, check the exact wording ("40+" or "more than 40") by eye in a browser.
- **Identifiers:** none found. The ROR API query for "Global Health Advocacy Incubator" had no matching org (top hits were unrelated incubators), and the Wikidata search returned nothing. CTFK has two Wikidata items, **Q54826496** and **Q55606508**, which may be duplicates, and no ROR record.

## 2. Examples by level

### Intrapersonal (the individual's own knowledge, beliefs, habits)
| Org | Why it fits | IDs | Verified |
|---|---|---|---|
| **CBT-i Coach** app (VA National Center for PTSD + Stanford + DoD) | Sleep diary, education and relaxation tools for one person. VA says it's for people in CBT-I *with a provider*, not stand-alone self-care | ROR 01dbbht76 (NCPTSD) | yes |
| **National Sleep Foundation** (thensf.org) | Consumer sleep tips, Sleep in America Poll, Sleep Awareness Week. Tagline is "Best Slept Self" | ROR 00zc1hf95, Q12238011 | yes |
| **Project Sleep** | Sleep Helpline, fact sheets, podcast | none found | yes |
| **Smokefree.gov** (NCI), general health | quitSTART app, SmokefreeTXT, quit plan builder | NCI: ROR 040gcmg81, Q664846 | yes |

### Interpersonal (family, caregivers, peers)
| Org | Why it fits | IDs | Verified |
|---|---|---|---|
| **Safe to Sleep** (NICHD) | Infant safe-sleep materials for "parents, grandparents, and healthcare providers" | NICHD: ROR 04byxyr05, Q5409765; "Back to Sleep" Q4839452 | yes |
| **Zero To Three** | Resources for parents and caregivers of babies. **No sleep page found on the homepage** (the guessed URL returned 404) | ROR 01qvk6016, Q124461169 | partial |
| **Talk. They Hear You.** (SAMHSA), general health | Coaches parents to talk to kids about underage drinking | SAMHSA: ROR 03t3qg659, Q7632057 | yes |
| **First Candle** | Infant safe sleep and SIDS org | ROR 03cezf402, Q30268330 | **no** (registry IDs only) |

### Organizational / institutional (schools, employers, hospitals)
| Org | Why it fits | IDs | Verified |
|---|---|---|---|
| **Start School Later** | Pushes school districts to change bell times | Q18392879 (no ROR) | yes |
| **NIOSH Training for Nurses on Shift Work and Long Work Hours** | Schedule-design strategies, with action steps for nurse managers | NIOSH: ROR 0502a2655, Q60346 | yes |
| **The Joint Commission**, Sentinel Event Alert 48 (Dec 2011, addendum May 2018) | Tells hospitals to assess fatigue risk, involve staff in scheduling and adopt a fatigue management plan | ROR 03skrcz21, Q1703687 | partial |
| **Cribs for Kids**, National Safe Sleep Hospital Certification | Bronze/silver/gold certification for hospitals | none found | partial (site blocked fetching) |
| **Alliance for a Healthier Generation**, general health | Action Center and awards for schools and districts | none found | yes |

### Community (local coalitions, health departments, community health workers)
| Org | Why it fits | IDs | Verified |
|---|---|---|---|
| **Kent County Health Department (MI)**, infant safe sleep program | County program. Search snippet says it works with fire/EMS on safe-sleep certification | ROR 012w2p114, Q30287959 | partial (Cloudflare blocked fetching) |
| **National Association of Community Health Workers** | Founded 2019 to "unify CHWs across geography, ethnicity, sector and experience" | none found | yes |
| **County Health Rankings & Roadmaps** (UW Population Health Institute + RWJF), general health | Data and strategies for local health planning | none for the program | yes |
| **NACCHO** | Its members are local health departments | ROR 048xpjb02, Q17070599 | partial |

Other county safe-sleep coalitions that turned up in search but were **not verified**: Kern County CA (Safe Sleep Coalition, since 2017), the Marion/Polk OR coalition, Healthy Start of Hillsborough FL, and Cole County MO (Safe Cribs for Missouri kits).

### Public policy (laws, regulation, funding)
| Org | Why it fits | IDs | Verified |
|---|---|---|---|
| **GHAI** | See section 1 | none | yes |
| **Campaign for Tobacco-Free Kids** | "the leading advocacy organization working to reduce tobacco use" | Q54826496 / Q55606508 | yes |
| **AASM advocacy** | Position statement backs **permanent standard time** (JCSM 2024;20(1):121-125) and says AASM will advocate at the federal level | ROR 0090hd978, Q2842842 | partial: confirmed via AASM news items in search results, but the statement page wasn't fetched. The 2016 DST "health advisory" page has only individual tips, so don't cite that one |
| **Sleep Research Society advocacy** | Advocacy Task Force, Hill Day (April 28, 2026), federal research funding, permanent standard time | ROR 00gm6mv51, Q7539716 | yes |
| **ChangeLab Solutions**, general health | Public health law and policy | ROR 01628rf48, Q30287184 | partial (site not read) |

## 3. Orgs that span several levels
- **Project Sleep** covers every level: helpline (intrapersonal); peer groups Narcolepsy Nerd Alert and Sleep Apnea Squad (interpersonal); Rising Voices speaker training and the Hollywood & Sleep Initiative with USC Norman Lear Center (community/media); public-policy work with decision-makers (policy).
- **Start School Later** works at the organizational level (districts), the community level ("over 165 volunteer-led chapters") and the policy level. The site says 31 states introduced start-time bills and 15 signed them into law; these are self-reported figures.
- **National Sleep Foundation** runs consumer tips (intrapersonal) plus policy work: Drowsy Driving Forum on Oct 29, 2026, position statements including later school start times, and the National Sleep Advocacy Roundtable.
- **Safe to Sleep** speaks to caregivers (interpersonal) and also supplies outreach toolkits and a partner network (community).
- **Zero To Three** serves parents (interpersonal) and runs a Policy Center (policy).
- **Cribs for Kids** works at the organizational level (hospital certification) and the community level (local partner network).
- **AASM** acts as a professional society (organizational) and as a federal advocate (policy).

## 4. Numbers to check before they appear in copy
- [ ] GHAI 217 / 38 / 40+ / 5B+: self-reported. Re-check the exact wording in a browser on the ship date.
- [ ] Start School Later 31 states / 15 laws / 165+ chapters: self-reported.
- [ ] Cribs for Kids partner count: sources conflict (600+ in 2017; 1,450+ and 2,000+ in 2024).
- [ ] SRS "nearly $600 million" NIH sleep portfolio: self-reported.
- [ ] Alliance for a Healthier Generation 1,376 schools (2026): self-reported.

## 5. Open items
- [ ] Choose a CTFK Wikidata QID (two items exist).
- [ ] Confirm Q4839452 ("Back to Sleep") is acceptable as the Safe to Sleep campaign's item.
- [ ] Find a current Zero To Three sleep resource URL, or swap in another caregiver-focused sleep org.
- [ ] Check in a browser the pages that blocked fetching (Kent County, Cribs for Kids, Joint Commission SEA 48).
- [ ] First Candle, NACCHO and ChangeLab descriptions are unverified.
