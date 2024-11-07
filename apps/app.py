import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from parliament_graph import parliament_graph_generator


def waterfall():
    import plotly.graph_objects as go

    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = ["relative", "relative", "relative", "total", "relative", "relative", "total"],
        x = ["Baseline", "Report", "Demonstration", "Votes 1", "Petition", "Report", "Votes 2"],
        textposition = "outside",
        text = ["270", "+40", "-26", "336", "+40", "-47", "329"],
        y = [270, 40, -26, 336, 40, -47, 329],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Evolution of intention to vote based on interventions",
            showlegend = True
    )

    st.plotly_chart(fig, theme="streamlit")

# Set page configuration as the very first line
st.set_page_config(page_title="Advocacy Impact Monitor", layout="wide")

# ------ DUMMY DATA ------
# path to excel input
file_path = "data/dummy/advocacy_impact_dummy_data.xlsx"
# Dummy topic options (in a real scenario, topics could be extracted from the data file or database)
# ------------------------

# Load the Excel file
xls = pd.ExcelFile(file_path)

sentiment_emoji_map = {
    "positive": "👍",
    "neutral": "😐",
    "negative": "👎"
}

# topic selection
mentions_data = pd.read_excel(xls, "topic_mentions")
topic_options = mentions_data["topic"].unique()
selected_topic = st.sidebar.selectbox("Select a topic", topic_options)

# Title and topic Selection (the name of the topic is displayed next to the title)
st.markdown(f"# Advocacy Impact Monitor - {selected_topic}")

# --- Mentions and Support Section ---
st.subheader("Mentions and Support")
mentions_data = pd.read_excel(xls, "mentions_support")
mentions_data = mentions_data[mentions_data["topic"] == selected_topic]
mentions_count = mentions_data["mentions_count"].iloc[0]
support_percentage = mentions_data["support_percentage"].iloc[0]
latest_mentions = pd.read_excel(xls, "topic_mentions")
latest_mentions = latest_mentions[latest_mentions["topic"] == selected_topic].head(3)
latest_mentions['formatted_date'] = pd.to_datetime(latest_mentions['date']).dt.strftime("%b %d")

# 3 columns with different size
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    # add green arrow going up in my text
    st.markdown("")
    st.markdown(f"### {mentions_count}")
    st.markdown("**Mentions in the last 7 days**")

with col2:
    st.markdown(f"### {support_percentage}%")
    st.markdown("**Support estimate**")

with col3:
    with st.container(border=True):
        st.markdown(f"### Latest mentions")
        for i, row in latest_mentions.iterrows():
            # Format the date as "Mon D" (e.g., "Nov 4")
            formatted_date = row['formatted_date']

            # Get the corresponding emoji for the sentiment
            sentiment_emoji = sentiment_emoji_map.get(row['sentiment'], "❓")  # Default to ❓ if sentiment is unrecognized

            # Display the mention with formatted date and emoji
            st.markdown(f"- **{formatted_date}**: {sentiment_emoji} {row['content']}")

# --- MEP Sentiment Section ---
st.markdown("---")
st.subheader("MEP sentiment")
mep_sentiment_data = pd.read_excel(xls, "mep_sentiment")
mep_list = mep_sentiment_data["name"].unique()
mep_sentiment_data = mep_sentiment_data[mep_sentiment_data["topic"] == selected_topic]
mep_selection = st.selectbox("Select MEP", mep_list)
mep_sentiment_data = mep_sentiment_data[mep_sentiment_data["name"] == mep_selection]

interventions_impact_data = pd.read_excel(xls, "interventions")
# sort the data by date
interventions_impact_data = interventions_impact_data[interventions_impact_data["topic"] == selected_topic].sort_values("date")

col1, col2 = st.columns([2,1])
# list of name from excel file column name

with col1:
    # Plotting Sentiment Over Time
    fig_sentiment = go.Figure()
    # Plotting MEP sentiment line plot
    # Add main sentiment line trace
    fig_sentiment.add_trace(go.Scatter(
        x=mep_sentiment_data["date"],
        y=mep_sentiment_data["value"],
        mode='lines+markers',
        name=f"{mep_selection} sentiment"
    ))

    # Add vertical lines and vertical text for each intervention
    for _, row in interventions_impact_data.iterrows():
        intervention_date = row["date"]
        intervention_name = row["Name"]

        # Add a vertical line at the intervention date
        fig_sentiment.add_vline(
            x=intervention_date,
            line=dict(color="gray", dash="dash"),
            opacity=0.7
        )

        # Add an annotation for the intervention name with vertical text
        fig_sentiment.add_annotation(
            x=intervention_date,
            y=max(mep_sentiment_data["value"]),  # Position at the top of y-axis range
            text=intervention_name,
            showarrow=False,
            textangle=-90,  # Rotate text to be vertical
            font=dict(size=10, color="black"),
            bgcolor="lightgray",
            bordercolor="gray",
            borderwidth=1,
            opacity=0.9,
            yshift=10  # Shift slightly away from the line
        )

    # Update layout with titles and display settings
    fig_sentiment.update_layout(
        title="Sentiment over time with interventions",
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        template="plotly"
    )

    # Display in Streamlit
    st.plotly_chart(fig_sentiment)

