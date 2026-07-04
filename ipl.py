"""
IPL Data Analysis Dashboard - Streamlit App
============================================
Interactive web dashboard for IPL data analysis (2008-2020)
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
warnings.filterwarnings('ignore')

# Directory this script lives in, so CSV paths work regardless of the
# folder you launch `streamlit run` from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set page configuration
st.set_page_config(
    page_title="IPL Data Analysis Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #43A047;
        padding: 10px 0;
    }
    .insight-box {
        background-color: #f0f8ff;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #1a1a1a !important;
    }
    .insight-box h4 {
        color: #0d47a1 !important;
    }
    .insight-box b {
        color: #1a1a1a !important;
    }
    .insight-box, .insight-box * {
        color: #1a1a1a;
    }
    .insight-box h4, .insight-box h4 * {
        color: #0d47a1;
    }
    .metric-card {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏏 IPL Data Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #666;'>Comprehensive analysis of IPL data from 2008 to 2020</h4>", unsafe_allow_html=True)
st.markdown("---")

# Cache data loading
@st.cache_data
def load_data():
    matches_df = pd.read_csv(os.path.join(BASE_DIR, 'IPL Matches 2008-2020.csv'))
    deliveries_df = pd.read_csv(os.path.join(BASE_DIR, 'IPL Ball-by-Ball 2008-2020.csv'))

    # Clean data
    matches_df['city'] = matches_df['city'].fillna('Unknown')
    matches_df['player_of_match'] = matches_df['player_of_match'].fillna('No Award')
    matches_df['result_margin'] = matches_df['result_margin'].fillna(0)
    matches_df['method'] = matches_df['method'].fillna('Normal')
    matches_df['date'] = pd.to_datetime(matches_df['date'])
    matches_df['season'] = matches_df['date'].dt.year

    # Standardize team names
    team_map = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Rising Pune Supergiants': 'Rising Pune Supergiant'
    }
    for old, new in team_map.items():
        matches_df['team1'] = matches_df['team1'].replace(old, new)
        matches_df['team2'] = matches_df['team2'].replace(old, new)
        matches_df['toss_winner'] = matches_df['toss_winner'].replace(old, new)
        matches_df['winner'] = matches_df['winner'].replace(old, new)
        deliveries_df['batting_team'] = deliveries_df['batting_team'].replace(old, new)
        deliveries_df['bowling_team'] = deliveries_df['bowling_team'].replace(old, new)

    return matches_df, deliveries_df

# Load data
matches_df, deliveries_df = load_data()

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Analysis Section:",
    ["Home", "Team Performance", "Player Statistics", "Match Insights",
     "Venue Analysis", "Season Trends", "Head-to-Head"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**About this Dashboard:**
This app analyzes IPL cricket data from 2008 to 2020 using interactive charts and visualizations.

**Datasets Used:**
- IPL Matches (816 matches)
- IPL Ball-by-Ball (193,468 deliveries)
""")

