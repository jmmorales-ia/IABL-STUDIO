#!/usr/bin/env bash
# Mac y Linux: lo mismo que `python3 herramientas/instalar.py` (el instalador de verdad, el mismo en Windows).
py=$(command -v python3 || command -v python || true)
[ -n "$py" ] || { echo "❌ Falta Python 3. Instálalo desde https://www.python.org o con uv (https://docs.astral.sh/uv/)."; exit 1; }
exec "$py" "$(cd "$(dirname "$0")" && pwd)/instalar.py" "$@"
