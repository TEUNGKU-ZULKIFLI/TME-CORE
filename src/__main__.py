"""
Entry point for TME-CORE when run as module: python3 -m src
"""

from src.engine import TMECore

if __name__ == "__main__":
    engine = TMECore()
    engine.start()