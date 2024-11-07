import pandas as pd
from pathlib import Path

INPUT_FILE_PATH = Path("../../data/dummy/Parliament_Members.xlsx")
SHEET_PARLIAMENT_MEMBERS = "Parliament_Members"
SHEET_EXPOSED_CONTENT = "Tabelle1"
SHEET_PRODUCED_CONTENT = "Content"
SHEET_VOTES = "Votes"


def read_input_files() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Read and pre-treat the input files
    """
    df_parliament_members = pd.read_excel(INPUT_FILE_PATH, sheet_name=SHEET_PARLIAMENT_MEMBERS)
    df_exposed_content = pd.read_excel(INPUT_FILE_PATH, sheet_name=SHEET_EXPOSED_CONTENT)
    df_produced_content = pd.read_excel(INPUT_FILE_PATH, sheet_name=SHEET_PRODUCED_CONTENT)
    df_votes = pd.read_excel(INPUT_FILE_PATH, sheet_name=SHEET_VOTES)

    return df_parliament_members, df_exposed_content, df_produced_content, df_votes
