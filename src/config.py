from pathlib import Path

# This creates an absolute path to the 'src' directory
SRC_ROOT = Path(__file__).resolve().parent

# This creates an absolute path to the project's root directory
# by going one level up from 'src'
PROJECT_ROOT = SRC_ROOT.parent