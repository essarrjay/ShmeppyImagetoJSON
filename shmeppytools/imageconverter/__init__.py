from sys import path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
PROJ_DIR = BASE_DIR.parent
path.append(str(PROJ_DIR))
path.append(str(BASE_DIR))

import shmeppify
