import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_url_to_heatmap_coordinates import youtube_url_to_heatmap_coordinates

def data_load(url):
    # transcript
    video_id = url.split("v=")[1]
    transcripts = YouTubeTranscriptApi.get_transcript(video_id)
    # heatmap
    heatmap_list = youtube_url_to_heatmap_coordinates(url)
    col_name = ['time_step', 'score']
    heatmap_df = pd.DataFrame(heatmap_list, columns=col_name)
    heatmap_df['time_step'] = round(heatmap_df['time_step'], 2)

    list_datasets = []
    for transcript in transcripts:
        text = transcript['text']
        text_time_step = round(transcript['start'] / transcripts[-1]['start'], 2)
        score = heatmap_df[heatmap_df['time_step'] == text_time_step]['score'].iloc[0]
        list_datasets.append([text, text_time_step, score])

    datasets_col_name = ['text', 'time_step', 'score']
    df_datasets = pd.DataFrame(list_datasets, columns=datasets_col_name)
    return df_datasets

