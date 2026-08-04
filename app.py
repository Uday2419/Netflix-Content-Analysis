import streamlit as st
import pandas as pd
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
    This interactive dashboard provides insights into Netflix movies and TV shows.
    Explore content trends, countries, genres, and release patterns.
    """
)


# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dataset/netflix_titles.csv")
    return df


df = load_data()


# Sidebar Filters
st.sidebar.header("🔎 Filter Options")


type_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].unique(),
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


# KPI Cards
st.subheader("📊 Netflix Statistics")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Titles",
        len(filtered_df)
    )


with col2:
    st.metric(
        "Movies",
        len(filtered_df[filtered_df["type"] == "Movie"])
    )


with col3:
    st.metric(
        "TV Shows",
        len(filtered_df[filtered_df["type"] == "TV Show"])
    )


with col4:
    st.metric(
        "Countries",
        filtered_df["country"].nunique()
    )


# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Overview",
        "🌎 Countries",
        "🎭 Genres",
        "📅 Trends"
    ]
)


# Overview Tab

with tab1:

    st.subheader("🎥 Movies vs TV Shows")

    content_count = filtered_df["type"].value_counts()


    fig = px.pie(
        values=content_count.values,
        names=content_count.index,
        title="Movies vs TV Shows Distribution",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)



# Countries Tab

with tab2:

    st.subheader("🌎 Top Content Producing Countries")


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
        labels={
            "x": "Country",
            "y": "Number of Titles"
        },
        title="Top 10 Countries"
    )


    st.plotly_chart(fig, use_container_width=True)



# Genres Tab

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
        x=genre.values,
        y=genre.index,
        orientation="h",
        labels={
            "x": "Number of Titles",
            "y": "Genre"
        },
        title="Top 10 Genres"
    )


    st.plotly_chart(fig, use_container_width=True)



# Trends Tab

with tab4:

    st.subheader("📅 Content Release Trend")


    year_count = (
        filtered_df["release_year"]
        .value_counts()
        .sort_index()
    )


    fig = px.line(
        x=year_count.index,
        y=year_count.values,
        labels={
            "x": "Year",
            "y": "Number of Releases"
        },
        title="Netflix Content Growth Over Years"
    )


    st.plotly_chart(fig, use_container_width=True)



# Search Section

st.subheader("🔍 Search Netflix Titles")


search = st.text_input(
    "Enter Movie or TV Show name"
)


if search:

    result = filtered_df[
        filtered_df["title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

    if len(result) > 0:
        st.dataframe(result)

    else:
        st.warning("No title found")



# Footer

st.success(
    "Dashboard created using Python, Pandas, Plotly and Streamlit"
)