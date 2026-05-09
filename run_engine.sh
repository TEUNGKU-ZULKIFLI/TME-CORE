#!/bin/bash

# Wrapper script untuk jalankan engine dengan import path yang benar

cd /home/teungku/TME-CORE
source venv/bin/activate

# Run dengan PYTHONPATH set ke project root
PYTHONPATH=/home/teungku/TME-CORE python3 -m src.engine

# Atau gunakan python3 main dengan relative import
# python3 -c "from src.engine import TMECore; engine = TMECore(); engine.start()"
