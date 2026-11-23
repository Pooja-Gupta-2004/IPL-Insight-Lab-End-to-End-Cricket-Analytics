-- IPL Insight Lab | SQLite analysis queries
-- Import the supplied CSVs as: matches, ball_by_ball, batter_totals, kohli.
-- Column names retain the source CSV spelling/case.

-- 1. Table row counts
SELECT 'matches' AS table_name, COUNT(*) AS row_count FROM matches
UNION ALL
SELECT 'ball_by_ball', COUNT(*) FROM ball_by_ball
UNION ALL
SELECT 'batter_totals', COUNT(*) FROM batter_totals
UNION ALL
SELECT 'kohli', COUNT(*) FROM kohli;

-- 2. Match and scoring summary
SELECT
    COUNT(DISTINCT ID) AS total_matches
FROM matches;

SELECT
    SUM(total_run) AS total_runs,
    COUNT(DISTINCT batter) AS unique_batters,
    SUM(isWicketDelivery) AS wicket_deliveries
FROM ball_by_ball;

-- 3. Matches by season
SELECT Season, COUNT(DISTINCT ID) AS total_matches
FROM matches
GROUP BY Season
ORDER BY MIN(Date);

-- 4. Matches by city
SELECT City, COUNT(DISTINCT ID) AS total_matches
FROM matches
GROUP BY City
ORDER BY total_matches DESC;

-- 5. Top 10 venues by match count
SELECT Venue, COUNT(DISTINCT ID) AS total_matches
FROM matches
GROUP BY Venue
ORDER BY total_matches DESC
LIMIT 10;

-- 6. Top 10 batters from ball-by-ball data
SELECT batter, SUM(batsman_run) AS total_runs
FROM ball_by_ball
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;

-- 7. Runs by batting team
SELECT BattingTeam, SUM(total_run) AS total_runs
FROM ball_by_ball
GROUP BY BattingTeam
ORDER BY total_runs DESC;

-- 8. Wins by team
SELECT WinningTeam, COUNT(*) AS total_wins
FROM matches
WHERE WinningTeam IS NOT NULL AND TRIM(WinningTeam) <> ''
GROUP BY WinningTeam
ORDER BY total_wins DESC;

-- 9. Dismissal-kind distribution (NULLs excluded)
SELECT kind, COUNT(*) AS wicket_deliveries
FROM ball_by_ball
WHERE isWicketDelivery = 1 AND kind IS NOT NULL
GROUP BY kind
ORDER BY wicket_deliveries DESC;

-- 10. Supplied Kohli file summary (no season inference)
SELECT
    COUNT(DISTINCT match_no) AS matches_in_file,
    SUM(runs) AS total_runs,
    AVG(runs) AS average_runs,
    MAX(runs) AS highest_score
FROM kohli;
