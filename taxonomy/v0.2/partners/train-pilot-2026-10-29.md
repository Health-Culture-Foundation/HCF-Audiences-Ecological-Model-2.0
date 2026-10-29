# TRAIN catalog pilot, 2026-10-29

A read of every 10th course in `https://www.train.org/sitemap-courses.xml` (391 of 3,908), made from Kalman's logged-in browser at one request a second with his approval. It used TRAIN's course record (`/a/course/<id>/`), the same data a course page shows. Only catalog fields were kept; no contact details or user data. It tests the crosswalks in this folder against real course tags. Counts are courses in the sample.

## Coverage
- 391 courses read, 0 errors.
- 360 are marked active, but only 91 are inside their expiry date. Most of the sitemap is old courses.
- 360 have audience tags, 360 have subject areas, 160 have a credit type.
- Languages: English 358, Russian 4, Spanish 2.
- Format: web self-study 213, archived webcast 89, recorded webcast 48, blended series 7.
- Skill level: introductory 290, intermediate 67, advanced 3.
- Availability: National 360, Massachusetts 1.

## Audience tags seen (42 of the 47 in `train-course-audience.csv`; all 42 are in the crosswalk)
Public Health 180 · General Public Health Staff 156 · Nurses 107 · Healthcare 101 · Physicians and Other Clinicians 98 · Emergency Management 72 · Educators / Trainers 65 · Other 64 · Emergency Responders / Receivers 49 · Allied Health Professionals 48 · Social Workers 47 · Epidemiologists / Surveillance Staff 45 · Policy / Planner 34 · Emergency Medical Services 31 · Communicable Disease Staff 30 · Environmental Health Professionals 30 · Mental Health Professionals 27 · Researchers / Analysts 24 · Laboratory Professionals 19 · Teacher / Faculty 16 · Substance Use Disorder Professionals 15 · Pharmacy Professionals 15 · Case Manager 15 · Student 14 · Hazardous Materials Personnel 13 · Dietitians 11 · Fire Service 9 · Public Safety Communications 9 · Occupational Health and Safety Professionals 8 · Home Care 8 · Animal Control / Veterinarians 7 · Public Information / Media Specialists 6 · Law Enforcement 6 · Childcare Providers 6 · Human Services 6 · Dental Professionals 4 · Biostatisticians 3 · Public Works 3 · Information Systems Professionals 3 · Military Personnel 1 · Community Health Workers 1 · Medical Examiner / Coroner / Mortician 1

What it means for v0.2: the TRAIN terms we map only loosely are common. Emergency Management (72), Allied Health (48), Environmental Health (30) and Laboratory (19) all land on broad parents today. They're the strongest case for new role ids.

## Credit types seen (31; all are in `train-credit-types.csv`)
IACET CEU 53 · Certificate of Attendance 37 · CHES 37 · ACCME CME 34 · ANCC CNE 33 · CPH 20 · CNE Contact Hours 18 · ACCME Non-Physician 12 · APA 8 · CME 7 · ACPE CPE 7 · AAFP 7 · Contact Hours 6 · ASWB 6 · NYSED SW 6 · NBCC 6 · Dietitians CPE 5 · HRC HEI 5 · ACPE Contact Hours 4 · AAVSB RACE 4 · Social Workers 3 · PACE 3 · JA IPCE 2 · NYSEDP 2 · ACPE-Technician 2 · Other, AAPA, COPE, AOTA, CDR, Florida Clinical Laboratory 1 each

## Subject areas seen (70) — input for a topics crosswalk
General Public Health 138 · Healthcare 89 · Emergency Management 66 · Education/Training/Exercises/Drills 58 · Other 54 · Prevention / Promotion 48 · Infectious Diseases / Immunizations 39 · Preparedness & Response 37 · Epidemiology / Biostatistics 34 · Workforce Development 31 · Performance / Quality Improvement 31 · Maternal / Child Health 30 · Cultural Competence 28 · Management / Leadership 27 · Mental Health 26 · Environmental / Industrial Health 25 · Minority Health / Health Disparities 24 · Health / Risk Communications 23 · Emergency Medical Services 23 · Policy / Planning 21 · Chronic Diseases 20 · Partnerships 20 · Access to Care (includes health insurance) 20 · Substance Use Disorder (Alcohol Tobacco and Other Drugs) 19 · Injury / Violence / Trauma 17 · Program Development 17 · Assessment/Analysis 17 · Surveillance 16 · Sexually Transmitted Diseases 16 · HIV/AIDS 15 · Public Safety 15 · International Health 15 · Evaluation 13 · Nutrition 12 · Fire 11 · Investigations / Inspections / Enforcement 11 · Research Methods 11 · Laboratory 11 · Health Screening 11 · Personal Communications 10 · Family Planning / Reproductive Health 10 · Hazmat 8 · Disability 8 · Occupational Health and Safety 8 · Volunteering 6 · SPECIAL TOPIC: Opioids 6 · Mass Prophylaxis 5 · Computer Skills/Training 5 · Legal / Ethical 5 · Home Care 5 · Pest / Vector Control 4 · Law Enforcement 4 · Public Works 4 · Informatics / Technology 3 · Marketing 3 · Geriatrics and Extended Care 3 · Agriculture 2 · Oral Health 2 · Animal Health 2 · Physical Activity / Obesity 2 · Genetics 1 · Finance / Grants 1 · Health Equity 1 · Vision / Eye Health 1 · Homelessness 1

## Next
- A full read (3,908 courses, about 65 minutes at the same pace) would give every subject area and the live addiction and mental health courses for library cards. Wait for PHF's OK or an export first (issue vivwebsolutions/health-culture.org#178).
- The sample is national courses from the sitemap. State-only courses, such as Massachusetts ones, are probably not in it.
