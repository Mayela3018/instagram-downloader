from flask import Flask, request
import yt_dlp
from datetime import datetime

app = Flask(__name__)

# 📌 Historial en memoria
historial = []

@app.route('/')
def home():
    lista_html = ""

    for item in historial[::-1]:
        lista_html += f"""
        <tr>
            <td>{item['nombre']}</td>
            <td>{item['fecha']}</td>
        </tr>
        """

    return f'''
    <html>
    <head>
        <title>Instagram Downloader</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
                color: white;
                text-align: center;
                padding: 50px;
            }}

            .container {{
                background: rgba(0, 0, 0, 0.65);
                padding: 30px;
                border-radius: 15px;
                width: 500px;
                margin: auto;
                box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
            }}

            input {{
                width: 90%;
                padding: 10px;
                border-radius: 8px;
                border: none;
                margin-bottom: 15px;
            }}

            button {{
                background: #ff0050;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
            }}

            table {{
                width: 100%;
                margin-top: 20px;
                border-collapse: collapse;
                background: rgba(255,255,255,0.1);
            }}

            th, td {{
                padding: 10px;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }}

            th {{
                background: rgba(0,0,0,0.3);
            }}

            footer {{
                margin-top: 15px;
                font-size: 12px;
                opacity: 0.7;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h1>📥 Instagram Downloader</h1>

            <form method="POST" action="/download">
                <input type="text" name="url" placeholder="Pega URL de Instagram" required>
                <br>
                <button type="submit">Descargar</button>
            </form>

            <h3>📜 Historial de descargas</h3>

            <table>
                <tr>
                    <th>Nombre</th>
                    <th>Fecha</th>
                </tr>
                {lista_html}
            </table>

            <footer>Proyecto Docker 🚀</footer>
        </div>
    </body>
    </html>
    '''


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']

    filename = f"video_{datetime.now().strftime('%H%M%S')}.mp4"

    ydl_opts = {
        'outtmpl': filename,
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # guardar historial
    historial.append({
        "nombre": filename,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # alert + regreso
    return '''
    <script>
        alert("✅ Video descargado correctamente");
        window.location.href = "/";
    </script>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)