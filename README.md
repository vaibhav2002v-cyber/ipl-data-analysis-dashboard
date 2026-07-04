# 🏏 IPL Data Analysis Dashboard

An interactive Streamlit dashboard for exploring IPL (Indian Premier League) cricket data from **2008 to 2020** — covering match results, player performance, venues, season trends, and team rivalries.

## 📌 What This Project Does

This app loads two IPL datasets (match-level and ball-by-ball data), cleans them, and presents seven interactive analysis sections through a sidebar navigation menu. Every chart is accompanied by a plain-English **"What this tells us"** summary box, so the numbers are explained rather than just shown.

## 🗂️ Dashboard Sections

| Section | What it covers |
|---|---|
| **Home** | Dataset overview — total matches, deliveries, seasons, teams, and sample data tables |
| **Team Performance** | Matches played, matches won, and win % by team, with bar charts ranking every franchise |
| **Player Statistics** | Tabbed view of top run scorers, top wicket takers, best strike rates (min. 500 balls faced), and most fours/sixes |
| **Match Insights** | Toss-decision trends, how often the toss winner also wins the match, match result types (runs vs. wickets), and the biggest wins by margin |
| **Venue Analysis** | Top 15 venues and top 15 cities by matches hosted |
| **Season Trends** | Matches played per season, plus a season-by-season win comparison for user-selected teams |
| **Head-to-Head** | Pick any two teams to see their full head-to-head record, recent meetings, and the all-time most frequent IPL matchups |

## 🛠️ What Was Built / Fixed

- **Built the core dashboard**: 7-page Streamlit app using `plotly` for interactive charts (bar, pie, and line/scatter), `pandas` for data wrangling, and custom CSS for styling.
- **Data cleaning pipeline**: handled missing values (city, player of match, result margin, method), converted dates, extracted season year, and standardized renamed franchises (e.g. Delhi Daredevils → Delhi Capitals).
- **Fixed file path bug**: `pd.read_csv()` calls originally used relative paths that broke when the app was launched from a different working directory. Paths are now resolved relative to the script's own location using `os.path.dirname(os.path.abspath(__file__))`.
- **Fixed a filename typo**: corrected a mismatched/misspelled CSV filename (`' Ball-by-Ball 2008-2020.csv'` → `'IPL Ball-by-Ball 2008-2020.csv'`).
- **Added insight summaries**: added "💡 What this tells us" explanatory boxes to every chart that was missing one (Boundaries tab, Match Insights toss/result charts, Venue city chart, both Season Trends charts, and both Head-to-Head charts), so each visualization is paired with a takeaway instead of a raw chart.
- **Fixed a dark-theme readability bug**: the insight boxes had no explicit text color, so text rendered white-on-white under Streamlit's dark theme. Added forced text colors via CSS so summaries are readable in any theme.

## 📊 Datasets Used

- `IPL Matches 2008-2020.csv` — 816 matches with team, toss, venue, result, and margin data
- `IPL Ball-by-Ball 2008-2020.csv` — 193,468 individual deliveries with batsman, bowler, and outcome data

> Both CSV files must sit in the same folder as `ipl.py` for the app to load correctly.

## 🚀 Running the App

```bash
pip install streamlit pandas numpy matplotlib seaborn plotly
streamlit run ipl.py
```

Then open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## 📦 Tech Stack

- **Streamlit** — app framework and UI
- **Pandas / NumPy** — data cleaning and aggregation
- **Plotly Express / Graph Objects** — interactive charts
- **Matplotlib / Seaborn** — imported for potential static plotting (available if extended)

## 📁 Files

```
.
├── ipl.py                              # Main Streamlit app
├── IPL Matches 2008-2020.csv           # Match-level dataset
├── IPL Ball-by-Ball 2008-2020.csv      # Delivery-level dataset
└── README.md                           # This file
```
