"""Dónde está cada cosa y qué dice tu marca (marca/marca.json). Todo vive dentro del repo:
tus clips en videos/entrada, cada vídeo en videos/trabajo/<nombre> y lo terminado en videos/salida."""
import json
import os
import subprocess
import sys
from pathlib import Path

WINDOWS = os.name == "nt"
EXE = ".exe" if WINDOWS else ""

# En Windows, Python lee y escribe en la codificación local (cp1252) salvo que se le diga lo contrario: los
# acentos y los emojis de las skills se romperían. Se vuelve a lanzar a sí mismo en modo UTF-8 (los lanzadores
# .cmd ya lo traen puesto: esto es la red de seguridad si alguien llama a formula.py a mano).
if WINDOWS and sys.flags.utf8_mode == 0:
    os.environ["PYTHONUTF8"] = "1"
    sys.exit(subprocess.call([sys.executable, "-X", "utf8", *sys.argv]))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

AQUI = Path(__file__).resolve().parent          # herramientas/
RAIZ = AQUI.parent                              # el repo
MARCA_DIR = RAIZ / "marca"
VIDEOS = RAIZ / "videos"
ENTRADA, TRABAJO, SALIDA = VIDEOS / "entrada", VIDEOS / "trabajo", VIDEOS / "salida"
HF_DIR = AQUI / ".hf"                           # HyperFrames y lo que usa (npm), lo pone instalar.sh
BIN = AQUI / ".bin"                             # ffmpeg y ffprobe, lo pone instalar.sh
FFMPEG, FFPROBE = str(BIN / f"ffmpeg{EXE}"), str(BIN / f"ffprobe{EXE}")
# ffmpeg y ffprobe (herramientas/.bin) y los programas del entorno de Python (yt-dlp) delante en el PATH:
# HyperFrames y los scripts los buscan por su nombre
os.environ["PATH"] = os.pathsep.join([str(BIN), str(Path(sys.executable).parent), os.environ.get("PATH", "")])
KIT = AQUI / "kit"

POR_DEFECTO = {
    "nombre": "",
    "idioma": "es",
    "zona_horaria": "Europe/Madrid",
    "cuentas": {"instagram": "", "tiktok": "", "facebook": ""},
    "colores": {"acento": "#FFD400", "panel": "#111111", "papel": "#F4F1EA", "tinta": "#111111"},
    "letras": {"texto": "Inter", "grande": "Bebas Neue", "mono": "JetBrains Mono", "titulo": "Instrument Serif"},
    "horas": {"mañana": "13:00", "tarde": "19:30"},
    "pie_otras_redes": "",
    "palabras_prohibidas": [],
}


def marca():
    """marca.json sobre los valores por defecto (un campo que falta no rompe nada)."""
    fichero = MARCA_DIR / "marca.json"
    propia = json.loads(fichero.read_text(encoding="utf-8")) if fichero.exists() else {}
    junta = {**POR_DEFECTO, **{k: v for k, v in propia.items() if not k.startswith("_")}}
    for k in ("cuentas", "colores", "letras", "horas"):   # los «_ayuda» son notas para ti: fuera
        junta[k] = {**POR_DEFECTO[k], **{c: v for c, v in propia.get(k, {}).items() if not c.startswith("_")}}
    return junta
