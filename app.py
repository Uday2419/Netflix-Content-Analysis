import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Page Configuration
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)


# Title
st.title("🎬 Netflix Content Analysis Dashboard")

st.write(
    """
    This dashboard provides insights into Netflix movies and TV shows.
    Explore trends, genres, countries, and content distribution.
    """
)


# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/netflix_titles.csv")
    return df


df = load_data()


# Sidebar
st.sidebar.header("Filter Options")


content_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)


filtered_df = df[df["type"].isin(content_type)]


# Dataset Preview
st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head())


# KPI Cards
st.subheader("📊 Netflix Statistics")


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Total Content",
        filtered_df.shape[0]
    )


with col2:
    movies = filtered_df[filtered_df["type"]=="Movie"].shape[0]
    st.metric(
        "Movies",
        movies
    )


with col3:
    shows = filtered_df[filtered_df["type"]=="TV Show"].shape[0]
    st.metric(
        "TV Shows",
        shows
    )


# Content Distribution

st.subheader("🎥 Movies vs TV Shows")


fig, ax = plt.subplots()

sns.countplot(
    data=filtered_df,
    x="type",
    ax=ax
)

st.pyplot(fig)



# Release Year Trend

st.subheader("📅 Content Release Trend")


year_count = filtered_df["release_year"].value_counts().sort_index()


fig, ax = plt.subplots(figsize=(10,4))

ax.plot(
    year_count.index,
    year_count.values
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of Releases")

st.pyplot(fig)



# Top Countries

st.subheader("🌎 Top 10 Content Producing Countries")


country = (
    filtered_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)


fig, ax = plt.subplots()

country.plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Number of Titles")

st.pyplot(fig)



# Genre Analysis

st.subheader("🎭 Popular Genres")


genre = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)


fig, ax = plt.subplots()

genre.plot(
    kind="barh",
    ax=ax
)

st.pyplot(fig)



# Footer

st.success(
    "Dashboard created using Python, Pandas, Matplotlib, Seaborn and Streamlit"
)