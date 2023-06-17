import requests
from pytube import YouTube
from tqdm import tqdm

def download_video(link):
    youtube_object = YouTube(link)
    youtube_stream = youtube_object.streams.get_highest_resolution()
    video_title = youtube_object.title
    video_size = youtube_stream.filesize

    chunk_size = 1024 * 1024  # 1 MB

    # Calculate the number of chunks to download
    num_chunks = video_size // chunk_size
    if video_size % chunk_size != 0:
        num_chunks += 1

    # Set up the progress bar
    progress_bar = tqdm(total=video_size, unit='B', unit_scale=True)

    try:
        # Open a file for writing the video content
        with open(f"{video_title}.mp4", 'wb') as video_file:
            response = requests.get(youtube_stream.url, stream=True)
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    video_file.write(chunk)
                    progress_bar.update(len(chunk))

        progress_bar.close()
        print("Download is completed successfully.")

    except Exception as e:
        progress_bar.close()
        print(f"An error has occurred: {str(e)}")


link = input("Enter the YouTube video URL: ")
download_video(link)
