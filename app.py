import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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

# Sidebar Filters

st.sidebar.header("Filter Options")


type_filter = st.sidebar.multiselect(
    "Select Content Type",
    df["type"].unique(),
    default=df["type"].unique()
)


year_filter = st.sidebar.slider(
    "Select Release Year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2010, 2025)
)


filtered_df = df[
    (df["type"].isin(type_filter)) &
    (df["release_year"].between(
        year_filter[0],
        year_filter[1]
    ))
]

st.subheader("📊 Netflix Statistics")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Titles",
    len(filtered_df)
)


col2.metric(
    "Movies",
    len(filtered_df[filtered_df["type"]=="Movie"])
)


col3.metric(
    "TV Shows",
    len(filtered_df[filtered_df["type"]=="TV Show"])
)


col4.metric(
    "Countries",
    filtered_df["country"].nunique()
)

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "🌎 Countries",
        "🎭 Genres"
    ]
)

with tab1:
    st.subheader("🎥 Movies vs TV Shows")

    # Count Movies and TV Shows
    content_count = filtered_df["type"].value_counts()

    # Create Plotly chart
    fig = px.bar(
        x=content_count.index,
        y=content_count.values,
        labels={
            "x": "Content Type",
            "y": "Number of Titles"
        },
        title="Movies vs TV Shows Distribution"
    )

    # Display chart
    st.plotly_chart(fig)
    
    with tab2:
    st.subheader("🌎 Top Countries")

    country = (
        filtered_df["country"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )

    fig = px.bar(
        x=country.index,
        y=country.values,
        title="Top 10 Countries"
    )

    st.plotly_chart(fig)
    
    with tab3:
    st.subheader("🎭 Popular Genres")

    genre = (
        filtered_df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )

    fig = px.bar(
        x=genre.index,
        y=genre.values,
        title="Top Genres"
    )

    st.plotly_chart(fig)
    
    
    
st.subheader("🔍 Search Netflix Titles")


search = st.text_input(
    "Enter Movie or TV Show name"
)


if search:
    result = filtered_df[
        filtered_df["title"]
        .str.contains(search, case=False, na=False)
    ]

    st.dataframe(result)

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

content_count = filtered_df["type"].value_counts()


fig = px.bar(
    content_count,
    x=content_count.index,
    y=content_count.values,
    title="Movies vs TV Shows"
)


st.plotly_chart(fig)

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