# ===================== HOME PAGE =====================
if page == "Home":
    st.markdown('<div class="sub-header">📋 Data Overview & Summary</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Matches", len(matches_df))
    with col2:
        st.metric("Total Deliveries", f"{len(deliveries_df):,}")
    with col3:
        st.metric("Seasons Covered", matches_df['season'].nunique())
    with col4:
        st.metric("Teams", matches_df['team1'].nunique())

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Matches Dataset Sample")
        st.dataframe(matches_df.head(10), use_container_width=True)
    with col2:
        st.markdown("### Deliveries Dataset Sample")
        st.dataframe(deliveries_df.head(10), use_container_width=True)

    st.markdown("---")

    st.markdown("""
    <div class="insight-box">
    <h4>🔍 Key Insights Available in this Dashboard:</h4>
    <ul>
        <li><b>Team Performance:</b> Win rates, matches played, seasonal trends</li>
        <li><b>Player Statistics:</b> Top run scorers, wicket takers, strike rates, boundaries</li>
        <li><b>Match Insights:</b> Toss impact, match margins, result types</li>
        <li><b>Venue Analysis:</b> Most used stadiums and their statistics</li>
        <li><b>Season Trends:</b> How teams performed across different seasons</li>
        <li><b>Head-to-Head:</b> Biggest rivalries and matchup records</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ===================== TEAM PERFORMANCE =====================
elif page == "Team Performance":
    st.markdown('<div class="sub-header">🏆 Team Performance Analysis</div>', unsafe_allow_html=True)

    # Team stats
    team1_counts = matches_df['team1'].value_counts()
    team2_counts = matches_df['team2'].value_counts()
    all_teams = set(team1_counts.index) | set(team2_counts.index)
    teams_played = pd.Series({team: team1_counts.get(team, 0) + team2_counts.get(team, 0) for team in all_teams})
    matches_won = matches_df['winner'].value_counts()

    team_stats = pd.DataFrame({
        'Matches Played': teams_played,
        'Matches Won': matches_won
    }).fillna(0).astype(int)
    team_stats['Win %'] = (team_stats['Matches Won'] / team_stats['Matches Played'] * 100).round(2)
    team_stats = team_stats.sort_values('Matches Won', ascending=False)

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("### Team Statistics")
        st.dataframe(team_stats, use_container_width=True)

    with col2:
        fig = px.bar(
            x=team_stats['Matches Won'].values,
            y=team_stats.index,
            orientation='h',
            title='Total Matches Won by Each Team',
            labels={'x': 'Wins', 'y': 'Team'},
            color=team_stats['Matches Won'].values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Win percentage chart
    fig2 = px.bar(
        x=team_stats['Win %'].values,
        y=team_stats.index,
        orientation='h',
        title='Win Percentage by Team',
        labels={'x': 'Win %', 'y': 'Team'},
        color=team_stats['Win %'].values,
        color_continuous_scale='Plasma'
    )
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 Insight:</h4>
    <b>{team_stats.index[0]}</b> leads with <b>{team_stats.iloc[0]['Matches Won']}</b> total wins, 
    while teams like <b>Chennai Super Kings</b> have high win percentages, showing consistency matters.
    </div>
    """, unsafe_allow_html=True)

# ===================== PLAYER STATISTICS =====================
elif page == "Player Statistics":
    st.markdown('<div class="sub-header">👤 Player Statistics</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Top Run Scorers", "Top Wicket Takers", "Strike Rates", "Boundaries"])

    # Top Run Scorers
    with tab1:
        batsman_runs = deliveries_df.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(15)
        fig = px.bar(
            x=batsman_runs.values,
            y=batsman_runs.index,
            orientation='h',
            title='Top 15 Run Scorers in IPL',
            labels={'x': 'Total Runs', 'y': 'Batsman'},
            color=batsman_runs.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
        <b>{batsman_runs.index[0]}</b> leads with <b>{batsman_runs.iloc[0]}</b> runs - the highest in IPL history!
        </div>
        """, unsafe_allow_html=True)

    # Top Wicket Takers
    with tab2:
        wicket_kinds = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
        wickets_df = deliveries_df[deliveries_df['dismissal_kind'].isin(wicket_kinds)]
        bowler_wickets = wickets_df.groupby('bowler').size().sort_values(ascending=False).head(15)
        fig = px.bar(
            x=bowler_wickets.values,
            y=bowler_wickets.index,
            orientation='h',
            title='Top 15 Wicket Takers in IPL',
            labels={'x': 'Total Wickets', 'y': 'Bowler'},
            color=bowler_wickets.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
        <b>{bowler_wickets.index[0]}</b> is the leading wicket-taker with <b>{bowler_wickets.iloc[0]}</b> wickets!
        </div>
        """, unsafe_allow_html=True)

    # Strike Rates
    with tab3:
        balls_faced = deliveries_df.groupby('batsman').size()
        total_runs = deliveries_df.groupby('batsman')['batsman_runs'].sum()
        strike_rate = (total_runs / balls_faced * 100).round(2)
        qualified = strike_rate[balls_faced >= 500].sort_values(ascending=False).head(15)
        fig = px.bar(
            x=qualified.values,
            y=qualified.index,
            orientation='h',
            title='Top 15 Strike Rates (Min 500 Balls)',
            labels={'x': 'Strike Rate', 'y': 'Batsman'},
            color=qualified.values,
            color_continuous_scale='Cividis'
        )
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
        <b>{qualified.index[0]}</b> has the best strike rate at <b>{qualified.iloc[0]}</b> among qualified batsmen!
        </div>
        """, unsafe_allow_html=True)

    # Boundaries
    with tab4:
        fours = deliveries_df[deliveries_df['batsman_runs'] == 4]
        sixes = deliveries_df[deliveries_df['batsman_runs'] == 6]
        most_fours = fours.groupby('batsman').size().sort_values(ascending=False).head(10)
        most_sixes = sixes.groupby('batsman').size().sort_values(ascending=False).head(10)

        fig = make_subplots(rows=1, cols=2, subplot_titles=['Most Fours', 'Most Sixes'])
        fig.add_trace(go.Bar(x=most_fours.values, y=most_fours.index, orientation='h',
                              marker_color='#2E86C1', name='Fours'), row=1, col=1)
        fig.add_trace(go.Bar(x=most_sixes.values, y=most_sixes.index, orientation='h',
                              marker_color='#E74C3C', name='Sixes'), row=1, col=2)
        fig.update_layout(height=500, showlegend=False, title_text="Top Boundary Hitters")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
        <h4>💡 What this tells us:</h4>
        <b>{most_fours.index[0]}</b> hits the most fours (<b>{most_fours.iloc[0]}</b>) while <b>{most_sixes.index[0]}</b> 
        clears the ropes most often (<b>{most_sixes.iloc[0]}</b> sixes). Players who top the sixes list tend to be 
        power-hitters valued for finishing innings, while four-hitters often anchor the innings with consistent timing.
        </div>
        """, unsafe_allow_html=True)

# ===================== MATCH INSIGHTS =====================
elif page == "Match Insights":
    st.markdown('<div class="sub-header">🎯 Match Insights</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Toss Analysis
        toss_match = matches_df[matches_df['toss_winner'] == matches_df['winner']]
        toss_pct = len(toss_match) / len(matches_df[matches_df['winner'] != 'No result']) * 100

        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                           subplot_titles=['Toss Decision', 'Toss Winner = Match Winner'])
        toss_dec = matches_df['toss_decision'].value_counts()
        fig.add_trace(go.Pie(labels=toss_dec.index, values=toss_dec.values, marker_colors=['#FF6B6B', '#4ECDC4']), row=1, col=1)
        fig.add_trace(go.Pie(labels=['Yes', 'No'],
                              values=[len(toss_match), len(matches_df[matches_df['winner'] != 'No result']) - len(toss_match)],
                              marker_colors=['#45B7D1', '#FFA07A']), row=1, col=2)
        fig.update_layout(title_text="Toss Analysis", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Result Type
        result_type = matches_df['result'].value_counts()
        fig = px.pie(names=result_type.index, values=result_type.values,
                     title='Match Result Types', color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 What this tells us:</h4>
    Most captains prefer <b>{toss_dec.index[0]}</b> after winning the toss ({toss_dec.iloc[0]} times), 
    reflecting the common strategy of chasing under lights. Matches are decided mostly by 
    <b>{result_type.index[0]}</b> ({result_type.iloc[0]} matches), showing how tight most IPL games are.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Biggest Wins
    st.markdown("### Biggest Wins")
    col1, col2 = st.columns(2)

    with col1:
        biggest_run = matches_df[matches_df['result'] == 'runs'].nlargest(5, 'result_margin')
        st.markdown("**By Runs:**")
        for _, row in biggest_run.iterrows():
            st.write(f"{row['winner']} beat {row['team1'] if row['winner'] == row['team2'] else row['team2']} by {int(row['result_margin'])} runs")

    with col2:
        biggest_wicket = matches_df[matches_df['result'] == 'wickets'].nlargest(5, 'result_margin')
        st.markdown("**By Wickets:**")
        for _, row in biggest_wicket.iterrows():
            st.write(f"{row['winner']} beat {row['team1'] if row['winner'] == row['team2'] else row['team2']} by {int(row['result_margin'])} wickets")

    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 Toss Insight:</h4>
    Teams winning the toss win <b>{toss_pct:.1f}%</b> of the time. 
    Choosing to field first gives a slight advantage with a higher win rate.
    </div>
    """, unsafe_allow_html=True)

# ===================== VENUE ANALYSIS =====================
elif page == "Venue Analysis":
    st.markdown('<div class="sub-header">🏟️ Venue Analysis</div>', unsafe_allow_html=True)

    top_venues = matches_df['venue'].value_counts().head(15)

    fig = px.bar(
        x=top_venues.values,
        y=top_venues.index,
        orientation='h',
        title='Top 15 IPL Venues by Matches Hosted',
        labels={'x': 'Matches', 'y': 'Venue'},
        color=top_venues.values,
        color_continuous_scale='Turbo'
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <b>{top_venues.index[0]}</b> has hosted the most IPL matches with <b>{top_venues.iloc[0]}</b> games!
    </div>
    """, unsafe_allow_html=True)

    # City analysis
    st.markdown("---")
    st.markdown("### Matches by City")
    city_counts = matches_df['city'].value_counts().head(15)
    fig2 = px.bar(
        x=city_counts.values,
        y=city_counts.index,
        orientation='h',
        title='Top 15 Cities by Matches Hosted',
        labels={'x': 'Matches', 'y': 'City'},
        color=city_counts.values,
        color_continuous_scale='Inferno'
    )
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 What this tells us:</h4>
    <b>{city_counts.index[0]}</b> has hosted the most matches overall ({city_counts.iloc[0]}), 
    which usually reflects either a home franchise playing many seasons there or the city being 
    used as a neutral/high-capacity venue during finals and playoffs.
    </div>
    """, unsafe_allow_html=True)

# ===================== SEASON TRENDS =====================
elif page == "Season Trends":
    st.markdown('<div class="sub-header">📈 Season Trends</div>', unsafe_allow_html=True)

    # Matches per season
    season_matches = matches_df['season'].value_counts().sort_index()
    fig = px.bar(
        x=season_matches.index,
        y=season_matches.values,
        title='Matches Per Season',
        labels={'x': 'Season', 'y': 'Matches'},
        color=season_matches.values,
        color_continuous_scale='Plasma'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 What this tells us:</h4>
    Matches per season have ranged from <b>{season_matches.min()}</b> to <b>{season_matches.max()}</b>, 
    reflecting format changes over the years — such as the addition of new franchises 
    (expanding the schedule) or seasons shortened by external factors like COVID-19 or team suspensions.
    </div>
    """, unsafe_allow_html=True)

    # Team performance over seasons
    st.markdown("---")
    st.markdown("### Team Performance Over Seasons")

    top_5_teams = matches_df['winner'].value_counts().head(5).index.tolist()
    if 'No result' in top_5_teams:
        top_5_teams.remove('No result')

    selected_teams = st.multiselect("Select teams to compare:",
                                     options=matches_df['winner'].unique().tolist(),
                                     default=top_5_teams[:5])

    if selected_teams:
        season_team = matches_df[
            (matches_df['winner'].isin(selected_teams)) &
            (matches_df['winner'] != 'No result')
        ].groupby(['season', 'winner']).size().reset_index(name='wins')

        pivot = season_team.pivot(index='season', columns='winner', values='wins').fillna(0)

        fig = go.Figure()
        colors = px.colors.qualitative.Bold
        for i, team in enumerate(selected_teams):
            if team in pivot.columns:
                fig.add_trace(go.Scatter(
                    x=pivot.index, y=pivot[team],
                    mode='lines+markers', name=team,
                    line=dict(color=colors[i % len(colors)], width=3)
                ))
        fig.update_layout(title='Season-wise Wins', xaxis_title='Season',
                         yaxis_title='Wins', height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        <h4>💡 What this tells us:</h4>
        Lines that stay consistently high show sustained team dominance across eras, while sharp 
        peaks and dips highlight standout seasons or rebuilding years — useful for spotting which 
        teams peaked early versus those that improved (or declined) over time.
        </div>
        """, unsafe_allow_html=True)

# ===================== HEAD-TO-HEAD =====================
elif page == "Head-to-Head":
    st.markdown('<div class="sub-header">⚔️ Head-to-Head Records</div>', unsafe_allow_html=True)

    # Team selector
    all_teams = sorted(set(matches_df['team1'].unique()) | set(matches_df['team2'].unique()))

    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("Select Team A:", all_teams, index=0)
    with col2:
        team_b = st.selectbox("Select Team B:", [t for t in all_teams if t != team_a], index=0)

    # H2H stats
    h2h_matches = matches_df[
        ((matches_df['team1'] == team_a) & (matches_df['team2'] == team_b)) |
        ((matches_df['team1'] == team_b) & (matches_df['team2'] == team_a))
    ]

    if len(h2h_matches) > 0:
        team_a_wins = len(h2h_matches[h2h_matches['winner'] == team_a])
        team_b_wins = len(h2h_matches[h2h_matches['winner'] == team_b])
        no_result = len(h2h_matches[h2h_matches['winner'] == 'No result'])

        col1, col2, col3 = st.columns(3)
        col1.metric(f"{team_a} Wins", team_a_wins)
        col2.metric(f"{team_b} Wins", team_b_wins)
        col3.metric("Total Matches", len(h2h_matches))

        # Pie chart
        fig = px.pie(
            names=[team_a, team_b, 'No Result'],
            values=[team_a_wins, team_b_wins, no_result],
            title=f'{team_a} vs {team_b} - Head to Head',
            color_discrete_sequence=['#1E88E5', '#E53935', '#BDBDBD']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Match details
        st.markdown("### Recent Encounters")
        recent = h2h_matches[['date', 'team1', 'team2', 'winner', 'venue', 'result', 'result_margin']].sort_values('date', ascending=False).head(10)
        recent['date'] = recent['date'].dt.date
        st.dataframe(recent, use_container_width=True)

        leader = team_a if team_a_wins > team_b_wins else (team_b if team_b_wins > team_a_wins else None)
        st.markdown(f"""
        <div class="insight-box">
        <h4>💡 What this tells us:</h4>
        {"<b>" + leader + "</b> holds the edge in this rivalry, winning " + str(max(team_a_wins, team_b_wins)) + f" of {len(h2h_matches)} meetings." if leader else f"This matchup is evenly poised at {team_a_wins}-{team_b_wins} across {len(h2h_matches)} meetings."}
        A lopsided head-to-head record can reflect a genuine tactical mismatch (e.g. a team's bowling 
        attack suiting the other's batting weaknesses) or simply that one side has fielded stronger 
        squads across the years they've met.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No matches found between these teams.")

    st.markdown("---")

    # Top rivalries
    st.markdown("### Top 10 IPL Rivalries (Most Encounters)")
    h2h_list = []
    for _, row in matches_df[matches_df['winner'] != 'No result'].iterrows():
        matchup = tuple(sorted([row['team1'], row['team2']]))
        h2h_list.append({'matchup': matchup})

    h2h_df = pd.DataFrame(h2h_list)
    top_rivalries = h2h_df['matchup'].value_counts().head(10)

    fig = px.bar(
        x=[f"{m[0][:12]} vs {m[1][:12]}" for m in top_rivalries.index],
        y=top_rivalries.values,
        title='Most Frequent Matchups',
        labels={'x': 'Matchup', 'y': 'Matches'},
        color=top_rivalries.values,
        color_continuous_scale='Magma'
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    <h4>💡 What this tells us:</h4>
    <b>{top_rivalries.index[0][0]}</b> vs <b>{top_rivalries.index[0][1]}</b> is the most frequent IPL 
    matchup, with <b>{top_rivalries.iloc[0]}</b> encounters. Teams meet more often either because they've 
    both been consistently competitive (qualifying for playoffs repeatedly) or because they've simply 
    been part of the league for most/all of its seasons.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>IPL Data Analysis Dashboard | Built with Streamlit | Data: 2008-2020</p>", unsafe_allow_html=True)