from flask import Flask, request, jsonify, render_template_string, send_file
import yt_dlp
import os
import json
from datetime import datetime

app = Flask(__name__)

DOWNLOAD_DIR = '/app/downloads'
HISTORY_FILE = '/app/downloads/historial.json'

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def add_to_history(video):
    history = load_history()
    history.append(video)
    save_history(history)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram Downloader</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%);
    min-height: 100vh;
    padding: 2rem 1rem;
    display: flex;
    align-items: flex-start;
    justify-content: center;
}

.wrap {
    width: 100%;
    max-width: 560px;
}

.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 0.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    padding: 2rem;
    color: #fff;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: center;
    margin-bottom: 0.5rem;
}

.logo-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
}

.logo-icon svg {
    width: 20px;
    height: 20px;
    fill: none;
    stroke: #fff;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}

h1 {
    font-size: 20px;
    font-weight: 600;
    color: #fff;
}

.subtitle {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    text-align: center;
    margin-bottom: 1.5rem;
}

.tabs {
    display: flex;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 1.5rem;
    gap: 4px;
}

.tab {
    flex: 1;
    padding: 9px;
    border: none;
    border-radius: 9px;
    background: transparent;
    color: rgba(255, 255, 255, 0.6);
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
}

.tab.on {
    background: rgba(255, 255, 255, 0.15);
    color: #fff;
    font-weight: 500;
}

.input-wrap {
    position: relative;
    margin-bottom: 12px;
}

.input-wrap svg {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    width: 16px;
    height: 16px;
    stroke: rgba(255, 255, 255, 0.5);
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    pointer-events: none;
}

#url {
    width: 100%;
    padding: 13px 13px 13px 42px;
    background: rgba(255, 255, 255, 0.1);
    border: 0.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: #fff;
    font-size: 14px;
    outline: none;
    transition: all 0.2s;
    font-family: inherit;
}

#url::placeholder { color: rgba(255, 255, 255, 0.4); }

#url:focus {
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.15);
}

.btn {
    width: 100%;
    padding: 13px;
    border: none;
    border-radius: 12px;
    background: #fff;
    color: #833ab4;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
}

.btn:hover {
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-1px);
}

.btn:active {
    transform: translateY(0);
    scale: 0.99;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

#res { margin-top: 1rem; }

.card {
    background: rgba(255, 255, 255, 0.12);
    border: 0.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 14px;
    padding: 1rem;
    margin-top: 8px;
}

.card-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 6px;
}

.card-label {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    flex-shrink: 0;
}

.card-val {
    font-size: 13px;
    color: #fff;
    font-weight: 500;
    word-break: break-all;
    text-align: right;
}

.dl-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 9px 16px;
    background: rgba(255, 255, 255, 0.15);
    border: 0.5px solid rgba(255, 255, 255, 0.3);
    border-radius: 9px;
    color: #fff;
    font-size: 13px;
    text-decoration: none;
    margin-top: 10px;
    transition: all 0.2s;
    font-family: inherit;
}

.dl-btn:hover { background: rgba(255, 255, 255, 0.25); }

.dl-btn svg {
    width: 14px;
    height: 14px;
    stroke: #fff;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.err {
    background: rgba(253, 29, 29, 0.2);
    border: 0.5px solid rgba(253, 29, 29, 0.4);
    border-radius: 12px;
    padding: 12px;
    font-size: 13px;
    color: #ffaaaa;
    margin-top: 8px;
}

.loading {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 0;
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
}

.spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

.status-ok {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #7bffb3;
    margin-bottom: 10px;
}

.dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #7bffb3;
}

.hist-empty {
    text-align: center;
    padding: 2rem;
    color: rgba(255, 255, 255, 0.4);
    font-size: 14px;
}

.hist-item {
    background: rgba(255, 255, 255, 0.08);
    border: 0.5px solid rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 8px;
}

.hist-title {
    font-size: 14px;
    font-weight: 500;
    color: #fff;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.hist-meta {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 8px;
}

.hist-actions { display: flex; justify-content: flex-end; }

.refresh-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    background: rgba(255, 255, 255, 0.1);
    border: 0.5px solid rgba(255, 255, 255, 0.2);
    border-radius: 9px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 13px;
    cursor: pointer;
    margin-bottom: 1rem;
    transition: all 0.2s;
    font-family: inherit;
}

.refresh-btn:hover { background: rgba(255, 255, 255, 0.2); }

.refresh-btn svg {
    width: 14px;
    height: 14px;
    stroke: currentColor;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}
</style>
</head>

