\# neuro-redflag-triage



evidence-based emergency clinical decision support engine for red-flag headache triage and neurovascular diagnostic risk stratification.



\## overview



headaches account for a substantial volume of emergency department presentations. while over 90% of cases are benign primary headache disorders like migraine or tension-type headache, 1% to 5% represent life-threatening secondary neurovascular emergencies:

\- aneurysmal subarachnoid hemorrhage (SAH)

\- acute bacterial and viral meningitis

\- temporal (giant cell) arteritis with risk of irreversible bilateral blindness

\- space-occupying intracranial lesions and elevated intracranial pressure (ICP)



due to diagnostic mimicry and high emergency room volume, secondary etiologies are frequently mistaken for migraines. additionally, false reassurance from normal non-contrast head CT scans performed after early diagnostic windows leads to premature discharges.



\*\*neuro-redflag-triage\*\* automates risk scoring and diagnostic safety checks to prevent premature discharge and guide rapid clinical escalation.



\## key features



\- \*\*secondary red-flag triage engine:\*\* implements the SNOOP10 criteria covering systemic symptoms, hyperacute onset kinetics (< 5 minutes), temporal arteritis features in patients aged 50+, and positional or pressure triggers.

\- \*\*false-negative CT safety gate:\*\* visualizes non-contrast head CT sensitivity decay over time and enforces a lumbar puncture recommendation when clinical suspicion remains high despite a normal scan after 6 hours.

\- \*\*interactive visualization:\*\* built with Plotly to model imaging sensitivity curves dynamically.



\## installation \& local run



```bash

git clone \[https://github.com/yeahnandinihere-droid/neuro-redflag-triage.git](https://github.com/yeahnandinihere-droid/neuro-redflag-triage.git)

cd neuro-redflag-triage

pip install -r requirements.txt

streamlit run app.py

