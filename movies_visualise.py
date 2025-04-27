import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
import numpy as np
import pymysql
from sqlalchemy import create_engine
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title="2024 Movie Insights", layout="wide") 


# Optional: Use environment variables (better for deployment security)
DB_USER = os.getenv("DB_USER", "p2aHuYniFSErmEa.root")
DB_PASS = os.getenv("DB_PASS", "NWD0BQJlfMc1Cgyu")
DB_HOST = os.getenv("DB_HOST", "gateway01.eu-central-1.prod.aws.tidbcloud.com")
DB_PORT = os.getenv("DB_PORT", "4000")
DB_NAME = os.getenv("DB_NAME", "imdb")

# Connect to MySQL database
def get_connection():
    user = 'p2aHuYniFSErmEa.root'
    password = 'NWD0BQJlfMc1Cgyu'
    host = 'gateway01.eu-central-1.prod.aws.tidbcloud.com'
    port = '4000'
    database = 'imdb'
    engine = create_engine("mysql+mysqlconnector://p2aHuYniFSErmEa.root:NWD0BQJlfMc1Cgyu@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/imdb")
    
    return engine

def load_data():
    try:
        engine = get_connection()
        query = "SELECT * FROM fivegenres_movie"
        df = pd.read_sql(query, engine)
        df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce")
        df['Duration_hours'] = df['Duration'] / 60
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Please check your database connection or data source.")
    st.stop()

# Custom Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #F7374F;  /* Page background */
    }
    .block-container {
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stSidebar {
        width: 280px;
        background-color: #283593;  /* Sidebar background */
        color: white;
    }
    .horizontal-scroll {
        overflow-x: auto;
        white-space: nowrap;
    }
    .main {
        background: linear-gradient(135deg, #f0f2f5, #dfe9f3);  
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.15); 
    }
    h1, h2, h3 {
        color: #2a3d60;
        font-family: 'Roboto', sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    h1 { font-size: 2.5rem; color: #f39c12; }
    h2 { font-size: 2rem; color: #2c3e50; }
    h3 { font-size: 1.75rem; color: #34495e; }
    .stButton button {
        background-color: #f39c12;
        color: white;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #e67e22;
    }
    .stSelectbox select, .stSlider input {
        border-radius: 5px;
        border: 1px solid #dcdcdc;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    st.image("https://img.icons8.com/ios/452/movie-projector.png", width=80)
    st.title("🎬 Filter Options")
    min_rating, max_rating = st.slider("Rating Range", 0.0, 10.0, (0.0, 10.0), 0.1)
    min_votes, max_votes = st.slider("Votes Range", int(df["Votes"].min()), int(df["Votes"].max()), 
                                     (int(df["Votes"].min()), int(df["Votes"].max())))
    selected_genres = st.multiselect("Select Genres", options=df["Genre"].unique(), default=df["Genre"].unique())
    min_duration, max_duration = st.slider("Duration (mins)", int(df["Duration"].min()), int(df["Duration"].max()), 
                                           (int(df["Duration"].min()), int(df["Duration"].max())))

# Apply filters
filtered_df = df[(df["Rating"] >= min_rating) & (df["Rating"] <= max_rating) &
                 (df["Votes"] >= min_votes) & (df["Votes"] <= max_votes) &
                 (df["Genre"].isin(selected_genres)) & 
                 (df["Duration"] >= min_duration) & (df["Duration"] <= max_duration)]

# Navigation Tabs
st.markdown('<div class="horizontal-scroll">', unsafe_allow_html=True)
selected = option_menu(
    menu_title=None,
    options=["Overview", "Genre Analysis", "Voting", "Durations", "Correlations"],
    icons=["bar-chart", "grid", "hand-thumbs-up", "clock", "scatter-chart"],
    orientation="horizontal",
    default_index=0,
    styles={
        "icon": {"color": "white", "font-size": "16px"},
        "nav-link": {
            "font-size": "16px",
            "padding": "10px 16px",
            "text-align": "center",
            "font-weight": "bold",
            "background-color": "#283593",  
            "border-radius": "8px",
            "color": "#ffffff"
        },
        "nav-link-selected": {"background-color": "#f39c12"},
    }
)
st.markdown('</div>', unsafe_allow_html=True)

# Tab Content
if selected == "Overview":
    st.title("Top 10 Movies by Rating and Voting")
    top_movies = filtered_df.sort_values(by=["Rating", "Votes"], ascending=[False, False]).head(10)
    st.dataframe(top_movies[["Title", "Rating", "Votes"]], use_container_width=True)

    st.title("Rating Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(filtered_df["Rating"], bins=10, kde=True, ax=ax2)
    st.pyplot(fig2)

elif selected == "Genre Analysis":
    st.title("Genre Distribution")
    genre_counts = filtered_df["Genre"].value_counts().reset_index()
    genre_counts.columns = ["Genre", "Count"]
    st.bar_chart(genre_counts.set_index("Genre"), use_container_width=True)

    st.title("Average Duration by Genre")
    avg_duration = filtered_df.groupby("Genre")["Duration"].mean().sort_values()
    st.bar_chart(avg_duration, use_container_width=True)

    st.title("Top-Rated Movie per Genre")
    top_per_genre = filtered_df.loc[filtered_df.groupby("Genre")["Rating"].idxmax()][["Genre", "Title", "Rating"]]
    st.dataframe(top_per_genre.sort_values(by="Rating", ascending=False), use_container_width=True)

    st.title("Average Ratings by Genre")
    rating_heatmap = filtered_df.pivot_table(index="Genre", values="Rating", aggfunc="mean")
    fig4, ax4 = plt.subplots()
    sns.heatmap(rating_heatmap, annot=True, cmap="YlGnBu", ax=ax4)
    st.pyplot(fig4)

elif selected == "Voting":
    st.title("Voting Trends by Genre")
    avg_votes = filtered_df.groupby("Genre")["Votes"].mean().sort_values(ascending=False)
    fig1 = px.bar(avg_votes, orientation='v', labels={'value': 'Average Votes', 'Genre': 'Genre'})
    st.plotly_chart(fig1, use_container_width=True)

    st.title("Most Popular Genres by Voting")
    vote_sum = filtered_df.groupby("Genre")["Votes"].sum().reset_index()
    fig3 = px.pie(vote_sum, values='Votes', names='Genre', title='Total Votes by Genre')
    st.plotly_chart(fig3, use_container_width=True)

elif selected == "Durations":
    st.title("Shortest and Longest Movies")
    col1, col2 = st.columns(2)
    shortest = filtered_df.loc[filtered_df["Duration"].idxmin()][["Title", "Duration"]]
    longest = filtered_df.loc[filtered_df["Duration"].idxmax()][["Title", "Duration"]]
    col1.metric("Shortest Movie", f"{shortest['Title']}", f"{shortest['Duration']} mins")
    col2.metric("Longest Movie", f"{longest['Title']}", f"{longest['Duration']} mins")

elif selected == "Correlations":
    st.title("Rating vs Votes Correlation")
    fig5 = px.scatter(filtered_df, x="Votes", y="Rating", hover_data=['Title'])
    st.plotly_chart(fig5, use_container_width=True)
