from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    video_url = get_video_url(url)
    if video_url:
        return redirect(video_url)
    else:
        return "No se pudo obtener el video. Asegúrate de que la URL sea válida."

def get_video_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_tag = soup.find('meta', property="og:video")
    if video_tag:
        return video_tag['content']
    return None

if __name__ == '__main__':
    app.run(debug=True)