<body>
<div class="wrap">
<div class="glass">

  <div class="logo">
    <div class="logo-icon">
      <svg viewBox="0 0 24 24">
        <rect x="2" y="2" width="20" height="20" rx="5"/>
        <circle cx="12" cy="12" r="4"/>
        <circle cx="17.5" cy="6.5" r="1" fill="#fff" stroke="none"/>
      </svg>
    </div>
    <h1>Instagram Downloader</h1>
  </div>

  <p class="subtitle">Descarga videos e imágenes fácilmente</p>

  <div class="tabs">
    <button class="tab on" onclick="show('d', this)">Descargar</button>
    <button class="tab" onclick="show('h', this)">Historial</button>
  </div>

  <div id="panel-d">
    <div class="input-wrap">
      <svg viewBox="0 0 24 24">
        <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/>
        <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/>
      </svg>
      <input id="url" placeholder="Pega aquí el enlace de Instagram..." />
    </div>
    <button class="btn" id="dlbtn" onclick="descargar()">Descargar</button>
    <div id="res"></div>
  </div>

  <div id="panel-h" style="display:none">
    <button class="refresh-btn" onclick="cargar()">
      <svg viewBox="0 0 24 24">
        <polyline points="1 4 1 10 7 10"/>
        <path d="M3.51 15a9 9 0 102.13-9.36L1 10"/>
      </svg>
      Actualizar historial
    </button>
    <div id="hist">
      <div class="hist-empty">Haz clic en "Actualizar historial" para ver tus descargas</div>
    </div>
  </div>

</div>
</div>

<script>
function show(x, btn) {
  document.getElementById('panel-d').style.display = x === 'd' ? 'block' : 'none';
  document.getElementById('panel-h').style.display = x === 'h' ? 'block' : 'none';
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('on'));
  btn.classList.add('on');
}

async function descargar() {
  const url = document.getElementById('url').value.trim();
  const res = document.getElementById('res');
  const btn = document.getElementById('dlbtn');

  if (!url) {
    res.innerHTML = '<div class="err">Por favor, ingresa un enlace válido.</div>';
    return;
  }

  btn.disabled = true;
  res.innerHTML = '<div class="loading"><div class="spinner"></div>Descargando, un momento...</div>';

  try {
    const r = await fetch('/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await r.json();

    if (data.success) {
      res.innerHTML = `<div class="card">
        <div class="status-ok"><div class="dot"></div>Descarga exitosa</div>
        <div class="card-row">
          <span class="card-label">Archivo</span>
          <span class="card-val">${data.filename}</span>
        </div>
        <a class="dl-btn" href="/downloads/${data.filename}">
          <svg viewBox="0 0 24 24">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          Guardar archivo
        </a>
      </div>`;
    } else {
      res.innerHTML = `<div class="err">Error: ${data.error}</div>`;
    }
  } catch (e) {
    res.innerHTML = '<div class="err">Error de conexión. Verifica que el servidor esté activo.</div>';
  }

  btn.disabled = false;
}

async function cargar() {
  const hist = document.getElementById('hist');
  hist.innerHTML = '<div class="loading"><div class="spinner"></div>Cargando historial...</div>';

  try {
    const r = await fetch('/history');
    const data = await r.json();

    if (!data.length) {
      hist.innerHTML = '<div class="hist-empty">No hay descargas aún.</div>';
      return;
    }

    hist.innerHTML = data.slice().reverse().map(v => `
      <div class="hist-item">
        <div class="hist-title">${v.title || 'Sin título'}</div>
        <div class="hist-meta">${v.fecha}</div>
        <div class="hist-actions">
          <a class="dl-btn" href="/downloads/${v.filename}">
            <svg viewBox="0 0 24 24">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Descargar otra vez
          </a>
        </div>
      </div>`).join('');
  } catch (e) {
    hist.innerHTML = '<div class="err">No se pudo cargar el historial.</div>';
  }
}

document.getElementById('url').addEventListener('keydown', e => {
  if (e.key === 'Enter') descargar();
});
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.json.get('url')

        ydl_opts = {
            'outtmpl': DOWNLOAD_DIR + '/%(title)s.%(ext)s',
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        add_to_history({
            "title": info.get('title'),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filename": os.path.basename(filename)
        })

        return jsonify({"success": True, "filename": os.path.basename(filename)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/downloads/<filename>')
def get_file(filename):
    return send_file(os.path.join(DOWNLOAD_DIR, filename), as_attachment=True)

@app.route('/history')
def history():
    return jsonify(load_history())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)