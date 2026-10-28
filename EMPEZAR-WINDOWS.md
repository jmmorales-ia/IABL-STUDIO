# IABL Studio en Windows (sin WSL)

Esta copia está adaptada para Windows nativo. Lo único que se ha probado es la parte de Linux; si algo falla en
Windows, copia el error tal cual y se arregla.

## Antes de nada (una vez, en PowerShell)

```powershell
winget install OpenJS.NodeJS.LTS
winget install astral-sh.uv
```

Cierra y abre PowerShell después, para que encuentre `node` y `uv`.

## Instalar

Abre esta carpeta en Claude Code (VS Code o la app) y dile: «instala IABL Studio y dime cuánto tarda cada paso».
O a mano:

```powershell
python herramientas\instalar.py
herramientas\formula.cmd --help
```

Si Chrome no se descarga solo, apunta a uno que ya tengas:

```powershell
$env:HYPERFRAMES_BROWSER_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## Probar con un clip tuyo

1. Copia un clip de 30 a 60 s hablando a cámara a `videos\entrada\`.
2. En Claude Code: `/edicion`.
3. Apunta cuánto tarda: transcribir, montar y renderizar el borrador. Es lo que más importa saber.

## Lo que cambia respecto al original

- `instalar.py` sustituye a `instalar.sh` (sin bash ni enlaces simbólicos, que en Windows piden administrador).
- `formula.cmd`, `formula-guion.cmd` y `formula-estudiar.cmd` para PowerShell y CMD.
- Codificación UTF-8 forzada, para que los acentos no se rompan.
- La portada no mide los ojos fuera de macOS: eliges el segundo con `formula portada NOMBRE --en S`.
