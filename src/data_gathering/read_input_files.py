import pandas as pd
from pathlib import Path

INPUT_FILE_PATH = Path("../../data/dummy")
INPUT_FILE_NAME = Path(INPUT_FILE_PATH, "Parliament_Members.xlsx")
SHEET_PARLIAMENT_MEMBERS = "Parliament_Members"
SHEET_EXPOSED_CONTENT = "Interventions"
SHEET_PRODUCED_CONTENT = "Content"
SHEET_VOTES = "Votes"
EXPOSED_OUTPUT_FILE_NAME = "exposed_content_sentiment.csv"
PRODUCED_OUTPUT_FILE_NAME = "produced_content_sentiment.csv"


def read_input_files() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Read and pre-treat the input files
    """
    df_parliament_members = pd.read_excel(INPUT_FILE_NAME, sheet_name=SHEET_PARLIAMENT_MEMBERS)
    df_exposed_content = pd.read_excel(INPUT_FILE_NAME, sheet_name=SHEET_EXPOSED_CONTENT)
    df_produced_content = pd.read_excel(INPUT_FILE_NAME, sheet_name=SHEET_PRODUCED_CONTENT)
    df_votes = pd.read_excel(INPUT_FILE_NAME, sheet_name=SHEET_VOTES)

    return df_parliament_members, df_exposed_content, df_produced_content, df_votes

def read_output_files() -> (pd.DataFrame, pd.DataFrame):
    """
    Read the output files that are produced by the sentiment analysis program
    """
    df_exposed_output_sentiment = pd.read_csv(Path(INPUT_FILE_PATH, EXPOSED_OUTPUT_FILE_NAME))
    df_produced_output_sentiment = pd.read_csv(Path(INPUT_FILE_PATH, PRODUCED_OUTPUT_FILE_NAME))

    return df_exposed_output_sentiment, df_produced_output_sentiment
