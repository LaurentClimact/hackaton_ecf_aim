from src.data_gathering.read_input_files import read_input_files, read_output_files


def run_content_type_analyzer():
    df_parliament_members, df_exposed_content, df_produced_content, df_votes = read_input_files()
    df_exposed_output_sentiment, df_produced_output_sentiment = read_output_files()

    df_exposed_output_sentiment = df_exposed_output_sentiment[["date", "categorie", "country"]]
    df_produced_output_sentiment = df_produced_output_sentiment[["Last Name", "First Name", "Publication Date", "Content Category", "sentiment"]]

    df_exposed_output_sentiment = df_exposed_output_sentiment.merge(df_parliament_members, left_on="country", right_on="Country")
    print(df_produced_output_sentiment)


if __name__ == '__main__':
    run_content_type_analyzer()