#!/usr/bin/env python3
"""Instala lo que usa IABL Studio, todo dentro de herramientas/ (nada en el sistema): Python con Whisper para
transcribir en local, ffmpeg, HyperFrames (el render), su Chrome sin ventana, los iconos y las letras.

Windows, Mac y Linux. Se puede pasar otra vez sin miedo: solo pone lo que falta. Ocupa ~2,5 GB con el modelo
de Whisper. Uso:   python herramientas/instalar.py      (en Mac y Linux, python3)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
WINDOWS = os.name == "nt"
EXE = ".exe" if WINDOWS else ""
VENV = AQUI / ".venv"
VENV_PY = VENV / ("Scripts/python.exe" if WINDOWS else "bin/python")
HF_DIR, BIN, KIT = AQUI / ".hf", AQUI / ".bin", AQUI / "kit"

# fuente → destino (en kit/fonts): las letras de Fontsource (licencia OFL)
LETRAS = {
    "@fontsource-variable/inter/files/inter-latin-wght-normal.woff2": "inter.woff2",
    "@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2": "jetbrains-mono.woff2",
    "@fontsource-variable/montserrat/files/montserrat-latin-wght-normal.woff2": "montserrat.woff2",
    "@fontsource/bebas-neue/files/bebas-neue-latin-400-normal.woff2": "bebas-neue.woff2",
    "@fontsource/anton/files/anton-latin-400-normal.woff2": "anton.woff2",
    "@fontsource/poppins/files/poppins-latin-600-normal.woff2": "poppins.woff2",
    "@fontsource/instrument-serif/files/instrument-serif-latin-400-normal.woff2": "instrument-serif.woff2",
    "@fontsource/instrument-serif/files/instrument-serif-latin-400-italic.woff2": "instrument-serif-italic.woff2",
}


def falta(que, como):
    print(f"\nX Falta {que}.\n  {como}")
    sys.exit(1)


def run(cmd, **kw):
    """Lanza un programa y para si falla. Los .cmd de Windows (npm, hyperframes) también valen."""
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def salida(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], check=True, capture_output=True, text=True, **kw).stdout.strip()


def python_para_el_entorno():
    """Un Python 3.12 o 3.13 con el que crear .venv (faster-whisper y av dan problemas con otras versiones)."""
    if sys.version_info[:2] in ((3, 12), (3, 13)):
        return sys.executable
    candidatos = [["python3.12"], ["python3.13"]]
    if WINDOWS and shutil.which("py"):
        candidatos = [["py", "-3.12"], ["py", "-3.13"]] + candidatos
    for cmd in candidatos:
        if shutil.which(cmd[0]):
            try:
                return salida([*cmd, "-c", "import sys; print(sys.executable)"])
            except (subprocess.CalledProcessError, OSError):
                continue
    return None


def paso1_python():
    print("1/5 Python y Whisper…")
    uv = shutil.which("uv")
    if uv:   # uv se baja Python solo si hace falta
        if not VENV_PY.exists():
            run([uv, "venv", "--python", "3.12", VENV])
        run([uv, "pip", "install", "--quiet", "--python", VENV_PY, "-r", AQUI / "requirements.txt"])
        return
    py = python_para_el_entorno()
    if not py:
        falta("Python 3.12",
              "Lo más fácil: instala uv y vuelve a pasar esto (uv se baja Python solo).\n"
              + ("  Windows:  winget install astral-sh.uv   (o https://docs.astral.sh/uv/)" if WINDOWS
                 else "  https://docs.astral.sh/uv/"))
    if not VENV_PY.exists():
        run([py, "-m", "venv", VENV])
    run([VENV_PY, "-m", "pip", "install", "--quiet", "-r", AQUI / "requirements.txt"])


def paso2_npm(npm):
    print("2/5 HyperFrames, iconos y letras (npm)…")
    HF_DIR.mkdir(exist_ok=True)
    shutil.copy2(AQUI / "package.json", HF_DIR / "package.json")
    run([npm, "install", "--silent", "--no-audit", "--no-fund"], cwd=HF_DIR)


def copiar_ejecutable(origen, destino):
    """Copia (no enlaza: en Windows crear un enlace pide permisos de administrador)."""
    destino.unlink(missing_ok=True)
    shutil.copy2(origen, destino)
    if not WINDOWS:
        destino.chmod(0o755)


def paso3_ffmpeg(node):
    print("3/5 ffmpeg y ffprobe…")
    BIN.mkdir(exist_ok=True)
    ffmpeg = salida([VENV_PY, "-c", "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"])
    ffprobe = salida([node, "-p", 'require("@ffprobe-installer/ffprobe").path'], cwd=HF_DIR)
    copiar_ejecutable(ffmpeg, BIN / f"ffmpeg{EXE}")
    copiar_ejecutable(ffprobe, BIN / f"ffprobe{EXE}")


def paso4_kit():
    print("4/5 El kit: GSAP y las letras…")
    modulos = HF_DIR / "node_modules"
    shutil.copy2(modulos / "gsap" / "dist" / "gsap.min.js", KIT / "gsap.min.js")
    (KIT / "fonts").mkdir(parents=True, exist_ok=True)
    for origen, destino in LETRAS.items():
        shutil.copy2(modulos / origen, KIT / "fonts" / destino)


def paso5_chrome():
    print("5/5 El Chrome sin ventana de HyperFrames (sin telemetría)…")
    hyperframes = HF_DIR / "node_modules" / ".bin" / ("hyperframes.cmd" if WINDOWS else "hyperframes")
    entorno = {**os.environ, "PATH": os.pathsep.join([str(BIN), os.environ.get("PATH", "")]),
               "DO_NOT_TRACK": "1", "HYPERFRAMES_TELEMETRY": "0"}
    subprocess.run([str(hyperframes), "telemetry", "disable"], env=entorno, capture_output=True)   # si falla, da igual
    puesto = os.environ.get("HYPERFRAMES_BROWSER_PATH")
    if puesto and Path(puesto).is_file():
        print(f"  Uso el Chrome que dices en HYPERFRAMES_BROWSER_PATH: {puesto}")
        return
    run([hyperframes, "browser", "ensure"], env=entorno)


def main():
    os.chdir(AQUI)
    node, npm = shutil.which("node"), shutil.which("npm")
    if not node or not npm:
        falta("Node.js (20 o más)", "Instálalo desde https://nodejs.org (en Windows: winget install OpenJS.NodeJS.LTS) "
                                    "y vuelve a pasar esto.")
    version = int(salida([node, "-p", 'process.versions.node.split(".")[0]']))
    if version < 20:
        falta("Node.js 20 o más", f"Tienes la {version}.")

    paso1_python()
    paso2_npm(npm)
    paso3_ffmpeg(node)
    paso4_kit()
    paso5_chrome()

    for carpeta in ("videos/entrada", "videos/trabajo", "videos/salida", "marca/musica"):
        (AQUI.parent / carpeta).mkdir(parents=True, exist_ok=True)
    if not WINDOWS:
        for f in ("iabl", "iabl-guion", "iabl-estudiar"):
            (AQUI / f).chmod(0o755)

    lanzador = r"herramientas\iabl.cmd" if WINDOWS else "herramientas/iabl"
    print(f"\nListo. Prueba: {lanzador} --help")
    print("   La primera transcripción baja el modelo de Whisper (~1,5 GB): tarda un poco, solo esa vez.")
    if sys.platform != "darwin":
        print("   Fuera de macOS la portada no mide los ojos: elige el segundo con «iabl portada NOMBRE --en S».")


if __name__ == "__main__":
    main()
