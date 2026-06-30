import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Product Feedback Analyzer",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>

    /* Main App */
    .stApp {
        background-color: #020617;
        color: white;
    }

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Headings */
    h1 {
        color: white !important;
        font-size: 52px !important;
        font-weight: 700 !important;
    }

    h2, h3 {
        color: white !important;
    }

    /* Paragraphs */
    p, label {
        color: #cbd5e1 !important;
        font-size: 18px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Text Area */
    .stTextArea textarea {
        background-color: #111827 !important;
        color: white !important;
        border-radius: 16px !important;
        border: 1px solid #334155 !important;
        padding: 15px !important;
        font-size: 16px !important;
    }

    /* File Upload */
    .stFileUploader {
        background-color: #111827;
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #334155;
    }

    /* Button */
    .stButton>button {

        background: linear-gradient(
            90deg,
            #2563eb,
            #3b82f6
        ) !important;

        color: white !important;

        border-radius: 14px !important;

        height: 55px;

        width: 240px;

        font-size: 20px !important;

        font-weight: 600 !important;

        border: none !important;

        margin-top: 10px;
    }

    /* Dataframes */
    .stDataFrame {
        background-color: white;
        border-radius: 12px;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {

        background-color: #111827;

        border: 1px solid #334155;

        padding: 20px;

        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown(
    """
    # 🤖 AI Feedback Analyzer
    ---
    """
)

st.sidebar.markdown(
    """
    ## 📊 About

    AI-powered application for analyzing customer reviews and identifying product pain points.
    """
)

st.sidebar.markdown(
    """
    ## 🚀 Features

    ✅ Theme categorization

    ✅ Product insights

    ✅ Sentiment analysis

    ✅ Charts & visualization

    ✅ Word cloud generation

    ✅ CSV upload support
    """
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Upload a CSV file or paste reviews to begin analysis."
)

# ---------------- HEADER ----------------

st.markdown(
    """
    # 🤖 AI Product Feedback Analyzer

    Analyze customer reviews and identify product pain points using AI-powered insights.
    """
)

st.markdown("---")

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# ---------------- TEXT INPUT ----------------

reviews_text = st.text_area(
    "Paste customer reviews (one review per line)",
    height=200
)

# ---------------- ANALYZE BUTTON ----------------

if st.button("🔍 Analyze Reviews"):

    # -------- LOAD REVIEWS --------

    reviews = []

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file)

        reviews = data.iloc[:, 0].dropna().tolist()

    else:

        reviews = reviews_text.split("\n")

    # -------- THEMES --------

    themes = {

        "Delivery Issues": [
            "late",
            "delivery",
            "slow",
            "delay",
            "tracking"
        ],

        "Payment Problems": [
            "payment",
            "failed",
            "refund",
            "transaction"
        ],

        "UI Problems": [
            "ui",
            "design",
            "confusing",
            "navigation",
            "interface"
        ],

        "Customer Support": [
            "support",
            "response",
            "help",
            "service"
        ],

        "Pricing": [
            "price",
            "cost",
            "expensive",
            "pricing"
        ]
    }

    # -------- SENTIMENT WORDS --------

    positive_words = [
        "good",
        "great",
        "fast",
        "excellent",
        "smooth",
        "amazing",
        "easy",
        "love",
        "best"
    ]

    negative_words = [
        "late",
        "slow",
        "bad",
        "failed",
        "confusing",
        "poor",
        "expensive",
        "worst",
        "issue",
        "problem",
        "delay"
    ]

    # -------- THEME ANALYSIS --------

    results = []

    for review in reviews:

        review_lower = review.lower()

        matched = False

        for theme, keywords in themes.items():

            if any(word in review_lower for word in keywords):

                results.append(theme)

                matched = True

        if not matched:

            results.append("Other")

    counter = Counter(results)

    df = pd.DataFrame({

        "Theme": list(counter.keys()),

        "Mentions": list(counter.values())
    })

    # -------- THEME TABLE --------

    st.markdown("---")

    st.subheader("📋 Theme Analysis")

    st.dataframe(df)

    # -------- PRIORITY INSIGHTS --------

    st.markdown("---")

    st.subheader("⚡ Priority Pain Points")

    sorted_df = df.sort_values(
        by="Mentions",
        ascending=False
    )

    for i, row in sorted_df.iterrows():

        feature = ""

        if row["Theme"] == "Delivery Issues":

            feature = "Improve real-time delivery tracking"

        elif row["Theme"] == "Payment Problems":

            feature = "Add payment retry system"

        elif row["Theme"] == "UI Problems":

            feature = "Redesign app navigation"

        elif row["Theme"] == "Customer Support":

            feature = "Add AI chatbot support"

        elif row["Theme"] == "Pricing":

            feature = "Introduce better discount plans"

        else:

            feature = "Further user research needed"

        st.write(
            f"• {row['Theme']} → Suggested Fix: {feature}"
        )

    # -------- SENTIMENT ANALYSIS --------

    st.markdown("---")

    st.subheader("😊 Sentiment Analysis")

    positive = 0
    negative = 0
    neutral = 0

    for review in reviews:

        review_lower = review.lower()

        pos_score = sum(
            word in review_lower for word in positive_words
        )

        neg_score = sum(
            word in review_lower for word in negative_words
        )

        if neg_score > pos_score:

            negative += 1

        elif pos_score > neg_score:

            positive += 1

        else:

            neutral += 1

    sentiment_df = pd.DataFrame({

        "Sentiment": [
            "Positive",
            "Negative",
            "Neutral"
        ],

        "Count": [
            positive,
            negative,
            neutral
        ]
    })

    st.dataframe(sentiment_df)

    # -------- METRICS --------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Reviews",
        len(reviews)
    )

    col2.metric(
        "Themes Found",
        len(df)
    )

    col3.metric(
        "Negative Reviews",
        negative
    )

    
    # -------- PIE CHART --------

    st.markdown("---")

    st.subheader("📈 Sentiment Distribution")

    fig3, ax3 = plt.subplots(
        figsize=(4, 4)
    )

    ax3.pie(
        sentiment_df["Count"],
        labels=sentiment_df["Sentiment"],
        autopct="%1.1f%%",
        textprops={"color": "white"}
    )

    fig3.patch.set_facecolor("#020617")

    ax3.set_facecolor("#020617")

    st.pyplot(fig3)


    # -------- BAR CHART --------

    st.markdown("---")

    st.subheader("📊 Theme Distribution")

    fig, ax = plt.subplots()

    ax.barh(
        df["Theme"],
        df["Mentions"]
    )

    st.pyplot(fig)

    # -------- WORD CLOUD --------

    st.markdown("---")

    st.subheader("☁️ Review Word Cloud")

    text = " ".join(reviews)

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate(text)

    fig2, ax2 = plt.subplots(figsize=(12, 6))

    ax2.imshow(wordcloud)

    ax2.axis("off")

    st.pyplot(fig2)

    # -------- DOWNLOAD REPORT --------

    st.markdown("---")

    report = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Analysis Report",
        data=report,
        file_name="feedback_analysis.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "Built with Streamlit • Python • Pandas • Matplotlib"
)