with col2:
    with st.container(border=True):
        st.markdown("Latest opinions")
        mep_sentiment_data['formatted_date'] = pd.to_datetime(mep_sentiment_data['date']).dt.strftime("%b %d")

        # limit to 3 latest opinions
        mep_sentiment_data = mep_sentiment_data.sort_values(by='date', ascending=False).head(3)
        for i, row in mep_sentiment_data.iterrows():
            # Format the date as "Mon D" (e.g., "Nov 4")
            formatted_date = row['formatted_date']

            # Get the corresponding emoji for the sentiment
            sentiment_emoji = sentiment_emoji_map.get(row['sentiment'], "❓")  # Default to ❓ if sentiment is unrecognized
    
            # Display the mention with formatted date and emoji
            st.markdown(f"- **{formatted_date}**: {sentiment_emoji} {row['opinion']}")

# # --- topic Impact Section ---
# st.markdown("---")
# st.subheader("Advocacy campaign impact")
#
# # Plotting topic Impact
# fig_impact = go.Figure()
# interventions_impact_data = pd.read_excel(xls, "interventions")
# # sort the data by date
# interventions_impact_data = interventions_impact_data[interventions_impact_data["topic"] == selected_topic].sort_values("date")
# fig_impact.add_trace(go.Scatter(x=interventions_impact_data["date"], y=interventions_impact_data["affected"],
#                                 mode='lines+markers', name="Affected"))
# fig_impact.update_layout(title=f"{mep_selection} affected by topic", xaxis_title="Date", yaxis_title="Impact Score", template="plotly_white")
#
# for _, row in interventions_impact_data.iterrows():
#     if pd.notna(row["Name"]):  # Only add annotation if there's a milestone name
#         fig_impact.add_annotation(
#             x=row["date"],
#             y=row["affected"],
#             text=row["Name"],
#             showarrow=True,
#             arrowhead=1,
#             ax=0,
#             ay=-40,
#             font=dict(size=10, color="black"),
#             bgcolor="lightyellow",
#             bordercolor="gray",
#             borderwidth=1
#         )
#
# # Update layout with titles and display settings
# fig_impact.update_layout(
#     title=f"{selected_topic} impact over time",
#     xaxis_title="Date",
#     yaxis_title="Impact Score",
#     template="plotly_white"
# )
#
# st.plotly_chart(fig_impact)


# --- Interventions Section ---
st.markdown("---")
st.subheader("Interventions")
waterfall()

# --- Voting Results Section ---
st.markdown("---")
st.subheader("Voting results")
voting_data = pd.read_excel(xls, "voting_results")
voting_data = voting_data[voting_data["topic"] == selected_topic]
voting_before = voting_data["voting_before"].iloc[0]
voting_after = voting_data["voting_after"].iloc[0]
total_seats = voting_data["total_seats"].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Before topic (estimated)")
    # show the number of positive votes
    st.markdown(f"Positive votes: {int(voting_before)}")
    plt = parliament_graph_generator(voting_before, total_seats)
    # plot plt in streamlit
    st.pyplot(plt)

with col2:
    st.markdown("### Final vote")
    st.markdown(f"Positive votes: {int(voting_after)} - evolution: {int(voting_after - voting_before)}")
    plt = parliament_graph_generator(voting_after, total_seats)
    # plot plt in streamlit
    st.pyplot(plt)

# Define the data
with_int = 22  # Number of people who did not change their vote
without_int = 37  # Number of people who changed their vote

st.subheader("Swing votes")

# Create the stacked bar chart
fig_swing = go.Figure(data=[
    go.Bar(
        name="With Intervention",
        x=["Votes"],
        y=[with_int],
        marker_color="green"
    ),
    go.Bar(
        name="Withou Intervention",
        x=["Votes"],
        y=[without_int],
        marker_color="lightblue"
    )
])

# Update layout for stacked view
fig_swing.update_layout(
    barmode='stack',
    title="Swinging Voters between Two Votes",
    xaxis_title="Vote Outcome",
    yaxis_title="Number of People",
    template="plotly_white"
)

# Display in Streamlit
st.plotly_chart(fig_swing)



