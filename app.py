import os
from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', message=None)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    try:
        video_url = get_video_url(url)
        if video_url:
            # Download the video and save it locally
            file_path = download_video(video_url)
            if file_path:
                # Once the video is downloaded, prompt the user to download it
                return send_file(file_path, as_attachment=True)
            else:
                return render_template('index.html', message="Error downloading the video.")
        else:
            return render_template('index.html', message="Could not retrieve the video. Please make sure the URL is valid.")
    except requests.exceptions.RequestException as e:
        return render_template('index.html', message=f"An error occurred while making the request: {e}")

def get_video_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tag = soup.find('meta', property="og:video")
    if video_tag:
        return video_tag['content']
    return None

def download_video(url):
    # Send a request to download the video
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        # Get the video file name from the URL (or you can specify your own)
        video_name = "downloaded_video.mp4"
        
        # Save the video to a file
        with open(video_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return video_name
    return None

if __name__ == '__main__':
    app.run(debug=True)
