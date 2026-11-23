from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
CLEAN = OUT / "cleaned"
OUT.mkdir(exist_ok=True)
CLEAN.mkdir(exist_ok=True)

FILES = {
    "matches": DATA / "ipl-matches.csv",
    "deliveries": DATA / "IPL_Ball_by_Ball_2008_2022.csv",
    "batsman_runs": DATA / "batsman_runs_ipl.csv",
    "kohli": DATA / "kohli_ipl.csv",
}

missing = [str(p) for p in FILES.values() if not p.exists()]
if missing:
    raise FileNotFoundError(
        "Missing input file(s):\n" + "\n".join(missing) +
        "\nPlace all four CSV files in the project data/ folder."
    )

matches = pd.read_csv(FILES["matches"])
deliveries = pd.read_csv(FILES["deliveries"])
batsman_runs = pd.read_csv(FILES["batsman_runs"])
kohli = pd.read_csv(FILES["kohli"])

# Normalize surrounding whitespace without deleting legitimate records.
for df in (matches, deliveries, batsman_runs, kohli):
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

# Standardize the known spelling variation seen in the supplied venue data.
if "Venue" in matches.columns:
    matches["Venue"] = matches["Venue"].replace(
        {"Wankhede Stadium, Mumbai": "Wankhede Stadium"}
    )

# Convert numeric fields safely.
for col in ["ID", "innings", "overs", "ballnumber", "batsman_run",
            "extras_run", "total_run", "isWicketDelivery"]:
    if col in deliveries.columns:
        deliveries[col] = pd.to_numeric(deliveries[col], errors="coerce")
if "ID" in matches.columns:
    matches["ID"] = pd.to_numeric(matches["ID"], errors="coerce")
if "batsman_run" in batsman_runs.columns:
    batsman_runs["batsman_run"] = pd.to_numeric(
        batsman_runs["batsman_run"], errors="coerce"
    )
if "runs" in kohli.columns:
    kohli["runs"] = pd.to_numeric(kohli["runs"], errors="coerce")

# Data quality report: report duplicates; do not blindly delete them.
tables = {
    "matches": matches,
    "deliveries": deliveries,
    "batsman_runs": batsman_runs,
    "kohli": kohli,
}
quality = []
for name, df in tables.items():
    quality.append({
        "table": name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_full_rows": int(df.duplicated().sum()),
    })
pd.DataFrame(quality).to_csv(OUT / "data_quality_report.csv", index=False)

# Delivery-key check. Repeated match IDs are expected in ball-by-ball data.
delivery_key = ["ID", "innings", "overs", "ballnumber"]
delivery_key_duplicates = int(deliveries.duplicated(delivery_key).sum())
pd.DataFrame([{
    "key": "ID + innings + overs + ballnumber",
    "duplicate_key_rows": delivery_key_duplicates
}]).to_csv(OUT / "delivery_key_check.csv", index=False)

# Core metrics. Wicket deliveries are explicitly not labelled bowler-credited wickets.
metrics = [
    ("Total Matches", int(matches["ID"].nunique())),
    ("Total Runs", int(deliveries["total_run"].sum())),
    ("Total Seasons", int(matches["Season"].nunique())),
    ("Unique Batters in Ball Data", int(deliveries["batter"].nunique())),
    ("Wicket Deliveries", int(deliveries["isWicketDelivery"].fillna(0).sum())),
]
pd.DataFrame(metrics, columns=["Metric", "Value"]).to_csv(
    OUT / "summary_metrics.csv", index=False
)

def grouped_count(df, group_col, output_name):
    result = (df.groupby(group_col, dropna=False)["ID"]
              .nunique().reset_index(name="Total_Matches")
              .sort_values("Total_Matches", ascending=False))
    result.to_csv(OUT / output_name, index=False)
    return result

grouped_count(matches, "Season", "matches_by_season.csv")
grouped_count(matches, "City", "matches_by_city.csv")
grouped_count(matches, "Venue", "matches_by_venue.csv")

top_batters = (deliveries.groupby("batter", dropna=False)["batsman_run"]
               .sum().reset_index(name="Total_Runs")
               .sort_values("Total_Runs", ascending=False).head(10))
top_batters.to_csv(OUT / "top_10_batters_from_ball_data.csv", index=False)

team_runs = (deliveries.groupby("BattingTeam", dropna=False)["total_run"]
             .sum().reset_index(name="Total_Runs")
             .sort_values("Total_Runs", ascending=False))
team_runs.to_csv(OUT / "team_total_runs.csv", index=False)

wins = (matches["WinningTeam"].dropna().value_counts()
        .rename_axis("Team").reset_index(name="Total_Wins"))
wins.to_csv(OUT / "wins_by_team.csv", index=False)

# Kohli file contains match_no and runs only; do not infer seasons or match IDs.
kohli_summary = pd.DataFrame([
    ("Matches in supplied Kohli file", int(kohli["match_no"].nunique())),
    ("Runs in supplied Kohli file", int(kohli["runs"].sum())),
    ("Average runs per row", round(float(kohli["runs"].mean()), 2)),
    ("Highest score in supplied file", int(kohli["runs"].max())),
], columns=["Metric", "Value"])
kohli_summary.to_csv(OUT / "kohli_summary.csv", index=False)

# Save cleaned copies, preserving source CSVs.
for name, df in tables.items():
    df.to_csv(CLEAN / f"{name}_cleaned.csv", index=False)

print("Analysis completed.")
print(f"Matches: {matches['ID'].nunique():,}")
print(f"Runs: {int(deliveries['total_run'].sum()):,}")
print(f"Delivery-key duplicate rows: {delivery_key_duplicates:,}")
print(f"Outputs saved in: {OUT}")
