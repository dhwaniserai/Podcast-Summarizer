import os
from podcast_downloader import SpotifyPodcast
from Transcriber import WhisperTranscriber
from Summarizer import GPT3Summarizer
from keys import API_KEYS
import gradio as gr

def setup():
    SPOTIFY_CLIENT_ID =  API_KEYS["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET =  API_KEYS["SPOTIFY_CLIENT_SECRET"]
    OPENAI_API_KEY =  API_KEYS["OPENAI_KEY"]

    OUTPUT = ['downloads/spotify', 'downloads/whisper',  'downloads/gpt3']
    # create output directories if they don't exist
    for dir in OUTPUT:
        if not os.path.exists(dir):
            os.makedirs(dir)
    return SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, OPENAI_API_KEY

def summarize(podcast_url, source, max_sentences=10):
    
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, OPENAI_API_KEY = setup()
    
    print('Initializing summarizer...')
    print(f'podcast_url: {podcast_url}')
    print(f'source: {source}')
    print(f'max_sentences: {max_sentences}')

    podcast = SpotifyPodcast(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    file_id = podcast_url.split('/')[-1]
    audio_path = podcast.download_episode(podcast_url)
    
    transcriber = WhisperTranscriber(OPENAI_API_KEY)
    transcript = transcriber.transcribe(audio_path)
    
    summarizer = GPT3Summarizer(OPENAI_API_KEY, model_engine="gpt-3.5-turbo")
    output = summarizer.summarize(file_id, transcript, max_sentences)
    
    print(f'Completed summarization for ({podcast_url})')
    return output

#ui code launching summarizer
with gr.Blocks() as card:

    gr.Markdown("# Welcome to Spotify Podcast Summarizer")
    url_input = gr.Textbox(label="Enter the url of the podcast", placeholder="")
    type_input = gr.Textbox(label="Type", placeholder="spotify")
    submit_button = gr.Button("Generate Summary")

    with gr.Accordion("Summary"):
        main_out = gr.Markdown()
    submit_button.click(summarize, inputs=[url_input,type_input], outputs=main_out)

card.launch() 
#summarize("https://open.spotify.com/episode/0YqflJb8Wco8IDdGHPNTu8", "spotify", 12)


