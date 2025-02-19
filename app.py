from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    # Enviar el mensaje como None cuando el usuario ingresa a la página inicialmente
    return render_template('index.html', message=None)

@app.route('/download', methods=['POST'])
def download():
    # Obtener la URL ingresada por el usuario
    url = request.form['url']
    
    try:
        # Intentar obtener la URL del video
        video_url = get_video_url(url)
        if video_url:
            # Si la URL del video se obtiene con éxito
            return render_template('index.html', message="¡Video descargado con éxito!")
        else:
            # Si no se pudo obtener la URL del video
            return render_template('index.html', message="No se pudo obtener el video. Asegúrate de que la URL sea válida.")
    except requests.exceptions.RequestException as e:
        # Si hay un error al realizar la solicitud HTTP (por ejemplo, conexión fallida)
        return render_template('index.html', message=f"Ocurrió un error al realizar la solicitud: {e}")

def get_video_url(url):
    # Cabeceras para la solicitud HTTP
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza un error si la solicitud falla
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar la metaetiqueta con la URL del video
    video_tag = soup.find('meta', property="og:video")
    if video_tag:
        return video_tag['content']
    return None

if __name__ == '__main__':
    app.run(debug=True)
