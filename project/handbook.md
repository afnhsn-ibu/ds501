# DS 501 Course Project Handbook

## Project overview

Each student completes one individual data science project on a real dataset, following CRISP-DM from question to recommendation. The project is worth 50% of the DS 501 grade: proposal 5%, final report 35%, presentation 10%.

The project should show that you can:

1. Turn a real decision into an actionable data science question.
2. Acquire, clean, and document data from at least one real source.
3. Explore the data and test at least one hypothesis with an appropriate statistical method.
4. Build and compare at least two models, judged against a baseline and a business-relevant metric.
5. Assess privacy, fairness, and ethical risks.
6. Communicate the result in a structured report and a short talk aimed at a decision-maker.

**Deliverables:** a proposal (week 7), a final report of 4,000–6,000 words, a reproducible Jupyter notebook in a GitHub repository, and a 12-minute presentation (week 12). Use the starter notebook `DS501_Project_Notebook_Template.ipynb`.

## Milestones and deadlines

The project runs all semester: three graded milestones (50% of the course grade) and two ungraded check-ins where students get feedback before it counts.

| Week | Milestone | What to submit | Weight |
| --- | --- | --- | --- |
| 3 | Topic and dataset | One paragraph: decision, question, dataset link | Ungraded |
| 5 | Data audit | Notebook sections 1–3: data loaded, described, quality issues listed | Ungraded |
| 7 | Proposal | Two-page proposal (template below) | 5% |
| 10 | Progress check | Notebook with EDA, one test, and a first model against a baseline | Ungraded |
| 12 | Final report, notebook, presentation | Report PDF, repository link, slides | 35% + 10% |

## Choosing a question and dataset

Start from a decision someone must make, then find data that can inform it. A good project question names a decision, a target, and a time frame (lesson 1-2).

Your dataset must:

- Contain at least 1,000 rows and 8 variables, or a smaller set that you collected yourself and justify.
- Include a variable you can predict or a clear hypothesis you can test.
- Be legally usable for coursework: open licence, your own collection, or written permission from the owner.
- Contain no directly identifying personal data. Anonymise workplace data before it leaves the organisation.
- Not be a dataset already used in a DS 501 lab (Penguins, Telco, Titanic, Tips, Diamonds, COMPAS), unless you combine it with new data.

Suggested sources:

