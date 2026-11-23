# IPL Insight Lab — End-to-End Cricket Analytics

An IPL analytics portfolio project combining Python data preparation and exploratory analysis, SQL business queries, and a six-page Power BI report.

## Repository contents

- `data/` — four supplied CSV datasets
- `src/ipl_analysis.py` — reproducible Python analysis
- `sql/ipl_analysis.sql` — SQLite analysis queries
- `powerbi/` — place the Power BI `.pbix` report here
- `screenshots/` — add screenshots of all six report pages
- `outputs/` — generated analysis results (created when Python runs)
- `requirements.txt` — Python dependency list

## Tools

Python, pandas, SQLite, Power BI Desktop, Power Query, and DAX.

## Run the Python analysis

Use Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python src/ipl_analysis.py
```

The script reads the four CSV files from `data/` and creates data-quality checks, summary metrics, season/city/venue summaries, top batters, team runs, team wins, and cleaned copies in `outputs/`.

## Run the SQL

Import the four CSVs into SQLite using these table names:

- `matches`
- `ball_by_ball`
- `batter_totals`
- `kohli`

Then execute `sql/ipl_analysis.sql` in a SQLite client.

## Power BI report

The report contains six pages covering IPL overview, Virat Kohli batting, team performance, venue and city insights, bowling and wicket insights, and season comparison/records. Put the `.pbix` file in `powerbi/` and add page screenshots to `screenshots/`.

## Data interpretation notes

- Match IDs repeat in ball-by-ball data because each match has many deliveries.
- The script reports duplicate rows and checks the composite delivery key `ID + innings + overs + ballnumber`; it does not automatically delete records.
- `isWicketDelivery` represents wicket deliveries and is not necessarily identical to bowler-credited wickets.
- The supplied Kohli file contains `match_no` and `runs` only; it does not support season-specific analysis by itself.
- The script standardizes the known `Wankhede Stadium, Mumbai` spelling to `Wankhede Stadium` in cleaned outputs.
- Check dataset redistribution/licensing terms before publishing the raw CSVs publicly.

## Before publishing

1. Run the Python script and inspect `outputs/`.
2. Run the SQL queries against the imported CSV tables.
3. Validate Power BI measures, relationships, and filters against the analysis outputs.
4. Add screenshots of all six report pages.
5. Confirm that the datasets may be redistributed publicly before committing them to a public repository.
