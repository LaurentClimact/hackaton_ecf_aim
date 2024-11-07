from tqdm import tqdm
from pathlib import Path
from src.data_gathering.read_input_files import read_input_files
from src.sentiment_analysis.sentiment_openai import sentiment_analysis


OUTPUT_FOLDER = "../../data/dummy"


def run_sentiment_analysis():
    df_parliament_members, df_exposed_content, df_produced_content, df_votes = read_input_files()

    print(f"Working on the produced content...")
    sentiment_score_produced_content = list()
    for _, produced_content in tqdm(df_produced_content.iterrows()):
        sentiment_score_produced_content.append(sentiment_analysis(
            produced_content["Published Content"],
            produced_content["Topic"]
        ))

    df_produced_content["sentiment"] = sentiment_score_produced_content
    df_produced_content.to_csv(Path(OUTPUT_FOLDER, "produced_content_sentiment.csv"))
    print(f'File {Path(OUTPUT_FOLDER, "produced_content_sentiment.csv")} has been written')

    print(f"Working on the exposed content...")
    sentiment_score_exposed_content = list()
    for _, exposed_content in tqdm(df_exposed_content.iterrows()):
        sentiment_score_exposed_content.append(sentiment_analysis(
            exposed_content["content"],
            exposed_content["topic"]
        ))

    df_exposed_content["sentiment"] = sentiment_score_exposed_content
    df_exposed_content.to_csv(Path(OUTPUT_FOLDER, "exposed_content_sentiment.csv"))
    print(f'File {Path(OUTPUT_FOLDER, "exposed_content_sentiment.csv")} has been written')

if __name__ == '__main__':
    run_sentiment_analysis()