| Source | What you find there | Link |
| --- | --- | --- |
| State Statistical Office of North Macedonia | Population, labour, prices, regional statistics | [stat.gov.mk](https://www.stat.gov.mk) |
| Open data portal of North Macedonia | Government datasets | [data.gov.mk](https://data.gov.mk) |
| EU Open Data Portal and Eurostat | European statistics and public-sector data | [data.europa.eu](https://data.europa.eu) |
| World Bank Open Data | Development indicators by country (API) | [data.worldbank.org](https://data.worldbank.org) |
| Open-Meteo | Historical and forecast weather (free API) | [open-meteo.com](https://open-meteo.com) |
| UCI Machine Learning Repository | Curated research datasets | [archive.ics.uci.edu](https://archive.ics.uci.edu) |
| Kaggle Datasets | Community datasets; check licence and quality | [kaggle.com/datasets](https://www.kaggle.com/datasets) |

**Week 3 checkpoint:** submit one paragraph with your decision, question, and dataset link on Moodle. The instructor approves or suggests changes within one week.

## Proposal template (week 7, 5%)

At most two pages plus references. It builds on the one-page briefs from lessons 2-1 and 2-2.

1. **Title and author.**
2. **Business understanding** (about 250 words): the decision, the stakeholder, the business objective and its success criterion, and constraints.
3. **Data science goal** (about 100 words): the analytic approach (descriptive, inferential, classification, regression, clustering), the target variable, and the model success criterion.
4. **Data** (about 250 words): sources with links, size, unit of analysis, key variables, licence or permission, and known quality issues.
5. **Method plan** (about 200 words): the hypothesis you will test, the models you will compare, the baseline, and the evaluation metric.
6. **Ethics and privacy** (about 150 words): who could be harmed, personal data and its legal basis, and fairness risks.
7. **Timeline**: what you will finish by week 10.
8. **References.**

## Final report structure (week 12, 35%)

4,000–6,000 words excluding references, appendices, and code. The structure follows Haider's report structure (lesson 8-3) mapped onto CRISP-DM.

| Section | Content | Words |
| --- | --- | --- |
| Cover page | Title, author, student ID, course, date, repository link | — |
| Executive summary | Question, main finding with its number, recommendation, key limitation | 250–300 |
| 1. Introduction and business understanding | Decision, stakeholders, objectives, success criteria | 400–600 |
| 2. Related work | 5–10 sources: what is known, the gap your project addresses | 400–700 |
| 3. Data | Sources, collection, licence, description, quality report | 500–800 |
| 4. Data preparation | Cleaning decisions, features built, final dataset, leakage checks | 400–700 |
| 5. Exploratory analysis and inference | Key distributions and relationships; at least one hypothesis test with its assumptions | 600–1,000 |
| 6. Modelling and evaluation | Baseline, at least two models, validation design, metrics, error costs | 700–1,100 |
| 7. Ethics, privacy, and fairness | GDPR basis, risks, a fairness check across at least one group | 300–500 |
| 8. Discussion and recommendation | What the decision-maker should do, limitations, next steps | 400–600 |
| References | APA 7th edition | — |
| Appendices | Data dictionary, extra charts, AI-use statement | — |

Every figure has a numbered caption and is referred to in the text. Every number in the executive summary must be traceable to the notebook.

## Notebook and repository requirements

The notebook is the evidence behind the report. It must run from top to bottom (`Kernel → Restart & Run All`) without errors.

- Start from `DS501_Project_Notebook_Template.ipynb`; keep its CRISP-DM section headings.
- Load data from a URL or from a `data/` folder in the repository; never from a path on your own computer.
- Set a random seed for every split and model so results can be reproduced.
- Explain each step in a markdown cell: what you did and why.
- List package versions in `requirements.txt`.
- Repository layout: `README.md` (question, data source, how to run), `notebook.ipynb`, `data/` (or a download script if the data is large or restricted), `report.pdf`, `requirements.txt`.
- Do not commit personal data, API keys, or passwords.

## Presentation guidelines (week 12, 10%)

12 minutes plus 5 minutes of questions, for an audience of decision-makers rather than data scientists.

1. The decision and why it matters (1 minute).
2. The data: what it covers and its main limitation (2 minutes).
3. The two or three findings that matter, each with one clear chart (5 minutes).
4. The model: how good it is compared with the baseline, in business terms (2 minutes).
5. The recommendation, its risks, and the ethical considerations (2 minutes).

At most 12 slides. Lead each slide with its message as the title. No code on slides; keep technical detail for the questions.

## Rubrics

Each criterion is scored on four levels: Excellent (100%), Good (75%), Adequate (50%), Insufficient (0–25%). The points are percentages of the component grade.

**Proposal (5% of course grade)**

| Criterion | Points | Excellent looks like |
| --- | --- | --- |
| Business understanding | 25 | A real decision, a named stakeholder, measurable success criteria |
| Data plan | 25 | Accessible, legal data that fits the question; quality risks identified |
| Method plan | 25 | Hypothesis, baseline, at least two candidate models, a justified metric |
| Ethics | 15 | Concrete risks and mitigations, legal basis for personal data |
| Clarity | 10 | Within two pages, well organised, referenced |

**Final report (35% of course grade)**

| Criterion | Points | Excellent looks like |
| --- | --- | --- |
| Problem framing and related work | 10 | Clear decision and gap, supported by 5+ relevant sources |
| Data acquisition and preparation | 15 | Documented sources, justified cleaning decisions, leakage avoided |
| Exploratory analysis and inference | 15 | Insightful EDA; correct test with checked assumptions and interpreted effect size |
| Modelling and evaluation | 20 | Baseline, 2+ models, sound validation, metric tied to error costs |
| Ethics, privacy, and fairness | 10 | Legal basis stated; fairness checked across at least one group |
| Recommendation and limitations | 10 | Actionable, honest about uncertainty and limits |
| Reproducibility | 10 | Notebook runs end to end; README and requirements complete |
| Writing and visualisation | 10 | Clear structure, labelled figures, executive summary a manager can act on |

**Presentation (10% of course grade)**

| Criterion | Points | Excellent looks like |
| --- | --- | --- |
| Message and structure | 30 | The decision and recommendation are clear within the first two minutes |
| Evidence and visuals | 30 | Each slide carries one finding with one clear chart |
| Handling questions | 20 | Accurate, concise answers that acknowledge limits |
| Timing and delivery | 20 | Within 12 minutes; audible, confident, no reading from slides |

## AI use, ethics, and submission checklists

**AI-use statement** (appendix of the proposal and the report). Generative AI is allowed for coding help, debugging, and brainstorming. State:

- Which tools you used (e.g. ChatGPT, Claude, GitHub Copilot) and for which tasks.
- How you checked the output (tests, documentation, re-running the analysis).
- Text written by AI and submitted as your own analysis is treated as plagiarism.

**Ethics checklist** (answer each in section 7 of the report):

- [ ] Who could be harmed by the decision this project supports?
- [ ] Does the data contain personal data? What is the legal basis under GDPR and the Law on Personal Data Protection?
- [ ] Is the data minimised to what the question needs, and anonymised or pseudonymised?
- [ ] Does model performance differ across groups (age, sex, region)? By how much?
- [ ] Can a decision based on the model be explained to the person affected?
- [ ] What happens when the model is wrong, and who can correct it?

**Submission checklist** (week 12):

- [ ] Report PDF uploaded to Moodle, within the word limit, with cover page and executive summary.
- [ ] Repository link in the report; repository is accessible to the instructor.
- [ ] Notebook runs top to bottom without errors.
- [ ] README, requirements.txt, and data or download script included.
- [ ] AI-use statement included.
- [ ] Slides uploaded before the presentation session.
