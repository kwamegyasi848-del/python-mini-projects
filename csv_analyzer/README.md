# CSV Analyzer (Python + pandas)

Generates a report for a CSV: shape, dtypes, missing values, numeric summary, and optional group summaries.

## Run
Basic:
python main.py --file sample.csv

Group + target:
python main.py --file sample.csv --group-by Department --target Salary

Export report:
python main.py --file sample.csv --group-by Department --target Salary --out report.md
